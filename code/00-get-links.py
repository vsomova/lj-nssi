import datetime
import os
import sys
import bs4
import time
import requests
import re
import csv
is_next_csv = False

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

def parse_year(year, name, has_only_one_year):
    time.sleep(3)
    if has_only_one_year:
        url = f"https://users.livejournal.com/{name}/calendar"
    else:
        url = f"https://users.livejournal.com/{name}/{year}"
    print("parsing "+url)
    soup = get_soup(url)
    cal_raw = soup.find("article", class_="j-e j-e-years")
    if cal_raw == None:
        return []
    months = cal_raw.find_all("div", class_="j-calendar-table-wrapper")
    posts = []
    for month in months:
        dates = month.find_all("a")
        for date in dates:
            posts.append(date["href"])
    return posts


def process_links(input):
    global is_next_csv

    if os.path.exists("../data/posts_links.csv"):
        with open("../data/posts_links.csv", "r") as file:
            data = file.readlines()
        last_link = data[-1]

        s1 = re.search("https://([\w-]+).livejournal.com/\d{4}/\d{2}/\d{2}/", last_link) #for stuff like https://1000-letters.livejournal.com/2010/08/07/
        s2 = re.search("https://users.livejournal.com/([\w-]+)/\d{4}/\d{2}/\d{2}/", last_link) #for stuff like https://users.livejournal.com/-ana-beauty-/2005/03/25/
        if s1:
            last_name = s1.group(1)
        elif s2:
            last_name = s2.group(1)
        else:
            print("regular expression cannot indentify the name within the link")
            sys.exit(-1)

        start = False
    else:
        start = True

    reader = csv.reader(input)

    if start:
        print("start")
    if not start:
        for row in reader:  # iterate until we find where we stopped
            if row[0].replace("_", "-") == last_name:  # found where we stopped
                break
        else:  # not found, seems like we start reading a new file
            if is_next_csv:
                input.seek(0)
                is_next_csv = False
            else:
                return #go to the new file


    for row in reader:
        is_next_csv = False
        name = row[0]
        name = name.replace("_", "-")
        years_we_need = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010"]
        url = f"https://users.livejournal.com/{name}/calendar"
        soup = get_soup(url)
        years_raw = soup.find_all("li", class_="j-nav-item")
        years = []
        posts = []
        for year in years_raw:
            years.append(year.string)
        for year_we_need in years_we_need:

            if year_we_need in years:
                if len(years) == 1:
                    has_only_one_year = True
                else:
                    has_only_one_year = False
                # print("parsing "+ url)
                posts.extend(parse_year(year_we_need, name, has_only_one_year))
            if len(posts) == 0:
                continue  # empty array, go next

        print(posts)
        with open("../data/posts_links.csv", "a", newline="\n") as f:
            writer = csv.writer(f, delimiter=',')
            for post in posts:
                writer.writerow([post])
    if row[0] == last_name:
        is_next_csv = True #we need the beginning of the next csv file
        return

def main():

    with open("../data/list-of-cutters.csv") as input:
        process_links(input)
    with open("../data/list-of-friends.csv") as input:
        process_links(input)
    with open("../data/list-of-fofs.csv") as input:
        process_links(input)


main()

