# now we gotta find number of english posts in each group
import csv
import json
import os
import pickle

with open("../data/list_of_cutters.p", "rb") as f:
    list_of_cutters = pickle.load(f)
with open("../data/list_of_friends.p", "rb") as f:
    list_of_friends = pickle.load(f)
with open("../data/list_of_fofs.p", "rb") as f:
    list_of_fofs = pickle.load(f)

english_list_of_cutters = 0 #number of posts in english in list of cutters
english_list_of_friends = 0
english_list_of_fofs = 0

total_list_of_cutters = 0
total_list_of_friends = 0
total_list_of_fofs = 0

dir = "../results/json_files"

for file in os.scandir(dir):

    link = r"D:\projects\LiveJournal\results\json_files" + "\\" + file.name
    with open(link, encoding='utf-8', newline='') as f:
        date = json.load(f)
        for post in date:
            if post["Author"] in list_of_cutters:
                total_list_of_cutters += 1
                if "Language" in post:  # if english language
                    english_list_of_cutters += 1
            if post["Author"] in list_of_friends:
                total_list_of_friends += 1
                if "Language" in post:  # if english language
                    english_list_of_friends +=1
            if post["Author"] in list_of_fofs:
                total_list_of_fofs += 1
                if "Language" in post:  # if english language
                    english_list_of_fofs +=1

cutters_percentage = english_list_of_cutters/total_list_of_cutters * 100
friends_percentage = english_list_of_friends/total_list_of_friends * 100
fofs_percentage = english_list_of_fofs/total_list_of_fofs * 100

# print((english_list_of_cutters))
# print((english_list_of_friends))
# print((english_list_of_fofs))
# print()
# print(total_list_of_cutters)
# print(total_list_of_friends)
# print(total_list_of_fofs)
# print()
# print(cutters_percentage)
# print(friends_percentage)
# print(fofs_percentage)

with open("../results/english-posts-stats.csv", "w", newline="\n") as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(["number of posts in English within the list of cutters", english_list_of_cutters])
    writer.writerow(["number of posts in English within the list of friends", english_list_of_friends])
    writer.writerow(["number of posts in English within the list of friends", english_list_of_fofs])

    writer.writerow(["number of total posts within the list of cutters", total_list_of_cutters])
    writer.writerow(["number of total posts within the list of friends", total_list_of_friends])
    writer.writerow(["number of total posts within the list of friends", total_list_of_fofs])

    writer.writerow(["percentage of posts in English for cutters", cutters_percentage])
    writer.writerow(["percentage of posts in English for friends", friends_percentage])
    writer.writerow(["percentage of posts in English for friends of friends", fofs_percentage])

