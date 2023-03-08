import pandas as pd
import numpy as np
import csv
import re

S_links = pd.read_csv("../results/type_S_links.csv", header=None)
S_links.columns = ["Links"]
S_links["Username"] = S_links["Links"].apply(lambda s: re.findall("https:\/\/(.*)\.livejournal\.com", s)[0]) # add "username" column

# create an array with each person's posts
prev = ""
with open("../results/type_S_links_sample.csv", "w", newline="\n") as f:
    writer = csv.writer(f, delimiter=',')

    for index, row in S_links.iterrows():
        if prev!=row["Username"]: #if new user
            mask = S_links["Username"] == row["Username"]
            persons_posts = S_links[mask]["Links"].to_numpy() #numpy array w current person's posts
            persons_posts_copy = np.copy(persons_posts)
            prev = row["Username"]

            random_array = np.random.binomial(1, 0.025, len(persons_posts)).astype(bool) # create a mask, we need 2.5% of all

            persons_posts = persons_posts[random_array]
            if len(persons_posts)==0:
                persons_posts = np.copy(persons_posts_copy)
                mask = np.random.choice(len(persons_posts), 1)
                persons_posts = persons_posts[mask]

            for link in persons_posts:
                writer.writerow([link])