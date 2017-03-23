import inspect

all_blocks = {}

def block(**kwargs):
    def block_decorator(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        # registers the function
        name = func.__name__
        # gets the function factory parameters
        sig_outer = inspect.signature(func)
        # gets the inner function  parameters
        sig_inner = inspect.signature(func())
        all_blocks[name] = {
            '_func':   func,
            '_parameters': sig_outer.parameters,
            '_inputs': sig_inner.parameters,
            '_output': sig_inner.return_annotation,
            **kwargs}

        return inner
    return block_decorator
