# Make things faster

## Don't use the pip-generated /usr/local/bin/blocks.py

It adds a significant overhead.

```
sudo rm /usr/local/bin/blocks.py
sudo ln -s /path/to/lambdablocks/bin/blocks.py /usr/local/bin/blocks.py
```

## Don't load all the blocks modules

Select only the ones you need.

```
blocks.py --no-internal-modules -m foo bar
```
