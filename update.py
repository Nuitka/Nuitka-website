#!/usr/bin/env python3.12

"""Main interface to Nuitka-Website build process."""


import copy
import datetime
import os
import re
import subprocess
import sys
from io import StringIO
from optparse import OptionParser
from pathlib import Path
from settings import development_mode

import requests
from lxml import html

from nuitka_import import importNuitka

importNuitka()

# isort:start

from nuitka.tools.quality.auto_format.AutoFormat import (
    withFileOpenedAndAutoFormatted,
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

my_print("Development mode:", development_mode)

FA_STYLE_MAP = {
    "fas": "solid",
    "far": "regular",
    "fab": "brands",
    "fal": "light",
    "fad": "duotone",
    "fat": "thin",
    "fass": "sharp-solid",
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
            my_print(
                f"cp <tar_dir>/svgs/{style_folder}/{icon_name}.svg <project_dir>/{style_folder}/{icon_name}.svg\n"
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

    element.tail = None

    parent.replace(element, svg_element)

    if tail:
        tail_element = html.Element("span")

        tail_element.text = tail

        parent.append(tail_element)


def inlineImagesSvg(doc, filename):
    for img_tag in doc.xpath("//img[@src]"):
        src = img_tag.get("src")

        if not src.endswith(".svg"):
            continue

        if src.startswith(("http://", "https://")):
            continue

        src_clean = os.path.basename(src)

        svg_path = f"{SVG_SOURCE_PATH}/{src_clean}"

        assert os.path.exists(svg_path), (filename, src, svg_path)

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


def updateDownloadPage():
    page_source = requests.get("https://nuitka.net/releases/").text

    tree = html.parse(StringIO(page_source))
    link_names = tree.xpath("//@href")

    max_pre_release = ""
    max_stable_release = ""

    def get_numeric_version(value):
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

        for v in value:
            if v in ".-+":
                parts.append(current)
                current = ""
            elif v.isdigit() and (current.isdigit() or not current):
                current += v
            elif v.isdigit():
                parts.append(current)
                current = v
            elif current == "":
                current = v
            elif current.isdigit():
                parts.append(current)
                current = v
            elif current.isalpha() and v.isalpha():
                current += v
            else:
                assert False, (value, v)

        if current != "":
            parts.append(current)

        parts = [int(part) if part.isdigit() else part for part in parts]

        if "ds" in parts:
            parts.remove("ds")

        assert parts, value

        return parts

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

        assert filename.lower().startswith("nuitka"), filename

        if filename.endswith(".msi"):
            continue

        if not filename.endswith(".zip.sig"):
            continue

        # print "FILE", filename

        filename = filename[len("nuitka_") : -len(".zip.sig")]

        # print "VER", filename

        if "pre" in filename or "rc" in filename:
            max_pre_release = max(max_pre_release, filename, key=get_numeric_version)
        else:
            max_stable_release = max(
                max_stable_release, filename, key=get_numeric_version
            )

    def makePlain(value):
        value = (
            value.replace("+ds", "")
            .replace("~pre", "pre")
            .replace("~rc", "rc")
            .split("-")[0]
        )

        return value

    my_print(
        "Max pre-release is %s %s " % (max_pre_release, makePlain(max_pre_release))
    )
    my_print(
        "Max stable release is %s %s "
        % (max_stable_release, makePlain(max_stable_release))
    )

    output = ""

    def extractDebVersion(path):
        match = re.search(r"nuitka_(.*)_all\.deb", path)

        return match.group(1)

    def makeRepositoryUrl(path):
        return f"https://nuitka.net/{path}"

    deb_info = {}

    for line in output.split("\n"):
        if not line:
            continue

        parts = line.split(os.path.sep)

        assert parts[0] == "deb"
        category = parts[1]
        code_name = parts[2]

        filename = parts[-1]

        deb_info[category, code_name] = (
            extractDebVersion(filename),
            makeRepositoryUrl(line),
        )

    def checkOBS(repo_name):
        url = (
            "https://download.opensuse.org/repositories/home:/kayhayen/%s/noarch/"
            % repo_name
        )

        command = "curl -s %s" % url

        output = subprocess.check_output(command.split())
        output = output.decode("utf8").split("\n")

        candidates = []

        for line in output:
            if ".rpm" not in line:
                continue

            if "unstable" in line:
                continue

            if "experimental" in line:
                continue

            # spell-checker: ignore mirrorlist
            match = re.search(
                r'href="(?:\./)?nuitka-(.*).noarch\.rpm(?:\.mirrorlist)?"', line
            )

            try:
                candidates.append(match.group(1))
            except Exception:
                print("problem with line %r from '%s'" % (line, url))
                raise

        def get_numeric_version(x):
            if x.startswith("lp"):
                x = x[2:]
            if x.startswith("bp"):
                x = x[2:]

            return int(x)

        def splitVersion(v):
            for w in v.split("."):
                yield from w.split("rc")

        def compareVersion(v):
            v = v.split("-")

            v = tuple(
                tuple(get_numeric_version(x) for x in splitVersion(value))
                for value in v
            )

            return v

        max_release = max(candidates, key=compareVersion)

        candidates = []

        for line in output:
            if ".rpm" not in line:
                continue

            if "unstable" not in line:
                continue

            match = re.search(
                r'href="(?:\./)?nuitka-unstable-(.*).noarch\.rpm(?:\.mirrorlist)?"',
                line,
            )

            try:
                candidates.append(match.group(1))
            except Exception:
                print("problem with line %r from '%s'" % (line, url))
                raise

        max_prerelease = max(candidates, key=compareVersion)

        assert "6.7" not in max_prerelease, command

        my_print("Repo %s %s" % (repo_name, max_prerelease))

        return max_release, max_prerelease

    min_rhel = 7
    max_rhel = 8
    min_fedora = 36
    max_fedora = 36

    rhel_rpm = {}
    for rhel_number in range(min_rhel, max_rhel + 1):
        stable, develop = checkOBS("RedHat_RHEL-%d" % rhel_number)

        rhel_rpm["stable", rhel_number] = stable
        rhel_rpm["develop", rhel_number] = develop

    max_centos6_release, max_centos6_prerelease = checkOBS("CentOS_CentOS-6")
    max_centos7_release, max_centos7_prerelease = checkOBS("CentOS_7")
    max_centos8_release, max_centos8_prerelease = checkOBS("CentOS_8")

    centos_rpm = {}
    centos_rpm["stable", 6] = max_centos6_release
    centos_rpm["develop", 6] = max_centos6_prerelease
    centos_rpm["stable", 7] = max_centos7_release
    centos_rpm["develop", 7] = max_centos7_prerelease
    centos_rpm["stable", 8] = max_centos8_release
    centos_rpm["develop", 8] = max_centos8_prerelease

    fedora_rpm = {}
    for fedora_number in range(min_fedora, max_fedora + 1):
        stable, develop = checkOBS("Fedora_%d" % fedora_number)

        fedora_rpm["stable", fedora_number] = stable
        fedora_rpm["develop", fedora_number] = develop

    opensuse_rpm = {}

    min_leap_minor = 4
    max_leap_minor = 4
    for leap_minor in range(min_leap_minor, max_leap_minor + 1):
        stable, develop = checkOBS(f"openSUSE_Leap_15.{leap_minor}")

        opensuse_rpm["stable", leap_minor] = stable
        opensuse_rpm["develop", leap_minor] = develop

    max_sle_150_release, max_sle_150_prerelease = checkOBS("SLE_15")

    findings = {
        "plain_prerelease": makePlain(max_pre_release),
        "deb_prerelease": max_pre_release,
        "plain_stable": makePlain(max_stable_release),
        "deb_stable": max_stable_release,
    }

    templates = {}

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

    fedora_data = [
        (
            f"Fedora {fedora_number}",
            makeRepoLinkText(f"Fedora_{fedora_number}"),
            makeFedoraText(fedora_number, "stable"),
            makeFedoraText(fedora_number, "develop"),
        )
        for fedora_number in range(max_fedora, min_fedora - 1, -1)
    ]

    fedora_table = makeTable(
        [["Fedora Version", "RPM Repository", "Stable", "Develop"]] + fedora_data
    )

    centos_data = [
        (
            "CentOS 8",
            makeRepoLinkText("CentOS_8"),
            makeCentOSText(8, "stable"),
            makeCentOSText(8, "develop"),
        ),
        (
            "CentOS 7",
            makeRepoLinkText("CentOS_7"),
            makeCentOSText(7, "stable"),
            makeCentOSText(7, "develop"),
        ),
        (
            "CentOS 6",
            makeRepoLinkText("CentOS_CentOS-6"),
            makeCentOSText(6, "stable"),
            makeCentOSText(6, "develop"),
        ),
    ]

    centos_table = makeTable(
        [["CentOS Version", "RPM Repository", "Stable", "Develop"]] + centos_data
    )

    rhel_data = [
        (
            f"RHEL {rhel_number}",
            makeRepoLinkText("RedHat_RHEL-%d" % rhel_number),
            makeRHELText(rhel_number, "stable"),
            makeRHELText(rhel_number, "develop"),
        )
        for rhel_number in range(max_rhel, min_rhel - 1, -1)
    ]

    rhel_table = makeTable(
        [["RHEL Version", "RPM Repository", "Stable", "Develop"]] + rhel_data
    )

    suse_data = [
        (
            f"openSUSE Leap 15.{leap_minor}",
            makeRepoLinkText(f"openSUSE_Leap_15.{leap_minor}"),
            makeLeapText(leap_minor, "stable"),
            makeLeapText(leap_minor, "develop"),
        )
        for leap_minor in range(min_leap_minor, max_leap_minor + 1)
    ]

    suse_data.insert(
        0,
        (
            "SLE 15",
            makeRepoLinkText("SLE_15"),
            makeVersionText(max_sle_150_release),
            makeVersionText(max_sle_150_prerelease),
        ),
    )

    suse_table = makeTable(
        [["SUSE Version", "RPM Repository", "Stable", "Develop"]] + suse_data
    )

    plain_prerelease = makePlain(max_pre_release)
    plain_stable = makePlain(max_stable_release)

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
        try:
            end_line = section_markers[count + 1][0]
        except IndexError:
            end_line = None

        yield title, lines[section_start_line + 3 : end_line]


def updateReleasePosts():
    _updateReleasePosts("site/changelog/Changelog.rst")
    _updateReleasePosts("site/changelog/Changelog-1.x.rst")
    _updateReleasePosts("site/changelog/Changelog-0.x.rst")


def _updateReleasePosts(changelog_filename):
    count = 0

    for title, lines in _splitRestByChapter(open(changelog_filename).readlines()):
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

        if os.path.exists(txt_path):
            pub_date = open(txt_path).readline().split(maxsplit=2)[2].strip()
        else:
            pub_date = datetime.datetime.now() + datetime.timedelta(days=1)
            pub_date = pub_date.strftime("%Y/%m/%d %H:%M")

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


def updateDocs():
    updateReleasePosts()


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
    processed_css = _processWithPostCSS(merged_css)

    # Validate processed CSS: fallback to original if empty or
    # invalid, but only in development mode.
    if not processed_css:
        assert development_mode
        processed_css = merged_css

        my_print("Warning, postcss failed, using original CSS")

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

        if processed_js is not None:
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

        found = 0
        result = b""

        for line in contents.splitlines():
            if found == 1:
                assert not line, value
                found = 2
                continue

            if found == 2:
                if not line:
                    break

                result += line.strip()
                continue

            if value in line:
                found = 1

        assert result, value
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
        result = subprocess.run(
            ["npm", "run", script],
            env={**os.environ, "INPUT": tmp_input_path, "OUTPUT": tmp_output_path},
            capture_output=True,
            text=True,
        )

        if result.stdout.strip():
            my_print(f"{label} tool output: {result.stdout.strip()}")

        if result.returncode != 0:
            my_print(f"{label} processing failed: {result.stderr.strip()}")
            return None

        processed = getFileContents(tmp_output_path, mode="r", encoding="utf-8")
        cache[contents] = processed

        processed_size = len(processed)
        if original_size > 0:
            reduction_percent = (original_size - processed_size) / original_size * 100
            my_print(
                f"{label} reduced by {reduction_percent:.1f}% ({original_size} → {processed_size} bytes)"
            )

    except Exception as e:
        my_print(f"Unexpected error running {label} tool: {e}")
        return None
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

        if result.stdout.strip():
            my_print(f"HTML-minifier output: {result.stdout.strip()}")

        if result.returncode != 0:
            my_print(f"HTML-minifier failed: {result.stderr.strip()}")
            return None

        if os.path.exists(filename):
            os.replace(filename, filename)
        else:
            my_print(f"Expected minified file not found: {filename}")
            return None

    except Exception as e:
        my_print(f"Unexpected error in HTML processing: {e}")
        return None

    _html_minifier_cache[filename] = getFileContents(
        filename, mode="r", encoding="utf-8"
    )


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

            assert script_tag.attrib["src"][0] == "/", script_tag.attrib["src"]
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
        if processed_theme_css:
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
            (head_node,) = doc.xpath("head")
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
                assert parent_tag.tag == "p", parent_tag
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
                    for sub_child in first_child:
                        first_child.remove(sub_child)
                        current_hub_title.insert(0, sub_child)

                    first_child.attrib["class"] = (
                        current_hub_card.attrib["class"] + " hub-card-link"
                    )

                break

        css_links = doc.xpath("//link[@rel='stylesheet']")
        assert css_links

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
            try:
                h1 = doc.xpath("//h1")[0]
            except IndexError:
                pass
            else:
                top_nav = html.fromstring("""<div class="top_nav"></div>""")
                h1.getparent().insert(h1.getparent().index(h1), top_nav)

                (top_link_nav,) = doc.xpath("//nav[@class='top_link_nav']")
                top_link_nav.getparent().remove(top_link_nav)
                top_nav.append(top_link_nav)

                social_container = doc.xpath("//div[@class='share-button-container']")[
                    0
                ]
                social_container.getparent().remove(social_container)
                top_link_nav.append(social_container)

                try:
                    blog_container = doc.xpath("//div[@class='blog-post-box']")[0]
                except IndexError:
                    pass
                else:
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

        assert os.path.exists(my_theme_filename), my_theme_filename
        if not os.path.islink(my_theme_filename):
            os.unlink(my_theme_filename)
            os.symlink(os.path.abspath("_static/my_theme.css"), my_theme_filename)

    cleanBuildSVGs()

# Post processing for the offline documentation bundle.
def runBundlePostProcessing(output_dir):
    my_print(f"Post-processing bundle in {output_dir}...")

    # Remove files that require external resources
    files_to_remove = (
        "searchindex.js",
        "searchtools.js",
        "search.html",
    )

    for filename in files_to_remove:
        deleteFile(os.path.join(output_dir, filename), must_exist=False)

    # Remove external font files that won't work offline
    fonts_path = os.path.join(output_dir, "_static/fonts")
    if os.path.exists(fonts_path):
        for filename in os.listdir(fonts_path):
            if filename.lower().startswith("fontawesome"):
                deleteFile(os.path.join(fonts_path, filename), must_exist=False)

    # Process HTML files to remove external content and fix links for offline use
    for html_file in getFileList(output_dir, only_suffixes=".html"):
        doc = html.fromstring(getFileContents(html_file, mode="rb"))

        file_dir = os.path.dirname(html_file)
        depth = len(os.path.relpath(file_dir, output_dir).split(os.sep))
        if os.path.relpath(file_dir, output_dir) == ".":
            depth = 0
        path_to_root = "../" * depth if depth > 0 else "./"

        # Fix absolute paths to relative paths for offline viewing
        for link_tag in doc.xpath("//a[@href]"):
            href = link_tag.get("href")
            if href.startswith("/") and not href.startswith("//"):
                link_tag.set("href", path_to_root + href.lstrip("/"))

        for img_tag in doc.xpath("//img[@src]"):
            src = img_tag.get("src")
            if src.startswith("/") and not src.startswith("//"):
                img_tag.set("src", path_to_root + src.lstrip("/"))

        for css_link in doc.xpath("//link[@href]"):
            href = css_link.get("href")
            if href.startswith("/") and not href.startswith("//"):
                css_link.set("href", path_to_root + href.lstrip("/"))

        for script_tag in doc.xpath("//script[@src]"):
            src = script_tag.get("src")
            if "search" in src.lower() or "analytics" in src.lower():
                script_tag.getparent().remove(script_tag)
                continue
            # Remove external scripts that require internet
            elif src.startswith(("http://", "https://", "//")):
                script_tag.getparent().remove(script_tag)
                continue
            elif src.startswith("/") and not src.startswith("//"):
                script_tag.set("src", path_to_root + src.lstrip("/"))

        # Remove external scripts without src attribute (inline scripts with external calls)
        for script_tag in doc.xpath("//script[not(@src)]"):
            if script_tag.text and ("http://" in script_tag.text or "https://" in script_tag.text):
                script_tag.getparent().remove(script_tag)

        # Remove all iframes
        for iframe in doc.xpath("//iframe"):
            iframe.getparent().remove(iframe)

        for style_tag in doc.xpath("//style"):
            if style_tag.text and "responsive-google-slides" in style_tag.text:
                style_tag.getparent().remove(style_tag)

        # Remove search form
        for search_form in doc.xpath("//form[@class='search']"):
            search_form.getparent().remove(search_form)

        for social_container in doc.xpath("//div[@class='share-button-container']"):
            social_container.getparent().remove(social_container)

        for lang_switcher in doc.xpath("//details[contains(@class, 'language-switcher')]"):
            lang_switcher.getparent().remove(lang_switcher)

        for blog_box in doc.xpath("//div[@class='blog-post-box']"):
            blog_box.getparent().remove(blog_box)

        result = html.tostring(
            doc,
            encoding="UTF-8",
            method="html",
            doctype="<!DOCTYPE html>",
        )
        with open(html_file, "wb") as output:
            output.write(result)

    my_print("Bundle post-processing complete.")


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
        "'doc/*.pdf'",
        # Google ownership marker, do not touch, spell-checker: ignore googlee
        "googlee5244704183a9a15.html",
        # Link into blog, for compatibility with old blog subscriptions.
        "rss.xml",
    ]

    target_dir = "/var/www/"
    command = f'rsync -ravz {" ".join(f"--exclude={exclude}" for exclude in excluded)} --chown www-data:git --chmod Dg+x --delete-after output/ root@ssh.nuitka.net:{target_dir}'

    my_print(command)

    assert 0 == os.system(command)


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

    callExecProcess(args, uac=False)


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
    from playwright.sync_api import sync_playwright

    try:
        my_print("Starting reference images update...")
        with sync_playwright() as p:
            for browser_name in browsers:
                browser_type = getattr(p, browser_name)
                browser = browser_type.launch(headless=True)

                for viewport_mode in devices:
                    if viewport_mode == "desktop":
                        device_config = DESKTOP_DEVICES[browser_name]
                    elif viewport_mode == "mobile":
                        device_config = MOBILE_DEVICES[browser_name]
                    else:
                        raise ValueError(f"Unknown viewport mode: {viewport_mode}")

                    context = browser.new_context(**device_config)
                    page = context.new_page()

                    for page_path in pages:
                        url = build_url(page_path)
                        safe_name = sanitizeUrl(page_path)
                        golden_path = (
                            golden_dir
                            / f"{browser_name}_{viewport_mode}_{safe_name}.png"
                        )

                        if verbose:
                            my_print(
                                f"  Generating {browser_name} / {viewport_mode} / {page_path} -> {golden_path}"
                            )

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
                        page.screenshot(path=golden_path, full_page=True, timeout=20000)

                    context.close()
                browser.close()

        my_print("Update completed successfully!")

    except Exception as e:
        import traceback

        my_print(f"Error during update: {e}")
        traceback.print_exc()
        return 1

    my_print("Summary:")
    my_print(f"- Browsers: {len(browsers)}")
    my_print(f"- Viewports: {len(devices)}")
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
        "--post-process-bundle",
        action="store_true",
        dest="post_process_bundle",
        default=False,
        help="""\
When given, the bundle is post processed. Default %default.""",
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

    assert not positional_args, positional_args

    if options.docs:
        updateTranslationStatusPage()
        updateDocs()

    if options.downloads:
        updateDownloadPage()

    if options.check_pages:
        checkRestPages()

    if options.post_process:
        runPostProcessing()

    if options.post_process_bundle:
        runBundlePostProcessing(output_dir="bundle-output")

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
