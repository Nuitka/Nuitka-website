from docutils import nodes
from sphinx.util.docutils import SphinxDirective, SphinxRole

# TODO: Implement a better way to handle CLASSES. I don't really like how I have to hard code the class names in directives.


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

class CarouselTopButton(SphinxDirective):
    has_content = False
    required_arguments = 1
    final_argument_whitespace = True

    def run(self):
        text = self.arguments[0]
        node = nodes.inline(text=text, classes=['carousel-tab-top'])
        return [node]

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

class CarouselCTA(SphinxDirective):
    has_content = True
    option_spec = {
        "url": str,
    }

    def run(self):
        url = self.options.get("url")

        content_html = '\n'.join(self.content)

        html = f'''
        <a href="{url}" class="carousel-button">
            {content_html}
        </a>
        '''

        return [nodes.raw('', html, format='html')]

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
    option_spec = {
        "url": str,
    }

    def run(self):
        url = self.options.get("url")

        tab_heading_text = self.arguments[0]
        content_html = '\n'.join(self.content)

        html = f'''
        <a href="{url}" class="carousel-tab-side">
            <p class="carousel-tab-heading">{tab_heading_text}</p>
            {content_html}
        </a>
        '''

        return [nodes.raw('', html, format='html')]

def setup(app):
    # TODO: We can add JS and CSS files here instead of in shared_conf.py, this way we keep all the carousel-related code in one place.

    app.add_directive("carousel-container", CarouselContainer)
    app.add_directive("carousel", Carousel)
    app.add_directive("carousel-top-controls", CarouselTopControls)
    app.add_directive("carousel-top-button", CarouselTopButton)
    app.add_directive("carousel-content", CarouselContent)
    app.add_directive("carousel-main-content", CarouselMainContent)
    app.add_directive("carousel-main-content-heading", CarouselMainContentHeading)
    app.add_directive("carousel-main-content-text", CarouselMainContentText)
    app.add_directive("carousel-cta", CarouselCTA)
    app.add_directive("carousel-side-tabs", CarouselSideTabs)
    app.add_directive("carousel-side-tab-container", CarouselSideTabContainer)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }