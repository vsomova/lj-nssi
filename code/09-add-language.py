import json
import os
import string
from nltk.corpus import words
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from nltk import pos_tag
lem = WordNetLemmatizer()
set_of_english_words = set(words.words("en"))
punctuation_marks = list(string.punctuation)


dir = r"D:\projects\LiveJournal\results\json_files"

for file in os.scandir(dir):

    link = "D:\projects\LiveJournal\\results\json_files" + "\\" + file.name
    with open(link, encoding='utf-8', newline='') as f:
        new_list = []
        date = json.load(f)
        for post in date:
            text = post["Text"]

            pos_translate = {"J": "a", "V": "v", "N": "n", "R": "r"}
            tokenized_words = word_tokenize(text)
            def pos2pos(tag):
                if tag in pos_translate: return pos_translate[tag]
                else: return "n"
            lemmatized_words = [lem.lemmatize(w, pos2pos(pos[0])).lower() for w, pos in pos_tag(tokenized_words) if all(word not in w for word in punctuation_marks)] # w not in punctuation_marks

            number_of_english_words = 0
            for word in lemmatized_words:
                if word in set_of_english_words:
                    number_of_english_words +=1
            if lemmatized_words: #make sure length is not equal to 0
                div = number_of_english_words/len(lemmatized_words)
            else:
                div = 0
            if div>=0.5: #the post is in english language
                post["Language"] = "English"

            new_list.append(post)


        with open(f"{link}", "w") as output:
            json.dump(new_list, output)