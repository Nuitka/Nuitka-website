#!/usr/bin/env python3.12

import copy
import datetime
import os
import re
import shutil
import subprocess
import sys
import zipfile
from io import StringIO
from optparse import OptionParser
from pathlib import Path
from urllib.request import urlretrieve

import requests
from lxml import html

# Which branches were already done.
updated_branches = set()


def _updateCheckout(branch, update):
    # We cannot use Nuitka directory change yet here.
    old_cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))

    try:
        if os.path.exists(f"Nuitka-{branch}") and not update:
            return

        if branch in updated_branches:
            return

        if os.path.exists(f"Nuitka-{branch}"):
            shutil.rmtree(f"Nuitka-{branch}")

        print(f"Updating {branch} checkout...")
        sys.stdout.flush()

        urlretrieve(
            f"https://github.com/Nuitka/Nuitka/archive/{branch}.zip", "nuitka.zip.tmp"
        )

        with zipfile.ZipFile("nuitka.zip.tmp") as archive:
            archive.extractall(".")

        os.unlink("nuitka.zip.tmp")
    finally:
        os.chdir(old_cwd)

    updated_branches.add(branch)


def updateNuitkaMain(update):
    _updateCheckout("main", update=update)


def updateNuitkaDevelop(update):
    _updateCheckout("develop", update=update)


def importNuitka():
    # TODO: Add an option to use other branches.
    updateNuitkaDevelop(update=False)

    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "Nuitka-develop"))
    )
    import nuitka.containers.OrderedSets

    del sys.path[0]

    return nuitka


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
)
from nuitka.utils.Hashing import getHashFromValues
from nuitka.utils.Jinja2 import getTemplate
from nuitka.utils.ReExecute import callExecProcess
from nuitka.utils.Rest import makeTable

in_devcontainer = os.getenv("REMOTE_CONTAINERS_DISPLAY_SOCK") is not None


def updateDownloadPage():
    page_source = requests.get("https://nuitka.net/releases/").text

    tree = html.parse(StringIO(page_source))
    link_names = tree.xpath("//@href")

    max_pre_release = ""
    max_stable_release = ""

    def numberize(value):
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
            max_pre_release = max(max_pre_release, filename, key=numberize)
        else:
            max_stable_release = max(max_stable_release, filename, key=numberize)

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

        def numberize(x):
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

            v = tuple(tuple(numberize(x) for x in splitVersion(value)) for value in v)

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


js_order = [
    "documentation_options.js",
    "jquery.js",
    "_sphinx_javascript_frameworks_compat.js",
    "doctools.js",
    "sphinx_highlight.js",
    "theme.js",
    "clipboard.min.js",
    "copybutton.js",
    "translations.js",
    "design-tabs.js",
]

excluded_js = [
    "carousel.js"
]


