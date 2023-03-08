#analyze html files (downloaded pages) that we have and create json files with summarized information

import datetime
import json
import os
import sys
import time
import bs4
import requests

def get_soup(url):
    try:
        jar = requests.cookies.RequestsCookieJar()
        jar.set(domain='.livejournal.com', name='prop_opt_readability', path='/', secure=True, value='1')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        connection = requests.get(url, headers=headers, cookies=jar)
        soup = bs4.BeautifulSoup(connection.text, "html.parser")
        return soup
    except Exception as e:
        print(e)
        print(datetime.datetime.now())
        time.sleep(60*5)
        try:
            jar = requests.cookies.RequestsCookieJar()
            jar.set(domain='.livejournal.com', name='prop_opt_readability', path='/', secure=True, value='1')
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            connection = requests.get(url, headers=headers, cookies=jar)
            soup = bs4.BeautifulSoup(connection.text, "html.parser")
            return soup
        except Exception as e:
            print(e)
            sys.exit()


def get_question_info(all_text, question):
    question_url = question.find("div", class_="flatquestionjournal-question-title").find("a").get("href")
    question_text = question.find("div", class_="flatquestionjournal-question-text")
    question_text = question_text.text
    question.extract()
    answer_text = all_text
    text = answer_text
    # print(question_text)
    return question_url, question_text, text

def get_repost_info(all_text):
    if "Originally posted" in all_text.text:  # if we have that phrase in generlal, we may have a repost, lets check
        main_text = all_text.find("div")  # gotta get rid of the main text of the post, find it first
        if main_text != None:
            main_text.extract()
            if "Originally posted by" in all_text.text:  # now we check if this phrase is actually in the beginning before the main text
                a_array = all_text.find_all("a")  # now we got a bunch of 'a' tags, gotta find among them the link to the original post
                if len(a_array) == 3: #if everything is structured as should be
                    is_repost = True
                    a = a_array[2] #searhing for the link to the original post...
                    original_post_link = a.get("href")  # got the link to the original post!
                    text = main_text  # text of the post
                    return is_repost, original_post_link, text
    return False, "", ""


def main():

    dir = "D:\projects\LiveJournal\data\html_pages"

    for file in os.scandir(dir):

        filename = file.name

        link = "D:\projects\LiveJournal\data\html_pages" + "\\" + filename
        with open(link, encoding='utf-8', newline='') as l:
            s = bs4.BeautifulSoup(l, "html.parser")

            author = filename[0:-16]
            date = filename[-15:-5]

            posts = s.find_all("article") #get all the posts from that date (page)
            list = []

            json_filename = filename[:-5] + ".json"
            if os.path.exists(r"../results/json_files/"+json_filename):
                continue #go to the next link

            for post in posts:
                try:
                    title = post.find("h3", class_="entryunit__title").find("a").text
                except Exception as e:
                    print(e)
                    print(link)
                    print(post)
                    continue
                # print(title)

                t = post.find("time").find("span", class_="date-entryunit__time").text #time of the post
                dt = datetime.datetime.strptime(t + " " + date, "%I:%M %p %Y-%m-%d")
                # print(dt)

                s_tags = post.find_all("a", rel="tag") #soup of tags
                tags = [] #array of tags
                for tag in s_tags:
                    tags.append(tag.text)
                # print(tags)

                # number of comments
                s_comments = post.find("li", class_="actions-entryunit__item actions-entryunit__item--comments")
                if s_comments == None:
                    n_comments = 0
                else:
                    s_n_comments = s_comments.find("span", class_="actions-entryunit__text")
                    if s_n_comments != None:
                        n_comments = s_n_comments.text
                    else:  # doesnt have a number t all (hidden button)
                        n_comments = 0
                # print(n_comments)

                up = post.find("div", class_="entryunit__userpic")
                if up != None: # if has a userpic
                    userpic = up.find("img").get("src")
                else:
                    userpic = None

                # does the post contain: repost, answer for question, embed post?
                is_repost = False
                is_answer = False
                has_cuts = False
                is_usual = False

                all_text = post.find("div", class_="entryunit__text")


                # if post is a repost
                is_repost, original_post_link, repost_text = get_repost_info(all_text)
                if is_repost:
                    text = repost_text
                else: #we dont even need all that variables, theyre only for reposts
                    del repost_text
                    del original_post_link


                # if post is an answer
                question = all_text.find("div", class_="flatquestionjournal")
                if question!=None:
                    is_answer = True
                    question_url, question_text, text = get_question_info(all_text, question)


                # if we have, for example, cut & question at the same time, the code next will just overwrite
                # the 'text' variable, but for now with the full text of the post (including whats under cut)

                # if has some text under "cut"
                cuts = post.find_all("b", class_="ljcut-link lj-widget")
                if cuts:
                    post_url = post.find("h3", class_="entryunit__title").find("a").get("href")  # url to the post itself with full text
                    post_url = post_url[8:].replace("/", "#")  # thats how we named our files
                    link = "../data/html_pages_of_posts_with_cut/" + post_url
                    with open(link, encoding='utf-8', newline='') as l:  # open the file w the full post
                        post_soup = bs4.BeautifulSoup(l, "html.parser")
                        a = post_soup.find_all("article", class_="b-singlepost-body entry-content e-content")
                        if len(a) == 1:
                            text = a[0]
                            has_cuts = True

                            if is_repost:
                                _, original_post_link, _ = get_repost_info(all_text)

                            if is_answer:
                                question_url, question_text, _ = get_question_info(all_text, question)


                if not has_cuts and not is_answer and not is_repost:
                    is_usual = True
                    text = all_text

                # now work with the text
                for br in text.find_all("br"):  # dont forget the new lines in the text!
                    br.replace_with("\n")
                text = text.get_text()
                text = text.strip()

                #now create a dictionary with all the data

                dict = {"Author": author, "Title": title, "Time": str(dt), "Tags": tags, "Number of comments": n_comments,
                        "Userpic": userpic, "Is repost": is_repost, "Is answer": is_answer}

                # print(author)
                # print(title)
                # print(dt)
                # print(tags)
                # print(n_comments)
                # print(userpic)

                if is_repost:
                    dict["Original post URL"] = original_post_link
                    # print("repost")
                    # print(original_post_link)

                if is_answer:
                    dict["Question URL"] = question_url
                    dict["Question text"] = question_text

                dict["Text"] = text

                    # print("answer")
                    # print(question_url)
                    # print(question_text)

                list.append(dict)


            # json_filename = filename[:-5] + ".json"
            with open(f"../results/json_files/{json_filename}", "w") as output:
                json.dump(list, output)


main()