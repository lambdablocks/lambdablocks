Write your own blocks
=====================

λ-blocks comes with some blocks libraries, but it is likely you will
write your own at some point. Whenever you've identified a
transformation that is small (a block should do one job and do it
well) and will be needed in one or more graphs, it's time to write a
block for it.

Let's consider this example block::


   from lb.registry import block
   from lb.types import ReturnType
   from lb.utils import ReturnEntry, default_function

   @block(engine='foo')
   def join(sep: str='\n'):
       """Joins a list of strings.

       :param str sep: What will separate the strings in the result.
       :input List[Any] data: The list of items you want to join.
       :output Any result: The joined result.
       """
       def inner(data: List[Any]) -> ReturnType[Any]:
           result = sep.join(data)
           return ReturnEntry(result=data)
       return inner

A block is a Python function, registered with the ``@block``
decorator; this permits the blocks registry to inspect it (to retrieve
its types, etc) and store it for when it will be called by a graph.

The function itself has a name, which will be the same as the block
name, in this case ``block``. It takes a list of arguments, often
typed, and often with default values (to ease the process of calling
this block from YAML).

There's an important distinction between *arguments* and *inputs*. The
arguments of a block are "static", in the sense that they are set at
compile time in the YAML graph. They are used to parameterize a
block. On the other hand, the inputs represent the data that flows
between blocks. In general, changing arguments will change the way the
block behaves with regards to its inputs, and will raise different
outputs.

A block returns a closure, for that purpose it creates an ``inner``
function, and returns it at the end (``return inner``). This inner
function takes the inputs of the block as arguments. It then
transforms the inputs, before returning one or more outputs.

In our case, the ``inner`` function takes a typed input named
``data``, uses both this input and the ``sep`` arg to create a new
value (``result``), and finally returns it.

Notice two things:

 * The return value can be typed with ``ReturnType``.
 * The return value is embedded into a ``ReturnEntry``, which can
   contain as many fields as you want.

Finally, the outer block (``join``) contains its documentation. It has
a block description, along with the list of parameters, inputs and
outputs. This is useful to auto-generate the blocks documentation.

In order to use this block, it must be contained in a file and
findable by your Python interpreter. By default, ``blocks.py`` will
import all the blocks it can find in ``lb.blocks.*``, and you can add
your own modules by doing::

   blocks.py -m mymodules.myblocks mymodules.myotherblocks

assuming you have the sub-modules ``myblocks`` and ``myotherblocks``
in the module ``mymodules``. Any combination is possible, as long as
it is importable by Python.
