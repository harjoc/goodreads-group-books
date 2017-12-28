## Installation
List the books of a GoodReads group's members

You will need to get a goodreads developer key, which you can get on goodreads.com.

Tested on Windows. To install goodreads python bindings:

```
pip install goodreads
```

## Usage

First list the group members: `python gb.py members` . This will save them to the group_fn listed at the top of gb.py.

Then list the books: `python gb.py`. This will create pickles for each user in shelves/<userid>.

You can load the pickles in python:

```
import pickle

f=open('shelves/123/1', 'rb')
while True:
  try:
    page = pickle.load(f)
  except EOFError:
    break
```
