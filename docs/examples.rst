Examples
========

Simple unix-like pipes
----------------------

The file `examples/unix.yml` parses the file `/etc/passwd` on your
system (if it exists), greps it for `root`, cuts some fields, keeps
only the last line, and finally displays the result::

   blocks.py -f examples/unix.yml

Over http
---------

The graph located in `examples/http.yml` does fetches a file over
http, filters it, and saves the result in a file::

   blocks.py -f examples/http.yml

Twitter Wordcount with sub-graph
--------------------------------

The graph in `examples/twitter_wordcount.yml` will count the most used
hashtags on the AFP timeline. For that purpose, it uses a sub-graph,
located in `examples/topology-wordcount.yml`, which does the counting
words part.

To make it work, you first need to fill in your Twitter API
credentials, and then::

   blocks.py -f examples/twitter_wordcount.yml

Wordcount with Spark and a sub-graph
------------------------------------

The graph in `examples/spark_wordcount.yml` does a Wordcount over a
file, using a sub-graph for counting words. It will display the result
both in the console and in a matplotlib plot.. You need to install
Matplotlib, Spark and Pyspark, and then::

   PYSPARK_PYTHON=python3 blocks.py -f examples/spark_wordcount.yml
