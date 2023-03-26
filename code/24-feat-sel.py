import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2
import importlib
apply_ML = importlib.import_module("22-apply-ML") # import the file so we can use functions from it

def FS(df, N_features):

    df = df.drop(columns=["~~n_posts~~", "~~n_words~~"])  # remove these columns
    X = df.drop(columns=["~~group~~"])  # everything except the target value
    y = df["~~group~~"]  # target value

    sel = SelectKBest(chi2, k=N_features)  # chi2 for classification
    sel.fit(X, y)
    mask = sel.get_support() # get a mask for chosen features
    chosen_features = X.columns[mask] # mask chosen features
    chosen_cols = list(chosen_features) + ["~~group~~"]
    new_df = df[chosen_cols] # new df with chosen features and the target value

    return new_df


def write_report(N_features, resample):

    report = ""

    df1 = pd.read_csv(f"../results/lemmas_normalized/norm_by_freq.csv", keep_default_na=False, index_col=0)
    new_df1 = FS(df1, N_features) # apply feature selection
    report += apply_ML.eval_norm_freq(new_df1, resample) # get a report for ML for new df

    report += "\n\n"

    df2 = pd.read_csv(f"../results/lemmas_normalized/norm_by_pres.csv", keep_default_na=False, index_col=0)
    new_df2 = FS(df2, N_features) # apply feature selection
    report += apply_ML.eval_norm_pres(new_df2, resample)  # get a report for ML for new df

    report += "\n\n"

    df3 = pd.read_csv(f"../results/lemmas_normalized/norm_by_med.csv", keep_default_na=False, index_col=0)
    new_df3 = FS(df3, N_features) # apply feature selection
    report += apply_ML.eval_norm_med(new_df3, resample)  # get a report for ML for new df

    if resample == "undersample":
        with open(f"../results/ML_reports/report_{N_features}_undersampled.txt", "w") as f:
            f.write(report)
    else:
        with open(f"../results/ML_reports/report_{N_features}.txt", "w") as f:
            f.write(report)


def main():
    # originally we have 6929 features, now we try to reduce them

    N_features = [3464, 1000, 100] # cut number of desired features in half, then see lower numbers
    for N in N_features:
        write_report(N, None) # no resampling
        write_report(N, "undersample") # try with undersample


main()