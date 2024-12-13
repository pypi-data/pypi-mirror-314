from bs4 import BeautifulSoup, Comment, NavigableString, Tag

from emmetify.config.base_config import EmmetifierConfig
from emmetify.nodes.html_nodes import HtmlNodePool
from emmetify.parsers.base_parser import BaseParser


class HtmlParser(BaseParser[HtmlNodePool]):
    def __init__(self, config: EmmetifierConfig):
        super().__init__(config)
        self.skip_tags = self._get_skip_tags()

    def _get_skip_tags(self) -> set[str]:
        if self.config.html.skip_tags:
            return set(self.config.html.tags_to_skip)
        return set()

    def _process_node_contents(self, node: Tag, node_pool: HtmlNodePool) -> list[str]:
        content_ids = []

        for content in node.contents:
            # Skip comments
            if isinstance(content, Comment):
                continue

            # Skip empty text nodes
            if isinstance(content, NavigableString):
                text = str(content).strip()
                if text:  # Only process non-empty text
                    text_id = node_pool.create_text_node(text)
                    content_ids.append(text_id)

            # Skip unnecessary tags
            elif isinstance(content, Tag):
                if content.name not in self.skip_tags:
                    tag_id = node_pool.get_or_create_node(content)
                    content_ids.append(tag_id)

                    child_ids = self._process_node_contents(content, node_pool)
                    for child_id in child_ids:
                        node_pool.update_parent_child(child_id, tag_id)

        return content_ids

    def _build_tree(self, soup: BeautifulSoup) -> HtmlNodePool:
        """Build tree structure handling both text and tag nodes."""
        node_pool = HtmlNodePool()

        root_tags: list[Tag] = []
        for tag in soup.children:
            if isinstance(tag, Tag) and tag.name not in self.skip_tags:
                root_tags.append(tag)

        for root_tag in root_tags:
            root_id = node_pool.get_or_create_node(root_tag, is_root=True)
            content_ids = self._process_node_contents(root_tag, node_pool)

            for content_id in content_ids:
                node_pool.update_parent_child(content_id, root_id)

        if self.config.debug:
            print(f"Nodes count: {node_pool.get_nodes_count()}")

        return node_pool

    def parse(self, content: str) -> HtmlNodePool:
        soup = BeautifulSoup(content, "html.parser")
        node_pool = self._build_tree(soup)
        if self.config.debug:
            node_pool.print_tree()
        return node_pool
