all_blocks = {}

# def input_block(func):
#     def inner(*args, **kwargs):
#         return func(*args, **kwargs)
#     return inner

# middle_block = input_block
# output_block = input_block


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
