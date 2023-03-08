import csv
import json
import os
import string
import sys
import time
import bs4
from nltk.corpus import words
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import pos_tag
from collections import Counter

import pandas as pd
lem = WordNetLemmatizer()
punctuation_marks = set(string.punctuation)


def post_is_a_repost(json_post):
    return json_post["Is repost"]


def find_json(date_link):
    date_link = date_link[:-4] + "json"
    link = "D:\projects\LiveJournal\\results\json_files" + "\\" + date_link
    with open(link, encoding='utf-8', newline='') as f:
        data = json.load(f)
        return data


def soup_get_posts(l):
    s = bs4.BeautifulSoup(l, "html.parser")
    posts = s.find_all("article")  # get all the posts from that date (page)
    return posts


def analyze_text(text):

    tokenized_words = wordpunct_tokenize(text)
    n_words = len(tokenized_words)

    pos_translate = {"J": "a", "V": "v", "N": "n", "R": "r"}
    def pos2pos(tag):
        if tag in pos_translate:
            return pos_translate[tag]
        else:
            return "n"
    lemmatized_words = [lem.lemmatize(w, pos2pos(pos[0])).lower() for w, pos in pos_tag(tokenized_words)]
    cntr = Counter(lemmatized_words)
    ps = pd.Series(cntr)

    # uppercase stuff
    listed_text = list(text)
    uppercase_letters = [letter for letter in listed_text if letter.isupper()]
    n_uppercase = len(uppercase_letters)
    percent_uppercase = n_uppercase / len(listed_text) * 100 #percent of uppercase letters

    return ps, percent_uppercase, n_words


def analyze_fonts(post_soup):
    fonts = post_soup.find_all("font")
    colors = []
    n_font_size = 0
    if fonts:

        # print(fonts)
        # print(post_soup)
        # print("_________________________")

        for font in fonts:
            if font.has_attr("color") and font["color"] != "" and font["color"][0]=="#":
                colors.append(font["color"])
            if font.has_attr("size"):
                n_font_size += len((font.getText()).split())  # count the number of words within the tag

    cntr = Counter(colors)
    ps = pd.Series(cntr, dtype="int64")

    return ps, n_font_size, len(colors)


def analyze_img(post_soup):
    text = post_soup.find("div", class_="entryunit__text")
    imgs = text.find_all("img")

    return len(imgs)


def analyze_b_strong(post_soup):
    b_tags = post_soup.find_all("b")
    strong_tags = post_soup.find_all("strong")
    n_b = 0
    n_s = 0

    if b_tags:
        for b in b_tags:
            n_b += len((b.getText()).split()) #count the number of words within the tag
    if strong_tags:
        for s in strong_tags:
            n_s += len((s.getText()).split()) #count the number of words within the tag

    n_b_strong = n_b + n_s
    return n_b_strong


def analyze_i_em(post_soup):
    i_tags = post_soup.find_all("i")
    em_tags = post_soup.find_all("em")

    n_i = 0
    n_e = 0

    if i_tags:
        for i in i_tags:
            n_i += len((i.getText()).split())  # count the number of words within the tag
    if em_tags:
        for e in em_tags:
            n_e += len((e.getText()).split())  # count the number of words within the tag

    n_i_em = n_i + n_e
    return n_i_em


def analyze_u(post_soup):
    u_tags = post_soup.find_all("u")
    n_u = 0
    if u_tags:
        for u in u_tags:
            n_u += len((u.getText()).split()) #count the number of words within the tag
    return n_u


def analyze_strike(post_soup):
    strike_tags = post_soup.find_all("strike")
    n_s = 0
    if strike_tags:
        for s in strike_tags:
            n_s += len((s.getText()).split()) #count the number of words within the tag
    return n_s


def get_post_vector(post_soup, json_post):

    author = json_post["Author"]
    text = json_post["Text"]
    n_words = 0

    if json_post["Title"]=="(no subject)":
        has_title = 0
    else:
        has_title = 1
        text = json_post["Title"] + " " + text

    post_vector = pd.Series(dtype = "int64")

    ################################################################################## change
    if text.strip() == "": #if post is empty
        return post_vector #return empty vector
    ##########################################################################################33

    #words and upper-case
    if text.strip() != "": #technically, not necessary, but ill leave it for now in  case ill need to fix smth
        ps_words, percent_uppercase, n_lemmas = analyze_text(text)
        post_vector = pd.concat([post_vector, ps_words])

    # font color and size
    ps_colors, n_font_size, n_colors = analyze_fonts(post_soup)
    post_vector = pd.concat([post_vector, ps_colors])

    # number of images
    n_imgs = analyze_img(post_soup)
    post_vector = pd.concat([post_vector, pd.Series({"~~n_imgs~~":n_imgs})])

    # the presence of a title
    post_vector = pd.concat([post_vector, pd.Series({"~~n_has_title~~": has_title})])

    # the combined number of 'b' and 'strong' tags
    n_b_strong = analyze_b_strong(post_soup)
    post_vector = pd.concat([post_vector, pd.Series({"~~n_b_strong~~": n_b_strong})])

    # the combined number of 'i' and 'em' tags
    n_i_em = analyze_i_em(post_soup)
    post_vector = pd.concat([post_vector, pd.Series({"~~n_i_em~~": n_i_em})])

    # the number of 'u' tags
    n_u = analyze_u(post_soup)
    post_vector = pd.concat([post_vector, pd.Series({"~~n_u~~": n_u})])

    # the number of 'strike' tags
    n_strike = analyze_strike(post_soup)
    post_vector = pd.concat([post_vector, pd.Series({"~~n_strike~~": n_strike})])

    # the number of 'font size' tags
    post_vector = pd.concat([post_vector, pd.Series({"~~n_font_size~~":n_font_size})])

    # the percent of letters in upper-case
    post_vector = pd.concat([post_vector, pd.Series({"~~percent_uppercase~~": percent_uppercase})])

    # number of 'words': real words + punctuation + img tags + colors
    n_words += n_lemmas
    n_words += n_imgs
    n_words += n_colors
    post_vector = pd.concat([post_vector, pd.Series({"~~n_words~~": n_words})])

    return post_vector


