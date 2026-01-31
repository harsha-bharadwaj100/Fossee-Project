import yaml
from .node import Node


def build_tree_from_yaml(file_path):
    """
    Reads a YAML file and constructs the tree.
    """
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    return _dict_to_node(data)


def _dict_to_node(data):
    """
    Helper function to recursively convert dictionary to Node objects.
    """
    if not data:
        return None

    node = Node(data.get("value"))

    if "left" in data:
        node.left = _dict_to_node(data["left"])

    if "right" in data:
        node.right = _dict_to_node(data["right"])

    return node


def tree_to_yaml(root, file_path):
    """
    Exports the tree to YAML.
    """
    data = _node_to_dict(root)
    with open(file_path, "w") as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)


def _node_to_dict(node):
    """
    Helper function to recursively convert Node objects to dictionary.
    """
    if not node:
        return None

    data = {"value": node.value}

    if node.left:
        data["left"] = _node_to_dict(node.left)

    if node.right:
        data["right"] = _node_to_dict(node.right)

    return data
