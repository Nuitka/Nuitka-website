#!/usr/bin/env python3.12

"""Bundle documentation for offline distribution."""

from pathlib import Path
import shutil
import re
import os
from optparse import OptionParser
from lxml import html

from nuitka_import import importNuitka
from builder_config import *

nuitka = importNuitka()

from nuitka.Tracing import my_print
from nuitka.utils.FileOperations import (
    deleteFile,
    getFileContents,
    getFileList,
)
from nuitka.utils.ReExecute import callExecProcess

SITE = Path("site")
DEST_SOURCE = Path(BUNDLE_DIR)
DEST_RST = Path(BUNDLE_RST_DIR)
DEST_HTML = Path(BUNDLE_HTML_DIR)

BUNDLE_SOURCE_PATTERNS = [
    "images/**/*",
    "variables.inc",
    "dynamic.inc",
    "doc/**/*",
    "commercial/**/*",
    "user-documentation/**/*",
]

def get_variables_to_remove(site):
    variables_inc_path = site / "variables.inc"
    variables_content = variables_inc_path.read_text()
    variables_to_remove = set()
    for line in variables_content.splitlines():
        match = re.match(r'..\s+\|([^|]+)\|', line)
        if match:
            variables_to_remove.add(match.group(1))
    return variables_to_remove

def get_replacements(site):
    dynamic_inc_path = site / "dynamic.inc"
    dynamic_content = dynamic_inc_path.read_text()
    replacements = {}
    lines = dynamic_content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r'..\s+\|([^|]+)\|\s+replace::', line)
        if match:
            var = match.group(1)
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            if i < len(lines):
                value = lines[i].strip()
                replacements[var] = value
                i += 1
        else:
            i += 1
    return replacements

def copy_files_to_bundle(site, bundle_dest, patterns):
    seen = set()
    for pattern in patterns:
        for path in site.glob(pattern):
            if not path.is_file():
                continue
            rel = path.relative_to(site)
            if rel in seen:
                continue
            seen.add(rel)
            target = bundle_dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

def inline_inc_file(inc_path_str, rst_dir, site):
    if inc_path_str.startswith("/"):
        inc_path = site / inc_path_str[1:]
    else:
        inc_path = (rst_dir / inc_path_str).resolve()
    if inc_path.exists() and inc_path.suffix == ".inc":
        inc_content = inc_path.read_text()
        return inc_content.splitlines()
    return None

def clean_blank_lines(lines):
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        is_blank = line.strip() == ""
        if is_blank and prev_blank:
            continue
        cleaned_lines.append(line)
        prev_blank = is_blank
    return cleaned_lines

def process_rst_file(rst_file, bundle_dest, site, variables_to_remove, replacements, rst_dest):
    rel_path = rst_file.relative_to(bundle_dest)
    content = rst_file.read_text()
    lines = content.splitlines()
    new_lines = []
    skip_html = False
    rst_dir = (site / rel_path).parent

    for line in lines:
        if skip_html:
            if line.strip() == "" or not line or (line and line[0].isspace()):
                continue
            else:
                skip_html = False
        if line.strip() == ".. raw:: html":
            skip_html = True
            continue
        # Remove lines containing variables from variables.inc
        if any(f"|{var}|" in line for var in variables_to_remove):
            continue
        # Remove include of variables.inc
        if ".. include::" in line and "variables.inc" in line:
            continue
        # Inline other .inc files
        if ".. include::" in line and ".inc" in line:
            parts = line.split(".. include::")
            if len(parts) == 2:
                inc_path_str = parts[1].strip()
                inlined = inline_inc_file(inc_path_str, rst_dir, site)
                if inlined:
                    new_lines.extend(inlined)
                    continue
        for var, val in replacements.items():
            line = line.replace(f"|{var}|", val)
        new_lines.append(line)

    cleaned_lines = clean_blank_lines(new_lines)
    new_content = "\n".join(cleaned_lines)

    target_rst = rst_dest / rel_path
    target_rst.parent.mkdir(parents=True, exist_ok=True)
    target_rst.write_text(new_content)


def generateBundleSource():
    seen = set()

    preserved_files = {}
    for filename in ["conf.py", "index.rst"]:
        file_path = DEST_SOURCE / filename
        if file_path.exists():
            preserved_files[filename] = file_path.read_text()

    if DEST_SOURCE.exists():
        shutil.rmtree(DEST_SOURCE)

    DEST_SOURCE.mkdir(parents=True)

    for filename, content in preserved_files.items():
        (DEST_SOURCE / filename).write_text(content)

    for pattern in BUNDLE_SOURCE_PATTERNS:
        for path in SITE.glob(pattern):
            if not path.is_file():
                continue

            rel = path.relative_to(SITE)

            if rel in seen:
                continue

            seen.add(rel)

            target = DEST_SOURCE / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

    my_print(f"Created bundle in '{DEST_SOURCE.as_posix()}'")

