from .function_stack import FunctionStack


def get_stack_values(function_stack: FunctionStack, variable_name: str) -> list:
    values = []
    for func, kwargs in function_stack.function_generator():
        if variable_name in kwargs:
            values.append(kwargs[variable_name])
    return values
