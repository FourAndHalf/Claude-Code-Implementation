import inspect
from app.helpers.registry import TOOL_REGISTRY

class ToolExecutor:

    async def execute(self, name: str, args: dict):
        tool = TOOL_REGISTRY[name]
        handler = tool["handler"]

        if inspect.iscoroutinefunction(handler):
            return await handler(**args)

        return handler(**args)
