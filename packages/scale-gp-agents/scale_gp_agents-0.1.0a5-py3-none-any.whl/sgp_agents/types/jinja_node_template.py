# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional

from .._models import BaseModel

__all__ = ["JinjaNodeTemplate"]


class JinjaNodeTemplate(BaseModel):
    jinja_helper_functions: Optional[List[Union[str, object]]] = None

    jinja_template_path: Optional[str] = None

    jinja_template_str: Optional[str] = None
    """Raw template to apply to the data.

    This should be a Jinja2 template string. Please note, the data will be mapped as
    'value' in the template. Default None corresponds to {{value}}. Should access
    property `jinja_template_str` or field `jinja_template_str_loaded` for the
    loaded template data
    """

    jinja_template_str_loaded: Optional[str] = None
    """
    The original jinja_template_str field from the config might not contain the
    needed template, and we may need to load S3 data specified with
    `jinja_template_path`. This field caches the loaded template content, it is also
    accessed through property `jinja_template_str`.
    """
