#!/usr/bin/env python

"""
Pandoc filter for adding image at absolute position in LaTeX.
"""

from __future__ import annotations

import re
from typing import Any

from panflute import (
    Block,
    Code,
    CodeBlock,
    Div,
    Doc,
    Element,
    Header,
    MetaInlines,
    MetaList,
    RawBlock,
    RawInline,
    Span,
    debug,
    run_filter,
)


def absolute_image(elem: Element, doc: Doc) -> list[Element] | None:
    """
    Apply absolute image transformation to element.

    Parameters
    ----------
    elem
        The element
    doc
        The original document.

    Returns
    -------
    list[Element] | None
        The additional elements if any.
    """
    # Is it in the right format and is it a Span, Div?
    if doc.format in ("latex", "beamer") and isinstance(
        elem, Span | Div | Code | CodeBlock | Header
    ):
        # Is there a latex-tip-icon attribute?
        if (
            "latex-absolute-image" in elem.attributes
            or "latex-absolute-image-reset" in elem.attributes
        ):
            return add_latex(
                elem,
                latex_code(
                    elem.attributes,
                    {
                        "image": "latex-absolute-image",
                        "image-odd": "latex-absolute-image-odd",
                        "image-even": "latex-absolute-image-even",
                        "reset": "latex-absolute-reset",
                        "reset-odd": "latex-absolute-reset-odd",
                        "reset-even": "latex-absolute-reset-even",
                        "width": "latex-absolute-width",
                        "width-odd": "latex-absolute-width-odd",
                        "width-even": "latex-absolute-width-even",
                        "height": "latex-absolute-height",
                        "height-odd": "latex-absolute-height-odd",
                        "height-even": "latex-absolute-height-even",
                        "anchor": "latex-absolute-anchor",
                        "anchor-odd": "latex-absolute-anchor-odd",
                        "anchor-even": "latex-absolute-anchor-even",
                        "x-coord": "latex-absolute-x-coord",
                        "x-coord-odd": "latex-absolute-x-coord-odd",
                        "x-coord-even": "latex-absolute-x-coord-even",
                        "y-coord": "latex-absolute-y-coord",
                        "y-coord-odd": "latex-absolute-y-coord-odd",
                        "y-coord-even": "latex-absolute-y-coord-even",
                        "opacity": "latex-absolute-opacity",
                        "opacity-odd": "latex-absolute-opacity-odd",
                        "opacity-even": "latex-absolute-opacity-even",
                    },
                ),
            )

        # Get the classes
        classes = set(elem.classes)
        # Loop on all font size definition
        # noinspection PyUnresolvedReferences
        for definition in doc.defined:
            # Are the classes correct?
            if classes >= definition["classes"]:
                return add_latex(elem, definition["latex"])

    return None


def add_latex(elem: Element, latex: str) -> list[Element] | None:
    """
    Add latex code.

    Parameters
    ----------
    elem
        Current element
    latex
        Latex code

    Returns
    -------
    list[Element] | None
        The additional elements if any.
    """
    if bool(latex):
        if isinstance(elem, Block):
            return [RawBlock(latex, "tex"), elem]
        return [RawInline(latex, "tex"), elem]
    return None


