class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def add_node_by_path(root, path, value):
    """
    Adds a node at a specific location defined by a string path.
    path: String of 'L' and 'R' characters (e.g., "LR").
    """
    if not path:
        return

    current = root
    # Traverse to the parent of the new node
    for char in path[:-1]:
        if char == "L":
            if current.left is None:
                raise ValueError(
                    f"Path {path} does not exist: Missing 'L' at intermediate step."
                )
            current = current.left
        elif char == "R":
            if current.right is None:
                raise ValueError(
                    f"Path {path} does not exist: Missing 'R' at intermediate step."
                )
            current = current.right
        else:
            raise ValueError(f"Invalid path character: {char}")

    # Add the new node
    new_node = Node(value)
    last_char = path[-1]

    if last_char == "L":
        current.left = new_node
    elif last_char == "R":
        current.right = new_node
    else:
        raise ValueError(f"Invalid path character: {last_char}")


def print_tree(root):
    """
    Prints the tree in a specific visual format.
    """
    if root is None:
        return

    print(f"Root:{root.value}")
    _print_recursive(root.left, "L", 0)
    _print_recursive(root.right, "R", 0)


def _print_recursive(node, side, level):
    # Depending on requirements, indentation might be needed.
    # Based on the example "L---5", "L---None" immediately following,
    # and the recursive nature, I will add indentation for clarity
    # even if not explicitly shown in the flat text block,
    # as it's standard for "visual format".
    # However, to strictly follow the example lines provided:
    # L---5
    # L---None
    # R---7
    # I will stick to a flat printable format with recursion if the level implies hierarchy.
    # Actually, let's try to match the string format exactly for the node.

    # We need to print None children too if they were explicitly shown in example ("L---None")
    # The example showed "L---None" which implies we print leaf terminators or missing branches?
    # BUT, the example tree only had L->5 and L->R->7.
    # 5's Left was None. 5's Right was 7.
    # So for Node 5: Printed "L---None" (Left child) and "R---7" (Right child).

    indent = "    " * level

    if node is None:
        print(f"{indent}{side}---None")
        return

    print(f"{indent}{side}---{node.value}")

    # Recurse if it has children or to match the verbose style of the example
    if node.left or node.right:
        _print_recursive(node.left, "L", level + 1)
        _print_recursive(node.right, "R", level + 1)
