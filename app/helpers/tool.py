import inspect
from app.helpers.registry import TOOL_REGISTRY

def _python_type_to_json(t):
    mapping={
        str: "string",
        int: "integer",
        bool: "boolean",
        float: "number"
    }

    return mapping.get(t, "string")

def tool(fn=None, *, name=None, description=None, tags=None):
    def wrapper(f):
        sig = inspect.signature(f)

        properties = {}
        required = []

        for param in sig.parameters.values():
            if param.name == "self":
                continue

            annotation = param.annotation if param.annotation != inspect._empty else str

            properties[param.name] = {
                "type": _python_type_to_json(annotation),
                "description": ""
            }

            if param.default is inspect._empty:
                required.append(param.name)

        tool_name = name or f.__name__

        TOOL_REGISTRY[tool_name] = {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": description or (f.__doc__ or ""),
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            },
            "handler": f,
            "tags": tags or []
        }

        return f

    if fn:
        return wrapper(fn)

    return wrapper
