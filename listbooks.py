#!/usr/bin/env python

from __future__ import with_statement
from goodreads import client
from goodreads.request import GoodreadsRequestException
import sys, pickle, os, time, random

try:
    import config as cfg
except ImportError:
    print 'first, copy local_config-example.py to local_config.py and edit it'
    sys.exit(1)

per_page = 200

gc = client.GoodreadsClient(cfg.api_key, cfg.api_secret)

def delay(secs=11):
    r = random.randint(secs, secs+8)
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
    with open(cfg.group_fn, 'wb') as f:    
        page = 1
        while True:
            print 'page', page
            
            resp = gc.request("/group/members/%d.xml" % cfg.group_id, {'sort':'date_joined', 'page':str(page)})            
            delay()
            
            group_users = resp['group_users']
            if 'group_user' not in group_users:
                break
            
            pickle.dump(group_users, f)
            
            page += 1

def load_group():
    print 'loading group'
    
    with open(cfg.group_fn, 'rb') as f:
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
    
    if not os.path.exists(cfg.shelves_dir):
        os.mkdir(cfg.shelves_dir)
        
    for user in user_ids:
        print user
        
        dir = cfg.shelves_dir + '/' + user
        
        all = dir + "/_all"        
        
        if not os.path.exists(dir):
            os.mkdir(dir)
        
        if os.path.exists(all):
            print "  user already done"
            continue
            
        page = 1
        pages = 0

        while True:
            if page > 1 and page > pages:
                break

            print "  page", page
            
            fn = dir + '/' + str(page)
            
            if os.path.exists(fn):
                print "    page already done"
                page += 1
                continue
                
            try:
                resp = gc.request("/review/list/%s.xml" % user, {'v':'2', 'per_page':str(per_page), 'page':str(page)})
                delay()
            except GoodreadsRequestException as e:
                delay()

                if page > 1:
                    print '  error not on first page, skipping'

                    open(all, 'wb').close()
                    open(dir + '/_page_err', 'wb').close()
                    delay(100)
                    break

                print '  checking if private'

                try:
                    resp = gc.request("/user/show/%s.xml" % user, {})
                    delay()
                except GoodreadsRequestException:
                    open(all, 'wb').close()
                    open(dir + '/_private_err', 'wb').close()
                    delay(100)
                    break
                
                if 'private' in resp['user'] and resp['user']['private'] == 'true':
                    print '  private'
                    
                    open(all, 'wb').close()
                    open(dir + '/_private', 'wb').close()
                    
                    break
                    
                print '  review/list failed but user is not private, skipping'

                open(all, 'wb').close()
                open(dir + '/_first_err', 'wb').close()
                delay(950)
                break
            
            reviews = resp['reviews']

            if page==1 and '@total' in reviews:
                total = int(reviews['@total'])
                pages = (total+per_page-1)/per_page
                print '    reviews:', total, 'pages:', pages
            
            if 'review' not in reviews:
                if pages > 0:
                    raise Exception('empty review list')
            else:
                with open(fn, 'wb') as f:
                    pickle.dump(reviews, f)
 
            if page >= pages:
                print '    done, merging pages'
                
                with open(all, 'wb') as f_all:
                    for p in xrange(1, pages+1):
                        with open(dir + '/' + str(p), 'rb') as f:
                            p = pickle.load(f)
                            pickle.dump(p, f_all)
                        
                break
                
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
print "loaded %d users" % len(user_ids)

query_shelves(user_ids)
