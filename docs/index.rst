.. Lambda-blocks documentation master file, created by
   sphinx-quickstart on Mon Dec  4 11:37:04 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to λ-blocks' documentation!
===================================

λ-blocks is a framework that allows developers to write data
processing programs without writing code. For that purpose, it uses a
graph representation of a program (often in the form of an ETL)
written in YAML, which links together blocks of Python code.

In this scenario, the code blocks are the vertices of the computation
graph, while the links between them represent how computed data
"flows" from one block to the other.

This provides many benefits, among them are **ease of writing** (in
the simple YAML description format), **code deduplication** (by
reusing code blocks in different computation graphs, or by embedding
sub-graphs into bigger ones), and the ability to **reason about a
graph**, to optimize or debug it for example (through the use of
plugins). While λ-blocks comes with some batteries included (a
collection of blocks and plugins), it is easy (and encouraged) to add
your own, in order to fit the purposes of your organization of the
range of problems you're solving.

We encourage you to read the tutorial, to learn how to write and
execute your programs with λ-blocks, before diving in the available
block collections and plugins.

.. toctree::
   :maxdepth: 2

   tutorial
   examples
   blocks
   plugins
   developers
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
