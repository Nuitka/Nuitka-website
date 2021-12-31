#!/usr/bin/env python3.9

import datetime
import os
import re
import shutil
import subprocess
import sys
from io import StringIO
from optparse import OptionParser

import requests
import restructuredtext_lint
import unidecode
from urllib.request import urlretrieve
import zipfile

from lxml import html


def _updateCheckout(branch, update):
    if os.path.exists(f"Nuitka-{branch}") and not update:
        return

    if os.path.exists(f"Nuitka-{branch}"):
        shutil.rmtree(f"Nuitka-{branch}")

    print(f"Updating {branch} checkout...")
    sys.stdout.flush()

    urlretrieve(
        f"https://github.com/Nuitka/Nuitka/archive/{branch}.zip", "nuitka.zip.tmp"
    )

    with zipfile.ZipFile(f"nuitka.zip.tmp") as archive:
        archive.extractall(".")

    os.unlink("nuitka.zip.tmp")

    for filename in (
        "README.rst",
        "Developer_Manual.rst",
    ):
        filename = os.path.join(f"Nuitka-{branch}", filename)

        with open(filename, "rb") as patched_file:
            old_contents = new_contents = patched_file.read()

        if filename.endswith(".rst"):
            # Sphinx has its own TOC method.
            new_contents = new_contents.replace(b".. contents::\n", b"")

            # Logo inside doc removed.
            new_contents = new_contents.replace(
                b"\n.. image:: doc/images/Nuitka-Logo-Symbol.png\n", b"\n"
            )
            new_contents = new_contents.replace(b"\n   :alt: Nuitka Logo", b"\n")

        if old_contents != new_contents:
            with open(filename, "wb") as out_file:
                out_file.write(new_contents)


def updateNuitkaMaster(update):
    _updateCheckout("master", update=update)


def updateNuitkaDevelop(update):
    _updateCheckout("develop", update=update)


def updateNuitkaFactory(update):
    _updateCheckout("factory", update=update)


def importNuitka():
    updateNuitkaFactory(update=False)

    sys.path.insert(0, os.path.abspath("Nuitka-factory"))
    import nuitka

    del sys.path[0]


importNuitka()

# isort:start

from nuitka.tools.quality.autoformat.Autoformat import (
    withFileOpenedAndAutoformatted,
)
from nuitka.Tracing import my_print
from nuitka.utils.Jinja2 import getTemplate
from nuitka.utils.Rest import makeTable


