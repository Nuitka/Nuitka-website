from docutils import nodes
from sphinx.util.docutils import SphinxDirective, SphinxRole

# TODO: Implement a better way to handle CLASSES. I don't really like how I have to hard code the class names in directives.

# TODO: I think this could be an extension, but I don't know how to do that yet. For now, will add each directive manually.

# TODO: Right now I have some directives, I think I can combine some of them.

class CarouselContainer(SphinxDirective):
    has_content = True

    def run(self):
        container = nodes.container()
        container['classes'] = ['carousel-rst-container']

        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]

class Carousel(SphinxDirective):
    has_content = True

    def run(self):
        container = nodes.container()
        container['classes'] = ['carousel']

        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]

class CarouselTopControls(SphinxDirective):
    has_content = True

    def run(self):
        container = nodes.container()
        container['classes'] = ['carousel-top']

        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]

class CarouselTopButton(SphinxRole):
    def run(self):
        node = nodes.inline(text=self.text, classes=['carousel-tab-top'])
        return [node], []

class CarouselContent(SphinxDirective):
    has_content = True

    def run(self):
        container = nodes.container()
        container['classes'] = ['carousel-content']

        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]

class CarouselMainContent(SphinxDirective):
    has_content = True
    final_argument_whitespace = True


    def run(self):
        container = nodes.container()
        container['classes'] = ['carousel-main']

        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]

class CarouselMainContentHeading(SphinxDirective):
    has_content = True

    def run(self):
        text = '\n'.join(self.content)
        heading_node = nodes.paragraph(text=text, classes=['carousel-heading'])
        return [heading_node]

class CarouselMainContentText(SphinxDirective):
    has_content = True
    final_argument_whitespace = True

    def run(self):
        text = '\n'.join(self.content)
        paragraph_node = nodes.paragraph(text=text, classes=['carousel-text'])
        return [paragraph_node]

class CarouselCTA(SphinxRole):
    def run(self):
        node = nodes.inline(text=self.text, classes=['carousel-button'])
        return [node], []

class CarouselSideTabs(SphinxDirective):
    has_content = True

    def run(self):
        container = nodes.container()
        container['classes'] = ['carousel-tabs-side']

        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]

class CarouselSideTabContainer(SphinxDirective):
    has_content = True
    required_arguments = 1
    final_argument_whitespace = True

    def run(self):
        tab_heading_text = self.arguments[0]

        container = nodes.container()
        container['classes'] = ['carousel-tab-side']

        tab_heading = nodes.paragraph(text=tab_heading_text, classes=['carousel-tab-heading'])

        container.append(tab_heading)

        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]