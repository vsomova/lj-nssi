import pandas as pd
import numpy as np
import csv
import re

def get_csv(type):
    df = pd.read_csv("../data/community-based-users.csv")
    # get all posts for ppl w type S and F
    mask = df["type"] == type
    type_arr = df[mask]["username"].to_numpy() #array of ppl w F/S type

    all_posts = pd.read_csv("../results/links-community-based-users.csv", header=None)
    all_posts = all_posts.to_numpy().squeeze() #array of all posts

    # make sure we have each name being separated (names within names not allowed), we have 2 types of links
    matchers = "https://" + type_arr + ".livejournal.com" # for links like https://1000-letters.livejournal.com

    # here, i would do a separate matcher for links like https://users.livejournal.com/-ana-beauty-/, but after we filtered the links, we do not have links of that type anymore

    # looking for each name in all posts
    matching = (s for s in all_posts if any(xs in s for xs in matchers)) #generator w chosen posts; go thru matchers and and extract the urls of their posts

    with open(f"../results/type_{type}_links.csv", "w", newline="\n") as f:
        writer = csv.writer(f, delimiter=',')
        for link in matching:
            writer.writerow([link])

def main():
    get_csv("S")
    get_csv("F")

main()