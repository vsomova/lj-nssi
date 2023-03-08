# normalize the table by frequency

import pandas as pd

df = pd.read_csv(f"../results/users-vs-lemmas.csv", keep_default_na=False, index_col=0)

# divide "~~n_b_strong~~", "~~n_i_em~~", "~~n_strike~~", "~~n_u~~", "~~n_font_size~~", "~~n_imgs~~" by number of words to normalize
df.iloc[:, :-5] = df.iloc[:, :-5].div(df["~~n_words~~"], axis=0) #divide all except the last 2 columns by corresponding n_words

# divide "~~n_has_title~~" by number of posts to normalize
df["~~n_has_title~~"] = df["~~n_has_title~~"].div(df["~~n_posts~~"], axis=0)

# introduce a new column: inverse average post length (total number of posts divided by total number of words)
df["~~inv_avg_post_len~~"] = df["~~n_posts~~"].div(df["~~n_words~~"], axis=0)

# normalize "~~percent_uppercase~~" to be the float number.
df["~~percent_uppercase~~"] = df["~~percent_uppercase~~"] / 100

# put group column at the end
g = df.pop("~~group~~") #extract the group column
df = pd.concat([df, g], 1) # concatenate so that "group" column is at the end

df.to_csv("../results/lemmas_normalized/norm_by_freq.csv")