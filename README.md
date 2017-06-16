# Lambda blocks

λ-blocks is a library to easily run data analysis programs.

It is composed of a registry of predefined "blocks", and it is easy to
add your own blocks using Python.

A block is a snippet of code performing one of these 3 actions:

* Generate data, for example from a file on disk on from an API.
* Transform data, for example filtering useless lines, counting,
  aggregating, feeding an ML engine, etc.
* Storing results, for example in a file or a plot.

λ-blocks runs on top of distributed (or not) data analysis engines,
such as Apache Spark, so it leverages all the distributed and
fault-tolerance mechanisms present in these frameworks. In fact, it
can use any framework (and combine them). It is simply a way to
organize and compose your blocks of code together.

A topology is written in YAML, and describes the pipeline of blocks
through which your data will flow and will be computed. Using a simple
format allows for many ways to write data analysis programs: writing
(and sharing) YAML, or using a graphical interface to compose your
topology.

To sum-up, λ-blocks has the following benefits:

* engine-agnostic representation format for describing data
  transformation,
* parametrisable, reusable and composable code snippets (blocks) which
  allow easy data mining, data exploration, and pipelining,
* composition of frameworks such as large-scale data analysis engines
  or plot engines.

We aim to enable large-scale data analysis for everyone, without
software skills.

## Dependencies

On Debian:

* python3
* python3-yaml
* python3-matplotlib
* python3-nose2
* python3-nose2-cov
* Apache Spark and pyspark

## Pre-requisites

* Be sure to have all dependencies installed, system-wide or in a
  virtualenv.
* `source env.sh`

## Run examples

```
python3 bin/blocks.py -f examples/display_wordcount.yml
```

## Generate documentation for registered blocks

```
python3 bin/doc.py 2>/dev/null
```
