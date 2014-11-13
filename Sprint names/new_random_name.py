 # -*- coding: utf-8 -*-
__author__ = 'Антон Зайниев'

import urllib2
import pandas
import random
import easygui

# attributes to log on pubs.zvq.me
theurl = 'http://pubs.zvq.me/top_slices/latest/general_top_tracks.csv'
username = 'pubs'
password = 'sei4Iof0Aem0eaH2'

# have no idea how, but it works
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, theurl, username, password)
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

# openings .csv, creating list of artists
top100_table = urllib2.urlopen(theurl)
colnames = ["cnt","track","release","artist_1", "artist_2", "artist_3"]
data = pandas.read_csv(top100_table, names=colnames, skipinitialspace=True)
artists = list(data.artist_1) + list(data.artist_2) + list(data.artist_3)

# clearing names
set_artists = []
for a in data.artist_1:
    b = a.strip('[]"')
    set_artists.append(b)

# clearing duplicates
set_artists = set(set_artists)
set_artists = list(set_artists)

# choosing sprint name
r = random.randint(0,len(set_artists) - 1)
sprint_name = set_artists[r]
sprint_name = sprint_name.strip("'[]")

# checking if it hasn't been used before (sprint_names.csv contains previously used sprint names), creating new one if needed
check_names = ['artist']
data_check = pandas.read_csv("sprint_names.csv", names = check_names)
artists_check = data_check['artist'].values.tolist()
for l in artists_check:
    if str(l) == str(sprint_name):
        r = random.randint(0,len(set_artists))
        sprint_name = set_artists[r]
        sprint_name = sprint_name.strip("'[]")
        continue

# requesting confirmation; if confirmed appending sprint name in sprint_names.csv
choice = False
while choice == False:
    if easygui.ccbox('RNG suggests ' + str(sprint_name), 'Confirm'):
        print ("You chose " + str(sprint_name))
        choice = True
        data_check.loc[len(data_check) + 1] = sprint_name
        data_check.to_csv("sprint_names.csv", header = False)
    else:
        break