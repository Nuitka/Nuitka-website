"""Examples that are compiled for real, and the directives of the tours.

.. nuitka-example:: csvsum.py
   :options: --mode=onefile
   :run: {program} sales.csv --column amount
   :cast:

   import argparse
   ...

The content is the main program. Files it works with are taken from the
folder "site/examples/<name>/", where the name defaults to the file name
without suffix. Everything else is computed by compiling and running the
example: the command, the files Nuitka creates, the important lines of its
log, and what the program prints. With "cast", an asciinema recording of the
same steps is made for "nuitka-example-cast".

Results go to "site/examples/<name>.json" and "site/casts/<name>.cast", and
are only made again when the example changes. The environment variable
"NUITKA_EXAMPLES_RECORD" can be "auto" (default, record what is outdated),
"no" (never record, warn instead), or "force" (record everything).

Options:

:name: Name of the example, default is the main file name without suffix.
:options: Nuitka options.
:requires: Packages to install with pip, the example then compiles in a
   virtualenv with only these.
:run: Command to run after compiling. "{program}" is the created program,
   "python" is the Python used to compile.
:timeout: Stop the program after this many seconds and keep its output,
   for programs that do not exit, e.g. servers.
:cast: Also record an asciinema cast.
:show: Parts to show, default "input command output run".

.. nuitka-example-cast:: csvsum

   The player for the cast of an example.

.. tour-step:: Install Nuitka

   A numbered step, the numbers are CSS counters.

.. program-output::

   Text a program prints, shown like a code block without highlighting.
"""

import base64
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinxcontrib.asciinema.asciinema import Asciinema

logger = logging.getLogger(__name__)

# Increase when the way results are made changes, so all are made again.
RECORDER_VERSION = 2

ROOT = Path(__file__).resolve().parent.parent

PART_LABELS = {
    "input": "Input",
    "command": "Command",
    "output": "Output",
    "run": "Run",
}

# Folders Nuitka keeps while building, not part of the result.
BUILD_FOLDER_SUFFIXES = (".build", ".onefile-build")


def _makePart(kind, *children, columns=False):
    part = nodes.container(classes=["example-part", "example-part-" + kind])
    part += nodes.paragraph("", PART_LABELS[kind], classes=["example-part-label"])

    body = nodes.container(classes=["example-part-body"])
    if columns:
        body["classes"].append("example-part-columns")
    body.extend(children)
    part += body

    return part


def _makeCode(text, language):
    literal = nodes.literal_block(text, text)
    literal["language"] = language
    return literal


def _makeProgramOutput(text):
    # The wrapper carries our class, so the theme still styles the code
    # block, it selects by class names starting with "highlight".
    wrapper = nodes.container(classes=["program-output"])
    wrapper += _makeCode(text, "text")
    return wrapper


def _makeTree(root_name, entries):
    """Draw a file tree, entries are (path parts, suffix) pairs.

    Folders are given as parts ending in "/", or implied by deeper parts.
    """
    tree = {}
    for parts, suffix in entries:
        level = tree
        for part in parts[:-1]:
            level = level.setdefault(part.rstrip("/") + "/", ({}, ""))[0]
        level.setdefault(parts[-1], ({}, suffix))

    lines = [root_name + "/"]

    def draw(level, prefix):
        names = sorted(level, key=lambda name: (name.startswith("..."), name.lower()))
        for index, name in enumerate(names):
            last = index == len(names) - 1
            children, suffix = level[name]
            line = prefix + ("└── " if last else "├── ") + name
            if suffix:
                line = line.ljust(28) + "  " + suffix
            lines.append(line.rstrip())
            draw(children, prefix + ("    " if last else "│   "))

    draw(tree, "")
    return "\n".join(lines)


def _splitPath(path):
    """Path parts for the tree, a folder keeps its "/" on the last part."""
    parts = path.rstrip("/").split("/")
    if path.endswith("/"):
        parts[-1] += "/"
    return tuple(parts)


def _listFiles(folder):
    return sorted(
        path.relative_to(folder).as_posix()
        for path in folder.rglob("*")
        if path.is_file()
    )


def _filterLog(log, plugins):
    """The lines worth showing: what enabled plugins did, and the result."""
    result = []
    for line in log.splitlines():
        prefix, _, message = line.partition(": ")
        if ":WARNING" in prefix or not prefix.startswith("Nuitka"):
            continue
        if prefix.startswith("Nuitka-Plugins:"):
            if prefix.split(":", 1)[1] in plugins:
                result.append(line)
        elif message.startswith(("Successfully created", "Creating single file")):
            result.append(line)
    return "\n".join(result)


