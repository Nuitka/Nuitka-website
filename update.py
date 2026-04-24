#!/usr/bin/env python3.12

"""Main interface to Nuitka-Website build process."""

import copy
import datetime
import os
import re
import shlex
import subprocess
import sys
from optparse import OptionParser
from pathlib import Path
from settings import development_mode

import requests
from lxml import html

from nuitka_import import importNuitka

importNuitka()

# isort:start

from nuitka.tools.quality.auto_format.AutoFormat import (
    withFileOpenedAndAutoFormatted as _withFileOpenedAndAutoFormatted,
)
from nuitka.tools.release.Documentation import checkRstLint
from nuitka.Tracing import my_print
from nuitka.utils.FileOperations import (
    deleteFile,
    getFileContents,
    getFileList,
    putTextFileContents,
    withTemporaryFile,
)
from nuitka.utils.Hashing import getHashFromValues
from nuitka.utils.Jinja2 import getTemplate
from nuitka.utils.ReExecute import callExecProcess
from nuitka.utils.Rest import makeTable
from regression_utils import (
    DEFAULT_WAIT_TIME,
    DESKTOP_DEVICES,
    GOLDEN_DIR,
    GOLDEN_PAGES,
    MOBILE_DEVICES,
    VIEWPORT_MODES,
    build_url,
    sanitizeUrl,
)


def withFileOpenedAndAutoFormatted(filename):
    return _withFileOpenedAndAutoFormatted(filename, filename)


my_print("Development mode:", development_mode)

FA_STYLE_MAP = {
    "fas": "solid",
    "far": "regular",
    "fab": "brands",
    "fal": "light",
    "fad": "duotone",
    "fat": "thin",
    "fass": "sharp-solid",  # spell-checker: ignore fass
}

FA_UTILITY_CLASSES = {
    "fa",
    "fa-fw",
    "fa-spin",
    "fa-pulse",
    "fa-lg",
    "fa-xs",
    "fa-sm",
    "fa-2x",
    "fa-3x",
    "fa-4x",
    "fa-5x",
}

FA_SVG_PATH = "site/images/fontawesome"
SVG_SOURCE_PATH = "images/svg"

FA_REPLACEMENT_CLASS = {
    "fa": "nuitka-fa",
    "fa-fw": "nuitka-fw",
}


SVG_CACHE = {}


class AssetProcessingError(RuntimeError):
    """Raised when website asset post-processing fails."""


class DocumentStructureError(ValueError):
    """Raised when generated HTML is missing required structure."""


class GoldenUpdateError(RuntimeError):
    """Raised when golden image updates fail."""


HTTP_REQUEST_TIMEOUT = 30
RELEASE_POST_DATE_FORMAT = "%Y/%m/%d %H:%M"


def _require_xpath_results(document, xpath, *, filename, description):
    result = document.xpath(xpath)

    if not result:
        raise DocumentStructureError(
            f"{filename}: expected at least one {description} matching {xpath!r}"
        )

    return result


def _require_single_xpath(document, xpath, *, filename, description):
    result = _require_xpath_results(
        document, xpath, filename=filename, description=description
    )

    if len(result) != 1:
        raise DocumentStructureError(
            f"{filename}: expected exactly one {description} matching {xpath!r}, found {len(result)}"
        )

    return result[0]


def _require_element_tag(element, expected_tag, *, filename, description):
    if element.tag != expected_tag:
        raise DocumentStructureError(
            f"{filename}: expected {description} to be <{expected_tag}>, got <{element.tag}>"
        )


def get_svg_content(svg_path):
    if svg_path not in SVG_CACHE:
        if not os.path.exists(svg_path):
            raise FileNotFoundError(f"SVG not found: {svg_path}")
        SVG_CACHE[svg_path] = getFileContents(svg_path, encoding="utf-8")
    return SVG_CACHE[svg_path]


def add_inline_svg(
    element, svg_path, is_fa_icon=False, style_folder=None, icon_name=None
):
    if not os.path.exists(svg_path):
        if is_fa_icon and style_folder and icon_name:
            my_print(f"Missing Font Awesome SVG: {svg_path}")
            my_print(
                "To fix, run the following command to copy it from the unpacked Pro+ tarball:\n"
            )
            # spell-checker: ignore svgs
            my_print(
                f"cp ../fontawesome-pro-7.2.0-web/svgs/{style_folder}/{icon_name}.svg {svg_path}\n"
            )

        raise FileNotFoundError(f"SVG file not found: {svg_path}")

    svg_content = get_svg_content(svg_path)
    svg_content = re.sub(r"<!--.*?-->", "", svg_content, flags=re.DOTALL)

    svg_element = html.fragment_fromstring(svg_content, create_parent=False)

    # For preserve colors from classes
    if is_fa_icon:
        for path in svg_element.xpath(".//path"):
            if "fill" not in path.attrib:
                path.set("fill", "currentColor")

    attrs = dict(element.attrib)

    for attr, value in attrs.items():
        if attr == "src":
            continue

        # For cases when we are using font-size as width like we do in the arrow icon
        if attr == "style" and "font-size" in value:
            start = value.find("font-size")
            end = value.find(";", start)

            if end == -1:
                end = len(value)

            font_size = value[start:end].split(":", 1)[1].strip()
            font_size_value = re.search(r"\d+", font_size).group()

            svg_element.set("width", font_size_value)
            svg_element.set("height", font_size_value)

            continue

        svg_element.set(attr, element.get(attr))

    attrs = dict(svg_element.attrib)

    if is_fa_icon and "width" not in attrs:
        class_attr = svg_element.get("class", element.get("class", ""))
        class_list = class_attr.split()
        class_list = [FA_REPLACEMENT_CLASS.get(cl, cl) for cl in class_list]
        svg_element.set("class", " ".join(class_list))

    parent = element.getparent()
    tail = element.tail
    svg_element.tail = tail

    parent.replace(element, svg_element)


def inlineImagesSvg(doc, filename):
    for img_tag in doc.xpath("//img[@src]"):
        src = img_tag.get("src")

        if not src.endswith(".svg"):
            continue

        if src.startswith(("http://", "https://")):
            continue

        src_clean = os.path.basename(src)

        svg_path = f"{SVG_SOURCE_PATH}/{src_clean}"

        if not os.path.exists(svg_path):
            raise FileNotFoundError(
                f"{filename}: image source {src!r} resolved to missing SVG {svg_path!r}"
            )

        add_inline_svg(img_tag, svg_path)


def inlineFontAwesomeSvg(doc):
    for i_tag in doc.xpath("//i[contains(@class, 'fa')]"):
        class_list = i_tag.get("class", "").split()

        style_class = next((cl for cl in class_list if cl in FA_STYLE_MAP), None)

        if not style_class and "fa" in class_list:
            style_class = "fas"

        icon_class = next(
            (
                c
                for c in class_list
                if c.startswith("fa-") and c not in FA_UTILITY_CLASSES
            ),
            None,
        )

        if not style_class or not icon_class:
            continue

        style_folder = FA_STYLE_MAP[style_class]
        icon_name = icon_class.replace("fa-", "")

        svg_path = os.path.join(FA_SVG_PATH, style_folder, f"{icon_name}.svg")

        add_inline_svg(
            i_tag,
            svg_path,
            is_fa_icon=True,
            style_folder=style_folder,
            icon_name=icon_name,
        )


