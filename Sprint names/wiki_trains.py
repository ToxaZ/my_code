__author__ = 'Anton Zayniev'
import wikipedia
import requests
import pandas
import random
from bs4 import BeautifulSoup

#creating globals
sprint_name = ''
choice = False
check_names = ['Train name']
data_check = pandas.read_csv("sprint_names.csv", names = check_names)

# parsing wikipedia category page "Lists_of_named_passenger_trains"
page = wikipedia.page("Lists of named passenger trains")
page_list = page.links

# creating list with urls of pages with named trains
links_list = []
for page in page_list:
    if page[:13] == "List of named":
        ulink = page.replace(" ", "_")
        link = 'http://en.wikipedia.org/wiki/' + ulink
        links_list.append(link)

# creating variables for columns
columns = list(['Train name', 'Railroad', 'Train endpoints', 'Link'])
trains = pandas.DataFrame(columns = columns)

# grabbing tables from page
for each_page in links_list:
    totable = []
    req = requests.get(each_page)
    soup_page = BeautifulSoup(req.text)
    table = soup_page.find_all("table", { "class" : "wikitable" })
    totable.append(table)

# converting tables from html to dataset
for each in totable:
    for wikitable in each:
        for row in wikitable.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 4:
                train_name = cells[0].find(text = True)
                railroad = cells[1].find(text = True)
                train_endpoints = str(cells[2].find_all(text = True))
                link = str(cells[0].find('a', href = True))
                if link[3:7] == 'href':
                    link = link.split('"')[1][6:]
                else:
                    link = 'no link'
                data = {columns[0]:[train_name], columns[1]:[railroad], columns[2]:[train_endpoints], columns[3]:[link]}
                app_train = pandas.DataFrame(data)
                trains = trains.append(app_train)
trains = trains.reset_index(drop = True)

def choose():
    global sprint_name
    '''choosing new sprint name randomly, providing wiki summary'''
    sprint_name = trains.iloc[random.randint(0,len(trains)), 3]
    trains_check = data_check['Train name'].values.tolist()
    # checking if it hasn't been used before (sprint_names.csv contains previously used sprint names),
    for l in trains_check:
        if l == sprint_name:
            # creating new one if needed
            sprint_name = trains.iloc[random.randint(0,len(trains)), 3]
            continue

    # providing wiki summary (if any)
    print (sprint_name)
    print (trains.iloc[random.randint(0,len(trains)), 1])
    try:
        sprint_descr = wikipedia.page(sprint_name)
        print (sprint_descr.summary)
    except:
        print "no description"


# asking if sprint name is good enough
choose()
while choice == False:
    respond = raw_input('Are we happy? ')
    if str(respond) == 'yes':
        # if sprint name confirmed, appending it in sprint_names.csv
        data_check.loc[len(data_check) + 1] = sprint_name
        data_check.to_csv("sprint_names.csv", header = False)
        choice = True
    elif str(respond) == 'cancel':
        break
    else:
        choose()