def _getPluginNames(options):
    result = set()
    for option in options:
        if option.startswith(("--enable-plugins=", "--enable-plugin=")):
            result.update(option.split("=", 1)[1].split(","))
    return result


def _getShownOutputEntries(results, example):
    """Entries for the output tree, created folders are shortened.

    Of a created folder, the program and what came from the input files are
    listed, e.g. data files, the rest is counted.
    """
    new_files = set(results["new_files"])
    created = set(re.findall(r"Successfully created '(.+?)'\.", results["log"]))
    input_names = {name.split("/")[0] for name in results["input_files"]}

    entries = []
    hidden = {}
    for path in results["output_files"]:
        parts = _splitPath(path)
        if len(parts) == 2:
            shown = path.rstrip("/") in created or parts[1].rstrip("/") in input_names
            if not shown:
                hidden[parts[0]] = hidden.get(parts[0], 0) + 1
                continue
        entries.append((parts, "<- new" if path in new_files else ""))

    for folder, count in hidden.items():
        entries.append(((folder, "... %d more" % count), ""))

    return entries


class _Example:
    """Inputs of one example and how to compute its results."""

    def __init__(self, directive):
        env = directive.env
        self.main = directive.arguments[0]
        self.name = directive.options.get("name", Path(self.main).stem)
        # The folder the example is in, as shown in file trees.
        self.root = Path(self.main).stem
        self.options = shlex.split(directive.options.get("options", ""))
        self.requires = directive.options.get("requires", "").split()
        self.run = directive.options.get("run")
        self.timeout = directive.options.get("timeout")
        self.cast = "cast" in directive.options
        self.code = "\n".join(directive.content) + "\n"

        self.folder = Path(env.srcdir) / "examples" / self.name
        self.results_path = Path(env.srcdir) / "examples" / (self.name + ".json")
        self.cast_path = Path(env.srcdir) / "casts" / (self.name + ".cast")

        self.files = _listFiles(self.folder) if self.folder.is_dir() else []

        for filename in self.files:
            env.note_dependency(str(self.folder / filename))
        env.note_dependency(str(self.results_path))

        self.python = os.environ.get("NUITKA_EXAMPLES_PYTHON", sys.executable)
        self.nuitka_path = os.environ.get(
            "NUITKA_EXAMPLES_NUITKA", str(ROOT / "Nuitka-develop")
        )

    def getCommand(self):
        return shlex.join(["python", "-m", "nuitka", *self.options, self.main])

    def getHash(self):
        digest = hashlib.sha256()
        for value in (
            RECORDER_VERSION,
            self.main,
            self.code,
            self.options,
            self.requires,
            self.run,
            self.timeout,
            self.cast,
        ):
            digest.update(repr(value).encode("utf8"))
        for filename in self.files:
            digest.update(filename.encode("utf8"))
            digest.update((self.folder / filename).read_bytes())
        return digest.hexdigest()

    def _prepareFolder(self, target):
        if self.folder.is_dir():
            shutil.copytree(self.folder, target, dirs_exist_ok=True)
        (target / self.main).write_text(self.code)

    def _getPython(self):
        if not self.requires:
            return self.python

        # One virtualenv per set of requirements, kept between builds.
        key = hashlib.sha256(repr((self.python, self.requires)).encode()).hexdigest()
        venv = ROOT / "_build" / "examples" / ("venv-" + key[:12])
        python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

        if not python.exists():
            subprocess.run([self.python, "-m", "venv", str(venv)], check=True)
            subprocess.run(
                [str(python), "-m", "pip", "install", "-q", *self.requires],
                check=True,
            )

        return str(python)

    def _getEnviron(self, python):
        environ = dict(os.environ)
        environ["PYTHONPATH"] = self.nuitka_path
        environ["PATH"] = os.path.dirname(python) + os.pathsep + environ["PATH"]
        # Long log lines are not wrapped.
        environ["COLUMNS"] = "1000"
        return environ

    def _getRunCommand(self, program):
        if self.run is None:
            return None
        return self.run.replace("{program}", program)

    def record(self):
        python = self._getPython()
        environ = self._getEnviron(python)

        with tempfile.TemporaryDirectory(prefix="nuitka-example-") as temp:
            folder = Path(temp)
            self._prepareFolder(folder)
            before = set(os.listdir(folder))

            process = subprocess.run(
                [python, "-m", "nuitka", *self.options, self.main],
                cwd=folder,
                env=environ,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            log = process.stdout
            if process.returncode != 0:
                raise RuntimeError("compilation failed:\n" + log[-3000:])

            created = re.findall(r"Successfully created '(.+?)'\.", log)
            program = "./" + created[-1] if created else None

            # Paths of folders end in "/", created folders with their entries.
            output_files = []
            new_files = []
            for name in sorted(os.listdir(folder)):
                if name.endswith(BUILD_FOLDER_SUFFIXES):
                    continue
                path = folder / name
                is_new = name not in before
                if path.is_dir():
                    if not is_new:
                        continue
                    output_files.append(name + "/")
                    new_files.append(name + "/")
                    for child in sorted(os.listdir(path), key=str.lower):
                        suffix = "/" if (path / child).is_dir() else ""
                        output_files.append(name + "/" + child + suffix)
                else:
                    output_files.append(name)
                    if is_new:
                        new_files.append(name)

            run_command = self._getRunCommand(program)
            run_output = None
            if run_command is not None:
                run_args = shlex.split(run_command)
                if run_args[0] == "python":
                    run_args[0] = python
                try:
                    run = subprocess.run(
                        run_args,
                        cwd=folder,
                        env=environ,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        timeout=float(self.timeout) if self.timeout else None,
                    )
                    run_output = run.stdout
                    if run.returncode != 0:
                        raise RuntimeError("program failed:\n" + run_output[-3000:])
                except subprocess.TimeoutExpired as e:
                    run_output = e.stdout or ""
                    if isinstance(run_output, bytes):
                        run_output = run_output.decode("utf8", "replace")

            if self.cast:
                self._recordCast(python, program)

        version = subprocess.run(
            [
                python,
                "-c",
                "import sys, platform; "
                "print('%d.%d' % sys.version_info[:2], platform.system())",
            ],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        ).stdout.split()
        nuitka_version = subprocess.run(
            [python, "-m", "nuitka", "--version"],
            env=environ,
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        ).stdout.split()[0]

        return {
            "hash": self.getHash(),
            "recorded_with": {
                "nuitka": nuitka_version,
                "python": version[0],
                "system": version[1],
            },
            "input_files": [self.main, *self.files],
            "command": self.getCommand(),
            "log": _filterLog(log, _getPluginNames(self.options)),
            "output_files": output_files,
            "new_files": new_files,
            "run_command": run_command,
            "run_output": run_output,
        }

    def _recordCast(self, python, program):
        steps = ["cat " + self.main, self.getCommand()]
        run_command = self._getRunCommand(program)
        if run_command is not None:
            steps.append(run_command)

        script = "#$ delay 50\n\n" + "".join(
            step + "\n#$ expect \\$\n\n" for step in steps
        )

        with tempfile.TemporaryDirectory(prefix="nuitka-cast-") as temp:
            folder = Path(temp) / self.name
            folder.mkdir()
            self._prepareFolder(folder)
            steps_path = Path(temp) / "steps.sh"
            steps_path.write_text(script)

            path = os.path.dirname(python) + os.pathsep + os.environ["PATH"]
            shell = (
                f'env -i PS="$ " PATH={shlex.quote(path)} '
                f"PYTHONPATH={shlex.quote(self.nuitka_path)} bash --noprofile --norc"
            )
            self.cast_path.parent.mkdir(exist_ok=True)
            automation = shutil.which(
                "asciinema-automation", path=os.path.dirname(sys.executable)
            ) or shutil.which("asciinema-automation")
            subprocess.run(
                [
                    automation,
                    "--timeout",
                    "3600",
                    "--asciinema-arguments",
                    f"--overwrite --idle-time-limit 2 -c {shlex.quote(shell)}",
                    str(steps_path),
                    str(self.cast_path),
                ],
                cwd=folder,
                check=True,
            )

    def getResults(self):
        """Stored results, made again if outdated and allowed to."""
        mode = os.environ.get("NUITKA_EXAMPLES_RECORD", "auto")
        results = None
        if self.results_path.exists():
            results = json.loads(self.results_path.read_text())

        current = results is not None and results["hash"] == self.getHash()
        if self.cast and not self.cast_path.exists():
            current = False

        if mode == "force" or (mode == "auto" and not current):
            logger.info("recording example %r, this compiles it" % self.name)
            try:
                results = self.record()
            except Exception as e:  # Shown as a warning, the page still builds.
                logger.warning("example %r could not be recorded: %s" % (self.name, e))
                return results, False
            self.results_path.write_text(
                json.dumps(results, indent=1, ensure_ascii=False) + "\n"
            )
            return results, True

        return results, current


class NuitkaExample(SphinxDirective):
    has_content = True
    required_arguments = 1
    option_spec = {
        "name": directives.unchanged,
        "options": directives.unchanged,
        "requires": directives.unchanged,
        "run": directives.unchanged,
        "timeout": directives.unchanged,
        "cast": directives.flag,
        "show": directives.unchanged,
    }

    def run(self) -> List[nodes.Node]:
        example = _Example(self)
        show = self.options.get("show", "input command output run").split()

        results, current = example.getResults()
        if not current:
            logger.warning(
                "example %r is not recorded for its current source, set "
                "NUITKA_EXAMPLES_RECORD=auto with Nuitka available" % example.name,
                location=self.get_location(),
            )

        result = nodes.container(classes=["nuitka-example"])

        if "input" in show:
            code = _makeCode(example.code.rstrip("\n"), "python")
            if example.files:
                tree = _makeTree(
                    example.root,
                    [(_splitPath(name), "") for name in [example.main, *example.files]],
                )
                result += _makePart(
                    "input", _makeCode(tree, "text"), code, columns=True
                )
            else:
                result += _makePart("input", code)

        if "command" in show:
            result += _makePart("command", _makeCode(example.getCommand(), "bash"))

        if results is None:
            return [result]

        if "output" in show:
            entries = _getShownOutputEntries(results, example)
            children = [_makeCode(_makeTree(example.root, entries), "text")]
            if results["log"]:
                children.append(_makeProgramOutput(results["log"]))
            result += _makePart("output", *children, columns=len(children) > 1)

        if "run" in show and results["run_command"] is not None:
            children = [_makeCode(results["run_command"], "bash")]
            if results["run_output"].strip():
                children.append(_makeProgramOutput(results["run_output"].rstrip("\n")))
            result += _makePart("run", *children)

        recorded = results["recorded_with"]
        result += nodes.paragraph(
            "",
            "Compiled and run with Nuitka %s on Python %s, %s."
            % (recorded["nuitka"], recorded["python"], recorded["system"]),
            classes=["nuitka-example-recorded"],
        )

        return [result]


class NuitkaExampleCast(SphinxDirective):
    required_arguments = 1
    option_spec = {"poster": directives.unchanged}

    def run(self) -> List[nodes.Node]:
        name = self.arguments[0]
        cast_path = Path(self.env.srcdir) / "casts" / (name + ".cast")
        self.env.note_dependency(str(cast_path))

        if not cast_path.exists():
            logger.warning(
                "no cast for example %r yet, it is recorded by its "
                "nuitka-example with the cast option" % name,
                location=self.get_location(),
            )
            return []

        options = dict(self.config.sphinxcontrib_asciinema_defaults)
        options.pop("path", None)
        if "poster" in self.options:
            options["poster"] = self.options["poster"]

        return [
            Asciinema(
                options=options,
                content=base64.b64encode(cast_path.read_bytes()).decode(),
                type="local",
                id=name,
            )
        ]


class TourStep(SphinxDirective):
    has_content = True
    required_arguments = 1
    final_argument_whitespace = True

    def run(self) -> List[nodes.Node]:
        step = nodes.container(classes=["tour-step"])

        title_nodes, messages = self.state.inline_text(self.arguments[0], self.lineno)
        title = nodes.paragraph("", "", *title_nodes, classes=["tour-step-title"])
        step += title
        step += messages

        self.state.nested_parse(self.content, self.content_offset, step)
        return [step]


class ProgramOutput(SphinxDirective):
    has_content = True

    def run(self) -> List[nodes.Node]:
        node = _makeProgramOutput("\n".join(self.content))
        self.set_source_info(node[0])
        return [node]


def _readCastUsersLast(app, env, docnames):
    """Pages showing casts are read last, after the examples recorded them."""

    def usesCast(docname):
        source = Path(env.doc2path(docname))
        return source.exists() and "nuitka-example-cast::" in source.read_text()

    docnames.sort(key=usesCast)


def setup(app):
    app.add_directive("nuitka-example", NuitkaExample)
    app.add_directive("nuitka-example-cast", NuitkaExampleCast)
    app.add_directive("tour-step", TourStep)
    app.add_directive("program-output", ProgramOutput)
    app.connect("env-before-read-docs", _readCastUsersLast)

    return {
        "version": "0.2",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
