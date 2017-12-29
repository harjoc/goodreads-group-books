#!/usr/bin/env python

from __future__ import with_statement
import sys, pickle, os

if len(sys.argv) < 2:
    print "need shelves_dir argument"
    sys.exit(1)

shelves_dir = sys.argv[1]

fmt = 'html'

if len(sys.argv) >= 3:
    if sys.argv[2] in ['text']:
        fmt = sys.argv[2]
    else:
        print "unknown format:", sys.argv[2]
        sys.exit(1)

min_reads = 5

if fmt == 'html':
    print """
<html>
<head>
<title>%s</title>
<style>
th {
    text-align: left;
    padding-right: 1em;
}

td {
    padding-right: 1em;
}

.reads {
    text-align: right ! important;
}

.average {
    text-align: right ! important;
}

.year {
    text-align: right ! important;
}

table {
    padding-left: 1em;
}

</style>
</head>
<body>

<table border=0>
<tr>
    <th>Reads
    <th>Year
    <th>Average
    <th>Ratings
    <th>Book
""" % shelves_dir

lst = []

for user in os.listdir(shelves_dir):
    if user in ['.', '..']: continue
    
    all = '%s/%s/_all' % (shelves_dir, user)
    page2 = '%s/%s/2' % (shelves_dir, user)
    
    if not os.path.exists(all): continue
    if os.stat(all).st_size == 0: continue
    
    # avoid spammers and voracious readers
    if os.path.exists(page2): continue

    print >>sys.stderr, 'user', user

    with open(all, 'rb') as f:
        while True:        
            try:
                revs = pickle.load(f)
                
                # Either I'm missing something or the 'reviews' structure
                # is interpreted as as a plain 'review' object if there 
                # is just one review, and as an array otherwise.
                # So let's make ourselves an array in all cases.                
                rev_lst = revs['review']
                if 'book' in rev_lst:
                    rev_lst = [rev_lst]
                    
                    
                for r in rev_lst:
                    try:
                        book = r['book']
                    except TypeError:
                        print r
                        sys.exit(1)
                    id = int(book['id']['#text'].encode('utf-8'))
                    
                    #print >>sys.stderr, "  ", id
                    
                    title = book['title_without_series'].encode('utf-8')
                    publication_year = (book['publication_year'] or '-').encode('utf-8')
                    average_rating = (book['average_rating'] or '-').encode('utf-8')
                    ratings_count = (book['ratings_count'] or '-').encode('utf-8')
                    link = book['link'].encode('utf-8')
                    
                    # same array/object issue as the one above for review
                    aut_lst = book['authors']
                    if 'author' in aut_lst:
                        aut_lst = [aut_lst]

                    author = aut_lst[0]['author']['name'].encode('utf-8')
                    
                    # todo make each entry a struct instead of a tuple
                    lst.append((
                        id, publication_year, average_rating, 
                                ratings_count, title, author, link))
                        
            except EOFError:
                break

freq = {}
bookmap = {}

for e in lst:
    id = e[0]
    if id not in freq:
        freq[id] = 1
    else:
        freq[id] += 1

    bookmap[id] = e

freq_list = [(id,cnt) for id,cnt in freq.iteritems()]

freq_list.sort(key=lambda e: e[1], reverse=True)

for id,cnt in freq_list:
    if cnt < min_reads: continue

    b = bookmap[id]

    if fmt == 'text':
        print "%010d  % 4s  % 4s  % 7s  %s - %s" % (cnt, b[0], b[1], b[2], b[3], b[4], b[5])
    elif fmt == 'html':
        print """
            <tr>
                <td class="reads">%d
                <td class="year">%s
                <td class="ratings">%s
                <td class="average">%s
                <td class="book"><a href="%s">%s - %s</a>
             """ % (cnt, b[1], b[2], b[3], b[6], b[4], b[5])

if fmt == 'html':
    print """
</table>
</body>
</html>
"""
