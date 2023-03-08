# now we need three numbers for three categories: authors, posts, words
import os
import pickle
import pandas as pd

with open("../data/list_of_cutters.p", "rb") as f:
    list_of_cutters = pickle.load(f)
with open("../data/list_of_friends.p", "rb") as f:
    list_of_friends = pickle.load(f)
with open("../data/list_of_fofs.p", "rb") as f:
    list_of_fofs = pickle.load(f)

cutters_authors = 0
friends_authors = 0
fofs_authors = 0

cutters_posts = 0
friends_posts = 0
fofs_posts = 0

cutters_words = 0
friends_words = 0
fofs_words = 0

n_authors_overall = 0

i=0

dir = "D:\projects\LifeJournal\lemmas_dataframes"
for file in os.scandir(dir):
    name = file.name
    df = pd.read_csv(dir + "\\" + name, index_col="Unnamed: 0")
    authors = df.columns
    n_authors_overall += len(authors)

    n_of_posts_for_authors = df.loc["~~n_posts~~"]
    n_of_words_for_authors = df.loc["~~n_words~~"]


    for author in authors:

        i+=1

        if author in list_of_cutters:
            cutters_authors +=1
            cutters_posts += n_of_posts_for_authors[author]
            cutters_words += n_of_words_for_authors[author]

        if author in list_of_friends:
            friends_authors +=1
            friends_posts += n_of_posts_for_authors[author]
            friends_words += n_of_words_for_authors[author]

        if author in list_of_fofs:
            fofs_authors +=1
            fofs_posts += n_of_posts_for_authors[author]
            fofs_words += n_of_words_for_authors[author]

print(n_authors_overall)
print()
print("cutters_authors: " + str(cutters_authors))
print("cutters_posts: " + str(cutters_posts))
print("cutters_words: " + str(cutters_words))
print()
print("friends_authors: " + str(friends_authors))
print("friends_posts: " + str(friends_posts))
print("friends_words: " + str(friends_words))
print()
print("fofs_authors: " + str(fofs_authors))
print("fofs_posts: " + str(fofs_posts))
print("fofs_words: " + str(fofs_words))

print("_____________________________________________________")
# print(len(list_of_cutters))
# print(len(list_of_friends))
# print(len(list_of_fofs))
print(str(cutters_authors + friends_authors + fofs_authors))
print(i)
