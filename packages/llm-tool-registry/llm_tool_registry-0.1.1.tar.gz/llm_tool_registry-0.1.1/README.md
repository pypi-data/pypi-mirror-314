The llm_tool_registry package simplifies tool/function calling integration with Language Models (LLMs) like OpenAI's GPT models. It provides a clean, type-safe way to register Python functions as tools that can be called by LLMs.

Key features:
- Type-safe function registration with automatic JSON Schema generation
- Automatic parameter validation and documentation checking
- Support for OpenAI's function calling format
- Clean decorator-based API for registering tools
- Built-in docstring validation to ensure complete documentation
- Handles common Python types including strings, numbers, booleans, lists, and dictionaries
- Support for optional parameters and Union types

Example usage:

```python
from llm_tool_registry import ToolRegistry

registry = ToolRegistry()

@registry.tool()
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get the weather for a location.
    
    Args:
        location: The city and state/country
        unit: The temperature unit (celsius/fahrenheit)
    """
    # Implementation here
    pass

# Get OpenAI-compatible schema
schemas = registry.get_openai_schema()

# Execute registered tool
result = registry.execute("get_weather", location="London, UK")