def updateDownloadPage():
    # TODO: Move to at least develop, after next releease, or even pip install as a requirement
    # after release with an option to use other branches.

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
            elif v.isdigit() and (current.isdigit() or current == ""):
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

    msi_info = {}

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

        if (
            filename.startswith("Nuitka-")
            and filename.endswith(".msi")
            and "factory" not in filename
        ):

            parts = filename.split(".")

            if parts[-3] == "win32":
                bits = "32"
            elif parts[-3] == "win-amd64":
                bits = "64"
            else:
                my_print("Ignoring broken MSI filename %s" % filename, file=sys.stderr)
                continue

            version = parts[-2][2:]

            if numberize(filename)[2] == 1:
                category = "stable"
            else:
                category = "develop"

            key = category, version, bits

            if key not in msi_info:
                msi_info[key] = filename
            else:
                msi_info[key] = max(msi_info[key], filename, key=numberize)

            continue

        if not filename.endswith(".deb") or not filename.endswith("_all.deb"):
            continue

        # print "FILE", filename

        filename = filename[len("nuitka_") : -len("_all.deb")]

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
        "Max stable release is %s %s " % (max_stable_release, makePlain(max_stable_release))
    )

    output = ""

    def extractDebVersion(path):
        match = re.search(r"nuitka_(.*)_all\.deb", filename)

        return match.group(1)

    def makeRepositoryUrl(path):
        return "https://nuitka.net/" + path

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
        command = (
            "curl -s download.opensuse.org/repositories/home:/kayhayen/%s/noarch/"
            % repo_name
        )

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

            match = re.search(r"\>nuitka-(.*).noarch\.rpm\<", line)
            candidates.append(match.group(1))

        def numberize(x):
            if x.startswith("lp"):
                x = x[2:]
            if x.startswith("bp"):
                x = x[2:]

            return int(x)

        def splitVersion(v):
            for w in v.split("."):
                for x in w.split("rc"):
                    yield x

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

            match = re.search(r"\>nuitka-unstable-(.*).noarch\.rpm\<", line)
            candidates.append(match.group(1))

        max_prerelease = max(candidates, key=compareVersion)

        assert "6.7" not in max_prerelease, command

        my_print("Repo %s %s" % (repo_name, max_prerelease))

        return max_release, max_prerelease

    min_rhel = 6
    max_rhel = 7
    min_fedora = 28
    max_fedora = 35

    rhel_rpm = {}
    for rhel_number in range(min_rhel,max_rhel+1):
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

    max_suse_131_release, max_suse_131_prerelease = checkOBS("openSUSE_13.1")
    max_suse_132_release, max_suse_132_prerelease = checkOBS("openSUSE_13.2")
    max_suse_150_release, max_suse_150_prerelease = checkOBS("openSUSE_Leap_15.0")
    max_suse_151_release, max_suse_151_prerelease = checkOBS("openSUSE_Leap_15.1")
    max_suse_152_release, max_suse_152_prerelease = checkOBS("openSUSE_Leap_15.2")

    max_sle_150_release, max_sle_150_prerelease = checkOBS("SLE_15")

    def extractMsiVersion(filename):
        if not filename:
            return ""

        m1, m2, m3 = numberize(filename)[1:4]

        if not m2:
            result = "0.%d.%drc%d" % (m1, m3 / 100, (m3 / 10) % 10)
        else:
            result = "0.%d.%d.%d" % (m1, (m3 // 10), m3 % 10)

        return result

    findings = {
        "plain_prerelease": makePlain(max_pre_release),
        "deb_prerelease": max_pre_release,
        "plain_stable": makePlain(max_stable_release),
        "deb_stable": max_stable_release,
        "max_suse_131_release": max_suse_131_release,
        "suse_131_stable": max_suse_131_release.replace("-5.1", ""),
        "max_suse_132_release": max_suse_132_release,
        "suse_132_stable": max_suse_132_release.replace("-5.1", ""),
        "max_suse_150_release": max_suse_150_release,
        "suse_150_stable": max_suse_150_release.replace("-5.1", ""),
        "max_suse_151_release": max_suse_151_release,
        "suse_151_stable": max_suse_151_release.replace("-5.1", ""),
        "max_suse_152_release": max_suse_152_release,
        "suse_152_stable": max_suse_152_release.replace("-5.1", ""),
        "max_sle_150_release": max_sle_150_release,
        "sle_150_stable": max_sle_150_release.replace("-5.1", ""),
        # Unstable
        "max_suse_131_prerelease": max_suse_131_prerelease,
        "suse_131_unstable": max_suse_131_prerelease.replace("-5.1", ""),
        "max_suse_132_prerelease": max_suse_132_prerelease,
        "suse_132_unstable": max_suse_132_prerelease.replace("-5.1", ""),
        "max_suse_150_prerelease": max_suse_150_prerelease,
        "suse_150_unstable": max_suse_150_prerelease.replace("-5.1", ""),
        "max_suse_151_prerelease": max_suse_151_prerelease,
        "suse_151_unstable": max_suse_151_prerelease.replace("-5.1", ""),
        "max_suse_152_prerelease": max_suse_152_prerelease,
        "suse_152_unstable": max_suse_152_prerelease.replace("-5.1", ""),
        "max_sle_150_prerelease": max_sle_150_prerelease,
        "sle_150_unstable": max_sle_150_prerelease.replace("-5.1", ""),
    }

    templates = {
        "NUITKA_STABLE_TAR_GZ": r"`Nuitka %(plain_stable)s (0.6 MB tar.gz) <https://nuitka.net/releases/Nuitka-%(plain_stable)s.tar.gz>`__",
        "NUITKA_STABLE_TAR_BZ": r"`Nuitka %(plain_stable)s (0.5 MB tar.bz2) <https://nuitka.net/releases/Nuitka-%(plain_stable)s.tar.bz2>`__",
        "NUITKA_STABLE_ZIP": r"`Nuitka %(plain_stable)s (1.1 MB zip) <https://nuitka.net/releases/Nuitka-%(plain_stable)s.zip>`__",
        "NUITKA_STABLE_WININST": r"`Nuitka %(plain_stable)s (1.2 MB exe) <https://nuitka.net/releases/Nuitka-%(plain_stable)s.win32.exe>`__",
        "NUITKA_STABLE_DEBIAN": r"`Nuitka %(plain_stable)s (0.2 MB deb) <https://nuitka.net/releases/nuitka_%(deb_stable)s_all.deb>`__",
        "NUITKA_UNSTABLE_TAR_GZ": r"`Nuitka %(plain_prerelease)s (0.6 MB tar.gz) <https://nuitka.net/releases/Nuitka-%(plain_prerelease)s.tar.gz>`__",
        "NUITKA_UNSTABLE_TAR_BZ": r"`Nuitka %(plain_prerelease)s (0.5 MB tar.bz2) <https://nuitka.net/releases/Nuitka-%(plain_prerelease)s.tar.bz2>`__",
        "NUITKA_UNSTABLE_ZIP": r"`Nuitka %(plain_prerelease)s (1.2 MB zip) <https://nuitka.net/releases/Nuitka-%(plain_prerelease)s.zip>`__",
        "NUITKA_UNSTABLE_DEBIAN": r"`Nuitka %(plain_prerelease)s (0.2 MB deb) <https://nuitka.net/releases/nuitka_%(deb_prerelease)s_all.deb>`__",
        "NUITKA_STABLE_SUSE131": r"`Nuitka %(suse_131_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/noarch/nuitka-%(max_suse_131_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_SUSE132": r"`Nuitka %(suse_132_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/noarch/nuitka-%(max_suse_132_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_SUSE150": r"`Nuitka %(suse_150_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/noarch/nuitka-%(max_suse_150_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_SUSE151": r"`Nuitka %(suse_151_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.1/noarch/nuitka-%(max_suse_151_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_SUSE152": r"`Nuitka %(suse_152_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.2/noarch/nuitka-%(max_suse_152_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_SLE150": r"`Nuitka %(sle_150_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/SLE_15/noarch/nuitka-%(max_sle_150_release)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_SUSE131": r"`Nuitka %(suse_131_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.1/noarch/nuitka-unstable-%(max_suse_131_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_SUSE132": r"`Nuitka %(suse_132_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_13.2/noarch/nuitka-unstable-%(max_suse_132_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_SUSE150": r"`Nuitka %(suse_150_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.0/noarch/nuitka-unstable-%(max_suse_150_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_SUSE151": r"`Nuitka %(suse_151_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.1/noarch/nuitka-unstable-%(max_suse_151_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_SUSE152": r"`Nuitka %(suse_152_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/openSUSE_Leap_15.2/noarch/nuitka-unstable-%(max_suse_152_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_SLE150": r"`Nuitka %(sle_150_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/SLE_15/noarch/nuitka-unstable-%(max_sle_150_prerelease)s.noarch.rpm>`__",
        "NUITKA_STABLE_VERSION": "%(plain_stable)s",
    }

    for (category, code_name), (release_number, release_url) in list(deb_info.items()):
        if category == "stable":
            release = "release"
        elif category == "develop":
            release = "prerelease"
        elif category == "factory":
            release = "factory"
        else:
            assert False, category

        findings[code_name + "_" + release] = release_number[
            : release_number.find("+ds")
        ]
        findings[code_name + "_" + release + "_url"] = release_url

        templates[
            "NUITKA_" + category.upper() + "_" + code_name.upper()
        ] = """\
`Nuitka %%(%(code_name)s_release)s (0.6 MB deb) <%%(%(code_name)s_release_url)s>`__""" % {
            "code_name": code_name
        }

    for (category, version, bits), filename in list(msi_info.items()):
        if category == "develop":
            category = "unstable"

        findings["max_msi_" + category + "_" + version + "_" + bits] = filename
        findings["msi_" + category + "_" + version + "_" + bits] = extractMsiVersion(
            filename
        )

        templates[
            "NUITKA_" + category.upper() + "_MSI_" + version + "_" + bits
        ] = r"`Nuitka %%(msi_%(category)s_%(version)s_%(bits)s)s Python%(dot_version)s %(bits)s bit MSI <https://nuitka.net/releases/%%(max_msi_%(category)s_%(version)s_%(bits)s)s>`__" % {
            "version": version,
            "bits": bits,
            "category": category,
            "dot_version": version[0] + "." + version[-1],
        }

    def makeFedoraText(fedora_number, release):
        version = fedora_rpm[release, fedora_number]

        return f"""Nuitka {version.split("-", 1)[0]}"""

    def makeCentOSText(centos_number, release):
        version = centos_rpm[release, centos_number]

        return f"""Nuitka {version.split("-", 1)[0]}"""


    def makeRHELText(rhel_number, release):
        version = rhel_rpm[release, rhel_number]

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
        ("CentOS 8", makeRepoLinkText(f"CentOS_8"), makeCentOSText(8, "stable"),
            makeCentOSText(8, "develop"),
        ),
        ("CentOS 7", makeRepoLinkText(f"CentOS_7"), makeCentOSText(7, "stable"),
            makeCentOSText(7, "develop"),
        ),
        ("CentOS 6", makeRepoLinkText(f"CentOS_CentOS-6"), makeCentOSText(6, "stable"),
            makeCentOSText(6, "develop"),
        )
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


    template_context = {
        "fedora_table": fedora_table,
        "centos_table": centos_table,
        "rhel_table": rhel_table,
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

    open("doc/doc/download.rst", "wb").write(("\n".join(output) + "\n").encode("utf8"))


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
of `Nuitka <https://nuitka.net>`_. It is the extremely
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

            output_path = "posts"
            txt_path = os.path.join(output_path, slug + ".rst")

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

            with withFileOpenedAndAutoformatted(txt_path) as output_file:
                output_file.write("".join(lines))


def updateDocs():
    updateReleasePosts()


def runSphinxBuild():
    assert 0 == os.system("sphinx-build doc output/ -a")


def runSphinxAutoBuild():
    os.system(
        "python -m sphinx_autobuild doc output/ -a --watch doc --watch pages --watch Pipenv.lock"
    )


def checkRstLint(document):
    my_print("Checking %r for proper restructed text ..." % document)
    lint_results = restructuredtext_lint.lint_file(document, encoding="utf8")

    lint_error = False
    for lint_result in lint_results:
        # Not an issue.
        if lint_result.message.startswith("Duplicate implicit target name:"):
            continue

        if lint_result.message.startswith('No directive entry for "youtube"'):
            continue
        if lint_result.message.startswith('Unknown directive type "youtube"'):
            continue

        my_print(lint_result)
        lint_error = True

    if lint_error:
        sys.exit("Error, no lint clean rest.")

    my_print("OK.")


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

    command = (
        "rsync -ravz %s --chown www-data:git --chmod Dg+x --delete-after output/ root@nuitka.net:/var/www/"
        % (" ".join("--exclude=%s" % exclude for exclude in excluded))
    )

    my_print(command)
    assert 0 == os.system(command)


def checkRestPages():
    for root, _dirnames, filenames in os.walk("."):
        for filename in filenames:
            full_name = os.path.join(root, filename)

            if full_name.endswith(".rst"):

                checkRstLint(full_name)


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
When given, the pages are not checked with rest lint. Default %default.""",
    )

    parser.add_option(
        "--build-site",
        action="store_true",
        dest="build",
        default=False,
        help="""\
When given, the site is built. Default %default.""",
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
    #
    parser.add_option(
        "--update-all",
        action="store_true",
        dest="all",
        default=False,
        help="""\
When given, all is updated. Default %default.""",
    )

    options, positional_args = parser.parse_args()

    assert not positional_args, positional_args

    if options.all:
        options.downloads = True
        options.docs = True
        options.build = True
        options.deploy = True

    if options.docs or options.build:
        updateNuitkaMaster(update=True)
        updateNuitkaDevelop(update=True)
        updateNuitkaFactory(update=True)

    if options.docs:
        updateDocs()

    if options.downloads:
        updateDownloadPage()

    if options.check_pages:
        checkRestPages()

    if options.build:
        # Avoid left over files.
        output_dir = "output"
        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)

        runSphinxBuild()

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
