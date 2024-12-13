from pydantic import BaseModel, Field

class HtmlAttributesPriority(BaseModel):
    """HTML attribute priorities configuration"""
    primary_attrs: set[str] = Field(
        default={
            'id',          # unique identifier, excellent for xpath
            'class',       # common for styling and semantic meaning
            'href',        # essential for links
            'role',        # semantic meaning for accessibility
            'aria-label',  # accessible label, often contains meaningful text
            'title'        # tooltip text, often descriptive
        },
        description="Highest priority attributes to keep"
    )
    
    secondary_attrs: set[str] = Field(
        default={
            'name',        # form elements and anchors
            'type',        # input/button types
            'value',       # form element values
            'placeholder', # input placeholder text
            'alt',         # image alternative text
            'for'         # label associations
        },
        description="Secondary attributes to keep if no primary attributes present"
    )
    
    ignore_attrs: set[str] = Field(
        default={
            'style',
            'target',
            'rel',
            'loading',
            'srcset',
            'sizes',
            'width',
            'height'
        },
        description="Attributes to always ignore"
    )

class HtmlConfig(BaseModel):
    """HTML-specific configuration"""

    # Optimization options
    simplify_classes: bool = False
    simplify_links: bool = False
    simplify_images: bool = False
    skip_tags: bool = False
    prioritize_attributes: bool = False

    # Tags to skip during conversion
    tags_to_skip: set[str] = Field(
        default={
            'script', 'style', 'noscript', 'head', 
            'meta', 'link', 'title', 'base', 'svg'
        },
        description="Tags to skip during conversion"
    )
    attributes_priority: HtmlAttributesPriority = Field(
        default_factory=HtmlAttributesPriority,
        description="Attribute priority configuration"
    )
