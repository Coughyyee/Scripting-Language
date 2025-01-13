from typing import Literal
from util.printer import value_print

ValueType = Literal["null", "number", "boolean", "object"]


class RuntimeVal:
    def __init__(self, type: ValueType):
        self.type = type

    def __str__(self):
        return value_print(self.__class__.__name__, None, self.type)


class NullVal(RuntimeVal):
    def __init__(self):
        super().__init__("null")
        self.value = None

    def __str__(self):
        return value_print(self.__class__.__name__, self.value, self.type)


class NumberVal(RuntimeVal):
    def __init__(self, value: float):
        super().__init__("number")
        self.value = value

    def __str__(self):
        return value_print(self.__class__.__name__, self.value, self.type)


class BooleanVal(RuntimeVal):
    def __init__(self, value: bool):
        super().__init__("boolean")
        self.value = value

    def __str__(self):
        return value_print(self.__class__.__name__, self.value, self.type)


class ObjectVal(RuntimeVal):
    def __init__(self, properties: dict[str, RuntimeVal]):
        super().__init__("object")
        self.properties = properties

    def __str__(self, level=0):
        indent = "  " * level
        nested_indent = "  " * (level + 1)

        # Recursively generate string for nested objects
        props_str = "\n".join(
            f"{nested_indent}{key}: {value.__str__(level+1) if isinstance(value, ObjectVal) else value}"
            for key, value in self.properties.items()
        )

        # Build the string for the current object
        result = f"[{self.__class__.__name__}] <value: {{\n{props_str}\n{indent}}}, type: {self.type}>"
        return result


"""Helper Functions"""


def MK_NULL():
    return NullVal()


def MK_NUMBER(n: float = 0):
    return NumberVal(n)


def MK_BOOL(b=True):
    return BooleanVal(b)
