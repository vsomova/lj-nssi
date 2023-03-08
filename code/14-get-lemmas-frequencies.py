import os
import pandas as pd

all_series_sum = pd.Series(dtype="int64")

dir = "D:\projects\LiveJournal\\results\lemmas_dataframes"
for file in os.scandir(dir):
    name = file.name
    df = pd.read_csv(dir + "\\" + name, index_col="Unnamed: 0", keep_default_na=False)
    df = df.drop(["~~n_b_strong~~", "~~n_font_size~~", "~~n_has_title~~", "~~n_i_em~~", "~~n_imgs~~", "~~n_posts~~",
                  "~~n_strike~~", "~~n_u~~", "~~n_words~~", "~~percent_uppercase~~"]) #we dont count metalemmas for this task
    sum_df = df.sum(axis=1) #series: how much is each lemma used in this file
    all_series_sum = all_series_sum.add(sum_df, fill_value=0) #cumulative of lemmas usage amount


all_series_sum = all_series_sum.astype(int)
print(all_series_sum)
all_series_sum.to_csv("../results/lemmas_frequencies.csv", header=False)

