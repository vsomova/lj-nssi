# we chose 95 percent, now merge the small dataframes
import os
import pandas as pd
sum_df = pd.DataFrame()

dir = "D:\projects\LiveJournal\\results\lemmas_dataframes_95"
for num in range(len(os.listdir(dir))):
    df = pd.read_csv(f"../results/lemmas_dataframes_95/{num}.csv", keep_default_na=False, index_col=0)
    sum_df = pd.concat([sum_df, df], axis=1)

sum_df = sum_df.fillna(0)
sum_df = sum_df.astype(int)

sum_df = sum_df.T # rotate to have lemmas as columns
sum_df.to_csv("../results/lemmas_dataframes_95/sum_df.csv")



