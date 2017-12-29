from __future__ import with_statement
import sys, pickle, os

if len(sys.argv) < 2:
	print "need shelves_dir argument"
	sys.exit(1)

shelves_dir = sys.argv[1]

for user in os.listdir(shelves_dir):
	if user in ['.', '..']: continue
	
	all = '%s/%s/_all' % (shelves_dir, user)
	
	if not os.path.exists(all): continue
	if os.stat(all).st_size == 0: continue
	
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
					
					# same array/object issue as the one above for review
					aut_lst = book['authors']
					if 'author' in aut_lst:
						aut_lst = [aut_lst]

					author = aut_lst[0]['author']['name'].encode('utf-8')
					
					print "%010d\t% 4s\t% 4s\t% 7s   %s - %s" % (id, publication_year, average_rating, 
							ratings_count, title, author)
			except EOFError:
				break
