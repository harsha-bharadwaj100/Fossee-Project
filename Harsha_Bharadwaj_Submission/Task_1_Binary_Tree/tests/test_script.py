import sys
import os

# Add the parent directory to sys.path so we can import the package directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from binary_tree_pkg import *


def main():
    print("--- 1. Manual Tree Construction ---")
    # 1. Create a root node (10).
    root = Node(10)

    # 2. Add nodes using paths "L", "R", "LL", "LR", "RL", "RR".
    add_node_by_path(root, "L", 5)
    add_node_by_path(root, "R", 15)
    add_node_by_path(root, "LL", 2)
    add_node_by_path(root, "LR", 7)
    add_node_by_path(root, "RL", 12)
    add_node_by_path(root, "RR", 18)

    # 3. Print the tree.
    print_tree(root)

    print("\n--- 2. YAML Tree Construction ---")
    # 4. Read from a "test.yaml" file (self-contained).
    yaml_content = """
value: 10
left:
  value: 5
  left:
    value: 2
  right:
    value: 7
right:
  value: 15
  left:
    value: 12
  right:
    value: 18
"""
    yaml_filename = "test.yaml"
    with open(yaml_filename, "w") as f:
        f.write(yaml_content.strip())

    try:
        # 5. Build the tree from that YAML and print it.
        yaml_root = build_tree_from_yaml(yaml_filename)
        print_tree(yaml_root)
    finally:
        # Clean up
        if os.path.exists(yaml_filename):
            os.remove(yaml_filename)


if __name__ == "__main__":
    main()
