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
                print("Ignoring broken MSI filename %s" % filename, file=sys.stderr)
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

    print("Max pre-release is", max_pre_release, makePlain(max_pre_release))
    print("Max stable release is", max_stable_release, makePlain(max_stable_release))
    sys.stdout.flush()

    if False:
        output = subprocess.check_output(
            r"ssh -l root nuitka.net cd /var/www && find deb -name \*.deb".split(),
            shell=False,
        )

        output = output.decode("utf8")
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

        def compareVersion(v):
            v = v.split("-")

            v = tuple(tuple(numberize(x) for x in value.split(".")) for value in v)

            return v

        max_release = max(candidates, key=compareVersion)

        for line in output:
            if ".rpm" not in line:
                continue

            if "unstable" not in line:
                continue

            match = re.search(r"\>nuitka-unstable-(.*).noarch\.rpm\<", line)
            max_prerelease = match.group(1)

            break

        return max_release, max_prerelease

    max_rhel6_release, max_rhel6_prerelease = checkOBS("RedHat_RHEL-6")
    max_rhel7_release, max_rhel7_prerelease = checkOBS("RedHat_RHEL-7")

    max_centos6_release, max_centos6_prerelease = checkOBS("CentOS_CentOS-6")
    max_centos7_release, max_centos7_prerelease = checkOBS("CentOS_7")
    max_centos8_release, max_centos8_prerelease = checkOBS("CentOS_8")

    max_f24_release, max_f24_prerelease = checkOBS("Fedora_24")
    max_f25_release, max_f25_prerelease = checkOBS("Fedora_25")
    max_f26_release, max_f26_prerelease = checkOBS("Fedora_26")
    max_f27_release, max_f27_prerelease = checkOBS("Fedora_27")
    max_f28_release, max_f28_prerelease = checkOBS("Fedora_28")
    max_f29_release, max_f29_prerelease = checkOBS("Fedora_29")
    max_f30_release, max_f30_prerelease = checkOBS("Fedora_30")
    max_f31_release, max_f31_prerelease = checkOBS("Fedora_31")
    max_f32_release, max_f32_prerelease = checkOBS("Fedora_32")
    max_f33_release, max_f33_prerelease = checkOBS("Fedora_33")
    max_f34_release, max_f34_prerelease = checkOBS("Fedora_34")

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
        "max_centos6_release": max_centos6_release,
        "centos6_stable": max_centos6_release.replace("-5.1", ""),
        "max_centos7_release": max_centos7_release,
        "centos7_stable": max_centos7_release.replace("-5.1", ""),
        "max_centos8_release": max_centos8_release,
        "centos8_stable": max_centos8_release.replace("-5.1", ""),
        "max_f24_release": max_f24_release,
        "f24_stable": max_f24_release.replace("-5.1", ""),
        "max_f25_release": max_f25_release,
        "f25_stable": max_f25_release.replace("-5.1", ""),
        "max_f26_release": max_f26_release,
        "f26_stable": max_f26_release.replace("-5.1", ""),
        "max_f27_release": max_f27_release,
        "f27_stable": max_f27_release.replace("-5.1", ""),
        "max_f28_release": max_f28_release,
        "f28_stable": max_f28_release.replace("-5.1", ""),
        "max_f29_release": max_f29_release,
        "f29_stable": max_f29_release.replace("-5.1", ""),
        "max_f30_release": max_f30_release,
        "f30_stable": max_f30_release.replace("-5.1", ""),
        "max_f31_release": max_f31_release,
        "f31_stable": max_f31_release.replace("-5.1", ""),
        "max_f32_release": max_f32_release,
        "f32_stable": max_f32_release.replace("-5.1", ""),
        "max_f33_release": max_f33_release,
        "f33_stable": max_f33_release.replace("-5.1", ""),
        "max_f34_release": max_f34_release,
        "f34_stable": max_f34_release.replace("-5.1", ""),
        "max_rhel6_release": max_rhel6_release,
        "rhel6_stable": max_rhel6_release.replace("-5.1", ""),
        "max_rhel7_release": max_rhel7_release,
        "rhel7_stable": max_rhel7_release.replace("-5.1", ""),
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
        "max_centos6_prerelease": max_centos6_prerelease,
        "centos6_unstable": max_centos6_prerelease.replace("-5.1", ""),
        "max_centos7_prerelease": max_centos7_prerelease,
        "centos7_unstable": max_centos7_prerelease.replace("-5.1", ""),
        "max_centos8_prerelease": max_centos8_prerelease,
        "centos8_unstable": max_centos8_prerelease.replace("-5.1", ""),
        "max_f24_prerelease": max_f24_prerelease,
        "f24_unstable": max_f24_prerelease.replace("-5.1", ""),
        "max_f25_prerelease": max_f25_prerelease,
        "f25_unstable": max_f25_prerelease.replace("-5.1", ""),
        "max_f26_prerelease": max_f26_prerelease,
        "f26_unstable": max_f26_prerelease.replace("-5.1", ""),
        "max_f27_prerelease": max_f27_prerelease,
        "f27_unstable": max_f27_prerelease.replace("-5.1", ""),
        "max_f28_prerelease": max_f28_prerelease,
        "f28_unstable": max_f28_prerelease.replace("-5.1", ""),
        "max_f29_prerelease": max_f29_prerelease,
        "f29_unstable": max_f29_prerelease.replace("-5.1", ""),
        "max_f30_prerelease": max_f30_prerelease,
        "f30_unstable": max_f30_prerelease.replace("-5.1", ""),
        "max_f31_prerelease": max_f31_prerelease,
        "f31_unstable": max_f31_prerelease.replace("-5.1", ""),
        "max_f32_prerelease": max_f32_prerelease,
        "f32_unstable": max_f32_prerelease.replace("-5.1", ""),
        "max_f33_prerelease": max_f33_prerelease,
        "f33_unstable": max_f33_prerelease.replace("-5.1", ""),
        "max_f34_prerelease": max_f34_prerelease,
        "f34_unstable": max_f34_prerelease.replace("-5.1", ""),
        "max_rhel6_prerelease": max_rhel6_prerelease,
        "rhel6_unstable": max_rhel6_prerelease.replace("-5.1", ""),
        "max_rhel7_prerelease": max_rhel7_prerelease,
        "rhel7_unstable": max_rhel7_prerelease.replace("-5.1", ""),
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
        "NUITKA_STABLE_RHEL6": r"`Nuitka %(rhel6_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/noarch/nuitka-%(max_rhel6_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_RHEL7": r"`Nuitka %(rhel7_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/noarch/nuitka-%(max_rhel7_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_CENTOS6": r"`Nuitka %(centos6_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/noarch/nuitka-%(max_centos6_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_CENTOS7": r"`Nuitka %(centos7_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/noarch/nuitka-%(max_centos7_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_CENTOS8": r"`Nuitka %(centos8_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_8/noarch/nuitka-%(max_centos8_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F20": r"`Nuitka %(f20_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_20/noarch/nuitka-%(max_f20_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F21": r"`Nuitka %(f21_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_21/noarch/nuitka-%(max_f21_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F22": r"`Nuitka %(f22_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_22/noarch/nuitka-%(max_f22_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F23": r"`Nuitka %(f23_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_23/noarch/nuitka-%(max_f23_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F24": r"`Nuitka %(f24_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/noarch/nuitka-%(max_f24_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F25": r"`Nuitka %(f25_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/noarch/nuitka-%(max_f25_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F26": r"`Nuitka %(f26_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/noarch/nuitka-%(max_f26_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F27": r"`Nuitka %(f27_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/noarch/nuitka-%(max_f27_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F28": r"`Nuitka %(f28_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/noarch/nuitka-%(max_f28_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F29": r"`Nuitka %(f29_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/noarch/nuitka-%(max_f29_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F30": r"`Nuitka %(f30_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_30/noarch/nuitka-%(max_f30_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F31": r"`Nuitka %(f31_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_31/noarch/nuitka-%(max_f31_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F32": r"`Nuitka %(f32_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_32/noarch/nuitka-%(max_f32_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F33": r"`Nuitka %(f33_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_33/noarch/nuitka-%(max_f33_release)s.noarch.rpm>`__",
        "NUITKA_STABLE_F34": r"`Nuitka %(f34_stable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_34/noarch/nuitka-%(max_f34_release)s.noarch.rpm>`__",
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
        "NUITKA_UNSTABLE_RHEL6": r"`Nuitka %(rhel6_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-6/noarch/nuitka-unstable-%(max_rhel6_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_RHEL7": r"`Nuitka %(rhel6_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/RedHat_RHEL-7/noarch/nuitka-unstable-%(max_rhel7_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_CENTOS6": r"`Nuitka %(centos6_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_CentOS-6/noarch/nuitka-unstable-%(max_centos6_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_CENTOS7": r"`Nuitka %(centos7_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_7/noarch/nuitka-unstable-%(max_centos7_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_CENTOS8": r"`Nuitka %(centos7_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/CentOS_8/noarch/nuitka-unstable-%(max_centos8_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F20": r"`Nuitka %(f20_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_20/noarch/nuitka-unstable-%(max_f20_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F21": r"`Nuitka %(f21_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_21/noarch/nuitka-unstable-%(max_f21_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F22": r"`Nuitka %(f22_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_22/noarch/nuitka-unstable-%(max_f22_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F23": r"`Nuitka %(f23_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_23/noarch/nuitka-unstable-%(max_f23_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F24": r"`Nuitka %(f24_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_24/noarch/nuitka-unstable-%(max_f24_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F25": r"`Nuitka %(f25_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_25/noarch/nuitka-unstable-%(max_f25_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F26": r"`Nuitka %(f26_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_26/noarch/nuitka-unstable-%(max_f26_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F27": r"`Nuitka %(f27_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_27/noarch/nuitka-unstable-%(max_f27_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F28": r"`Nuitka %(f28_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_28/noarch/nuitka-unstable-%(max_f28_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F29": r"`Nuitka %(f29_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_29/noarch/nuitka-unstable-%(max_f29_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F30": r"`Nuitka %(f30_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_30/noarch/nuitka-unstable-%(max_f30_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F31": r"`Nuitka %(f31_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_31/noarch/nuitka-unstable-%(max_f31_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F32": r"`Nuitka %(f32_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_32/noarch/nuitka-unstable-%(max_f32_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F33": r"`Nuitka %(f33_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_33/noarch/nuitka-unstable-%(max_f33_prerelease)s.noarch.rpm>`__",
        "NUITKA_UNSTABLE_F34": r"`Nuitka %(f34_unstable)s RPM <https://download.opensuse.org/repositories/home:/kayhayen/Fedora_34/noarch/nuitka-unstable-%(max_f34_prerelease)s.noarch.rpm>`__",
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

    download_page = open("pages/download.rst").read()

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

    open("pages/download.rst", "wb").write(("\n".join(output) + "\n").encode("utf8"))


