from emmetify.config.base_config import EmmetifierConfig
from emmetify.config.html_config import HtmlAttributesPriority
from emmetify.converters.base_converter import BaseConverter
from emmetify.nodes.html_nodes import HtmlNode, HtmlNodePool
from emmetify.utils.tokens import SingleTokenNames


class HtmlPriorityAttributeFilter:
    """Filters HTML attributes based on priority rules"""

    def __init__(self, priority_config: HtmlAttributesPriority):
        self.config = priority_config

    def _is_data_attribute(self, attr: str) -> bool:
        """Check if attribute is a data-* attribute"""
        return attr.startswith("data-")

    def _is_event_handler(self, attr: str) -> bool:
        """Check if attribute is an event handler"""
        return attr.startswith("on")

    def filter_attributes(self, attrs: dict[str, str]) -> dict[str, str]:
        """
        Filter attributes based on priority rules.
        Returns the most relevant attributes for LLM understanding and XPath creation.
        """
        if not attrs:
            return {}

        # Always remove ignored attributes
        filtered_attrs = {
            k: v
            for k, v in attrs.items()
            if k not in self.config.ignore_attrs
            and not self._is_data_attribute(k)
            and not self._is_event_handler(k)
        }

        # Check for primary attributes
        primary_attrs_present = {
            k: v for k, v in filtered_attrs.items() if k in self.config.primary_attrs
        }

        # If we have primary attributes, return only those
        if primary_attrs_present:
            return primary_attrs_present

        # Otherwise, keep secondary attributes
        return {
            k: v for k, v in filtered_attrs.items() if k in self.config.secondary_attrs
        }


class HtmlConverter(BaseConverter[HtmlNodePool]):
    """Converts HTML nodes to Emmet"""

    def __init__(self, config: EmmetifierConfig):
        super().__init__(config)

        self.priority_filter = HtmlPriorityAttributeFilter(
            config.html.attributes_priority
        )
        self.single_token_names = SingleTokenNames()

        self.classes_map: dict[str, str] = {}
        self.links_map: dict[str, str] = {}
        self.images_map: dict[str, str] = {}

    def _escape_text(self, text: str) -> str:
        """Escape * and $ in text content."""
        escape_chars = {
            "\\": "\\\\",
            "*": "\*",
            "$": "\$",
        }
        escaped = text.translate(str.maketrans(escape_chars))
        no_white_chars = " ".join(escaped.split())
        return no_white_chars

    def _node_to_emmet(self, node: HtmlNode) -> str:
        """Convert single node to Emmet notation with attribute filtering."""
        if node.is_text_node:
            return f"{{{self._escape_text(node.text_content)}}}"

        # Start with tag name
        parts = [node.tag]

        # Filter attributes before processing
        if self.config.html.prioritize_attributes:
            attributes = self.priority_filter.filter_attributes(node.attrs)
        else:
            attributes = node.attrs

        # Process id if present
        if "id" in attributes:
            parts.append(f'#{attributes["id"]}')

        # Process classes if present
        if "class" in attributes:
            emmet_class_name = f".{'.'.join(attributes['class'])}"
            space_separated_class_name = " ".join(
                attributes["class"]
            )  # for class map
            if self.config.html.simplify_classes:
                mapped_class = self.classes_map.get(space_separated_class_name)
                # the same class must be mapped to the same token
                # because llm making wrong assumptions in xpath generation
                # and making simpler xpath for the same class names (because it see it as diferent tokens)
                if not mapped_class:
                    single_token_class = self.single_token_names.get_name()
                    self.classes_map[space_separated_class_name] = single_token_class
                    parts.append(f".{single_token_class}")
                else:
                    parts.append(f".{mapped_class}")
            else:
                parts.append(emmet_class_name)

        # Process href for links
        if self.config.html.simplify_links and "href" in attributes:
            mapped_url = self.links_map.get(attributes["href"])
            if not mapped_url:
                single_token_url = self.single_token_names.get_name()
                self.links_map[attributes["href"]] = single_token_url
                attributes["href"] = single_token_url
            else:
                attributes["href"] = mapped_url

        # Process src for images
        if self.config.html.simplify_images and "src" in attributes:
            mapped_src = self.images_map.get(attributes["src"])
            if not mapped_src:
                single_token_src = self.single_token_names.get_name()
                self.images_map[attributes["src"]] = single_token_src
                attributes["src"] = single_token_src
            else:
                attributes["src"] = mapped_src

        # Remove id and class from remaining attributes since we've handled them
        remaining_attrs = {
            k: v for k, v in attributes.items() if k not in ["id", "class"] and v
        }

        # Add remaining filtered attributes
        if remaining_attrs:
            # if there are spaces in attribute value, it must be wrapped in quotes
            attr_str = " ".join(f'{k}="{v}"' if " " in v else f'{k}={v}' for k, v in remaining_attrs.items())
            parts.append(f"[{attr_str}]")

        return "".join(parts)

    def _build_emmet(
        self, node_pool: HtmlNodePool, node_data: str | HtmlNode, level: int = 0
    ) -> str:
        """Recursively build Emmet notation with optional indentation."""
        indent = " " * (self.config.indent_size * level) if self.config.indent else ""

        if isinstance(node_data, str):
            node = node_pool.get_node(node_data)
        else:
            node = node_data

        if not node:
            return ""

        # Emmetify current node
        node_emmet = self._node_to_emmet(node)

        # Get children nodes
        children_non_text_nodes: list[HtmlNode] = []
        child_text_node: HtmlNode | None = None  # Text node should be single and not grouped
        for child_id in node.children_ids:
            child_node = node_pool.get_node(child_id)
            if child_node.is_text_node:
                child_text_node = child_node
            else:
                children_non_text_nodes.append(child_node)

        # Emmetify children
        children_emmet: list[str] = []
        for child_node in children_non_text_nodes:
            child_emmet = self._build_emmet(node_pool, child_node, level + 1)
            children_emmet.append(child_emmet)

        # Emmetify text node
        text_node_emmet = self._node_to_emmet(child_text_node) if child_text_node else ""

        if self.config.indent:
            children_emmet_str = "+\n".join(children_emmet)
        else:
            children_emmet_str = "+".join(children_emmet)

        if children_emmet_str:
            if self.config.indent:
                children_group = f">\n{children_emmet_str}"
                # children_group = f">(\n{children_emmet_str}\n{indent})"
            else:
                children_group = f">{children_emmet_str}"
                # children_group = f">({children_emmet_str})"
        else:
            children_group = ""

        sibilings_count = node_pool.get_siblings_count(node.id)
        is_node_with_siblings_and_children = sibilings_count > 0 and len(children_non_text_nodes) > 0

        node_emmet_str = ""
        if is_node_with_siblings_and_children:
            node_emmet_str = f"({node_emmet}{text_node_emmet}{children_group})"
        else:
            node_emmet_str = f"{node_emmet}{text_node_emmet}{children_group}"

        return f"{indent}{node_emmet_str}"

    def convert(self, node_pool: HtmlNodePool) -> str:
        result = super().convert(node_pool)

        return {
            "result": result,
            "maps": {
                "classes": {v: k for k, v in self.classes_map.items()},
                "links": {v: k for k, v in self.links_map.items()},
                "images": {v: k for k, v in self.images_map.items()},
            },
        }
