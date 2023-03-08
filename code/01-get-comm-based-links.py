import csv
with open("../results/links-community-based-users.csv", "w", newline="\n") as f: #change later
    with open("../data/community-based-users.csv") as subset:
            sub_reader = csv.reader(subset)

            next(sub_reader)
            for sub_row in sub_reader:
                name = sub_row[0].replace("_", "-") # replacing "_" to "-" since their links work that way
                # url1 is for links like https://1000-letters.livejournal.com/
                # url2 is for links like https://users.livejournal.com/-ana-beauty-/
                url1 = "https://" + name + ".livejournal.com"
                url2 = "https://users.livejournal.com/" + name
                with open("../data/posts_links.csv") as set:
                    set_reader = csv.reader(set)
                    for set_row in set_reader:
                        if url1 in set_row[0]:
                            writer = csv.writer(f, delimiter=',')
                            writer.writerow(set_row)
                        elif url2 in set_row[0]:
                            writer = csv.writer(f, delimiter=',')
                            writer.writerow(set_row)