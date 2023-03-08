# ABANDONED

import csv

list_of_cutters = set()
list_of_friends = set()
list_of_fofs = set()


# with open("D:\projects\LiveJournal\data\list-of-cutters.csv") as input:
#     reader = csv.reader(input)
#     for row in reader:
#         list_of_cutters.add(row[0].replace("_", "-"))
#
# with open("D:\projects\LiveJournal\data\list-of-friends.csv") as input:
#     reader = csv.reader(input)
#     for row in reader:
#         list_of_friends.add(row[0].replace("_", "-"))
#
# with open("D:\projects\LiveJournal\data\list-of-fofs.csv") as input:
#     reader = csv.reader(input)
#     for row in reader:
#         list_of_fofs.add(row[0].replace("_", "-"))


with open("../data/posts_links.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)