def _makeJsCombined(js_filenames):
    js_filenames = list(js_filenames)
    if "_static/jquery.js" not in js_filenames:
        js_filenames.append("_static/jquery.js")

    js_filenames = [
        js for js in js_filenames
        if os.path.basename(js) not in excluded_js
    ]

    js_set_contents = (
        "\n".join(getFileContents(f"output/{js_name}") for js_name in js_filenames)
        + """
jQuery(function () {
    SphinxRtdTheme.Navigation.enable(true);
});
    """
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


def runPostProcessing():
    # Compress the CSS and JS files into one file, clean up links, and
    # do other touch ups. spell-checker: ignore searchindex,searchtools

    for delete_filename in ("searchindex.js", "searchtools.js", "search.html"):
        deleteFile(os.path.join("output", delete_filename), must_exist=False)
        for translation in _translations:
            deleteFile(
                os.path.join("output", translation, delete_filename), must_exist=False
            )

    # Force working on the root document first.
    file_list = getFileList("output", only_suffixes=".html")
    file_list.remove("output/index.html")
    file_list.insert(0, "output/index.html")

    root_doc = None
    for filename in file_list:
        doc = html.fromstring(getFileContents(filename, mode="rb"))

        if root_doc is None:
            root_doc = doc

        # Repair favicon extension not cooperation with ablog extension,
        # copy over the root_doc links.
        fav_icons = doc.xpath("//head/link[@rel='icon']")

        if not fav_icons:
            (head_node,) = doc.xpath("head")
            for fav_icon in root_doc.xpath("//head/link[@rel='icon']"):
                fav_icon = copy.deepcopy(fav_icon)
                fav_icon.attrib["href"] = "/" + fav_icon.attrib["href"]

                head_node.append(fav_icon)

        # Check copybutton.js
        has_highlight = doc.xpath("//div[@class='highlight']")

        has_inline_tabs = doc.xpath("//*[@class='sd-tab-label']")

        # Detect if asciinema is used in the page
        has_asciinema = False
        for script_tag in doc.xpath("//script"):
            if script_tag.text and "AsciinemaPlayer" in script_tag.text:
                has_asciinema = True

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
            if "my_theme" not in css_link.get("href") or not in_devcontainer
            if "asciinema" not in css_link.get("href")
        ]:
            output_filename = "/_static/css/combined_%s.css" % getHashFromValues(
                *css_filenames
            )

            if not os.path.exists(output_filename):
                merged_css = "\n".join(
                    getFileContents(css_filename)
                    for css_filename in sorted(css_filenames, key=lambda x: "my_" in x)
                )

                # Do not display fonts on mobile devices.
                merged_css = re.sub(
                    r"@font-face\{(?!.*?awesome)(.*?)\}",
                    r"@media(min-width:901px){@font-face{\1}}",
                    merged_css,
                    flags=re.S,
                )
                merged_css = re.sub(
                    r"@font-face\{([^)]*?Lato)(.*?)\}",
                    r"",
                    merged_css,
                    flags=re.S,
                )
                merged_css = merged_css.replace("Lato", "ui-sans-serif")
                merged_css = re.sub(
                    r"@font-face\{([^)]*?Roboto Slab)(.*?)\}",
                    r"",
                    merged_css,
                    flags=re.S,
                )
                merged_css = merged_css.replace(
                    "Roboto Slab",
                    "Rockwell, 'Rockwell Nova','Roboto Slab','DejaVu Serif','Sitka Small',serif",
                )
                merged_css = re.sub(
                    r"@font-face\{(.*?)\}",
                    r"@font-face{font-display:swap;\1}",
                    merged_css,
                    flags=re.S,
                )

                merged_css = merged_css.replace(
                    "@media(min-width: 1200px)", "@media(min-width: 1500px)"
                )
                merged_css = merged_css.replace(
                    "@media(min-width: 992px)", "@media(min-width: 1192px)"
                )

                # Strip comments and trailing whitespace (created by that in part)
                merged_css = re.sub(r"/\*.*?\*/", "", merged_css, flags=re.S)
                merged_css = re.sub(r"\s+\n", r"\n", merged_css, flags=re.M)

                putTextFileContents(
                    filename=f"output{output_filename}", contents=merged_css
                )

            css_links[0].attrib["href"] = output_filename
            for css_link in css_links[1:]:
                if in_devcontainer and "my_theme" in css_link.attrib["href"]:
                    continue

                if "asciinema" in css_link.attrib["href"] and has_asciinema:
                    continue

                css_link.getparent().remove(css_link)

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

            if any(excluded_js_name in script_tag.attrib["src"] for excluded_js_name in excluded_js):
                continue


            if not has_highlight and "copybutton" in script_tag.attrib["src"]:
                script_tag.getparent().remove(script_tag)
            elif not has_highlight and "clipboard" in script_tag.attrib["src"]:
                script_tag.getparent().remove(script_tag)
            elif not has_inline_tabs and "design-tabs" in script_tag.attrib["src"]:
                script_tag.getparent().remove(script_tag)
            else:
                if script_tag_first is None:
                    script_tag_first = script_tag
                else:
                    script_tag.getparent().remove(script_tag)

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

                    js_filenames.append(script_tag.attrib["src"][1:])

        if script_tag_first is not None:
            script_tag_first.attrib["src"] = _makeJsCombined(js_filenames)

        file_language, translated_filenames = _getTranslationFileSet(filename)

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
            if top_link_nav is not None and False:
                top_link_nav.append(node)

        document_bytes = b"<!DOCTYPE html>\n" + html.tostring(
            doc, include_meta_content_type=True
        )

        document_bytes = fixupSymbols(document_bytes)

        document_bytes = document_bytes.replace(b"now &#187;", b"now&nbsp;&nbsp;&#187;")
        document_bytes = document_bytes.replace(b"/ yr", b'<i class="sub">/ yr</i>')

        with open(filename, "wb") as output:
            output.write(document_bytes)

    if in_devcontainer:
        my_theme_filename = "output/_static/my_theme.css"

        assert os.path.exists(my_theme_filename), my_theme_filename
        if not os.path.islink(my_theme_filename):
            os.unlink(my_theme_filename)
            os.symlink(os.path.abspath("_static/my_theme.css"), my_theme_filename)


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
        "intl",
        "--watch",
        "Pipenv.lock",
    ]

    callExecProcess(args, uac=False)


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

    if options.serve:
        runSphinxAutoBuild()

    if options.deploy:
        runDeploymentCommand()


if __name__ == "__main__":
    importNuitka()

    os.environ["PATH"] = (
        os.path.dirname(sys.executable) + os.pathsep + os.environ["PATH"]
    )

    main()