def write_df_to_csv(df_all):
    df_all = df_all.fillna(0)
    ###########################################################################################################
    #we were adding percentage of uppercase letter for every post, now its time to calculate the average percent of uppercase letters per post by diving by the number of posts
    df_all.loc["~~percent_uppercase~~"] = df_all.loc["~~percent_uppercase~~"] / df_all.loc["~~n_posts~~"]
    ###########################################################################################################
    done = False
    i = 0
    while not done:
        if os.path.exists(f"../results/lemmas_dataframes/{str(i)}.csv"): #iterate thru existing files
            i+=1
        else:
            df_all.to_csv(f"../results/lemmas_dataframes/{str(i)}.csv")
            done = True


def get_last_name_on_csv():
    i = 1  # not a new program; lets start going thru every file to find the last one
    finished = False
    while not finished:
        if os.path.exists(f"../results/lemmas_dataframes/{str(i)}.csv"):
            i += 1
        else:
            finished = True

    i = i - 1  # now 'i' is the name of the last file we created
    df = pd.read_csv(f"../results/lemmas_dataframes/{str(i)}.csv")
    last_name_on_csv = df.columns[-1]
    return last_name_on_csv


def is_new_program():
    if os.path.exists(f"../results/lemmas_dataframes/0.csv"): #not a new program
        return False
    else:
        return True


def find_last_recorded_link(reader, last_name_on_csv):
    last_link = ""
    going_thru_last_author = False
    for row in reader:
        author = row[0][0:-11]
        if author == last_name_on_csv:
            going_thru_last_author = True
            last_link = row[0]
        if going_thru_last_author and author != last_name_on_csv: #we went thru our last author and stumbled upon a new one
            return last_link


def set_reader_to_where_stopped(reader, last_recorded_link):
    for row in reader:
        if row[0]==last_recorded_link:
            return



def main():

    if is_new_program():
        new_program = True
    else:
        new_program = False
        last_name_on_csv = get_last_name_on_csv()

    df_all = pd.DataFrame(dtype = "int64")
    is_the_end = False
    last_author_name = ""

    with open("../results/posts_in_english.csv") as input:
        reader = csv.reader(input)

        if not new_program:
            last_recorded_link = find_last_recorded_link(reader, last_name_on_csv)
            input.seek(0)
            set_reader_to_where_stopped(reader, last_recorded_link)

        for row in reader:

            date_link = row[0] + ".html"
            author = date_link[0:-16]

            # print(date_link)

            chosen_posts = row[1].split() #the array of numbers of posts we need to go thru

            link = "D:\projects\LiveJournal\data\html_pages" + "\\" + date_link
            with open(link, encoding='utf-8', newline='') as l:

                if is_the_end:
                    if last_author_name != author: # we finished the last author and here we see the new one
                        write_df_to_csv(df_all)
                        df_all = pd.DataFrame(dtype="int64") #create a new table
                        is_the_end = False
                        last_author_name = ""



                post_iterator = 0


                posts = soup_get_posts(l)
                json_date = find_json(date_link)

                date_vector = pd.Series(dtype = "int64")


                for post in posts:
                    if str(post_iterator) in chosen_posts: #go thru only chosen posts (the ones in english)
                        # print(date_link)
                        json_post = json_date[post_iterator]
                        if not post_is_a_repost(json_post): #we dont consider reposts
                            post_vector = get_post_vector(post, json_post)
                            date_vector = date_vector.add(post_vector, fill_value=0)
                            # print(date_vector)

                    post_iterator+=1

                # # number of posts
                date_vector = pd.concat([date_vector, pd.Series({"~~n_posts~~": len(posts)})])

                # turn it to dataframe
                date_df = date_vector.to_frame(name=author)

                # now add date vector to the author's vector
                df_all = df_all.add(date_df, fill_value=0)


                # print(df_all.sort_index())
                # print("______________________________________________________________________________")
                # print(author)


                if (len(df_all.columns)) == 100:
                    is_the_end = True
                    last_author_name = author


#     we finished the file
    write_df_to_csv(df_all)
    print("program finished")



main()