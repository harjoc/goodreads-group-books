## Installation
This lists the books of a GoodReads group's members.

You will need to get a developer key from goodreads.com.

Tested on Windows with Python 2.7.11 and Ubuntu 17.10. To install goodreads python2 bindings:

```
pip install goodreads
```

## Usage

Copy config-example.py to config.py and edit it. 

Then list the group members: `./listbooks.py members`. This will save them to the group_fn configured in config.py.

Then list the books: `./listbooks.py`. This will create pickles for each user in shelves_dir as configured in config.py.

Then create a html list sorted by frequency: `./sort.py shelves_dir > top.html`.

There is a default of `min_reads = 5` in sort.py so books with less reads don't show up in the output. You can change it as needed.
