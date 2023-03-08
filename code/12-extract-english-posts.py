#create a table: 1st column - link to the file, second column - which posts in that date are in english
import csv
import json
import os

dir = "D:\projects\LiveJournal\\results\json_files"

with open("../results/posts_in_english.csv", "w", newline="\n") as f:
    writer = csv.writer(f, delimiter=",")

    for file in os.scandir(dir):

        link = "D:\projects\LiveJournal\\results\json_files" + "\\" + file.name
        with open(link, encoding='utf-8', newline='') as f:
            iterator_number_of_post = 0
            numbers_of_english_posts = "" #string of numbers of english posts (representing the order)
            date = json.load(f)
            filename = file.name[:-5]
            for post in date:
                if "Language" in post:
                    numbers_of_english_posts += str(iterator_number_of_post) + " "

                iterator_number_of_post += 1

            numbers_of_english_posts = numbers_of_english_posts.strip()

            if numbers_of_english_posts != "":
                writer.writerow([filename, numbers_of_english_posts])