# Lambda blocks

## Dependencies

* python3
* python3-yaml
* python3-matplotlib
* Apache Spark and pyspark

## Pre-requisites

* Be sure to have all dependencies installed, system-wide or in a
  virtualenv.
* `source env.sh`

## Run examples

```
python3 bin/blocks.py -f examples/wordcount.yml
```

## Generate documentation for registered blocks

```
python3 bin/doc.py 2>/dev/null
```
