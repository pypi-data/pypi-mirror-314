import json
from typing import List, Optional, Union

from duowen_agent.tools.base import Tool


class ToolManager:
    """ToolManager helps Agent to manage tools"""

    def __init__(self, tools: List[Tool]):
        self.tools: List[Tool] = tools

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Find specified tool by tool name.
        Args:
            tool_name(str): The name of the tool.

        Returns:
            Optional[Tool]: The specified tool or None if not found.
        """
        return next((tool for tool in self.tools if tool.name == tool_name), None)

    def run_tool(self, tool_name: str, parameters: Union[str, dict]) -> str:
        """Run tool by input tool name and data inputs

        Args:
            tool_name(str): The name of the tool.
            parameters(Union[str, dict]): The parameters for the tool.

        Returns:
            str: The result of the tool.
        """
        tool = self.get_tool(tool_name)

        if tool is None:
            return (
                f"{tool_name} has not been provided yet, please use the provided tool."
            )

        if isinstance(parameters, dict):
            return tool.run(**parameters)
        else:
            return tool.run(parameters)

    @property
    def tool_names(self) -> str:
        """Get all tool names."""
        tool_names = ""
        for tool in self.tools:
            tool_names += f"{tool.name}, "
        return tool_names[:-2]

    @property
    def tool_descriptions(self) -> str:
        """Get all tool descriptions, including the schema if available."""
        tool_descriptions = ""
        for tool in self.tools:
            tool_descriptions += (
                json.dumps(
                    tool.to_schema(),
                    ensure_ascii=False,
                )
                + "\n"
            )
        return tool_descriptions
