Tutorial
========

In this tutorial, we go through the steps of installing λ-blocks,
writing a computation graph, and proceed to execute it.

Installation
------------

Dependencies
^^^^^^^^^^^^

If you're using Debian, Ubuntu, or a system of this family, the
required dependencies should all be available in your package manager::

   sudo apt install python3 python3-venv libyaml-dev

If you're not using Debian or a Debian-based system, be sure to
install Python 3 and the development headers of ``libyaml``, this is
necessary for ``pip`` to compile PyYAML.

Finally, if you want to use the Spark blocks, you will need Spark and
``pyspark`` to be installed on your system (but this is not required
for this tutorial).

λ-blocks
^^^^^^^^

While λ-blocks is still in its early days of development, it is not
available through ``pip``, nor in any distribution package
manager. Therefore, the best is to install it in a virtual environment
this way::

   git clone https://github.com/lambdablocks/lambdablocks.git
   cd lambdablocks
   pyvenv VENV
   source VENV/bin/activate
   python3 setup.py install

Also not required for this tutorial, these dependencies are needed for
some blocks in the included library::

   pip install matplotlib requests-oauthlib


Verification
^^^^^^^^^^^^

Don't leave your activated virtual environment, and try executing::

   blocks.py --help

If you get the help page of this executable, all is set!

Writing a computation graph
---------------------------

Now that everything is installed, let's dive into writing a first
λ-blocks program.

Such a program, also called a computation graph, is written in `YAML
<http://yaml.org/>`_, a simple data representation format. Create a
new file and name it ``wordcount.yml``: it will contain the description
of a computation graph to perform a Wordcount. Add this content::

   ---
   name: wordcount
   description: Counts words
   ---
   - block: cat
     name: cat
     args:
       filename: examples/wordlist

This YAML file contains two parts: the first one is a key/value list
giving information on the computation graph (such as its name and
description). The second part is more interesting: it contains the
list of the code blocks that are the vertices of our graph. For now,
there is only one vertice: it uses the block
:py:func:`lb.blocks.unixlike.cat`. It has a unique name ``cat`` (since
we use only once the block ``cat`` in this program, the vertice name
can be the same as the block name), and one argument, a path to a
file. As you may have guessed, this block acts like the Unix ``cat``
utility: it reads a file.

This program won't do much, except for reading a file. You can try to
execute it this way::

   blocks.py -f wordcount.yml

If nothing happens, it is normal: the file has been read by λ-blocks,
but it isn't supposed to be displayed on the console. If you get an
error, the path you provided may be incorrect: be sure to execute the
command within in the ``lambdablocks`` folder, or to change the
``filename`` argument.

Let's add a few vertices in our graph, and link them together to
compute a Wordcount implementation::

   ---
   name: wordcount
   description: counts words
   ---
   - block: cat
     name: cat
     args:
       filename: examples/wordlist

   - block: group_by_count
     name: group
     inputs:
       data: cat.result

   - block: sort
     name: sort
     args:
       key: "lambda x: x[1]"
       reverse: true
     inputs:
       data: group.result

   - block: show_console
     name: show
     inputs:
      data: sort.result

We now have 4 blocks (or vertices):

* ``cat`` reads a file and outputs a list of lines found in this file;

* ``group_by_count`` reads a list, and outputs a list of unique items,
  along with the number of times they appear in the list;

* ``sort`` reads a list, and outputs a sorted list, sorted by the second
  item of each element;

* ``show_console`` displays its inputs on the user console.

A block has named inputs and named outputs. To link two blocks
together, we specify the inputs of a block in the ``inputs`` key. For
example, the block ``group_by_count`` takes one input, ``data``, that is
the output ``result`` of the block ``cat``.

Let's try to execute this graph::

   blocks.py -f wordcount.yml

That's it! You should get a list of fruits, along with their number of
occurences.

Using plugins
-------------

λ-blocks, while processing a computation graph, can execute plugins,
which are pieces of Python code able to act on the graph. For example,
let's try the included :py:mod:`lb.plugins.debug` plugin::

   blocks.py -f wordcount.yml -p lb.plugins.debug

This plugin will display an excerpt of the results produced by each
block, which allows you to effectively see what every block is
doing. This is useful to follow the data as it is transformed from the
entry of the graph to all the following vertices.

You can also try to execute the :py:mod:`lb.plugins.instrumentation`
plugin the same way, which will measure the time taken by every block
to compute, useful to detect bottlenecks::

   blocks.py -f wordcount.yml -p lb.plugins.debug lb.plugins.instrumentation

Unsurprisingly, the ``cat`` block should be the slowest, because it
requires to read a file on disk.

Next steps
----------

Now that we've seen some possibilities of λ-blocks and how it works,
you can look at some :doc:`examples <examples>`, :doc:`check the list
of available blocks <blocks>`, :doc:`the list of available plugins
<plugins>`, :doc:`write your own blocks <write-blocks>` or :doc:`write
your own plugins <write-plugins>`.
