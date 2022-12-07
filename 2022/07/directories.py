"""Solution for adventofcode.com/2022/day/07
"""
from typing import Optional, List, Set

from dataclasses import dataclass, field


@dataclass
class Node:
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

    @property
    def is_dir(self) -> bool:
        return bool(self.children)

    def add_node(self, name: str, size: int = 0) -> "Node":
        new = Node(name, parent=self, size=size)
        self.children.add(new)
        return new

    def change_dir(self, new_dir: str) -> "Node":
        if new_dir == "..":
            return self.parent

        new_current = next((node for node in self.children if node.name == new_dir), None)
        return new_current

    def list(self, output: List[List[str]]):
        for line in output:
            node_type, name = line.split(" ")
            if node_type.isdigit():
                size = int(node_type)
            elif node_type == "dir":
                size = 0

            self.add_node(name, size)

    @property
    def total_size(self) -> int:
        if self.is_dir:
            return sum(child.total_size for child in self.children)

        return self.size

    def to_tree(self, level: int = 0) -> str:
        indent = "  " * level
        char = "+" if self.is_dir else "-"
        tree_list = [f"{indent}{char} {self}"]

        for child in self.children:
            tree_list.extend(child.to_tree(level + 1))

        return tree_list

    @classmethod
    def from_command_list(cls, commands: List[str]) -> "Node":
        """Traverses a list of commands and assembles a node tree.
        """
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


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read()

    commands = content.strip().split("\n$ ")
    root_dir = Node.from_command_list(commands)
    print("\n".join(root_dir.to_tree()))
