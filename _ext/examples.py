"""Directives for examples and tours, with plain HTML output styled by CSS.

.. tour-step:: Install Nuitka

   A numbered step, the numbers are CSS counters.

.. example-part:: input
   :columns:

   Labeled part of an example, one of input, command, output, or run. With
   "columns" its blocks are shown side by side on wide screens.

.. program-output::

   Text a program prints, shown like a code block without highlighting.
"""

from typing import List

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

EXAMPLE_PART_LABELS = {
    "input": "Input",
    "command": "Command",
    "output": "Output",
    "run": "Run",
}


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


class ExamplePart(SphinxDirective):
    has_content = True
    required_arguments = 1
    option_spec = {"columns": directives.flag}

    def run(self) -> List[nodes.Node]:
        kind = directives.choice(self.arguments[0], tuple(EXAMPLE_PART_LABELS))

        part = nodes.container(classes=["example-part", "example-part-" + kind])
        part += nodes.paragraph(
            "", EXAMPLE_PART_LABELS[kind], classes=["example-part-label"]
        )

        body = nodes.container(classes=["example-part-body"])
        if "columns" in self.options:
            body["classes"].append("example-part-columns")
        self.state.nested_parse(self.content, self.content_offset, body)
        part += body

        return [part]


class ProgramOutput(SphinxDirective):
    has_content = True

    def run(self) -> List[nodes.Node]:
        text = "\n".join(self.content)

        literal = nodes.literal_block(text, text)
        literal["language"] = "text"
        self.set_source_info(literal)

        # The wrapper carries our class, so the theme still styles the code
        # block, it selects by class names starting with "highlight".
        wrapper = nodes.container(classes=["program-output"])
        wrapper += literal
        return [wrapper]


def setup(app):
    app.add_directive("tour-step", TourStep)
    app.add_directive("example-part", ExamplePart)
    app.add_directive("program-output", ProgramOutput)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
