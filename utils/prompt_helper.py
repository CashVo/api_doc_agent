from enum import Enum
'''Using enum to write out verbose prompt instructions'''

# Define the JSON format that captures the structure of class and function signatures 
class PARSER_TEXT(Enum):
    JSON_FORMAT = '''
        {
            "classes": [
                {
                    "class": "name of class",
                    "description": "provide a short descripton about this class"
                    "constructors": ["provide a list of class constructors"],
                    "functions": [
                    {
                        "function": "name of function",
                        "description": "provide a short description about this function",
                        "function_signature": "full function signature",
                        "parameters": {
                            "param1": "description: provide a short description",
                            "param2": "description: provide a short description"
                        }
                    }
                    ]
                }
            ]
        }
'''
    # An example of what the final JSON would look like after file is parsed
    EXAMPLES = '''Here is an example response
{
    "classes": [
        {
            "class": "ShapeCalculator",
            "description": "A class that calculates the area and perimeter of different shapes",
            "constructors": [
                "def __init__(self, length: float, width: float) -> None:",
                "def __init__(self, radius: float = 1.0) -> None:",
                "def __init__(self, *sides: float) -> None:"
            ],
            "functions": [
                {
                    "function": "calculate_rectangle_area",
                    "description": "Calculates the area of a rectangle",
                    "function_signature": "def calculate_rectangle_area(self, length: float, width: float) -> float:",
                    "parameters": {
                        "length": "The length of the rectangle",
                        "width": "The width of the rectangle"
                    }
                },
                {
                    "function": "calculate_circle_area",
                    "description": "Calculates the area of a circle",
                    "function_signature": "def calculate_circle_area(self, radius: float = 1.0) -> float:",
                    "parameters": {
                        "radius": "The radius of the circle (default is 1.0)"
                    }
                },
                {
                    "function": "calculate_polygon_perimeter",
                    "description": "Calculates the perimeter of a polygon",
                    "function_signature": "def calculate_polygon_perimeter(self, *sides: float) -> float:",
                    "parameters": {
                        "*sides": "A variable number of side lengths"
                    }
                }
            ]
        }
    ]
}
'''
