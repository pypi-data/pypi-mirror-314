"""Functions for handling treesitter outputs."""

import sys
import warnings

import tree_sitter

if sys.version_info >= (3, 9):
    import tree_sitter_language_pack as tsl

    MAKE_PARSER = tsl.get_parser("make")
else:
    import tree_sitter_languages as tsl

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        MAKE_PARSER = tsl.get_parser("make")


def to_string(node: tree_sitter.Node, indent: int = 0) -> str:
    """Convert a treesitter parse tree into a printable string."""
    ret = "  " * indent + f"{node.type} [{node.start_point} - {node.end_point}]"
    for child in node.children:
        ret += "\n" + to_string(child, indent + 1)
    return ret


def structural_equality(
    lhs: tree_sitter.Node,
    rhs: tree_sitter.Node,
) -> bool:
    """Check the structural equality of two treesitter parse trees."""
    if lhs.type != rhs.type:
        return False
    if len(lhs.children) != len(rhs.children):
        return False
    if len(lhs.children) == 0:
        return lhs.text == rhs.text
    for lhs_child, rhs_child in zip(lhs.children, rhs.children):
        if not structural_equality(lhs_child, rhs_child):
            return False
    return True
