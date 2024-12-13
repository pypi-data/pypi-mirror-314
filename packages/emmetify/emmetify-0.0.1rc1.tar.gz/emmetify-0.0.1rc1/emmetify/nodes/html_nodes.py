from dataclasses import dataclass, field

from bs4 import Tag

from emmetify.nodes.base_nodes import BaseNode, BaseNodePool


@dataclass
class HtmlNode(BaseNode):
    id: str
    tag: str
    attrs: dict
    parent_id: str | None = None
    children_ids: list[str] = field(default_factory=list)
    sequence_index: int = 0
    text_content: str | None = None
    is_text_node: bool = False
    next_sibling_id: str | None = None
    prev_sibling_id: str | None = None
    non_text_children_count: int = 0
    # non_text_siblings_count: int = -1 # single child node has no siblings so will set to 0

    def __str__(self) -> str:
        """String representation of html node for printing."""
        parts = []
        if self.is_text_node:
            parts.append(f'"{self.text_content}"')
        else:
            parts.append(self.tag)
            if self.attrs:
                attrs_str = " ".join(f'{k}="{v}"' for k, v in self.attrs.items())
                parts.append(f"[{attrs_str}]")
            if self.text_content:
                parts.append(f'"{self.text_content}"')
        return "".join(parts)
    
    def has_siblings(self) -> bool:
        """Check if the node has siblings."""
        return self.prev_sibling_id is not None or self.next_sibling_id is not None


class HtmlNodePool(BaseNodePool[HtmlNode]):
    """Manages a collection of html nodes for a single HTML conversion."""

    def __init__(self):
        self._next_id = 0
        self._nodes: dict[str, HtmlNode] = {}
        self._root_ids: set[str] = set()
        self._sequence_counter = 0

    def get_nodes_count(self) -> int:
        """Get number of nodes in the pool."""
        return len(self._nodes)

    def get_next_id(self) -> str:
        """Generate unique node ID."""
        self._next_id += 1
        return f"n{self._next_id}"

    def create_text_node(self, text: str, sequence_index: int | None = None) -> str:
        """Create a node for text content."""
        new_id = self.get_next_id()
        if sequence_index is None:
            self._sequence_counter += 1
            sequence_index = self._sequence_counter

        node = HtmlNode(
            id=new_id,
            tag="#text",
            attrs={},
            sequence_index=sequence_index,
            text_content=text.strip(),
            is_text_node=True,
        )
        self._nodes[new_id] = node
        return new_id

    def get_or_create_node(self, tag: Tag, is_root: bool = False) -> str:
        """Get existing node or create new one."""
        self._sequence_counter += 1
        new_id = self.get_next_id()

        node = HtmlNode(
            id=new_id,
            tag=tag.name,
            attrs=tag.attrs,
            sequence_index=self._sequence_counter,
        )

        self._nodes[new_id] = node
        if is_root:
            self._root_ids.add(new_id)

        return new_id

    def get_node(self, node_id: str) -> HtmlNode | None:
        """Get node by ID."""
        return self._nodes.get(node_id)

    def get_root_ids(self) -> set[str]:
        """Get all root node IDs."""
        return self._root_ids.copy()

    def update_parent_child(self, child_id: str, parent_id: str) -> None:
        """Update parent-child relationship between nodes."""
        child_node = self._nodes[child_id]
        parent_node = self._nodes[parent_id]

        child_node.parent_id = parent_id
        if child_id not in parent_node.children_ids:
            parent_node.children_ids.append(child_id)

        # Update sibling relationships
        if parent_node.children_ids:
            for index, child_id in enumerate(parent_node.children_ids):
                curr_node = self._nodes[child_id]
                if index > 0:
                    prev_id = parent_node.children_ids[index - 1]
                    curr_node.prev_sibling_id = prev_id
                if index < len(parent_node.children_ids) - 1:
                    next_id = parent_node.children_ids[index + 1]
                    curr_node.next_sibling_id = next_id

        # Update non-text siblings count
        if not child_node.is_text_node:
            parent_node.non_text_children_count += 1

    def get_siblings_count(self, node_id: str) -> int:
        """Get number of siblings for a node."""
        node = self._nodes[node_id]
        parent = self._nodes.get(node.parent_id)
        if parent:
            return parent.non_text_children_count - 1 # exclude current node    
        return 0

    def print_tree(self, node_id: str | None = None, level: int = 0) -> None:
        """Pretty print the tree structure."""
        if node_id is None:
            print("\nTree Structure:")
            print("=" * 50)
            for root_id in sorted(self._root_ids):
                self.print_tree(root_id)
            print("=" * 50)
            return

        node = self._nodes[node_id]
        indent = "  " * level

        # Print current node
        print(f"{indent}[{node.id}] {node}")

        # Print relationship info
        relations = []
        if node.parent_id:
            parent = self._nodes[node.parent_id]
            relations.append(f"parent: {parent.id}({parent.tag})")
        if node.prev_sibling_id:
            prev = self._nodes[node.prev_sibling_id]
            relations.append(f"prev: {prev.id}({prev.tag})")
        if node.next_sibling_id:
            next_ = self._nodes[node.next_sibling_id]
            relations.append(f"next: {next_.id}({next_.tag})")
        if relations:
            print(f"{indent}     → {', '.join(relations)}")

        # Print children
        for child_id in node.children_ids:
            self.print_tree(child_id, level + 1)
