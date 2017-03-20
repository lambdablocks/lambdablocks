from lb.decorators import middle_block, block

@middle_block
def text_to_words():
    def inner(input_):
        o = input_.map(lambda x: x.lower())

        for sep in [',', '.', '!', '?', ';', '"', "'"]:
            o = o.map((lambda sep: lambda x: x.replace(sep, ''))(sep))

        o = o.flatMap(lambda x: x.split())
        return o
    return inner

@middle_block
def map_with_one():
    def inner(input_):
        o = input_.map(lambda el: (el, 1))
        return o
    return inner

@middle_block
def add():
    def inner(input_):
        o = input_.reduceByKey(lambda a,b: a+b)
        return o
    return inner

@middle_block
def swap():
    def inner(input_):
        o = input_.map(lambda x: (x[1],x[0]))
        return o
    return inner

@middle_block
def sort():
    def inner(input_):
        o = input_.sortByKey(ascending=False)
        return o
    return inner

@middle_block
def first_n(n):
    def inner(input_):
        o = input_.take(n)
        return o
    return inner

# @block(type='transform', inputs=['list'], outputs=['csv'])
# def list_to_csv():
#     def inner(input_):
#         o = []
#         for elem in input_:
#             o.append(','.join([str(x) for x in elem]))
#         return o
#     return inner