def _updateCheckout(branch):
    print(f"Updating {branch} checkout...")
    if os.path.exists(f"Nuitka-{branch}"):
        shutil.rmtree(f"Nuitka-{branch}")

    urlretrieve(
        f"https://github.com/Nuitka/Nuitka/archive/{branch}.zip", "nuitka.zip.tmp"
    )

    with zipfile.ZipFile(f"nuitka.zip.tmp") as develop_archive:
        develop_archive.extractall(".")

    os.unlink("nuitka.zip.tmp")

    for filename in (
        "README.rst",
        "Developer_Manual.rst",
    ):
        filename = os.path.join(f"Nuitka-{branch}", filename)

        with open(filename, "rb") as patched_file:
            old_cotents = new_contents = patched_file.read()

        if filename.endswith(".rst"):
            # Sphinx has its own TOC method.
            new_contents = new_contents.replace(b".. contents::\n", b"")

            # Logo inside doc removed.
            new_contents = new_contents.replace(
                b"\n.. image:: doc/images/Nuitka-Logo-Symbol.png\n", b"\n"
            )
            new_contents = new_contents.replace(b"\n   :alt: Nuitka Logo", b"\n")

        if old_cotents != new_contents:
            with open(filename, "wb") as out_file:
                out_file.write(new_contents)


