import functools
from pathlib import Path

from dominate.tags import html_tag, span
from dominate.util import raw
from iolanta.facets.html.base import HTMLFacet


@functools.lru_cache(maxsize=None)
def icons_path() -> Path:
    try:
        import material
    except ImportError:
        raise ValueError(
            'Cannot use mkdocs-material icons. '
            'Please install mkdocs-material theme.',
        )

    return Path(material.__file__).parent / '.icons'


class MkdocsMaterialIcon(HTMLFacet):
    """
    Render a mkdocs-material icon.

    `<… markdown="1">` can be used to render markdown emoji inside HTML but that
    is complicated. This attribute must be set for **each** of the nested
    HTML tags.

    # FIXME This is undocumented because user must find the path to the icon
        file themselves, which is… kind of ugly.
    """

    def show(self) -> html_tag:
        icon_name = self.iri.removeprefix(
            'https://github.com/squidfunk/mkdocs-material/blob/master/material/.icons/',
        )

        path = icons_path() / icon_name

        return span(
            raw(path.read_text()),
            _class='twemoji',
        )
