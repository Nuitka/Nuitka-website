from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from typing import List, cast

# TODO: Add carousel js here.
# TODO: Add :doc: to the button links.

class CarouselContainer(SphinxDirective):
    has_content = True

    def run(self) -> List[nodes.Node]:
        container = nodes.container()
        container['classes'] = ['carousel-rst-container']

        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]

class Carousel(SphinxDirective):
    has_content = True

    def run(self) -> List[nodes.Node]:
        carousel = nodes.container()
        carousel['classes'] = ['carousel']

        top_controls = nodes.container()
        top_controls['classes'] = ['carousel-top']

        content = nodes.container()
        content['classes'] = ['carousel-content']

        side_tabs = nodes.container()
        side_tabs['classes'] = ['carousel-tabs-side']

        temp_container = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, temp_container)

        tab_count = 0
        for child in temp_container.children:
            child_container = cast(nodes.container, child)
            if 'carousel-main' in child_container.attributes.get('classes', []):
                content.append(child)
                tab_name = child_container.attributes.get('tab-name')
                if tab_name:
                    radio_html = f'''
                    <input type="radio" name="carousel-tab" id="carousel-tab-{tab_count}"
                           class="carousel-radio" {'checked' if tab_count == 0 else ''}>
                    '''
                    carousel += nodes.raw('', radio_html, format='html')

                    label_html = f'''
                    <label for="carousel-tab-{tab_count}" class="carousel-tab-top">
                        {tab_name}
                        <div class="carousel-duration">
                            <div class="carousel-progress"></div>
                        </div>
                    </label>
                    '''
                    top_controls += nodes.raw('', label_html, format='html')

                    tab_count += 1

            elif 'carousel-tab-side' in child_container.attributes.get('classes', []):
                side_tabs.append(child)

        carousel.append(top_controls)
        carousel.append(content)
        carousel.append(side_tabs)

        return [carousel]

class CarouselContent(SphinxDirective):
    has_content = True
    required_arguments = 1
    final_argument_whitespace = True

    def run(self) -> List[nodes.Node]:
        tab_name = self.arguments[0]

        container = nodes.container()
        container['classes'] = ['carousel-main']
        container.attributes['tab-name'] = tab_name

        if self.content:
            content_lines = list(self.content)

            heading_text = content_lines[0]
            heading_node = nodes.raw('', f'<h2 class="carousel-heading">{heading_text}</h2>', format='html')
            container.append(heading_node)

            if len(content_lines) > 2:
                text = '\n'.join(content_lines[1:-1])
                text_node = nodes.paragraph(text=text, classes=['carousel-text'])
                container.append(text_node)

            if len(content_lines) > 1:
                cta_text = content_lines[-1]
                cta_node = nodes.container(classes=['carousel-button'])
                cta_node += nodes.raw('', cta_text, format='html')
                container.append(cta_node)

        return [container]

class CarouselSideTab(SphinxDirective):
    has_content = True
    required_arguments = 1
    final_argument_whitespace = True

    def run(self) -> List[nodes.Node]:
        tab_heading = self.arguments[0]
        content_text = '\n'.join(self.content)

        container = nodes.container()
        container['classes'] = ['carousel-tab-side']

        heading = nodes.paragraph(text=tab_heading, classes=['carousel-tab-heading'])
        content = nodes.paragraph(text=content_text)

        container.append(heading)
        container.append(content)

        return [container]

def setup(app):
    app.add_directive("carousel-container", CarouselContainer)
    app.add_directive("carousel", Carousel)
    app.add_directive("carousel-content", CarouselContent)
    app.add_directive("carousel-side-tab", CarouselSideTab)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
