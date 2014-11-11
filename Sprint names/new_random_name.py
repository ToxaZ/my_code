 # -*- coding: utf-8 -*-
__author__ = 'Антон Зайниев'

import urllib2
import pandas
import random
import easygui


theurl = 'http://pubs.zvq.me/top_slices/latest/general_top_tracks.csv'
username = 'pubs'
password = 'sei4Iof0Aem0eaH2'


passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
# this creates a password manager
passman.add_password(None, theurl, username, password)
# because we have put None at the start it will always
# use this username/password combination for  urls
# for which `theurl` is a super-url

authhandler = urllib2.HTTPBasicAuthHandler(passman)
# create the AuthHandler

opener = urllib2.build_opener(authhandler)

urllib2.install_opener(opener)
# All calls to urllib2.urlopen will now use our handler
# Make sure not to include the protocol in with the URL, or
# HTTPPasswordMgrWithDefaultRealm will be very confused.
# You must (of course) use it when fetching the page though.

top100_table = urllib2.urlopen(theurl)
# authentication is now handled automatically for us

colnames = ["cnt","track","release","artist_1", "artist_2", "artist_3"]
data = pandas.read_csv(top100_table, names=colnames, quotechar='"', delimiter=',', skipinitialspace=True, encoding='utf-8')
artists = list(data.artist_1)
dec_artists = []
for i in artists:
    j = i.encode('utf-8')
    dec_artists.append(j)
set_artists = set(artists)

choice = False
artists_check = open('sprint_names.txt', 'r')
for l in artists_check:
    if l == sprint_name:
        sprint_name = str(random.sample(set_artists, 1))
        continue
    while choice == False:
        if easygui.ccbox('RNG suggests ' + str(sprint_name), 'Confirm'):
            artists_check = open('sprint_names.txt', 'a')
            artists_check.write(str(sprint_name) + ', ')
            print "You chose " + (u''.join(sprint_name))
            choice = True
        else:
            break