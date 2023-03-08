import csv

def put_s():
    with open("../results/type_S_links_sample.csv") as input:
        reader = csv.reader(input)
        with open("../results/F_and_Ssample_links.csv", "a", newline="\n") as f:
            writer = csv.writer(f, delimiter=',')
            for row in reader:
                writer.writerow(row)

def put_f():
    with open("../results/type_F_links.csv") as input:
        reader = csv.reader(input)
        with open("../results/F_and_Ssample_links.csv", "a", newline="\n") as f:
            writer = csv.writer(f, delimiter=',')
            for row in reader:
                writer.writerow(row)

put_s()
put_f()