import csv
import pickle

i=0

list_of_cutters = set()
list_of_friends = set()
list_of_fofs = set()


with open("D:\projects\LiveJournal\data\list-of-cutters.csv") as input:
    reader = csv.reader(input)
    for row in reader:
        list_of_cutters.add(row[0].replace("_", "-"))

with open("D:\projects\LiveJournal\data\list-of-friends.csv") as input:
    reader = csv.reader(input)
    for row in reader:
        list_of_friends.add(row[0].replace("_", "-"))

with open("D:\projects\LiveJournal\data\list-of-fofs.csv") as input:
    reader = csv.reader(input)
    for row in reader:
        list_of_fofs.add(row[0].replace("_", "-"))

pickle.dump(list_of_cutters, open("../data/list_of_cutters.p", "wb"))
pickle.dump(list_of_friends, open("../data/list_of_friends.p", "wb"))
pickle.dump(list_of_fofs, open("../data/list_of_fofs.p", "wb"))