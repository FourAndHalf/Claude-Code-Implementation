from typing import Dict, Callable, Any
from openai.types.chat import ChatCompletionToolParam

class RegisteredTool:
    def __init__(
        self,
        schema: ChatCompletionToolParam,
        handler: Callable[..., Any],
        tags: list[str] | None = None
    ):
        self.schema = schema
        self.handler = handler
        self.tags = tags or []

TOOL_REGISTRY: Dict[str, RegisteredTool] = {}

