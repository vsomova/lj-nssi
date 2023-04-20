import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2

def show_best_features(df, N_features):
    df = df.drop(columns=["~~n_posts~~", "~~n_words~~"])  # remove these columns

    X = df.drop(columns=["~~group~~"])  # everything except the target value
    y = df["~~group~~"]  # target value

    sel = SelectKBest(chi2, k=N_features)  # chi2 for classification
    f = sel.fit(X, y) # run the score function on our data
    fitscores = pd.DataFrame(f.scores_)  # get the scores
    cols = pd.DataFrame(X.columns)
    result = pd.concat([cols, fitscores], axis=1)  # get names of the columns
    result.columns = ["Feature", "Score"]  # give names to result's columns
    res = str(result.nlargest(N_features, 'Score'))  # show the features with the highest scores and their scores
    return res

def main():
    report = ""
    N_features = 25 # the number of best features to show

    df = pd.read_csv(f"../results/lemmas_normalized/norm_by_freq.csv", keep_default_na=False, index_col=0)

    report += "Best features for lemmas normalized by frequency:\n"
    report += show_best_features(df, N_features)

    df = pd.read_csv(f"../results/lemmas_normalized/norm_by_pres.csv", keep_default_na=False, index_col=0)
    report += "\n\nBest features for lemmas normalized by presence:\n"
    report += show_best_features(df, N_features)

    df = pd.read_csv(f"../results/lemmas_normalized/norm_by_med.csv", keep_default_na=False, index_col=0)
    report += "\n\nBest features for lemmas normalized by median:\n"
    report += show_best_features(df, N_features)

    with open(f"../results/best_features.txt", "w") as f:
        f.write(report)

main()