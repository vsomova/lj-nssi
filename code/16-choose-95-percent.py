import os
import pickle
import pandas as pd

chosen_words = list(pickle.load(open("../results/95_percent_words.p", "rb")))

dir = "D:\projects\LiveJournal\\results\lemmas_dataframes"
for file in os.scandir(dir):
    name = file.name
    df = pd.read_csv(f"../results/lemmas_dataframes/{name}", keep_default_na=False, index_col=0)
    chosen_words_for_this_table = set()
    chosen_words_for_this_table.update(["~~n_b_strong~~", "~~n_font_size~~", "~~n_has_title~~",
                                        "~~n_i_em~~", "~~n_imgs~~", "~~n_posts~~", "~~n_strike~~", "~~n_u~~",
                                        "~~n_words~~", "~~percent_uppercase~~"])
    for word in chosen_words:
        if word in df.index:
            chosen_words_for_this_table.add(word)
    df = df.loc[chosen_words_for_this_table]
    df.to_csv(f"../results/lemmas_dataframes_95/{name}")
