# normalize the table by presence: use binary mode for whether a lemma is used by the user (true) or not (false)
import pandas as pd

df = pd.read_csv(f"../results/users-vs-lemmas.csv", keep_default_na=False, index_col=0)

num = df.iloc[:, :-3] #exclude group, n_posts and n_words from the operation

num[num > 0] = 1 #assign 1 (true) to lemmas that have been used by author (usage is not 0)

df = num.join(df.iloc[:, -3:]) # add group, n_posts and n_words back

df.to_csv("../results/lemmas_normalized/norm_by_pres.csv")