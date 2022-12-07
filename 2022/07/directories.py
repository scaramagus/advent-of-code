"""Solution for adventofcode.com/2022/day/07
"""
from typing import Optional, List, Set

from dataclasses import dataclass, field


@dataclass
class Node:
    """Base Node class. Can be either a file or a directory.
    Directories will have size = 0 and children Nodes.
    Files will have size > 0.
    """
    name: str
    parent: Optional["Node"] = None
    size: int = 0
    children: Set["Node"] = field(default_factory=set)

    def __hash__(self):
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name} {self.total_size}"

    def __repr__(self):
        return str(self)

    def __getitem__(self, key):
        return next((node for node in self.children if node.name == key), None)

    @property
    def is_dir(self) -> bool:
        """If the node has children, it is a directory.
        """
        return bool(self.children)

    def add_child(self, name: str, size: int = 0) -> "Node":
        """Adds a new child node into the current one.
        """
        new = Node(name, parent=self, size=size)
        self.children.add(new)
        return new

    def change_dir(self, new_dir: str) -> "Node":
        """Searches for the given node name in either parent or children and returns it.
        """
        if new_dir == "..":
            return self.parent

        return self[new_dir]

    def list(self, output: List[List[str]]):
        for line in output:
            node_type, name = line.split(" ")
            if node_type.isdigit():
                size = int(node_type)
            elif node_type == "dir":
                size = 0

            self.add_child(name, size)

    @property
    def total_size(self) -> int:
        """Calculates total size of node. For directories this is the sum
        of the total_size of its children. For files it is the size attribute.
        """
        if not self.is_dir:
            return self.size

        return sum(child.total_size for child in self.children)

    def _build_tree(self, level: int = 0) -> List[str]:
        indent = "  " * level
        char = "+" if self.is_dir else "-"
        tree_list = [f"{indent}{char} {self}"]

        for child in self.children:
            tree_list.extend(child._build_tree(level + 1))

        return tree_list

    def to_tree(self) -> str:
        tree_list = self._build_tree()
        print("\n".join(tree_list))

    @classmethod
    def from_file(cls, file_name: str) -> "Node":
        """Traverses a list of commands and assembles a node tree.
        """
        with open(file_name) as f:
            content = f.read()

        commands = content.strip().split("\n$ ")

        root = current = cls("/")

        for command in commands[1:]:
            if command.startswith("ls"):
                output = command.split("\n")
                current.list(output[1:])
            else:
                operation, node = command.split(" ")
                if operation == "cd":
                    if node == "/":
                        current = root
                    else:
                        current = current.change_dir(node)

        return root

    def filter_dirs_by_min_size(self, min_size: int) -> List["Node"]:
        dirs = []

        for node in self.children:
            if node.is_dir and node.total_size > min_size:
                dirs.append(node)
                dirs.extend(node.filter_dirs_by_min_size(min_size))

        return dirs


def calculate_total_size_of_dirs_to_delete(root: Node, max_size: int) -> int:
    """Calculates the total size of all directories with size < max_size.
    """
    total_size = 0

    for node in root.children:
        if not node.is_dir:
           continue

        if node.total_size < max_size:
            total_size += node.total_size

        total_size += calculate_total_size_of_dirs_to_delete(node, max_size)

    return total_size


def find_smallest_dir_to_delete(root: Node, total_disk_space: int, space_needed: int) -> Node:
    unused_space = total_disk_space - root.total_size
    dir_size = space_needed - unused_space
    print(dir_size)
    smallest_dirs = root.filter_dirs_by_min_size(dir_size)
    return sorted(smallest_dirs, key=lambda x: x.total_size)[0]


if __name__ == "__main__":
    root_dir = Node.from_file("input.txt")
    total_size = calculate_total_size_of_dirs_to_delete(root_dir, 100000)
    smallest_dir = find_smallest_dir_to_delete(root_dir, 70000000, 30000000)
    print(smallest_dir.total_size)