# pylint: disable=too-many-arguments,too-many-locals,too-many-statements
def latex_code(definition: dict[str, Any], keys: dict[str, str]) -> str:
    """
    Get the latex code.

    Parameters
    ----------
    definition
        The defition
    keys
        Key mapping

    Returns
    -------
    str
        The latex code.
    """
    path = definition.get(keys["image"])
    path_odd = definition.get(keys["image-odd"], path)
    path_even = definition.get(keys["image-even"], path)

    reset = definition.get(keys["reset"])
    reset_odd = definition.get(keys["reset-odd"], reset)
    reset_even = definition.get(keys["reset-even"], reset)

    width = get_latex_size(definition.get(keys["width"]))
    width_odd = get_latex_size(definition.get(keys["width-odd"]), width)
    width_even = get_latex_size(definition.get(keys["width-even"]), width)

    height = get_latex_size(definition.get(keys["height"]))
    height_odd = get_latex_size(definition.get(keys["height-odd"]), height)
    height_even = get_latex_size(definition.get(keys["height-even"]), height)

    anchor = get_anchor(definition.get(keys["anchor"]))
    anchor_odd = get_anchor(definition.get(keys["anchor-odd"]), anchor)
    anchor_even = get_anchor(definition.get(keys["anchor-even"]), anchor)

    opacity = get_opacity(definition.get(keys["opacity"]))
    opacity_odd = get_opacity(definition.get(keys["opacity-odd"]), opacity)
    opacity_even = get_opacity(definition.get(keys["opacity-even"]), opacity)

    x_coord = get_latex_size(
        definition.get(keys["x-coord"], "0cm"),
        "0cm",
    )
    x_coord_odd = get_latex_size(
        definition.get(keys["x-coord-odd"], x_coord),
        x_coord,
    )
    x_coord_even = get_latex_size(
        definition.get(keys["x-coord-even"], x_coord), x_coord
    )

    y_coord = get_latex_size(
        definition.get(keys["y-coord"], "0cm"),
        "0cm",
    )
    y_coord_odd = get_latex_size(definition.get(keys["y-coord-odd"], y_coord), y_coord)
    y_coord_even = get_latex_size(
        definition.get(keys["y-coord-even"], y_coord),
        y_coord,
    )

    if reset_odd:
        picture_odd = """
"""
    else:
        options = []
        if width_odd:
            options.append(f"width={width_odd}")
        if height_odd:
            options.append(f"height={height_odd}")
        options = ",".join(options)

        node_options = []
        if anchor_odd:
            node_options.append(f"anchor={anchor_odd}")
        if opacity_odd:
            node_options.append(f"opacity={opacity_odd}")
        node_options = ",".join(node_options)

        picture_odd = f"""
\\begin{{tikzpicture}}[
    overlay,                         % Do our drawing on an overlay instead of inline
    remember picture,                % Allow us to share coordinates with other drawings
    shift=(current page.north west), % Set the top (north) left (west) as the origin
    yscale=-1,                       % Switch the y-axis to increase down the page
    inner sep=0,                     % Remove inner separator
]
\\node[{node_options}] at ({x_coord_odd}, {y_coord_odd})
    {{\\includegraphics[{options}]{{{path_odd}}}}};
\\end{{tikzpicture}}
"""

    if reset_even:
        picture_even = """
"""
    else:
        options = []
        if width_even:
            options.append(f"width={width_even}")
        if height_odd:
            options.append(f"height={height_even}")
        options = ",".join(options)

        node_options = []
        if anchor_even:
            node_options.append(f"anchor={anchor_even}")
        if opacity_even:
            node_options.append(f"opacity={opacity_even}")
        node_options = ",".join(node_options)

        picture_even = f"""
\\begin{{tikzpicture}}[
    overlay,                         % Do our drawing on an overlay instead of inline
    remember picture,                % Allow us to share coordinates with other drawings
    shift=(current page.north west), % Set the top (north) left (west) as the origin
    yscale=-1,                       % Switch the y-axis to increase down the page
    inner sep=0,                     % Remove inner separator
]
\\node[{node_options}] at ({x_coord_even}, {y_coord_even})
  {{\\includegraphics[{options}]{{{path_even}}}}};
\\end{{tikzpicture}}
"""

    return f"""
\\renewcommand\\PandocLaTeXAbsoluteImage{{%
\\ifodd\\value{{page}}%
{picture_odd.strip()}
\\else
{picture_even.strip()}
\\fi
}}
"""


def get_latex_size(size: str | None, default: str | None = None) -> str | None:
    """
    Get the correct size.

    Parameters
    ----------
    size
        The initial size
    default
        The default size

    Returns
    -------
    str | None
        The correct size.
    """
    if size is None:
        return default
    regex = re.compile("^(\\d+(\\.\\d*)?)(?P<unit>pt|mm|cm|in|em)?$")
    if regex.match(size):
        if regex.match(size).group("unit"):
            return size
        return size + "pt"
    debug(
        f"[WARNING] pandoc-latex-absolute-image: "
        f"size must be a correct LaTeX length; using {default}"
    )
    return default


