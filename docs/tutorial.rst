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

   apt install python3 python3-yaml

Also not required for this tutorial, these dependencies are needed for
some blocks in the included library::

   apt install python3-matplotlib python3-requests-oauthlib

If you're not using Debian or a Debian-based system, be sure to
install Python 3, and PyYAML through `pip`.

Finally, if you want to use the Spark blocks, you will need Spark and
Pyspark to be installed on your system (but this is not required for
this tutorial).

λ-blocks
^^^^^^^^

While λ-blocks is still in its early days of development, it is not
available through `pip`, nor in any distribution package
manager. Therefore, you can install it this way::

   git clone https://github.com/lambdablocks/lambdablocks.git
   cd lambdablocks
   python3 setup.py install

Verification
^^^^^^^^^^^^

Try executing::

   blocks.py --help

If you get the help page of this executable, all is set!

Writing a computation graph
---------------------------

Now that everything is installed, let's dive into writing a first
λ-blocks program.

Such a program, also called a computation graph, is written in `YAML
<http://yaml.org/>`_, a simple data representation format. Create a
new file and name it `wordcount.yml`: it will contain the description
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
there is only one vertice: it uses the block `cat` from the
`lb.blocks.unixlike` blocks library. It has a unique name `cat` (since
we use only once the block `cat` in this program, the vertice name can
be the same as the block name), and one argument, a path to a file. As
you may have guessed, this block acts like the Unix `cat` utility: it
reads a file.

This program won't do much, except for reading a file. You can try to
execute it this way::

   blocks.py -f wordcount.yml

If nothing happens, it is normal: the file has been read by λ-blocks,
but it isn't supposed to be displayed on the console. If you get an
error, the path you provided may be incorrect: be sure to execute the
command within in the `lambdablocks` folder, or to change the
`filename` argument.

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

* `cat` reads a file and outputs a list of lines found in this file;

* `group_by_count` reads a list, and outputs a list of unique items,
  along with the number of times they appear in the list;

* `sort` reads a list, and outputs a sorted list, sorted by the second
  item of each element;

* `show_console` displays its inputs on the user console.

A block has named inputs and named outputs. To link two blocks
together, we specify the inputs of a block in the `inputs` key. For
example, the block `group_by_count` takes one input, `data`, that is
the output `result` of the block `cat`.

Let's try to execute this graph::

   blocks.py -f wordcount.yml

That's it! You should get a list of fruits, along with their number of
occurences.