def updateNuitkaMaster():
    _updateCheckout("master")


def updateNuitkaDevelop():
    _updateCheckout("develop")


def updateNuitkaFactory():
    _updateCheckout("factory")


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

    with open("doc/Changelog.rst", "w") as changelog_output:

        for title, lines in splitRestByChapter(
            open("Nuitka-factory/Changelog.rst").readlines()
        ):
            if count == 5:
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
                changelog_lines = [line.replace("=", "-") if line.startswith("===") else line for line in lines]
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

            pub_date = datetime.datetime.now() + datetime.timedelta(days=1)
            data = "\n".join(
                [
                    ".. title: " + title,
                    ".. slug: " + slug,
                    ".. date: " + pub_date.strftime("%Y/%m/%d %H:%M"),
                    ".. tags: compiler,Python,Nuitka",
                ]
            )

            output_path = "posts"
            meta_path = os.path.join(output_path, slug + ".meta")
            txt_path = os.path.join(output_path, slug + ".rst")

            if not os.path.isfile(meta_path) or "draft" in open(meta_path).read():
                with open(meta_path, "wb") as output_file:
                    output_file.write(data.encode("utf8"))

            with open(txt_path, "wb") as output_file:
                output_file.write("".join(lines).encode("utf8"))


def updateDocs():
    updateNuitkaMaster()
    updateNuitkaDevelop()
    updateNuitkaFactory()
    updateReleasePosts()


