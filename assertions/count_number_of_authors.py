import csv

authors = set()

with open("../results/posts_in_english.csv") as input:
    reader = csv.reader(input)

    for row in reader:

        date_link = row[0] + ".html"
        author = date_link[0:-16]
        authors.add(author)

print(len(authors)) # 2998