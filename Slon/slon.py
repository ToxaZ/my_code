#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ToxaZ'

import urllib2
import bs4
import pandas as pd

#creating table
headers = ['name','link','date']
new_articles_table = pd.DataFrame(columns=headers)

# attributes to log on pubs.zvq.me
theurl = 'http://slon.ru/insights/'
username = 'uname'
password = 'pass'

# creating authorisation opener
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, theurl, username, password)
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0')]
urllib2.install_opener(opener)

# parsing main page
main_page = urllib2.urlopen(theurl)
the_page = main_page.read()
soup = bs4.BeautifulSoup(the_page)
main = soup.find("div", {"class": "rubric-posts"})

# parsing page for values
search_dict = {headers[0]:'title', headers[1]:'href', headers[2]:'datetime'}
for key, value in search_dict.items():
    row_n = 0
    for each in main.find_all():
        if each.get(value) is not None:
            # print each.get(value), n
            new_articles_table.loc[row_n, key] = each.get(value)
            row_n += 1

# searching for new articles and downloading them
old_articles_table = pd.read_csv('old_articles.csv', encoding='utf8')
to_send = list(set(new_articles_table['link']) - set(old_articles_table['link']))

# saving new dataframe
new_articles_table.to_csv('old_articles.csv', index = False, encoding='utf8')