def get_anchor(anchor: str | None, default: str | None = None) -> str | None:
    """
    Get the anchor.

    Parameters
    ----------
    anchor
        The initial anchor
    default
        The default anchor

    Returns
    -------
    str | None
        The correct anchor.
    """
    if anchor in (
        "north",
        "south",
        "west",
        "east",
        "north west",
        "north east",
        "south west",
        "south east",
    ):
        return anchor
    return default


def get_opacity(opacity: str | None, default: str | None = None) -> str | None:
    """
    Get the opacity.

    Parameters
    ----------
    opacity
        The initial opacity
    default
        The default opacity

    Returns
    -------
    str | None
        The correct opacity.
    """
    if opacity:
        if re.match("^(1.0)|(0.\\d+)$", opacity):
            return opacity
        debug(
            f"[WARNING] pandoc-latex-absolute-image: "
            f"opacity must be a correct opacity; using {default}"
        )
    return default


def add_definition(doc: Doc, definition: dict[str, Any]) -> None:
    """
    Add definition to document.

    Parameters
    ----------
    doc
        The original document
    definition
        The definition
    """
    # Get the classes
    classes = definition["classes"]

    # Add a definition if correct
    if bool(classes):
        latex = latex_code(
            definition,
            {
                "image": "image",
                "image-odd": "image-odd",
                "image-even": "image-even",
                "reset": "reset",
                "reset-odd": "reset-odd",
                "reset-even": "reset-even",
                "width": "width",
                "width-odd": "width-odd",
                "width-even": "width-even",
                "height": "height",
                "height-odd": "height-odd",
                "height-even": "height-even",
                "anchor": "anchor",
                "anchor-odd": "anchor-odd",
                "anchor-even": "anchor-even",
                "x-coord": "x-coord",
                "x-coord-odd": "x-coord-odd",
                "x-coord-even": "x-coord-even",
                "y-coord": "y-coord",
                "y-coord-odd": "y-coord-odd",
                "y-coord-even": "y-coord-even",
                "opacity": "opacity",
                "opacity-odd": "opacity-odd",
                "opacity-even": "opacity-even",
            },
        )
        if latex:
            # noinspection PyUnresolvedReferences
            doc.defined.append({"classes": set(classes), "latex": latex})


def prepare(doc: Doc) -> None:
    """
    Prepare the document.

    Parameters
    ----------
    doc
        The original document.
    """
    # Prepare the definitions
    doc.defined = []

    # Get the meta data
    # noinspection PyUnresolvedReferences
    meta = doc.get_metadata("pandoc-latex-absolute-image")

    if isinstance(meta, list):
        # Loop on all definitions
        for definition in meta:
            # Verify the definition
            if (
                isinstance(definition, dict)
                and "classes" in definition
                and isinstance(definition["classes"], list)
            ):
                add_definition(doc, definition)


def finalize(doc: Doc) -> None:
    """
    Finalize the document.

    Parameters
    ----------
    doc
        The original document
    """
    # Add header-includes if necessary
    if "header-includes" not in doc.metadata:
        doc.metadata["header-includes"] = MetaList()
    # Convert header-includes to MetaList if necessary
    elif not isinstance(doc.metadata["header-includes"], MetaList):
        doc.metadata["header-includes"] = MetaList(doc.metadata["header-includes"])

    doc.metadata["header-includes"].append(
        MetaInlines(RawInline("\\usepackage{tikz}", "tex"))
    )
    doc.metadata["header-includes"].append(
        MetaInlines(RawInline("\\newcommand\\PandocLaTeXAbsoluteImage{}", "tex"))
    )
    doc.metadata["header-includes"].append(
        MetaInlines(
            RawInline(
                "\\AddToHook{shipout/background}{\\PandocLaTeXAbsoluteImage}", "tex"
            )
        )
    )


def main(doc: Doc | None = None) -> Doc:
    """
    Transform the pandoc document.

    Arguments
    ---------
    doc
        The pandoc document

    Returns
    -------
    Doc
        The transformed document
    """
    return run_filter(absolute_image, prepare=prepare, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
