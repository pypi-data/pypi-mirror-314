from typing import Any, Callable, Dict, List, Type, get_type_hints, TypedDict, Union
from dataclasses import dataclass
from enum import Enum
import inspect
from docstring_parser import parse
from functools import wraps

class ParameterType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"

class ToolSchema(TypedDict):
    name: str
    description: str
    parameters: Dict[str, Dict[str, Any]]
    required: List[str]

@dataclass
class Tool:
    func: Callable
    schema: ToolSchema

class DocstringValidationError(Exception):
    pass

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def _parse_type_hint(self, hint: Type) -> Dict[str, str]:
        """Convert Python type hints to JSON Schema types."""
        type_mapping = {
            str: ParameterType.STRING,
            int: ParameterType.NUMBER,
            float: ParameterType.NUMBER,
            bool: ParameterType.BOOLEAN,
            list: ParameterType.ARRAY,
            dict: ParameterType.OBJECT
        }

        if hasattr(hint, "__origin__") and hint.__origin__ == Union:
            args = [arg for arg in hint.__args__ if arg != type(None)]
            if len(args) == 1:
                return self._parse_type_hint(args[0])

        if hint in type_mapping:
            return {"type": type_mapping[hint]}

        if hasattr(hint, "__origin__"):
            if hint.__origin__ in (list, List):
                return {"type": ParameterType.ARRAY}
            if hint.__origin__ in (dict, Dict):
                return {"type": ParameterType.OBJECT}

        raise ValueError(f"Unsupported type hint: {hint}")

    def _validate_docstring(self, func: Callable, docstring_params: Dict[str, Any], sig_params: Dict[str, Any]):
        """Validate docstring parameters match function signature."""
        # Get parameter names excluding 'self'
        sig_param_names = {name for name in sig_params if name != 'self'}
        doc_param_names = set(docstring_params.keys())

        # Check for missing parameters in docstring
        missing_in_doc = sig_param_names - doc_param_names
        if missing_in_doc:
            raise DocstringValidationError(
                f"Function '{func.__name__}' is missing documentation for parameters: {', '.join(missing_in_doc)}"
            )

        # Check for extra parameters in docstring
        extra_in_doc = doc_param_names - sig_param_names
        if extra_in_doc:
            raise DocstringValidationError(
                f"Function '{func.__name__}' has documentation for non-existent parameters: {', '.join(extra_in_doc)}"
            )

    def tool(self):
        """Decorator to register a function as a tool."""
        def decorator(func: Callable) -> Callable:
            if not func.__doc__:
                raise ValueError(f"Function {func.__name__} must have a docstring")

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            hints = get_type_hints(func)
            docstring = parse(func.__doc__)
            sig = inspect.signature(func)

            # Create param description mapping
            param_descriptions = {
                param.arg_name: param.description
                for param in docstring.params
            }

            # Validate docstring against function signature
            self._validate_docstring(func, param_descriptions, sig.parameters)

            parameters = {}
            required = []

            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue

                param_type = hints.get(param_name)
                if param_type is None:
                    raise ValueError(f"Parameter {param_name} must have type hints")

                param_schema = self._parse_type_hint(param_type)

                # Description must exist from validation step
                param_schema["description"] = param_descriptions[param_name]
                parameters[param_name] = param_schema

                if param.default == inspect.Parameter.empty:
                    required.append(param_name)

            tool_schema = ToolSchema(
                name=func.__name__,
                description=docstring.short_description or "",
                parameters={
                    "type": "object",
                    "properties": parameters,
                    "required": required
                },
                required=required
            )

            self._tools[func.__name__] = Tool(func=wrapper, schema=tool_schema)
            return wrapper

        return decorator

    def get_openai_schema(self) -> List[Dict[str, Any]]:
        """Convert registered tools to OpenAI's schema format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.schema["name"],
                    "description": tool.schema["description"],
                    "parameters": tool.schema["parameters"]
                }
            }
            for tool in self._tools.values()
        ]

    def execute(self, tool_name: str, **kwargs: Any) -> Any:
        """Execute a registered tool by name."""
        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name].func(**kwargs)