def runSphinxBuild():
    assert 0 == os.system("sphinx-build doc/ doc_generated/ -a")
    assert 0 == os.system("cp doc/*.rst doc_generated/")


def runNikolaCommand(command):
    assert 0 == os.system("nikola " + command)


def checkRstLint(document):
    print("Checking %r for proper restructed text ..." % document)
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

        print(lint_result)
        lint_error = True

    if lint_error:
        sys.exit("Error, no lint clean rest.")

    print("OK.")


def checkRestPages():
    for root, _dirnames, filenames in os.walk("."):
        for filename in filenames:
            full_name = os.path.join(root, filename)

            if full_name.endswith(".rst"):

                checkRstLint(full_name)


def updatePageDates():
    for root, _dirnames, filenames in os.walk("pages"):
        for filename in filenames:
            full_name = os.path.join(root, filename)

            if full_name.endswith(".rst"):
                output = subprocess.check_output(
                    ["git", "log", "-1", "--pretty=%ci", full_name], shell=False
                ).strip()

                meta_filename = full_name[:-3] + "meta"

                if not os.path.exists(meta_filename):
                    meta_filename = full_name

                with open(meta_filename, "rb") as input_file:
                    meta_contents = input_file.readlines()

                new_date = b".. date: " + output + b"\n"

                meta_contents = [
                    new_date if m.startswith(b".. date") else m for m in meta_contents
                ]

                with open(meta_filename, "wb") as output_file:
                    output_file.writelines(meta_contents)


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

    submodule = "output"
    if os.path.isdir(submodule):
        shutil.rmtree(submodule)

    if options.all:
        options.downloads = True
        options.docs = True
        options.build = True
        options.deploy = True

    if options.downloads:
        updateDownloadPage()

    if options.docs:
        updateDocs()

    if options.check_pages:
        checkRestPages()

    if options.build:
        updatePageDates()
        runSphinxBuild()
        runNikolaCommand("status")
        runNikolaCommand("build")

    if options.deploy:
        runNikolaCommand("deploy")


if __name__ == "__main__":
    print("Running with %s" % sys.executable)
    os.environ["PATH"] = (
        os.path.dirname(sys.executable) + os.pathsep + os.environ["PATH"]
    )

    main()
