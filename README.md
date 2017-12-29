## Installation
This lists the books of a GoodReads group's members.

You will need to get a goodreads developer key, which you can get on goodreads.com.

Tested on Windows. To install goodreads python bindings:

```
pip install goodreads
```

## Usage

Copy config-example.py to config.py and edit it. 

Then list the group members: `./listbooks.py members`. This will save them to the group_fn listed in config.py.

Then list the books: `./listbooks.py`. This will create pickles for each user in shelves_dir/<userid>.

Then create a html list sorted by frequency: `./sort.py shelves_dir > top.html`.

There is a default of `min_reads = 5` in sort.py so books with less reads don't show up in the output. You can change it as needed.
