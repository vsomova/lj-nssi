import os
import sys
import time
import requests
import csv

def get_file_name(url):
    file_name = url[8:].replace("/", "#") #everything after 'https://'
    return file_name

def write_html(url):
    try:
        time.sleep(2)
        jar = requests.cookies.RequestsCookieJar()
        jar.set(domain='.livejournal.com', name='prop_opt_readability', path='/', secure=True, value='1')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        connection = requests.get(url, headers=headers, cookies=jar)
        file = get_file_name(url)
        with open(f"../data/html_pages_of_posts_with_cut/{file}", "w", encoding='utf-8') as f:
            f.write(connection.text)

    except Exception as e:
        print(e)
        print()
        time.sleep(60*5)
        try:
            jar = requests.cookies.RequestsCookieJar()
            jar.set(domain='.livejournal.com', name='prop_opt_readability', path='/', secure=True, value='1')
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            connection = requests.get(url, headers=headers, cookies=jar)
            file = get_file_name(url)
            with open(f"../data/html_pages_of_posts_with_cut/{file}", "w", encoding='utf-8') as f:
                f.write(connection.text)

        except Exception as e:
            print(e)
            sys.exit()

def main():
    with open("../data/posts_with_cut.csv") as input:
        reader = csv.reader(input)
        for row in reader:  # iterate until we find where we stopped
            url = row[0]
            if os.path.exists("../data/html_pages_of_posts_with_cut/"+get_file_name(url)):
                # start = False #we are not starting to go thru links, some files already exist
                continue #go to the next link
            else:
                print("accessing " + url)
                write_html(url)

main()