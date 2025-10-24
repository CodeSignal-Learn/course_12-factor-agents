import inspect
from typing import get_type_hints, get_origin


class ClientTool:
    """Wraps a Python function to create an OpenAI-compatible tool with auto-generated schema.
    
    Attributes:
        name (str): Tool name for the function schema.
        description (str): Description of what this tool does.
        function (callable): The Python function to execute.
        schema (dict): OpenAI function schema generated from the function signature.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        function
    ):
        # Schema is generated eagerly so the Agent can pass it to the model at construction time
        self.name = name
        self.description = description
        self.function = function
        self.schema = self._generate_schema()
    
    def execute(self, **kwargs):
        """Execute the underlying function with keyword arguments.
        
        Args:
            **kwargs: Arguments to pass to the function.
        
        Returns:
            The return value from the function.
        """      
        return self.function(**kwargs)
    
    def _generate_schema(self):
        """Generate OpenAI function schema from the function signature.
        
        Uses introspection to extract parameter names, types, and defaults.
        Parameters without defaults are marked as required.
        
        Returns:
            dict: OpenAI-compatible function schema.
        """
        # Reflect on the target function for its parameters and annotations
        signature = inspect.signature(self.function)
        annotations = get_type_hints(self.function)

        # Clean, explicit Python -> JSON type mapping
        type_map = {
            int: "integer",
            float: "number",
            str: "string",
            bool: "boolean",
            list: "array",
            dict: "object",
            tuple: "array",
            type(None): "null",
        }

        properties = {}
        required = []

        for param_name, param in signature.parameters.items():
            # Skip implicit instance/class parameters in methods
            if param_name in ("self", "cls"):
                continue

            # Look up the annotation; if none, default to str
            annotation = annotations.get(param_name, str)
            origin = get_origin(annotation)
            base = origin or annotation

            json_type = type_map.get(base, "string")
            properties[param_name] = {"type": json_type}

            # No default value means the argument is required
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        schema = {
            "type": "function",
            "name": self.name,                    # Provided by the user when wrapping the function
            "description": self.description,      # Short, human-readable description
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False
            }
        }

        return schema
