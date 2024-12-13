from emmetify.emmetifier import Emmetifier
from emmetify.config import __all__ as config_all


def emmetify(content, format="html", **options):
    """Convenience function for quick conversions"""
    emmetifier = Emmetifier(format=format, **options)
    return emmetifier.emmetify(content)

def emmetify_compact_html(content):
    """Convenience function for quick HTML conversion with simplified tags and attributes"""
    emmetifier = Emmetifier(format="html", config={"html": {
        "skip_tags": True,
        "prioritize_attributes": True,
        "simplify_classes": True,
        "simplify_links": True,
        "simplify_images": True
    }})
    return emmetifier.emmetify(content)

__all__ = [
    "Emmetifier",
    "emmetify",
    "emmetify_compact_html",
    *config_all,
]
