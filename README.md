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

## Documentation

[The documentation of λ-blocks is available on ReadTheDocs](http://lambdablocks.readthedocs.io).

You'll find there the information needed to install the framework and
run your programs.
