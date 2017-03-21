all_blocks = {}

def block(inputs=[], outputs=[]):
    def block_decorator(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        # registers the function
        all_blocks[func.__name__] = {
            'func': func,
            'inputs': inputs,
            'outputs': outputs}
        return inner
    return block_decorator
