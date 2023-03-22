import os
import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2

nd = "../results/after_feat_sel" # new directory
if not os.path.exists(nd):
    os.makedirs(nd)

N_features = 1000 # number of desired features

df = pd.read_csv(f"../results/lemmas_normalized/norm_by_freq.csv", keep_default_na=False, index_col=0)

df = df.drop(columns=["~~n_posts~~", "~~n_words~~"])  # remove these columns

X = df.drop(columns=["~~group~~"])  # everything except the target value
y = df["~~group~~"]  # target value

sel = SelectKBest(chi2, k=N_features)  # chi2 for classification
sel.fit(X, y)
mask = sel.get_support()
chosen_features = X.columns[mask]
new_df = df[chosen_features] # new df with chosen features