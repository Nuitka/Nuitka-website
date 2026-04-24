from lxml import html

from update import add_inline_svg


def test_add_inline_svg_preserves_tail_before_following_sibling(tmp_path):
    svg_path = tmp_path / "icon.svg"
    svg_path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0h1v1H0z"/></svg>',
        encoding="utf-8",
    )

    doc = html.fromstring('<p><img src="icon.svg"/>tail<span>B</span></p>')
    img_tag = doc.xpath(".//img")[0]

    add_inline_svg(img_tag, str(svg_path))

    assert [child.tag for child in doc] == ["svg", "span"]
    assert doc[0].tail == "tail"
    assert doc[1].text == "B"
