#!/usr/bin/env python3.10

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


def updateNuitkaFactory(update):
    _updateCheckout("factory", update=update)


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
    getFileContents,
    getFileList,
    putTextFileContents,
)
from nuitka.utils.Hashing import getHashFromValues
from nuitka.utils.Jinja2 import getTemplate
from nuitka.utils.Rest import makeTable


def updateDownloadPage():
    page_template = getTemplate(
        package_name=None, template_name="download.rst.j2", template_subdir="doc/doc"
    )

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
            except Exception as e:
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
            makeRepoLinkText(f"CentOS_8"),
            makeCentOSText(8, "stable"),
            makeCentOSText(8, "develop"),
        ),
        (
            "CentOS 7",
            makeRepoLinkText(f"CentOS_7"),
            makeCentOSText(7, "stable"),
            makeCentOSText(7, "develop"),
        ),
        (
            "CentOS 6",
            makeRepoLinkText(f"CentOS_CentOS-6"),
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
            makeRepoLinkText(f"RedHat_RHEL-%d" % rhel_number),
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
            makeRepoLinkText(f"SLE_15"),
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

    template_context = {
        "stable_version": plain_stable,
        "fedora_table": fedora_table,
        "centos_table": centos_table,
        "rhel_table": rhel_table,
        "suse_table": suse_table,
        "source_table": source_table,
    }

    download_page = page_template.render(name=page_template.name, **template_context)

    variable = None
    output = []

    for line in download_page.rstrip().split("\n"):
        if not line:
            output.append(line)
            continue

        if variable is not None:
            output.append("   " + templates[variable] % findings)
        else:
            output.append(line)

        if line.startswith("..") and line.endswith("replace::"):
            parts = line.split("|")
            assert len(parts) == 3

            variable = parts[1]
        else:
            variable = None

    with withFileOpenedAndAutoFormatted("doc/doc/download.rst") as output_file:
        output_file.write("\n".join(output) + "\n")


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


def splitRestByChapter(lines):
    marker = "***"

    await_title = "outside"

    for count, line in enumerate(lines):
        line = line.rstrip("\n")

        if line.startswith(marker):
            if await_title == "outside":
                await_title = "title"
            elif await_title == "marker":
                await_title = "outside"

                for count2, line in enumerate(lines[count + 1 :]):
                    count2 += count

                    if line.startswith(marker):
                        title = lines[count - 1].rstrip("\n")

                        body = lines[count + 1 : count2]

                        while body and not body[0].rstrip("\n"):
                            del body[0]

                        yield title, body
                        break
        elif await_title == "title":
            await_title = "marker"


def updateReleasePosts():
    count = 0
    sep = "#"

    # Make sure changelog is there.
    updateNuitkaFactory(update=True)

    with open("doc/doc/Changelog.rst", "w") as changelog_output:
        for title, lines in splitRestByChapter(
            open("Nuitka-factory/Changelog.rst").readlines()
        ):
            if count == 3:
                older = "Older Releases"

                changelog_output.write("\n\n" + sep * len(older) + "\n")
                changelog_output.write(older + "\n")
                changelog_output.write(sep * len(older) + "\n\n")
                changelog_output.write("These are older releases of Nuitka.")

                sep = "="

            changelog_output.write("\n\n")
            if sep != "=":
                changelog_output.write(sep * len(title) + "\n")
            else:
                title = title.lstrip()

            changelog_output.write(title + "\n")
            changelog_output.write(sep * len(title) + "\n\n")

            if sep == "=":
                changelog_lines = [
                    line.replace("=", "-") if line.startswith("===") else line
                    for line in lines
                ]
            else:
                changelog_lines = lines

            changelog_output.writelines(changelog_lines)
            count += 1

            # Ignore draft for pages.
            if "Draft" in title:
                continue

            # For the pages, use a leading sentence.
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

            slug = slugify(title)

            if "release-038" in slug:
                slug += "---windows-support"

            if "release-02" in slug:
                slug = slug.replace("nuitka-release", "release-nuitka")

            if "release-011" in slug:
                slug = "minor-" + slug.replace("nuitka-release", "release-nuitka")

            output_path = "doc/posts"
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


def runPostProcessing():
    # Compress the CSS and JS files into one file.

    documentation_options_js_filename = "output/_static/documentation_options.js"

    searchindex_js_filename = "output/searchindex.js"

    search_html_filename = "output/search.html"

    js_set_1 = [
        "documentation_options",
        "jquery",
        "_sphinx_javascript_frameworks_compat",
        "doctools",
        "sphinx_highlight",
        "js/theme",
    ]
    js_set_1_contents = (
        "\n".join(
            getFileContents(f"output/_static/{js_name}.js") for js_name in js_set_1
        )
        + """
jQuery(function () {
    SphinxRtdTheme.Navigation.enable(true);
});
    """
    )

    js_set_1_output_filename = "/_static/combined_%s.js" % getHashFromValues(
        js_set_1_contents
    )

    putTextFileContents(f"output{js_set_1_output_filename}", js_set_1_contents)

    for filename in getFileList("output", only_suffixes=".html"):
        doc = html.fromstring(getFileContents(filename, mode="rb"))

        # Check copybutton.js
        has_highlight = doc.xpath("//div[@class='highlight']")

        has_inline_tabs = doc.xpath("//*[@class='sd-tab-label']")

        for search_link in doc.xpath("//link[@rel='search']"):
            search_link.getparent().remove(search_link)

        css_links = doc.xpath("//link[@rel='stylesheet']")
        assert css_links

        bread_crumbs_hr = doc.xpath("//div[@role='navigation']/hr")
        if bread_crumbs_hr:
            bread_crumbs_hr[0].getparent().remove(bread_crumbs_hr[0])

        for caption_node in doc.xpath("//p[@class='caption' and @role='heading']"):
            caption_node.attrib["aria-expanded"] = "true"

        if css_filenames := [
            os.path.normpath(
                f'output/{os.path.relpath(os.path.dirname(filename), "output")}/{css_link.get("href")}'
            ).split("?")[0]
            for css_link in css_links
            if "combined_" not in css_link.get("href")
            if "copybutton" not in css_link.get("href") or has_highlight
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
                merged_css = merged_css.replace(
                    "Lato", "ui-sans-serif"
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
                css_link.getparent().remove(css_link)

        for link in doc.xpath("//a[not(contains(@classes, 'intern'))]"):
            if (
                link.attrib["href"].startswith("http:")
                or link.attrib["href"].startswith("https:")
            ) and "nuitka.net" not in link.attrib["href"]:
                link.attrib["target"] = "_blank"

        for link in doc.xpath("//link[@rel='canonical']"):
            if link.attrib["href"].endswith("/index.html"):
                link.attrib["href"] = link.attrib["href"][:-11]

        (logo_img,) = doc.xpath("//img[@class='logo']")

        logo_img.attrib["width"] = "208"
        logo_img.attrib["height"] = "209"

        logo_parent = logo_img.getparent()
        logo_parent.remove(logo_img)
        logo_div = html.fromstring("""<div class="logo_container"></div>""")
        logo_div.append(logo_img)
        logo_parent.append(logo_div)

        social_images = doc.xpath("//img[contains(@src, '/_static/icon-')]")
        assert len(social_images) == 4, (filename, social_images)

        for social_image in social_images:
            social_image.attrib["width"] = "24"
            social_image.attrib["height"] = "24"

        for script_tag in doc.xpath("//script"):
            if "src" not in script_tag.attrib:
                if (
                    script_tag.text
                    and "SphinxRtdTheme.Navigation.enable(true);" in script_tag.text
                ):
                    script_tag.getparent().remove(script_tag)

                continue

            script_tag.attrib["async"] = ""

            # Google search.
            if "google" in script_tag.attrib["src"]:
                continue

            if not has_highlight and "copybutton" in script_tag.attrib["src"]:
                script_tag.getparent().remove(script_tag)
            elif not has_highlight and "clipboard" in script_tag.attrib["src"]:
                script_tag.getparent().remove(script_tag)
            elif not has_inline_tabs and "design-tabs" in script_tag.attrib["src"]:
                script_tag.getparent().remove(script_tag)
            elif (
                any(js_name in script_tag.attrib["src"] for js_name in js_set_1)
                and "combined" not in script_tag.attrib["src"]
            ):
                if js_set_1[0] in script_tag.attrib["src"]:
                    script_tag.attrib["src"] = js_set_1_output_filename
                else:
                    script_tag.getparent().remove(script_tag)

        file_language, translated_filenames = _getTranslationFileSet(filename)

        if len(translated_filenames) == 1:
            for node in doc.xpath('//footer//details["sd-dropdown"]'):
                node.getparent().remove(node)
        else:
            # assert False, (translated_files, filename)
            doc.xpath('//footer//details["sd-dropdown"]/summary')[
                0
            ].text = file_language

            link_node = doc.xpath("//footer//details//@href")[0].getparent()
            line_node = link_node.getparent()
            dropdown_node = line_node.getparent()
            dropdown_node.clear()

            for translated_filename in sorted(translated_filenames):
                if filename == translated_filename:
                    continue

                language, _ = _getLanguageFromFilename(translated_filename)

                link_node.attrib["href"] = "/" + os.path.relpath(
                    translated_filename, "output"
                )
                link_node.text = language

                new_line_node = copy.deepcopy(line_node)

                dropdown_node.append(new_line_node)

        document_bytes = b"<!DOCTYPE html>\n" + html.tostring(
            doc, include_meta_content_type=True
        )

        document_bytes = document_bytes.replace(b"now &#187;", b"now&nbsp;&nbsp;&#187;")
        document_bytes = document_bytes.replace(b"/ yr", b'<i class="sub">/ yr</i>')

        with open(filename, "wb") as output:
            output.write(document_bytes)

    if os.path.exists(searchindex_js_filename):
        os.unlink(searchindex_js_filename)

    if os.path.exists(search_html_filename):
        os.unlink(search_html_filename)


def runDeploymentCommand():
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
        # Google ownership marker, do not touch.
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
    # Use sphinx_autobuild, but force misc/sphinx-build to be used.
    # TODO: For Windows, a batch file would be needed that does the
    # same thing.
    os.system(
        "python misc/sphinx_autobuild_wrapper.py doc output/ --watch misc --watch update.py --watch doc --watch intl --watch Pipenv.lock"
    )


def getTranslationStatus():
    status = {}
    for path in Path("doc").rglob("*.rst"):
        translations = []
        for locale in Path("locales").glob("*"):
            if Path(
                locale, "LC_MESSAGES", f"{str(path.relative_to('doc'))[:-3]}po"
            ).exists():
                translations.append(locale.name)

            status[path] = translations

    return status


def updateTranslationStatusPage():
    page_template = getTemplate(
        package_name=None,
        template_name="translation-status.rst.j2",
        template_subdir="doc",
    )

    table = [["Site", "Translations"]]

    for path, translations in sorted(getTranslationStatus().items()):
        if translations:
            table += [
                [
                    str(path.relative_to("doc")).replace("\\", "/"),
                    ", ".join(sorted(translations)),
                ]
            ]

    template_context = {"translation_table": makeTable(table)}

    output = page_template.render(name=page_template.name, **template_context)

    with withFileOpenedAndAutoFormatted("doc/translation-status.rst") as output_file:
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
When given, the site is post processed with minify. Default %default.""",
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
