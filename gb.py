from __future__ import with_statement
from goodreads import client
from goodreads.request import GoodreadsRequestException
import sys, pickle, os, time, random

import local_config

gc = client.GoodreadsClient(api_key, api_secret)

def delay():
	r = random.randint(5, 12)
	for i in reversed(range(r)):
		sys.stderr.write('\r%d... ' % i)
		sys.stderr.flush()
		time.sleep(1)

	sys.stderr.write('\r...  ')
	sys.stderr.flush()

	time.sleep(random.uniform(0, 1))

	sys.stderr.write('\r      \r')
	sys.stderr.flush()

def query_group():
	with open(group_fn, 'wb') as f:	
		page = 1
		while True:
			print 'page', page
			
			resp = gc.request("/group/members/%d.xml" % group_id, {'sort':'date_joined', 'page':str(page)})			
			delay()
			
			group_users = resp['group_users']
			if 'group_user' not in group_users:
				break
			
			pickle.dump(group_users, f)
			
			page += 1

def load_group():
	print 'loading group'
	
	with open(group_fn, 'rb') as f:
		ret = []
		
		while True:
			try:
				group_users = pickle.load(f)
			except EOFError:
				break
				
			for group_user in group_users['group_user']:
				ret.append(group_user['user']['id']['#text'])
				
		return ret

def query_shelves(user_ids):
	print "querying user shelves"
	
	if not os.path.exists(shelves_dir):
		os.mkdir(shelves_dir)
		
	for user in user_ids:
		print user
		
		dir = shelves_dir + '/' + user
		
		all = dir + "/_all"		
		
		if not os.path.exists(dir):
			os.mkdir(dir)
		
		if os.path.exists(all):
			print "  user already done"
			continue
			
		page = 1
		while True:
			print "  page", page
			
			fn = dir + '/' + str(page)
			
			if os.path.exists(fn):
				print "    page already done"
				continue
				
			try:
				resp = gc.request("/review/list/%s.xml" % user, {'v':'2', 'per_page':'200', 'page':str(page)})
				delay()
			except GoodreadsRequestException as e:
				print '  checking if private'
				resp = gc.request("/user/show/%s.xml" % user, {})
				delay()
				
				if 'private' in resp['user'] and resp['user']['private'] == 'true':
					print '  private'
					
					with open(all, 'wb') as f: pass					
					with open(dir + '/_private', 'wb') as f: pass	
					
					break
					
				print '  review/list failed but user is not private, so throwing'
				raise e
			
			reviews = resp['reviews']
			
			if 'review' not in reviews:
				print '    done, merging pages'
				
				with open(all, 'wb') as f_all:
					for p in xrange(1, page):
						with open(dir + '/' + str(p), 'rb') as f:
							p = pickle.load(f)
							pickle.dump(p, f_all)
						
				break
				
			with open(fn, 'wb') as f:
				pickle.dump(reviews, f)
				
			page += 1
	
### main

if len(sys.argv) >= 2:
	if sys.argv[1] == 'members':
		query_group()
		sys.exit(0)
	else:
		print 'unknown cmd:', sys.argv[1]
		sys.exit(1)

user_ids = load_group()
query_shelves(user_ids)
