## Installation
This lists the books of a GoodReads group's members.

You will need to get a developer key from goodreads.com.

Tested with Python 2.7. To install goodreads bindings:

```
pip install goodreads
```

## Output format

Reads|Year|Ratings|Book
---:|---:|---:|:---
238|1950|2167591|[1984 - George Orwell](https://www.goodreads.com/book/show/5470.1984)
211|1993|1480351|[The Alchemist - Paulo Coelho](https://www.goodreads.com/book/show/865.The_Alchemist)
192|2003|12405|[Maitreyi - Mircea Eliade](https://www.goodreads.com/book/show/817199.Maitreyi)
182|2004|2899284|[The Great Gatsby - F. Scott Fitzgerald](https://www.goodreads.com/book/show/4671.The_Great_Gatsby)
181|2000|2272395|[Pride and Prejudice - Jane Austen](https://www.goodreads.com/book/show/1885.Pride_and_Prejudice)
...|||

A complete result for a group with 3000 members is here: http://patraulea.com/goodreads/shelves_romania%20topbooks.html

## Usage

1. Copy config-example.py to config.py and fill in the API key. 

2. Get the group members: `./listbooks.py members`. This will save them to the group_fn configured in config.py.

3. Get the books: `./listbooks.py`. This will create pickles for each user in shelves_dir as configured in config.py.

4. Sort by number of reads: `./sort.py shelves_dir > top.html`.

There is a default of `min_reads = 5` in sort.py so books with less reads don't show up in the output. You can change it as needed.
