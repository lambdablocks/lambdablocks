def input_block(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

middle_block = input_block
output_block = input_block


def block(type=None, inputs=[], outputs=[]):
    def block_decorator(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return block_decorator
