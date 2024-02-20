

class FunctionStack:
    """
    The FunctionStack class allows for processing of the required Outpost scan range after all functions and their
    scan ranges have been called.

    ex:

    func1: scan range 10

    func2: scan range 25

    func3: scan range 15

    Without FunctionStack, a range 10 would be scanned, followed by a scan of range 25. With FunctionStack, the 'done'
    signal is passed to EnvironmentManager after func3, requiring only one scan of range 25.
    """
    def __init__(self):
        self.func_stack = []

    def add_to_stack(self, func, **kwargs):
        new_func = (func, kwargs)
        self.func_stack.append(new_func)

    def function_generator(self):
        for func, kwargs in self.func_stack:
            yield func, kwargs