def _fetchUrlText(url, description):
    try:
        response = requests.get(url, timeout=HTTP_REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch {description} from {url}: {e}") from e

    return response.text


def _getReleaseVersionKey(value):
    if value == "":
        return []

    value = (
        value.replace("~pre", ".")
        .replace("pre", ".")
        .replace("~rc", ".")
        .replace("rc", ".")
        .replace("~nd", "")
    )

    parts = []
    current = ""

    for value_part in value:
        if value_part in ".-+":
            parts.append(current)
            current = ""
        elif value_part.isdigit() and (current.isdigit() or not current):
            current += value_part
        elif value_part.isdigit():
            parts.append(current)
            current = value_part
        elif current == "":
            current = value_part
        elif current.isdigit():
            parts.append(current)
            current = value_part
        elif current.isalpha() and value_part.isalpha():
            current += value_part
        else:
            raise ValueError(
                f"Unexpected version token {value_part!r} while parsing {value!r}"
            )

    if current != "":
        parts.append(current)

    parts = [int(part) if part.isdigit() else part for part in parts]

    if "ds" in parts:
        parts.remove("ds")

    if not parts:
        raise ValueError(f"Failed to split version string {value!r}")

    return parts


def _makePlainReleaseVersion(value):
    return (
        value.replace("+ds", "")
        .replace("~pre", "pre")
        .replace("~rc", "rc")
        .split("-")[0]
    )


def _fetchReleasePageLinkNames():
    page_source = _fetchUrlText("https://nuitka.net/releases/", "release listing")
    tree = html.fromstring(page_source)
    return tree.xpath("//@href")


def _selectLatestReleaseVersions(link_names):
    max_pre_release = ""
    max_stable_release = ""

    for filename in link_names:
        # Navigation links
        if filename.startswith("?C") or filename == "/":
            continue

        if filename.startswith("0.3"):
            continue
        if filename.startswith("0.4"):
            continue

        if "CPython" in filename or "shedskin" in filename or "PySide" in filename:
            continue

        if not filename.lower().startswith("nuitka"):
            raise ValueError(f"Unexpected release link target {filename!r}")

        if filename.endswith(".msi"):
            continue

        if not filename.endswith(".zip.sig"):
            continue

        filename = filename[len("nuitka_") : -len(".zip.sig")]

        if "pre" in filename or "rc" in filename:
            max_pre_release = max(max_pre_release, filename, key=_getReleaseVersionKey)
        else:
            max_stable_release = max(
                max_stable_release, filename, key=_getReleaseVersionKey
            )

    if not max_pre_release:
        raise ValueError("Did not find any pre-release source archives")

    if not max_stable_release:
        raise ValueError("Did not find any stable source archives")

    return max_pre_release, max_stable_release


def _getObsNumericVersion(value):
    if value.startswith("lp"):
        value = value[2:]
    if value.startswith("bp"):
        value = value[2:]

    return int(value)


def _splitObsVersion(value):
    for part in value.split("."):
        yield from part.split("rc")


def _getObsVersionKey(value):
    version_parts = value.split("-")

    return tuple(
        tuple(_getObsNumericVersion(part) for part in _splitObsVersion(value_part))
        for value_part in version_parts
    )


def _extractObsRpmCandidates(lines, url, *, prerelease):
    if prerelease:
        pattern = r'href="(?:\./)?nuitka-unstable-(.*).noarch\.rpm(?:\.mirrorlist)?"'
        description = "pre-release"
    else:
        # spell-checker: ignore mirrorlist
        pattern = r'href="(?:\./)?nuitka-(.*).noarch\.rpm(?:\.mirrorlist)?"'
        description = "stable"

    candidates = []

    for line in lines:
        if ".rpm" not in line:
            continue

        if prerelease:
            if "unstable" not in line:
                continue
        else:
            if "unstable" in line:
                continue

            if "experimental" in line:
                continue

        match = re.search(pattern, line)

        if not match:
            raise ValueError(
                f"Failed to parse {description} OBS entry {line!r} from {url!r}"
            )

        candidates.append(match.group(1))

    if not candidates:
        raise ValueError(f"Did not find any {description} OBS RPMs in {url!r}")

    return candidates


def _fetchObsRepositoryVersions(repo_name):
    url = (
        "https://download.opensuse.org/repositories/home:/kayhayen/%s/noarch/"
        % repo_name
    )
    output_lines = _fetchUrlText(
        url, f"OBS repository listing for {repo_name}"
    ).splitlines()

    stable_candidates = _extractObsRpmCandidates(output_lines, url, prerelease=False)
    prerelease_candidates = _extractObsRpmCandidates(output_lines, url, prerelease=True)

    max_release = max(stable_candidates, key=_getObsVersionKey)
    max_prerelease = max(prerelease_candidates, key=_getObsVersionKey)

    if "6.7" in max_prerelease:
        raise RuntimeError(
            f"Unexpected OBS pre-release candidate {max_prerelease!r} from {url!r}"
        )

    my_print("Repo %s %s" % (repo_name, max_prerelease))

    return max_release, max_prerelease


def _discoverObsNumberedRepositories(prefix):
    page_source = _fetchUrlText(
        "https://download.opensuse.org/repositories/home:/kayhayen/",
        "OBS repository root",
    )
    tree = html.fromstring(page_source)

    discovered_repositories = {}

    for href in tree.xpath("//@href"):
        repo_name = href.rstrip("/").split("/")[-1]
        match = re.fullmatch(rf"{re.escape(prefix)}_(\d+)", repo_name)

        if match:
            discovered_repositories[int(match.group(1))] = repo_name

    if not discovered_repositories:
        raise ValueError(f"Did not discover any OBS repositories for {prefix!r}")

    return discovered_repositories


def _fetchObsDownloadVersions():
    obs_versions = {
        "rhel": {},
        "centos": {},
        "fedora": {},
        "opensuse": {},
        "sle": {},
    }

    for rhel_number in range(7, 9):
        stable, develop = _fetchObsRepositoryVersions("RedHat_RHEL-%d" % rhel_number)

        obs_versions["rhel"]["stable", rhel_number] = stable
        obs_versions["rhel"]["develop", rhel_number] = develop

    for centos_number, repo_name in (
        (6, "CentOS_CentOS-6"),
        (7, "CentOS_7"),
        (8, "CentOS_8"),
    ):
        stable, develop = _fetchObsRepositoryVersions(repo_name)

        obs_versions["centos"]["stable", centos_number] = stable
        obs_versions["centos"]["develop", centos_number] = develop

    for fedora_number, repo_name in sorted(
        _discoverObsNumberedRepositories("Fedora").items()
    ):
        stable, develop = _fetchObsRepositoryVersions(repo_name)

        obs_versions["fedora"]["stable", fedora_number] = stable
        obs_versions["fedora"]["develop", fedora_number] = develop

    for leap_minor in range(4, 5):
        stable, develop = _fetchObsRepositoryVersions(f"openSUSE_Leap_15.{leap_minor}")

        obs_versions["opensuse"]["stable", leap_minor] = stable
        obs_versions["opensuse"]["develop", leap_minor] = develop

    stable, develop = _fetchObsRepositoryVersions("SLE_15")
    obs_versions["sle"]["stable", 15] = stable
    obs_versions["sle"]["develop", 15] = develop

    return obs_versions


def _renderDownloadPageFiles(max_pre_release, max_stable_release, obs_versions):
    plain_prerelease = _makePlainReleaseVersion(max_pre_release)
    plain_stable = _makePlainReleaseVersion(max_stable_release)

    my_print("Max pre-release is %s %s " % (max_pre_release, plain_prerelease))
    my_print("Max stable release is %s %s " % (max_stable_release, plain_stable))

    fedora_rpm = obs_versions["fedora"]
    centos_rpm = obs_versions["centos"]
    rhel_rpm = obs_versions["rhel"]
    opensuse_rpm = obs_versions["opensuse"]
    sle_rpm = obs_versions["sle"]

    def makeFedoraText(fedora_number, release):
        version = fedora_rpm[release, fedora_number]

        return f"""Nuitka {version.split("-", 1)[0]}"""

    def makeCentOSText(centos_number, release):
        version = centos_rpm[release, centos_number]

        return f"""Nuitka {version.split("-", 1)[0]}"""

    def makeRHELText(rhel_number, release):
        version = rhel_rpm[release, rhel_number]

        return f"""Nuitka {version.split("-", 1)[0]}"""

    def makeLeapText(leap_number, release):
        version = opensuse_rpm[release, leap_number]

        return f"""Nuitka {version.split("-", 1)[0]}"""

    def makeVersionText(version):
        return f"""Nuitka {version.split("-", 1)[0]}"""

    def makeRepoLinkText(repo_name):
        return f"""`repository file <https://download.opensuse.org/repositories/home:/kayhayen/{repo_name}/home:kayhayen.repo>`__"""

    fedora_versions = sorted(
        {fedora_number for _release, fedora_number in fedora_rpm}, reverse=True
    )
    fedora_data = [
        (
            f"Fedora {fedora_number}",
            makeRepoLinkText(f"Fedora_{fedora_number}"),
            makeFedoraText(fedora_number, "stable"),
            makeFedoraText(fedora_number, "develop"),
        )
        for fedora_number in fedora_versions
    ]

    fedora_table = makeTable(
        [["Fedora Version", "RPM Repository", "Stable", "Develop"]] + fedora_data
    )

    centos_data = [
        (
            f"CentOS {centos_number}",
            makeRepoLinkText(
                "CentOS_CentOS-6" if centos_number == 6 else f"CentOS_{centos_number}"
            ),
            makeCentOSText(centos_number, "stable"),
            makeCentOSText(centos_number, "develop"),
        )
        for centos_number in sorted(
            {centos_number for _release, centos_number in centos_rpm}, reverse=True
        )
    ]

    centos_table = makeTable(
        [["CentOS Version", "RPM Repository", "Stable", "Develop"]] + centos_data
    )

    rhel_versions = sorted(
        {rhel_number for _release, rhel_number in rhel_rpm}, reverse=True
    )
    rhel_data = [
        (
            f"RHEL {rhel_number}",
            makeRepoLinkText("RedHat_RHEL-%d" % rhel_number),
            makeRHELText(rhel_number, "stable"),
            makeRHELText(rhel_number, "develop"),
        )
        for rhel_number in rhel_versions
    ]

    rhel_table = makeTable(
        [["RHEL Version", "RPM Repository", "Stable", "Develop"]] + rhel_data
    )

    leap_minors = sorted({leap_minor for _release, leap_minor in opensuse_rpm})
    suse_data = [
        (
            f"openSUSE Leap 15.{leap_minor}",
            makeRepoLinkText(f"openSUSE_Leap_15.{leap_minor}"),
            makeLeapText(leap_minor, "stable"),
            makeLeapText(leap_minor, "develop"),
        )
        for leap_minor in leap_minors
    ]

    suse_data.insert(
        0,
        (
            "SLE 15",
            makeRepoLinkText("SLE_15"),
            makeVersionText(sle_rpm["stable", 15]),
            makeVersionText(sle_rpm["develop", 15]),
        ),
    )

    suse_table = makeTable(
        [["SUSE Version", "RPM Repository", "Stable", "Develop"]] + suse_data
    )

    source_table = makeTable(
        [["Branch", "zip", "tar.gz", "tar.bz2"]]
        + [
            (
                "Stable",
                f"`Nuitka {plain_stable}.zip <https://nuitka.net/releases/Nuitka-{plain_stable}.zip>`__",
                f"`Nuitka {plain_stable}.tar.gz <https://nuitka.net/releases/Nuitka-{plain_stable}.tar.gz>`__",
                f"`Nuitka {plain_stable}.tar.bz2 <https://nuitka.net/releases/Nuitka-{plain_stable}.tar.bz2>`__",
            ),
            (
                "Develop",
                f"`Nuitka {plain_prerelease}.zip <https://nuitka.net/releases/Nuitka-{plain_prerelease}.zip>`__",
                f"`Nuitka {plain_prerelease}.tar.gz <https://nuitka.net/releases/Nuitka-{plain_prerelease}.tar.gz>`__",
                f"`Nuitka {plain_prerelease}.tar.bz2 <https://nuitka.net/releases/Nuitka-{plain_prerelease}.tar.bz2>`__",
            ),
        ]
    )

    major, minor = plain_stable.split(".")[:2]
    major = int(major)
    minor = int(minor)

    plain_stable_minor = "%d.%d" % (major, minor)

    if minor == 9:
        major += 1
        minor = 0
    else:
        minor += 1

    plain_stable_next = "%d.%d" % (major, minor)

    if plain_stable_next == "2.9":
        plain_stable_next = "4.0"

    with withFileOpenedAndAutoFormatted("site/dynamic.inc") as output_file:
        output_file.write(
            """
.. |NUITKA_VERSION| replace:: %s

.. |NUITKA_VERSION_MINOR| replace:: %s

.. |NUITKA_VERSION_NEXT| replace:: %s
"""
            % (plain_stable, plain_stable_minor, plain_stable_next),
        )

    with withFileOpenedAndAutoFormatted("site/doc/fedora-downloads.inc") as output_file:
        output_file.write(fedora_table)
    with withFileOpenedAndAutoFormatted("site/doc/centos-downloads.inc") as output_file:
        output_file.write(centos_table)
    with withFileOpenedAndAutoFormatted("site/doc/rhel-downloads.inc") as output_file:
        output_file.write(rhel_table)
    with withFileOpenedAndAutoFormatted("site/doc/suse-downloads.inc") as output_file:
        output_file.write(suse_table)
    with withFileOpenedAndAutoFormatted("site/doc/source-downloads.inc") as output_file:
        output_file.write(source_table)


def updateDownloadPage():
    link_names = _fetchReleasePageLinkNames()
    max_pre_release, max_stable_release = _selectLatestReleaseVersions(link_names)
    obs_versions = _fetchObsDownloadVersions()

    _renderDownloadPageFiles(
        max_pre_release=max_pre_release,
        max_stable_release=max_stable_release,
        obs_versions=obs_versions,
    )


# slugify is copied from
# http://code.activestate.com/recipes/
# 577257-slugify-make-a-string-usable-in-a-url-or-filename/
_slugify_strip_re = re.compile(r"[^\w\s-]")
_slugify_hyphenate_re = re.compile(r"[-\s]+")


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    if type(value) is str:
        import unidecode

        value = unidecode.unidecode(value)
    value = str(_slugify_strip_re.sub("", value).strip().lower())
    return _slugify_hyphenate_re.sub("-", value)


def _splitRestByChapter(lines):
    marker = "****"

    section_markers = []

    for count, line in enumerate(lines):
        if line.startswith(marker) and lines[count + 2].startswith(marker):
            section_markers.append((count, lines[count + 1].strip()))

    for count, (section_start_line, title) in enumerate(section_markers):
        if count + 1 < len(section_markers):
            end_line = section_markers[count + 1][0]
        else:
            end_line = None

        yield title, lines[section_start_line + 3 : end_line]


def _parseReleasePostDate(release_post_date):
    try:
        datetime.datetime.strptime(release_post_date, RELEASE_POST_DATE_FORMAT)
    except ValueError as e:
        raise ValueError(
            "Expected --release-post-date in format YYYY/MM/DD HH:MM"
        ) from e

    return release_post_date


def _getDefaultReleasePostDate():
    return datetime.datetime.now(datetime.UTC).strftime("%Y/%m/%d")


def _getReleasePostPublicationDate(txt_path, release_post_date):
    if os.path.exists(txt_path):
        with open(txt_path, encoding="utf-8") as input_file:
            first_line = input_file.readline()

        if not first_line.startswith(".. post:: "):
            raise ValueError(f"{txt_path}: malformed post metadata line")

        return first_line.removeprefix(".. post:: ").strip()

    if release_post_date is None:
        return _getDefaultReleasePostDate()

    return release_post_date


def updateReleasePosts(release_post_date=None):
    _updateReleasePosts("site/changelog/Changelog.rst", release_post_date)
    _updateReleasePosts("site/changelog/Changelog-1.x.rst", release_post_date)
    _updateReleasePosts("site/changelog/Changelog-0.x.rst", release_post_date)


def _updateReleasePosts(changelog_filename, release_post_date):
    count = 0

    with open(changelog_filename, encoding="utf-8") as changelog_file:
        changelog_lines = changelog_file.readlines()

    for title, lines in _splitRestByChapter(changelog_lines):
        title = title.lstrip()
        count += 1

        # Ignore draft for pages.
        if "Draft" in title:
            continue

        slug = slugify(title)

        # For the pages except very first, use a leading sentence.
        if "release-01-releasing" not in slug:
            lines = (
                [
                    """\
This is to inform you about the new stable release
of `Nuitka <https://nuitka.net>`__. It is the extremely
compatible Python compiler,  `"download now" </doc/download.html>`_.\n""",
                    "\n",
                ]
                + lines
            )
        else:
            lines.append(
                """

But yes, lets see what happens. Oh, and you will find its `latest
version here </doc/download.html>`_.

Kay Hayen
"""
            )
        if "release-038" in slug:
            slug += "---windows-support"

        if "release-02" in slug:
            slug = slug.replace("nuitka-release", "release-nuitka")

        if "release-011" in slug:
            slug = "minor-" + slug.replace("nuitka-release", "release-nuitka")

        if "release-01-releasing" in slug:
            slug = "releasing-nuitka-to-the-world"

        output_path = "site/posts"
        txt_path = os.path.join(output_path, f"{slug}.rst")

        pub_date = _getReleasePostPublicationDate(txt_path, release_post_date)

        lines = [
            ".. post:: %s\n" % pub_date,
            "   :tags: compiler, Python, Nuitka\n",
            "   :author: Kay Hayen\n",
            "\n",
            title.strip() + "\n",
            "~~~~~\n",
            "\n",
        ] + lines

        with withFileOpenedAndAutoFormatted(txt_path) as output_file:
            output_file.write("".join(lines))


def updateDocs(release_post_date=None):
    updateReleasePosts(release_post_date=release_post_date)


_translations = ("zh_CN/", "de_DE/")


def _getLanguageFromFilename(filename):
    filename_relative = os.path.relpath(filename, "output")
    if filename_relative.startswith(("zh_CN/", "de_DE/")):
        return filename_relative[3:5].upper(), filename_relative[6:]
    else:
        return "EN", filename_relative


def _getTranslationFileSet(filename):
    language, filename_translation = _getLanguageFromFilename(filename)

    filename_translations = {
        os.path.join("output", translation, filename_translation)
        for translation in _translations
        if os.path.exists(os.path.join("output", translation, filename_translation))
    }

    filename_translations.add(os.path.join("output", filename_translation))

    return language, filename_translations


def _makeCssCombined(css_filenames, css_links, has_asciinema):
    # Simply concatenate CSS files - let PostCSS handle the processing
    merged_css = "\n".join(
        getFileContents(css_filename)
        for css_filename in sorted(css_filenames, key=lambda x: "my_" in x)
    )

    # orig_css = merged_css

    # Process with PostCSS
    try:
        processed_css = _processWithPostCSS(merged_css)
    except AssetProcessingError as e:
        if not development_mode:
            raise

        processed_css = merged_css
        my_print(f"Warning, {e}, using original CSS")

    # Validate processed CSS: fallback to original if empty or
    # invalid, but only in development mode.
    if not processed_css:
        if not development_mode:
            raise AssetProcessingError("CSS processing produced empty output")

        processed_css = merged_css

        my_print("Warning, CSS processing produced empty output, using original CSS")

    del merged_css

    output_filename = "/_static/css/combined_%s.css" % getHashFromValues(processed_css)

    putTextFileContents(filename=f"output{output_filename}", contents=processed_css)
    # putTextFileContents(filename=f"output{output_filename}.orig", contents=orig_css)

    css_links[0].attrib["href"] = output_filename
    for css_link in css_links[1:]:
        if development_mode and "my_theme" in css_link.attrib["href"]:
            continue

        if "asciinema" in css_link.attrib["href"] and has_asciinema:
            continue

        css_link.getparent().remove(css_link)


def _makeJsCombined(js_filenames):
    js_filenames = list(js_filenames)

    js_set_contents = """
    const jQuery = {};
    jQuery.fn = {};
    """ + (
        "\n".join(
            getFileContents(f"output/{js_filename}") for js_filename in js_filenames
        )
        + """
(function() {
var id = '82f00db2-cffd-11ee-882e-0242ac130002';
var ci_search = document.createElement('script');
ci_search.type = 'text/javascript';
ci_search.async = true;
ci_search.src = 'https://cse.expertrec.com/api/js/ci_common.js?id=' + id;
var s = document.getElementsByTagName('script')[0];
s.parentNode.insertBefore(ci_search, s);
})();
"""
    )

    if not development_mode:
        processed_js = _processWithTerser(js_set_contents)

        if not processed_js:
            raise AssetProcessingError("JS processing produced empty output")

        js_set_contents = processed_js

    js_set_output_filename = "/_static/combined_%s.js" % getHashFromValues(
        js_set_contents
    )

    filename = f"output{js_set_output_filename}"

    if not os.path.exists(filename):
        putTextFileContents(filename, js_set_contents)

    return js_set_output_filename


def fixupSymbols(document_bytes):
    contents = getFileContents("site/variables.inc", mode="rb")

    def replaceSymbol(value):
        value = value.group(0)
        symbol_name = value.decode("utf-8", "replace")

        found = 0
        result = b""

        for line in contents.splitlines():
            if found == 1:
                if line:
                    raise ValueError(
                        f"Malformed symbol definition for {symbol_name}: expected a blank line after its directive in site/variables.inc"
                    )
                found = 2
                continue

            if found == 2:
                if not line:
                    break

                result += line.strip()
                continue

            if value in line:
                found = 1

        if not result:
            raise ValueError(
                f"Could not expand symbol {symbol_name} from site/variables.inc"
            )
        return result

    document_bytes = re.sub(
        b"\\|.*?_SYMBOL\\|",
        replaceSymbol,
        document_bytes,
        flags=re.S,
    )

    return document_bytes


_postcss_cache = {}
_terser_cache = {}


def _processWithNpmBuild(contents, script, suffix, cache, label):
    """Generic processor for content via an npm script"""
    if contents in cache:
        return cache[contents]

    original_size = len(contents)

    with withTemporaryFile(suffix=suffix, mode="w", delete=False) as tmp_input:
        tmp_input.write(contents)
        tmp_input_path = tmp_input.name

    with withTemporaryFile(mode="w", suffix=suffix, delete=False) as tmp_output:
        tmp_output_path = tmp_output.name

    try:
        try:
            result = subprocess.run(
                ["npm", "run", script],
                env={
                    **os.environ,
                    "INPUT": tmp_input_path,
                    "OUTPUT": tmp_output_path,
                },
                capture_output=True,
                text=True,
            )
        except OSError as e:
            raise AssetProcessingError(f"Unable to run {label} tool: {e}") from e

        if result.stdout.strip():
            my_print(f"{label} tool output: {result.stdout.strip()}")

        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip()
            raise AssetProcessingError(
                f"{label} processing failed: {message or f'exit code {result.returncode}'}"
            )

        try:
            processed = getFileContents(tmp_output_path, mode="r", encoding="utf-8")
        except OSError as e:
            raise AssetProcessingError(
                f"Unable to read {label} output from {tmp_output_path}: {e}"
            ) from e

        cache[contents] = processed

        processed_size = len(processed)
        if original_size > 0:
            reduction_percent = (original_size - processed_size) / original_size * 100
            my_print(
                f"{label} reduced by {reduction_percent:.1f}% ({original_size} → {processed_size} bytes)"
            )
    finally:
        deleteFile(tmp_input_path, must_exist=False)
        deleteFile(tmp_output_path, must_exist=False)

    return processed


def _processWithPostCSS(css_content):
    """Process CSS content through PostCSS with PurgeCSS."""
    return _processWithNpmBuild(
        contents=css_content,
        script="build:css",
        suffix=".css",
        cache=_postcss_cache,
        label="CSS",
    )


def _processWithTerser(js_content):
    """Process JavaScript content through Terser minifier."""
    return _processWithNpmBuild(
        contents=js_content,
        script="build:js",
        suffix=".js",
        cache=_terser_cache,
        label="JS",
    )


_html_minifier_cache = {}


def _minifyHtml(filename):
    """Process HTML content through HTML-MINIFIER"""
    if filename in _html_minifier_cache:
        with open(filename, "w", encoding="utf-8") as output:
            output.write(_html_minifier_cache[filename])
        return

    my_print("Minifying HTML:", filename)

    try:
        result = subprocess.run(
            ["npm", "run", "build:html"],
            env={**os.environ, "INPUT": filename},
            capture_output=True,
            text=True,
        )
    except OSError as e:
        raise AssetProcessingError(f"Unable to run HTML minifier: {e}") from e

    if result.stdout.strip():
        my_print(f"HTML-minifier output: {result.stdout.strip()}")

    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise AssetProcessingError(
            f"HTML minifier failed for {filename}: {message or f'exit code {result.returncode}'}"
        )

    if not os.path.exists(filename):
        raise AssetProcessingError(
            f"Expected minified HTML file was not produced: {filename}"
        )

    try:
        _html_minifier_cache[filename] = getFileContents(
            filename, mode="r", encoding="utf-8"
        )
    except OSError as e:
        raise AssetProcessingError(
            f"Unable to read minified HTML file {filename}: {e}"
        ) from e


def handleJavaScript(filename, doc):
    # Check copybutton.js
    has_highlight = doc.xpath("//div[@class='highlight']")

    # Check carousel.js
    has_carousel = doc.xpath("//div[contains(@class, 'carousel')]")

    # Check inline tabs
    has_inline_tabs = doc.xpath("//*[@class='sd-tab-label']")

    # Detect if asciinema is used in the page
    has_asciinema = False
    for script_tag in doc.xpath("//script"):
        if script_tag.text and "AsciinemaPlayer" in script_tag.text:
            has_asciinema = True

    script_tag_first = None
    js_filenames = []
    for script_tag in doc.xpath("//script"):
        if "src" in script_tag.attrib:
            script_tag.attrib["src"] = script_tag.get("src").split("?")[0]
        else:
            if (
                script_tag.text
                and "SphinxRtdTheme.Navigation.enable(true);" in script_tag.text
            ):
                script_tag.getparent().remove(script_tag)

            # Wait before executing Asciinema script tags, so the async load
            # of its Javascript can complete still.
            if script_tag.text and "AsciinemaPlayer" in script_tag.text:
                script_tag.attrib["defer"] = "true"

            continue

        script_tag.attrib["async"] = ""

        if "combined_" in script_tag.attrib["src"]:
            script_tag_first = None
            break

        # Google search.
        if "google" in script_tag.attrib["src"]:
            continue

        if "asciinema" in script_tag.attrib["src"]:
            if not has_asciinema:
                script_tag.getparent().remove(script_tag)

            continue

        if script_tag.attrib["src"].startswith("http"):
            continue

        if not has_highlight and "copybutton" in script_tag.attrib["src"]:
            script_tag.getparent().remove(script_tag)
        elif not has_highlight and "clipboard" in script_tag.attrib["src"]:
            script_tag.getparent().remove(script_tag)
        elif not has_inline_tabs and "design-tabs" in script_tag.attrib["src"]:
            script_tag.getparent().remove(script_tag)
        elif not has_carousel and "carousel" in script_tag.attrib["src"]:
            script_tag.getparent().remove(script_tag)
        else:
            # Make script source absolute, so it's easier to find
            if not script_tag.attrib["src"].startswith("/"):
                while script_tag.attrib["src"].startswith("../"):
                    script_tag.attrib["src"] = script_tag.attrib["src"][3:]

                for translation in _translations:
                    if translation in filename:
                        script_tag.attrib["src"] = (
                            "/" + translation + "/" + script_tag.attrib["src"]
                        )
                        break
                else:
                    script_tag.attrib["src"] = "/" + script_tag.attrib["src"]
            if script_tag_first is None:
                script_tag_first = script_tag
            else:
                script_tag.getparent().remove(script_tag)

            if not script_tag.attrib["src"].startswith("/"):
                raise ValueError(
                    f"{filename}: script source did not normalize to an absolute path: {script_tag.attrib['src']!r}"
                )
            js_filenames.append(script_tag.attrib["src"][1:])

    if script_tag_first is not None:
        script_tag_first.attrib["src"] = _makeJsCombined(js_filenames)


def cleanBuildSVGs():
    for dirpath, dirnames, filenames in os.walk("output/_images"):
        for filename in filenames:
            if not filename.endswith(".svg"):
                continue

            deleteFile(os.path.join(dirpath, filename), must_exist=False)


def runPostProcessing():
    # Compress the CSS and JS files into one file, clean up links, and
    # do other touch ups. spell-checker: ignore searchindex,searchtools

    for delete_filename in (
        "searchindex.js",
        "searchtools.js",
        "search.html",
        "_static/jquery.js",
    ):
        print("removing", os.path.join("output", delete_filename))
        deleteFile(os.path.join("output", delete_filename), must_exist=False)
        for translation in _translations:
            deleteFile(
                os.path.join("output", translation, delete_filename), must_exist=False
            )

    output_base_theme_path = "output/_static/css/theme.css"
    fa_fonts_path = "output/_static/fonts"

    if os.path.exists(output_base_theme_path):
        my_print(f"Processing base theme with PostCSS...")
        theme_css_content = getFileContents(
            output_base_theme_path, mode="r", encoding="utf-8"
        )
        processed_theme_css = _processWithPostCSS(theme_css_content)
        if not processed_theme_css:
            raise AssetProcessingError(
                f"CSS processing produced empty output for {output_base_theme_path}"
            )

        putTextFileContents(
            filename=output_base_theme_path, contents=processed_theme_css
        )
        my_print(f"Successfully processed and cleaned base theme")

    if os.path.exists(fa_fonts_path):
        for filename in os.listdir(fa_fonts_path):
            if filename.lower().startswith("fontawesome"):
                deleteFile(os.path.join(fa_fonts_path, filename), must_exist=False)

    # Force working on the root document first.
    file_list = getFileList("output", only_suffixes=".html")
    file_list.remove("output/index.html")
    file_list.insert(0, "output/index.html")

    root_doc = None
    for filename in file_list:
        doc = html.fromstring(getFileContents(filename, mode="rb"))

        if root_doc is None:
            root_doc = doc

        # Check copybutton.js
        has_highlight = doc.xpath("//div[@class='highlight']")

        # Detect if asciinema is used in the page
        has_asciinema = False
        for script_tag in doc.xpath("//script"):
            if script_tag.text and "AsciinemaPlayer" in script_tag.text:
                has_asciinema = True

        # Repair favicon extension not cooperation with ablog extension,
        # copy over the root_doc links.
        fav_icons = doc.xpath("//head/link[@rel='icon']")

        if not fav_icons:
            head_node = _require_single_xpath(
                doc, "head", filename=filename, description="document head"
            )
            for fav_icon in root_doc.xpath("//head/link[@rel='icon']"):
                fav_icon = copy.deepcopy(fav_icon)
                fav_icon.attrib["href"] = "/" + fav_icon.attrib["href"]

                head_node.append(fav_icon)

        for search_link in doc.xpath("//link[@rel='search']"):
            search_link.getparent().remove(search_link)

        for current_link in doc.xpath("//a[@class='current reference internal']"):
            current_link.attrib["href"] = "/" + os.path.relpath(filename, "output")

        for current_link in doc.xpath("//a[@class='reference internal']"):
            if current_link.attrib["href"] == "index.html":
                current_link.attrib["href"] = "/" + os.path.relpath(
                    os.path.dirname(filename), "output"
                )

        for current_link in doc.xpath(
            "//ul[contains(@class, 'hub-toc')]//a[@class='reference internal']"
        ):
            if current_link.attrib["href"] in ("/", "#"):
                parent_tag = current_link.getparent()
                _require_element_tag(
                    parent_tag,
                    "p",
                    filename=filename,
                    description="hub navigation current link parent",
                )
                parent_tag.attrib["class"] = "hub-nav-current"
                for child in current_link:
                    current_link.remove(child)
                    parent_tag.append(child)

                parent_tag.remove(current_link)

        for current_hub_card in doc.xpath(
            "//div[contains(@class, 'hub-card-set')]//div[contains(@class, 'sd-card-body')]"
        ):

            has_arrow_div = current_hub_card.xpath("div[@class='hub-circle-button']")

            if not has_arrow_div:
                hub_card_div = html.fromstring(
                    """<div class="hub-card-contents"></div>"""
                )

                for child in current_hub_card:
                    current_hub_card.remove(child)
                    hub_card_div.append(child)

                current_hub_card.append(hub_card_div)

                current_hub_card.append(
                    html.fromstring(
                        """<div class="hub-circle-button"><i class="fa fa-arrow-circle-right" aria-hidden="true" style="font-size: 25px;"></i></div>"""
                    )
                )

                current_hub_card.attrib["class"] = (
                    current_hub_card.attrib["class"] + " hub-card"
                )

        for current_hub_title in doc.xpath(
            "//div[contains(@class, 'hub-card-set')]//div[contains(@class, 'sd-card-title')]"
        ):

            for first_child in current_hub_title:
                if first_child.tag == "a":
                    card_body = _require_single_xpath(
                        current_hub_title,
                        "ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' hub-card ')][1]",
                        filename=filename,
                        description="hub card ancestor",
                    )

                    for sub_child in first_child:
                        first_child.remove(sub_child)
                        current_hub_title.insert(0, sub_child)

                    first_child.attrib["class"] = (
                        card_body.attrib["class"] + " hub-card-link"
                    )

                break

        css_links = _require_xpath_results(
            doc,
            "//link[@rel='stylesheet']",
            filename=filename,
            description="stylesheet link",
        )

        # Remove version trick from links, we don't need it really.
        for css_link in css_links:
            css_link.attrib["href"] = css_link.get("href").split("?")[0]

        bread_crumbs_hr = doc.xpath("//div[@role='navigation']/hr")
        if bread_crumbs_hr:
            bread_crumbs_hr[0].getparent().remove(bread_crumbs_hr[0])

        if css_filenames := [
            os.path.normpath(
                f'output/{os.path.relpath(os.path.dirname(filename), "output")}/{css_link.get("href")}'
            )
            for css_link in css_links
            if "combined_" not in css_link.get("href")
            if "copybutton" not in css_link.get("href") or has_highlight
            if "my_theme" not in css_link.get("href") or not development_mode
            if "asciinema" not in css_link.get("href")
        ]:
            _makeCssCombined(
                css_filenames, css_links=css_links, has_asciinema=has_asciinema
            )

        for link in doc.xpath("//a[not(contains(@class, 'intern'))]"):
            if (
                link.attrib["href"].startswith("http:")
                or link.attrib["href"].startswith("https:")
            ) and "nuitka.net" not in link.attrib["href"]:
                link.attrib["target"] = "_blank"

        for link in doc.xpath("//link[@rel='canonical']"):
            if link.attrib["href"].endswith("/index.html"):
                link.attrib["href"] = link.attrib["href"][:-11]

        # Make internal links more canonical, no index.html, no trailing #
        for link in doc.xpath("//a[not(contains(@class, 'extern'))]"):
            link_target = link.attrib["href"]

            if link_target.startswith("http"):
                continue

            if link_target.endswith("/index.html"):
                link_target = link_target[:-11]

            if link_target.endswith("#"):
                link_target = link_target[:-1]

            if not link_target:
                link_target = "/"

            link.attrib["href"] = link_target

        has_top_nav = doc.xpath("//div[@class='top_nav']")

        top_link_nav = None

        if not has_top_nav:
            h1 = doc.xpath("//h1")

            if h1:
                h1 = h1[0]
                top_nav = html.fromstring("""<div class="top_nav"></div>""")
                h1.getparent().insert(h1.getparent().index(h1), top_nav)

                top_link_nav = _require_single_xpath(
                    doc,
                    "//nav[@class='top_link_nav']",
                    filename=filename,
                    description="top link navigation",
                )
                top_link_nav.getparent().remove(top_link_nav)
                top_nav.append(top_link_nav)

                social_container = _require_single_xpath(
                    doc,
                    "//div[@class='share-button-container']",
                    filename=filename,
                    description="share button container",
                )
                social_container.getparent().remove(social_container)
                top_link_nav.append(social_container)

                blog_container = doc.xpath("//div[@class='blog-post-box']")
                if blog_container:
                    blog_container = blog_container[0]
                    blog_container.getparent().remove(blog_container)
                    top_nav.getparent().insert(
                        top_nav.getparent().index(top_nav) + 1, blog_container
                    )

        for node in doc.xpath("//div[@class='wy-side-nav-search']"):
            node.getparent().remove(node)

        handleJavaScript(filename, doc)

        file_language, translated_filenames = _getTranslationFileSet(filename)

        # Disabled for now, pylint: disable=condition-evals-to-constant
        if len(translated_filenames) == 1 or True:
            for node in doc.xpath(
                "//details[contains(@class, 'language-switcher-container')]"
            ):
                node.getparent().remove(node)
        else:
            # assert False, (translated_files, filename)
            for summary_node in doc.xpath(
                '//details["language-switcher-container"]/summary'
            ):
                summary_node.text = file_language

            # for link_node in doc.xpath("//details//@href"):
            #     link_node = link_node.getparent()
            #     line_node = link_node.getparent()
            #     dropdown_node = line_node.getparent()
            #     if dropdown_node is not None:
            #         dropdown_node.clear()

            #     for translated_filename in sorted(translated_filenames):
            #         if filename == translated_filename:
            #             continue

            #         language, _ = _getLanguageFromFilename(translated_filename)

            #         link_node.attrib["href"] = "/" + os.path.relpath(
            #             translated_filename, "output"
            #         )
            #         link_node.text = language

            #         new_line_node = copy.deepcopy(line_node)

            #         if dropdown_node is not None:
            #             dropdown_node.append(new_line_node)

        for node in doc.xpath(
            "//details[contains(@class, 'language-switcher-container')]"
        ):
            node.getparent().remove(node)

            # TODO: Enable language switcher later on
            # Disabled for now, pylint: disable=condition-evals-to-constant

            if top_link_nav is not None and False:
                top_link_nav.append(node)

        document_bytes = b"<!DOCTYPE html>\n" + html.tostring(
            doc, include_meta_content_type=True
        )

        document_bytes = fixupSymbols(document_bytes)

        document_bytes = document_bytes.replace(b"now &#187;", b"now&nbsp;&nbsp;&#187;")
        document_bytes = document_bytes.replace(b"/ yr", b'<i class="sub">/ yr</i>')

        doc = html.fromstring(document_bytes)

        inlineImagesSvg(doc=doc, filename=filename)
        inlineFontAwesomeSvg(doc)

        result = html.tostring(
            doc,
            encoding="UTF-8",
            method="html",
            doctype="<!DOCTYPE html>",
        )

        with open(filename, "wb") as output:
            output.write(result)

        if not development_mode:
            _minifyHtml(filename)

    if development_mode:
        my_theme_filename = "output/_static/my_theme.css"

        if not os.path.exists(my_theme_filename):
            raise FileNotFoundError(
                f"Development theme stylesheet not found: {my_theme_filename}"
            )
        if not os.path.islink(my_theme_filename):
            os.unlink(my_theme_filename)
            os.symlink(os.path.abspath("_static/my_theme.css"), my_theme_filename)

    cleanBuildSVGs()


def runDeploymentCommand():
    # spell-checker: ignore doctrees,buildinfo,apidoc

    excluded = [
        # Build information from Sphinx
        ".buildinfo",
        ".doctrees",
        "objects.inv",
        # API doc is provided separately. TODO: That should be Sphinx too.
        "apidoc",
        # Debian repository, do not touch.
        "deb",
        # Download files, do not touch.
        "releases",
        # For user download
        "ccache",
        "volatile",
        # PDF documentation for current release
        "doc/*.pdf",
        # Google ownership marker, do not touch, spell-checker: ignore googlee
        "googlee5244704183a9a15.html",
        # Link into blog, for compatibility with old blog subscriptions.
        "rss.xml",
    ]

    target_dir = "/var/www/"
    command = [
        "rsync",
        "-ravz",
        *(f"--exclude={exclude}" for exclude in excluded),
        "--chown=www-data:git",
        "--chmod=Dg+x",
        "--delete-after",
        "output/",
        f"root@ssh.nuitka.net:{target_dir}",
    ]

    my_print(" ".join(shlex.quote(part) for part in command))

    subprocess.run(command, check=True)


def checkRestPages():
    for root, _dirnames, filenames in os.walk("."):
        for filename in filenames:
            full_name = os.path.join(root, filename)

            if full_name.endswith(".rst"):
                checkRstLint(full_name)


def runSphinxAutoBuild():
    args = [
        sys.executable,
        sys.executable,
        os.path.join(os.path.dirname(__file__), "misc", "sphinx_autobuild_wrapper.py"),
        "site",
        "output",
        "--watch",
        "misc",
        "--watch",
        "update.py",
        "--watch",
        "site",
        "--watch",
        "settings.ini",
        "--watch",
        "state.ini",
        "--watch",
        "intl",
        "--watch",
        "Pipenv.lock",
        "--watch",
        "_static",
    ]

    callExecProcess(args, False)


def _close_playwright_resource(
    resource, description, *, raise_on_failure, playwright_error_type
):
    if resource is None:
        return

    try:
        resource.close()
    except playwright_error_type as e:
        if raise_on_failure:
            raise GoldenUpdateError(f"Failed to close {description}") from e

        my_print(f"Additional cleanup failure for {description}: {e}")


def _get_golden_device_config(browser_name, viewport_mode):
    try:
        if viewport_mode == "desktop":
            return DESKTOP_DEVICES[browser_name]

        if viewport_mode == "mobile":
            return MOBILE_DEVICES[browser_name]
    except KeyError as e:
        raise ValueError(
            f"No {viewport_mode} device configuration for {browser_name}"
        ) from e

    raise ValueError(f"Unknown viewport mode: {viewport_mode}")


def _update_golden_page(
    page,
    *,
    golden_dir,
    browser_name,
    viewport_mode,
    page_path,
    wait,
    verbose,
    playwright_error_type,
    playwright_timeout_error_type,
):
    url = build_url(page_path)
    safe_name = sanitizeUrl(page_path)
    golden_path = golden_dir / f"{browser_name}_{viewport_mode}_{safe_name}.png"

    if verbose:
        my_print(
            f"  Generating {browser_name} / {viewport_mode} / {page_path} -> {golden_path}"
        )

    try:
        page.goto(url, timeout=20000)
        if wait > 0:
            page.wait_for_timeout(wait)

        page.add_style_tag(
            content="""
        * {
            font-family: Arial, Helvetica, sans-serif !important;
            -webkit-font-smoothing: none !important;
            -moz-osx-font-smoothing: grayscale !important;
        }
        """
        )

        page.wait_for_function("document.fonts.ready")
        page.screenshot(
            path=golden_path,
            full_page=True,
            timeout=20000,
        )
    except (OSError, playwright_timeout_error_type, playwright_error_type) as e:
        raise GoldenUpdateError(
            f"Failed to generate golden image for {browser_name} / {viewport_mode} / {page_path}"
        ) from e


def _update_golden_context(
    browser,
    *,
    golden_dir,
    browser_name,
    viewport_mode,
    pages,
    wait,
    verbose,
    playwright_error_type,
    playwright_timeout_error_type,
):
    context = None
    context_completed = False

    try:
        device_config = _get_golden_device_config(browser_name, viewport_mode)

        try:
            context = browser.new_context(**device_config)
        except playwright_error_type as e:
            raise GoldenUpdateError(
                f"Failed to create {viewport_mode} context for {browser_name}"
            ) from e

        try:
            page = context.new_page()
        except playwright_error_type as e:
            raise GoldenUpdateError(
                f"Failed to create a page in the {browser_name} / {viewport_mode} context"
            ) from e

        for page_path in pages:
            _update_golden_page(
                page,
                golden_dir=golden_dir,
                browser_name=browser_name,
                viewport_mode=viewport_mode,
                page_path=page_path,
                wait=wait,
                verbose=verbose,
                playwright_error_type=playwright_error_type,
                playwright_timeout_error_type=playwright_timeout_error_type,
            )

        context_completed = True
    finally:
        _close_playwright_resource(
            context,
            f"{browser_name} / {viewport_mode} context",
            raise_on_failure=context_completed,
            playwright_error_type=playwright_error_type,
        )


def _update_golden_browser(
    playwright_context,
    *,
    golden_dir,
    browser_name,
    devices,
    pages,
    wait,
    verbose,
    playwright_error_type,
    playwright_timeout_error_type,
):
    browser = None
    browser_completed = False

    try:
        try:
            browser_type = getattr(playwright_context, browser_name)
        except AttributeError as e:
            raise ValueError(f"Unknown browser: {browser_name}") from e

        try:
            browser = browser_type.launch(headless=True)
        except playwright_error_type as e:
            raise GoldenUpdateError(
                f"Failed to launch browser {browser_name} for golden image updates"
            ) from e

        for viewport_mode in devices:
            _update_golden_context(
                browser,
                golden_dir=golden_dir,
                browser_name=browser_name,
                viewport_mode=viewport_mode,
                pages=pages,
                wait=wait,
                verbose=verbose,
                playwright_error_type=playwright_error_type,
                playwright_timeout_error_type=playwright_timeout_error_type,
            )

        browser_completed = True
    finally:
        _close_playwright_resource(
            browser,
            f"{browser_name} browser",
            raise_on_failure=browser_completed,
            playwright_error_type=playwright_error_type,
        )


def runUpdateGolden(
    browsers=None,
    devices=None,
    pages=None,
    wait=None,
    clean=False,
    verbose=False,
):
    browsers = browsers or ["chromium", "firefox", "webkit"]
    devices = devices or VIEWPORT_MODES
    pages = pages or GOLDEN_PAGES
    wait = wait or DEFAULT_WAIT_TIME

    if verbose:
        my_print("Configuration:")
        my_print(f"- Browsers: {browsers}")
        my_print(f"- Devices: {devices}")
        my_print(f"- Pages: {pages}")
        my_print(f"- Wait time: {wait} ms")
        my_print(f"- Clean directory: {'Yes' if clean else 'No'}")

    golden_dir = Path(GOLDEN_DIR)
    if clean and golden_dir.exists():
        my_print(f"Cleaning reference images directory: {golden_dir}")
        for file in golden_dir.glob("*.png"):
            deleteFile(file, must_exist=False)
    golden_dir.mkdir(parents=True, exist_ok=True)

    # Avoid dependency on playwright for other operations.
    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise GoldenUpdateError(
            "Playwright is required for golden image updates"
        ) from e

    my_print("Starting reference images update...")

    try:
        with sync_playwright() as p:
            for browser_name in browsers:
                _update_golden_browser(
                    p,
                    golden_dir=golden_dir,
                    browser_name=browser_name,
                    devices=devices,
                    pages=pages,
                    wait=wait,
                    verbose=verbose,
                    playwright_error_type=PlaywrightError,
                    playwright_timeout_error_type=PlaywrightTimeoutError,
                )
    except (OSError, PlaywrightTimeoutError, PlaywrightError) as e:
        raise GoldenUpdateError("Golden image update failed") from e

    my_print("Update completed successfully!")

    my_print("Summary:")
    my_print(f"- Browsers: {len(browsers)}")
    my_print(f"- Devices: {len(devices)}")
    my_print(f"- Pages: {len(pages)}")
    my_print(f"- Total images: {len(browsers) * len(devices) * len(pages)}")
    return 0


def getTranslationStatus():
    status = {}
    for path in Path("site").rglob("*.rst"):
        translations = []
        for locale in Path("locales").glob("*"):
            if Path(
                locale, "LC_MESSAGES", f"{str(path.relative_to('site'))[:-3]}po"
            ).exists():
                translations.append(locale.name)

            status[path] = translations

    return status


def updateTranslationStatusPage():
    page_template = getTemplate(
        package_name=None,
        template_name="translation-status.rst.j2",
        template_subdir="site",
    )

    table = [["Site", "Translations"]]

    for path, translations in sorted(getTranslationStatus().items()):
        if translations:
            table += [
                [
                    str(path.relative_to("site")).replace("\\", "/"),
                    ", ".join(sorted(translations)),
                ]
            ]

    template_context = {"translation_table": makeTable(table)}

    output = page_template.render(name=page_template.name, **template_context)

    with withFileOpenedAndAutoFormatted("site/translation-status.rst") as output_file:
        output_file.write(output + "\n")


def main():
    parser = OptionParser()

    parser.add_option(
        "--update-downloads",
        action="store_true",
        dest="downloads",
        default=False,
        help="""\
When given, the download page is updated. Default %default.""",
    )

    parser.add_option(
        "--update-docs",
        action="store_true",
        dest="docs",
        default=False,
        help="""\
When given, the rest files are updated and changelog is split into pages. Default %default.""",
    )

    parser.add_option(
        "--release-post-date",
        dest="release_post_date",
        default=None,
        help="""\
Publication date to use for newly generated release posts, formatted as YYYY/MM/DD HH:MM. Existing posts keep their current metadata, and new posts default to the current UTC day when this option is omitted.""",
    )

    parser.add_option(
        "--check-pages",
        action="store_true",
        dest="check_pages",
        default=False,
        help="""\
When given, the pages are checked with rest lint. Default %default.""",
    )

    parser.add_option(
        "--post-process",
        action="store_true",
        dest="post_process",
        default=False,
        help="""\
When given, the site is post processed. Default %default.""",
    )

    parser.add_option(
        "--serve-site",
        action="store_true",
        dest="serve",
        default=False,
        help="""\
When given, the site is re-built on changes and served locally. Default %default.""",
    )

    parser.add_option(
        "--deploy-site",
        action="store_true",
        dest="deploy",
        default=False,
        help="""\
When given, the site is deployed. Default %default.""",
    )

    parser.add_option(
        "--update-golden",
        action="store_true",
        dest="update_golden",
        default=False,
        help="Update reference images",
    )

    parser.add_option(
        "--browsers",
        dest="browsers",
        default=None,
        help="Comma-separated list of browsers to use",
    )

    parser.add_option(
        "--devices",
        dest="devices",
        default=None,
        help="Comma-separated list of device types to use",
    )

    parser.add_option(
        "--pages",
        dest="pages",
        default=None,
        help="Comma-separated list of pages to update",
    )

    parser.add_option(
        "--wait",
        type="int",
        dest="wait",
        default=None,
        help="Wait time in milliseconds before capture",
    )

    parser.add_option(
        "--clean",
        action="store_true",
        dest="clean",
        default=False,
        help="Clean images directory before updating",
    )

    parser.add_option(
        "--verbose",
        action="store_true",
        dest="verbose",
        default=False,
        help="Show detailed information during execution",
    )

    options, positional_args = parser.parse_args()

    if positional_args:
        raise ValueError(f"Unexpected positional arguments: {positional_args!r}")

    release_post_date = (
        _parseReleasePostDate(options.release_post_date)
        if options.release_post_date is not None
        else None
    )

    if options.docs:
        updateTranslationStatusPage()
        updateDocs(release_post_date=release_post_date)

    if options.downloads:
        updateDownloadPage()

    if options.check_pages:
        checkRestPages()

    if options.post_process:
        runPostProcessing()

    if options.serve:
        runSphinxAutoBuild()

    if options.deploy:
        runDeploymentCommand()

    if options.update_golden:
        runUpdateGolden(
            browsers=options.browsers.split(",") if options.browsers else None,
            devices=options.devices.split(",") if options.devices else None,
            pages=options.pages.split(",") if options.pages else None,
            wait=options.wait,
            clean=options.clean,
            verbose=options.verbose,
        )


if __name__ == "__main__":
    importNuitka()

    os.environ["PATH"] = (
        os.path.dirname(sys.executable) + os.pathsep + os.environ["PATH"]
    )

    main()
