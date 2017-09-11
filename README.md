# Lambda blocks

## Introduction

λ-blocks is a framework to easily run data processing programs.

It allows to declaratively describe a list of actions to take on an
input dataset, and get results. The list of actions is actually a DAG,
a directed acyclic graph, a powerful data structure often used to
internally represent data processing programs. Every action is
associated to a block, a piece of code (usually a function) that
performs a particular task.

λ-blocks runs on top of distributed (or not) data analysis engines,
such as Apache Spark, so it leverages all the distributed and
fault-tolerance mechanisms present in these frameworks. In fact, it
can use any framework (and combine them). It is simply a way to
organize and compose your blocks of code together.

To sum-up, λ-blocks has the following benefits:

* engine-agnostic representation format for describing data
  transformation,
* parametrisable, reusable and composable code snippets (blocks) which
  allow easy data mining, data exploration, and pipelining,
* composition of frameworks such as large-scale data analysis engines
  or plot engines,
* DAG as a first-class citizen, to allow complex DAG manipulations and
  optimizations.

This repository contains the reference implementation of λ-blocks,
which uses YAML as the DAG description format, and Python3 as the
programming language for blocks. The engine itself is written in
Python3. However, it is possible (and encouraged) to write other
implementations with different language choices.

## How to install

### Debian dependencies

Python libraries:
`apt install python3 python3-yaml python3-matplotlib python3-nose2 python3-nose2-cov python3-requests-oauthlib`

If you want to write topologies based on Spark, you need to install
Spark and pyspark.

### Other systems

The Python dependencies are all part of Pypi and installable through
`pip`. It should work on all UNIX-based systems, and, who knows, on
Windows. Be sure to report installation failures/successes on
different systems!

### Getting λ-blocks

At the moment, the best way to get λ-blocks locally is to clone this
repository. After installing the dependencies, everything should work
out of the box.

### Running tests

* Be sure to have all dependencies installed, system-wide or in a
  virtualenv.
* `source env.sh`
* `make test`

## Examples

The folder `examples` shows some basic examples of what you can do
with λ-blocks. To run them:

```
source env.sh
python3 bin/blocks.py -f examples/display_wordcount.yml
```
