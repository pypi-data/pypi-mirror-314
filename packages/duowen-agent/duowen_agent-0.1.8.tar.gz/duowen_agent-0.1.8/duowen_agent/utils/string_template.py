import re
from typing import List

from jinja2 import Environment, meta
from jinja2.sandbox import SandboxedEnvironment
from typing_extensions import Literal


def _get_jinja2_variables(template: str) -> List[str]:
    env = Environment()
    ast = env.parse(template)
    variables = meta.find_undeclared_variables(ast)
    return list(variables)


def _jinja2_format(template: str, **kwargs) -> str:
    return SandboxedEnvironment().from_string(template).render(**kwargs)


class StringTemplate:
    """String Template for llm. It can generate a complex prompt."""

    def __init__(self, template: str, template_format: Literal["f-string", "jinja2"] = "f-string"):
        self.template: str = template
        self.template_format: str = template_format
        self.variables: List[str] = []

        if template_format == "f-string":
            self.variables = re.findall(r"\{(\w+)\}", self.template)
        elif template_format == "jinja2":
            self.variables = _get_jinja2_variables(template)
        else:
            raise ValueError(f"template_format must be one of 'f-string' or 'jinja2'. Got: {template_format}")

    def format(self, **kwargs) -> str:
        """Enter variables and return the formatted string."""

        if self.template_format == "f-string":
            return self.template.format(**kwargs)
        elif self.template_format == "jinja2":
            return _jinja2_format(self.template, **kwargs)
