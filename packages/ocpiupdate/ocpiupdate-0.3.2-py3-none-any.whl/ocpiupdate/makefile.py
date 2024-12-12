"""Functions for handling makefiles."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tree_sitter


def update_variables_with_variable_assignment(
    node: tree_sitter.Node,
    variables: dict[str, str],
) -> None:
    """Update a variable collection with a variable assignment tree sitter node."""
    # Discount anything we can't parse
    lhs_node = node.children[0]
    op_node = node.children[1]
    rhs_node = None if len(node.children) == 2 else node.children[2]
    if lhs_node.type != "word":
        message = (
            f"Node ('{lhs_node.text.decode('utf-8')}') of type "
            f"'{lhs_node.type}' is not supported in variable assignments at "
            f"{lhs_node.start_point}"
        )
        raise RuntimeError(message)
    if op_node.type not in ["=", ":=", "::=", ":::=", "?=", "+="]:
        message = (
            f"Operator ('{op_node.text.decode('utf-8')}') of type "
            f"'{op_node.type}' is not supported in variable assignments at "
            f"{op_node.start_point}"
        )
        raise RuntimeError(message)
    if rhs_node is not None and rhs_node.type != "text":
        message = (
            f"Node ('{rhs_node.text.decode('utf-8')}') of type "
            f"'{rhs_node.type}' is not supported in variable assignments at "
            f"{rhs_node.start_point}"
        )
        raise RuntimeError(message)
    # We can parse
    lhs = lhs_node.text.decode("utf-8").lower()
    op = op_node.type
    rhs = "" if rhs_node is None else rhs_node.text.decode("utf-8")
    # Catch an error that the treesitter parser has with operator parsing:
    # https://github.com/alemuller/tree-sitter-make/issues/28
    if lhs.endswith(("+", "?")):
        op = f"{lhs[-1]}{op}"
        lhs = lhs[:-1]
    # Handle rhs containing line continuations and tab characters
    rhs = rhs.replace("\\", " ")
    rhs = rhs.replace("\n", " ")
    rhs = rhs.replace("\t", " ")
    rhs = " ".join(rhs.strip().split())
    # Add to variables
    if op in ["=", ":=", "::=", ":::="] or (op == "?=" and variables.get(lhs)) is None:
        variables[lhs] = rhs
    elif op == "+=":
        current = variables.get(lhs)
        if current is None:
            variables[lhs] = rhs
        else:
            variables[lhs] = f"{variables[lhs]} {rhs}"
