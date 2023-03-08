# normalize the table using the median: use binary mode for whether a lemma is above the median (true) or not (below or equal to) (false)

import pandas as pd

df = pd.read_csv(f"../results/users-vs-lemmas.csv", keep_default_na=False, index_col=0)

num = df.iloc[:, :-1] #exclude group from the operation

num = (num>num.median()).astype(int) #find the median for each lemma, assign 1 if author uses the lemma the amount of times  higher than median for that lemma, 0 for equal or lower than median

df = num.join(df.iloc[:, -1:]) # add group, n_posts and n_words back

df.to_csv("../results/lemmas_normalized/norm_by_med.csv")