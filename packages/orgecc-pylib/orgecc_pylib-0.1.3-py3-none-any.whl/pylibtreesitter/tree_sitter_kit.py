
def nodes_by_type_suffix(nodes: list, node_type_suffix: str) -> list:
    return [node for node in nodes if node.type.endswith(node_type_suffix)]
