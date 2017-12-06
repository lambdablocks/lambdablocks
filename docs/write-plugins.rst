Write your own plugins
======================

As seen in the :doc:`tutorial`, using plugins is convenient to add
dynamic features to computation graphs. And they are easy to write!
Let's begin with an example::

   from lb.plugins_manager import before_block_execution, \
        after_block_execution, \
        before_graph_execution, \
        after_graph_execution

   state = {'count': 0}

   @before_block_execution
   def tell_user_block(block, results):
       print('About to execute block {}.'.format(
           block.fields['name']))

   @after_block_execution
   def inc_block_counter(block, results):
       state['count'] += 1

   @before_graph_execution
   def tell_user_graph(vertices, entry_points):
       print('About to execute a graph with {} vertices.'.format(
           len(vertices)))

   @after_graph_execution
   def tell_user_total(results):
       print('Finished! The graph execution triggered {} block executions.'.format(
           state['count']))

Name this file something like ``log.py``, move it in
``lambdablocks/lb/plugins/``, and use it this way::

   blocks.py -f path/to/your/graph.yaml -p log

Let's see what happens in this example:

* Events from the plugin manager are imported, and registered with the
  decorators ``@before_block_execution``, ``@after_block_execution``,
  ``@before_graph_execution``, ``@after_graph_execution``.

* The registered functions are called at different points during the
  graph execution.

* A state can be kept as a module variable (``state`` in this example).

Now, the list of events that can be registered:

* ``before_graph_execution``: this happens after the graph has been
  parsed, checked, and all blocks have been found in the registry;
  right before executing the first entry points. Two variables are
  passed to registered functions: ``vertices`` (the list of vertices
  of the graph, each containing their in- and out-links), and
  ``entry_points`` (the vertices which don't have any inputs, and
  hence are the entry points of the computation graph).

* ``after_graph_execution``: this happens after the graph has finished
  its execution, and all the vertices reachable from the entry points
  have been executed. It receives one variable, ``results``, a
  dictionary containing all the vertices results (the data they've
  computed).

* ``before_block_execution``: this happens before every block is
  computed, and functions receive two variables: ``block`` (the block
  about to be executed) and ``results``, all the results that have
  been computed so far.

* ``after_block_execution``: likewise, this happens after every block
  has been computed. The passed variables are the same as in
  ``before_block_execution``.
