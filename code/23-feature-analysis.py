import os
import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2

def show_best_features(df, N_features):
    df = df.drop(columns=["~~n_posts~~", "~~n_words~~"])  # remove these columns

    X = df.drop(columns=["~~group~~"])  # everything except the target value
    y = df["~~group~~"]  # target value

    sel = SelectKBest(chi2, k=N_features)  # chi2 for classification
    f = sel.fit(X, y)
    fitscores = pd.DataFrame(f.scores_)  # get the scores
    cols = pd.DataFrame(X.columns)
    result = pd.concat([cols, fitscores], axis=1)  # get names of the columns
    result.columns = ["Feature", "Score"]  # give names to result's columns
    print(result.nlargest(N_features, 'Score'))  # show the features with the highest scores and their scores

def main():
    N_features = 25 # the number of best features to show

    df = pd.read_csv(f"../results/lemmas_normalized/norm_by_freq.csv", keep_default_na=False, index_col=0)

    # ____________________________________________________________________________________________________________________
    # analyze the number of words and posts before we remove them; maybe they affect something?
    # if a person cuts oneself, would they talk on the internet more?
    df2 = df.copy() # copy the original database
    df2 = df2[["~~n_words~~", "~~n_posts~~", "~~group~~"]] # focus on what we need
    df2_gr = df2.groupby(by="~~group~~")[["~~n_posts~~", "~~n_words~~"]].sum() # find the amount of words and posts per group
    df2_gr = df2_gr.T # rotate for easier access
    vc = df["~~group~~"].value_counts() #how many people in each group?
    # divide by the total number of people in a group and get average number of words and posts per person in this group
    df2_gr["Cutters"] = df2_gr["Cutters"]/vc.loc["Cutters"]
    df2_gr["Friends"] = df2_gr["Friends"]/vc.loc["Friends"]
    df2_gr["FoF"] = df2_gr["FoF"]/vc.loc["FoF"]
    print(df2_gr) # take a look at the results
    # the average number of words and posts per person in all groups is relatively the same, with cutters having slightly less amount
    # ____________________________________________________________________________________________________________________

    print("\nBest features for lemmas normalized by frequency:")
    show_best_features(df, N_features)

    df = pd.read_csv(f"../results/lemmas_normalized/norm_by_pres.csv", keep_default_na=False, index_col=0)
    print("\nBest features for lemmas normalized by presence:")
    show_best_features(df, N_features)

    df = pd.read_csv(f"../results/lemmas_normalized/norm_by_med.csv", keep_default_na=False, index_col=0)
    print("\nBest features for lemmas normalized by median:")
    show_best_features(df, N_features)

main()