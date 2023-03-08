# we need to see full text, so we have to go thru all our saved pages, see if they have any "cut" and if so, put the link into csv file
import csv
import os
import bs4

def main():
    dir = r"D:\projects\LiveJournal\data\html_pages"
    for file in os.scandir(dir):
        name = file.name
        link = r"D:\projects\LiveJournal\data\html_pages" + "\\" + name
        with open(link, encoding='utf-8', newline='') as l:
            soup = bs4.BeautifulSoup(l, "html.parser")
            posts = soup.find_all("article")
            for post in posts:
                cuts = post.find_all("b", class_="ljcut-link lj-widget")
                if not cuts:
                    continue
                else:
                    post_url = post.find("h3", class_="entryunit__title").find("a").get("href")
                    with open ("../data/posts_with_cut.csv", "a", newline="\n") as output:
                        writer = csv.writer(output, delimiter=',')
                        writer.writerow([post_url])

