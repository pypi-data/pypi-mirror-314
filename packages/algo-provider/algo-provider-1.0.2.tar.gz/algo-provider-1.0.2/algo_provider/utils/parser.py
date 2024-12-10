import inspect
import re

TYPE_MAPPING = {
    "int": "number",
    "float": "number",
    "str": "string",
    "bool": "boolean",
    "list": "array",
    "Any": "any",
}


def extract_algorithm_metadata(function):
    # Get the docstring of the function (if it exists)
    docstring = function.__doc__

    # Parse function signature using inspect module
    signature = inspect.signature(function)

    # Initialize the structure for the metadata
    algorithm_metadata = {
        "id": function.__name__,
        "name": function.__name__.replace("_", " ").title(),
        "description": (
            docstring.split("\n\n")[0].strip() if docstring else ""
        ),  # Default empty if no docstring
        "inputs": [],
        "outputs": [],
    }

    # Extraction of the function arguments with their types and descriptions
    args_details = {}
    return_details = {"type": None, "description": None}
    if docstring:
        # Docstring example::
        # This is a simple algorithm that adds two numbers together.
        # Parameters:
        #     input1 (int): The first number to add.
        #     input2 (int): The second number to add.
        # Returns:
        #     int: The sum of the two numbers.

        # This regular expression match the parameters in the docstring of the function
        # It looks for a word followed by a colon and the type in parenthesis
        input_pattern = re.compile(r"(\w+)\s*\(([^)]+)\):\s*([^\n]+)")

        for match in input_pattern.finditer(docstring):
            param_name = match.group(1)
            param_type = match.group(2)
            param_description = match.group(3)

            args_details[param_name] = {
                "type": TYPE_MAPPING.get(param_type, param_type),
                "description": param_description,
            }

        # This regular expression match the return type in the docstring of the function
        # It looks for the word "Returns:" followed by the type
        return_pattern = re.compile(r"Returns:\s*([^\n]+)")

        match = return_pattern.search(docstring)
        if match:
            # match.group(1): "int: The sum of the two numbers."
            if match.group(1):
                return_details["type"] = match.group(1).split(":")[0].strip()
                return_details["description"] = match.group(1).split(":")[1].strip()

    # Gets inputs from function signature
    for param_name, param in signature.parameters.items():
        param_data = args_details.get(param_name, {})
        param_type = param_data.get("type")

        if not param_type:
            if param.annotation != inspect.Parameter.empty:
                param_type = TYPE_MAPPING.get(
                    param.annotation.__name__, param.annotation.__name__
                )
            else:
                param_type = "any"

        # Input
        input_metadata = {
            "name": param_name,
            "description": param_data.get("description", ""),
            "type": param_type,
        }

        # Array type
        if param_type == "array" and hasattr(param.annotation, "__args__"):
            array_type = TYPE_MAPPING.get(
                param.annotation.__args__[0].__name__,
                param.annotation.__args__[0].__name__,
            )
            input_metadata["arrayType"] = array_type

        # Add default value
        if param.default != inspect.Parameter.empty:
            input_metadata["default"] = param.default

        # Add to the inputs list
        algorithm_metadata["inputs"].append(input_metadata)

    # Output
    if return_details["type"]:
        return_type = TYPE_MAPPING.get(return_details["type"], return_details["type"])
    else:
        return_type = (
            TYPE_MAPPING.get(str(signature.return_annotation.__name__), "any")
            if signature.return_annotation != inspect.Signature.empty
            else "any"
        )

    if return_details["description"]:
        return_description = return_details["description"]
    else:
        return_description = f"The result of {function.__name__}."

    algorithm_metadata["outputs"].append(
        {
            "name": "result",
            "description": return_description,
            "type": return_type,
        }
    )

    return algorithm_metadata