def generateRSTBundle():
    bundle_source = Path(BUNDLE_DIR)
    rst_dest = DEST_RST

    # Preserve existing conf.py and index.rst from the bundle-rst directory
    preserved_files = {}
    for filename in ["conf.py", "index.rst"]:
        file_path = rst_dest / filename
        if file_path.exists():
            preserved_files[filename] = file_path.read_text()

    if rst_dest.exists():
        shutil.rmtree(rst_dest)
    rst_dest.mkdir(parents=True)

    # Restore preserved files to bundle-rst
    for filename, content in preserved_files.items():
        (rst_dest / filename).write_text(content)

    for pattern in BUNDLE_SOURCE_PATTERNS:
        for path in bundle_source.glob(pattern):
            if not path.is_file() or path.suffix in {'.rst', '.inc'}:
                continue
            if "fontawesome" in path.parts:
                continue
            rel = path.relative_to(bundle_source)
            target = rst_dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

    # Get data for processing
    variables_to_remove = get_variables_to_remove(SITE)
    replacements = get_replacements(SITE)

    # Find and process RST files from bundle source
    rst_files = list(bundle_source.glob("**/*.rst"))
    # Exclude conf.py's directory level index.rst if it was already preserved
    rst_files = [f for f in rst_files if f.name not in preserved_files or f.parent != bundle_source]

    for rst_file in rst_files:
        process_rst_file(rst_file, bundle_source, SITE, variables_to_remove, replacements, rst_dest)

    my_print(f"Created RST bundle in '{rst_dest.as_posix()}'")

def runHtmlPostprocessing():
    my_print(f"Post-processing bundle in {DEST_HTML.as_posix()}...")

    # Remove files that require external resources
    files_to_remove = (
        "searchindex.js",
        "searchtools.js",
        "search.html",
    )

    for filename in files_to_remove:
        deleteFile(os.path.join(DEST_HTML, filename), must_exist=False)

    # Remove external font files that won't work offline
    fonts_path = os.path.join(DEST_HTML, "_static/fonts")
    if os.path.exists(fonts_path):
        for filename in os.listdir(fonts_path):
            if filename.lower().startswith("fontawesome"):
                deleteFile(os.path.join(fonts_path, filename), must_exist=False)

    # Process HTML files to remove external content and fix links for offline use
    for html_file in getFileList(DEST_HTML, only_suffixes=".html"):
        doc = html.fromstring(getFileContents(html_file, mode="rb"))

        file_dir = os.path.dirname(html_file)
        depth = len(os.path.relpath(file_dir, DEST_HTML).split(os.sep))
        if os.path.relpath(file_dir, DEST_HTML) == ".":
            depth = 0
        path_to_root = "../" * depth if depth > 0 else "./"

        # Fix absolute paths to relative paths for offline viewing or rewrite to main site if not bundled
        for link_tag in doc.xpath("//a[@href]"):
            href = link_tag.get("href")
            if href.startswith("/") and not href.startswith("//"):
                target_path = DEST_HTML / href.lstrip("/")
                if target_path.exists():
                    link_tag.set("href", path_to_root + href.lstrip("/"))
                else:
                    link_tag.set("href", "https://nuitka.net" + href)

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


def buildBundleHtml():
    """Build HTML from bundle source using Sphinx."""
    import subprocess

    conf_dir = os.path.dirname(BUNDLE_CONF) if BUNDLE_CONF else BUNDLE_DIR
    cmd = [
        "pipenv",
        "run",
        "sphinx-build",
        "-W",
        "--keep-going",
        "-c",
        conf_dir,
        BUNDLE_DIR,
        BUNDLE_HTML_DIR,
    ]
    subprocess.run(cmd, check=True)
    my_print(f"Built HTML bundle in '{BUNDLE_HTML_DIR}'")


def main():
    parser = OptionParser()

    parser.add_option(
        "--source",
        action="store_true",
        dest="source",
        default=False,
        help="Generate bundle source from site directory",
    )

    parser.add_option(
        "--rst",
        action="store_true",
        dest="rst",
        default=False,
        help="Generate RST bundle (processes .rst/.inc files)",
    )

    parser.add_option(
        "--html",
        action="store_true",
        dest="html",
        default=False,
        help="Build HTML from RST bundle using Sphinx",
    )

    parser.add_option(
        "--postprocess",
        action="store_true",
        dest="postprocess",
        default=False,
        help="Post-process HTML bundle for offline use",
    )

    parser.add_option(
        "--all",
        action="store_true",
        dest="all",
        default=False,
        help="Run all bundle steps (source, rst, html, postprocess)",
    )

    options, positional_args = parser.parse_args()

    assert not positional_args, positional_args

    if options.all:
        generateBundleSource()
        generateRSTBundle()
        buildBundleHtml()
        runHtmlPostprocessing()
    else:
        if options.source:
            generateBundleSource()

        if options.rst:
            generateRSTBundle()

        if options.html:
            buildBundleHtml()

        if options.postprocess:
            runHtmlPostprocessing()


if __name__ == "__main__":
    importNuitka()
    main()