from docutils import nodes
from docutils.parsers.rst import Directive, directives

class CarouselContent(Directive):
    has_content = True
    optional_arguments = 0
    option_spec = {
        'class': directives.class_option,
    }

    def run(self):
        text = '\n'.join(self.content)
        classes = self.options.get('class', [])

        paragraph_node = nodes.paragraph(text=text, classes=classes)
        return [paragraph_node]
