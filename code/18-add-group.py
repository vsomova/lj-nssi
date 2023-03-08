import pandas as pd
import pickle

with open("../data/list_of_cutters.p", "rb") as f:
    list_of_cutters = pickle.load(f)
with open("../data/list_of_friends.p", "rb") as f:
    list_of_friends = pickle.load(f)
with open("../data/list_of_fofs.p", "rb") as f:
    list_of_fofs = pickle.load(f)

def get_group(username):
    if username in list_of_cutters:
        return "Cutters"
    elif username in list_of_friends:
        return "Friends"
    elif username in list_of_fofs:
        return "FoF"
    else:
        return None


df = pd.read_csv(f"../results/lemmas_dataframes_95/sum_df.csv", keep_default_na=False, index_col=0)
df["~~group~~"] = df.index
df["~~group~~"] = df["~~group~~"].apply(get_group)
df = df.reindex(sorted(df.columns), axis=1) #sort by lemma

# prettify
metalemmas = ["~~n_b_strong~~", "~~n_i_em~~", "~~n_strike~~", "~~n_u~~", "~~n_font_size~~", "~~n_imgs~~",
              "~~n_has_title~~", "~~percent_uppercase~~", "~~n_posts~~", "~~n_words~~", "~~group~~"]

df = df[[c for c in df if c not in metalemmas] + [c for c in metalemmas]] #regroup columns, put metalemmas at the end

df.to_csv("../results/users-vs-lemmas.csv")