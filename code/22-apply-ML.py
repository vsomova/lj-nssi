from imblearn.under_sampling import RandomUnderSampler
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB


def logit(X_train, X_test, y_train, y_test):
    report = ("\nLogistic regression:\n")
    logi = LogisticRegression(
        max_iter=200)  # w/o max_iter gives a warning _logistic.py:765: ConvergenceWarning: lbfgs failed to converge (status=1):STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.
    logi.fit(X_train, y_train)
    report += "Training: " + str(logi.score(X_train, y_train)) + " " + "Testing: " + str(
        logi.score(X_test, y_test)) + "\n"
    report += (pd.DataFrame(confusion_matrix(y_test, logi.predict(X_test)), index=["positive", "negative"],
                            columns=["classified as positive", "classified as negative"])).to_string() + "\n"
    return report


def RF(X_train, X_test, y_train, y_test):
    report = ("\nRandom forest classifier:\n")
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    report += "Training: " + str(rf.score(X_train, y_train)) + " " + "Testing: " + str(rf.score(X_test, y_test)) + "\n"
    report += (pd.DataFrame(confusion_matrix(y_test, rf.predict(X_test)), index=["positive", "negative"],
                            columns=["classified as positive", "classified as negative"])).to_string() + "\n"
    return report


def MNB(X_train, X_test, y_train, y_test):
    report = ("\nMultinomial Naive Bayes:\n")
    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)
    report += "Training: " + str(mnb.score(X_train, y_train)) + " " + "Testing: " + str(
        mnb.score(X_test, y_test)) + "\n"
    report += (pd.DataFrame(confusion_matrix(y_test, mnb.predict(X_test)), index=["positive", "negative"],
                            columns=["classified as positive", "classified as negative"])).to_string() + "\n"
    return report


def BNB(X_train, X_test, y_train, y_test):
    report = ("\nBernoulli Naive Bayes:\n")
    bnb = BernoulliNB()
    bnb.fit(X_train, y_train)
    report += "Training: " + str(bnb.score(X_train, y_train)) + " " + "Testing: " + str(
        bnb.score(X_test, y_test)) + "\n"
    report += (pd.DataFrame(confusion_matrix(y_test, bnb.predict(X_test)), index=["positive", "negative"],
                            columns=["classified as positive", "classified as negative"])).to_string() + "\n"
    return report


def get_features(df):
    features = list(df.columns)
    features.remove("~~group~~")  # we're gonna predict it
    return features


def eval_cont(df, resample):  # evaluate continuous data
    features = get_features(df)

    X_train, X_test, y_train, y_test = train_test_split(df[features], df["~~group~~"], test_size=0.3,
                                                        random_state=12)  # split into training and testing # also tried stratify=df["~~group~~"] parameter -> the scores are dropping

    if resample == "undersample":
        # perform undersample
        unds = RandomUnderSampler(sampling_strategy="majority", random_state=12)
        X_train, y_train = unds.fit_resample(X_train, y_train)

    report = "\nTarget values in general:\n"
    report += (df["~~group~~"].value_counts()).to_string() + "\n"
    report += "\nTarget values in training:\n"
    report += (y_train.value_counts()).to_string() + "\n"

    report += logit(X_train, X_test, y_train, y_test)  # perform and evaluate Logistic regression
    report += RF(X_train, X_test, y_train, y_test)  # perform and evaluate Random forest classifier
    report += MNB(X_train, X_test, y_train, y_test)  # perform and evaluate Multinomial Naive Bayes

    return report


def eval_bool(df, resample):  # evaluate boolean data
    features = get_features(df)
    X_train, X_test, y_train, y_test = train_test_split(df[features], df["~~group~~"], test_size=0.3,
                                                        random_state=12)  # split into training and testing # also tried stratify=df["~~group~~"] parameter -> the scores are dropping

    if resample == "undersample":
        # perform undersample
        unds = RandomUnderSampler(sampling_strategy="majority", random_state=12)
        X_train, y_train = unds.fit_resample(X_train, y_train)

    report = "\nTarget values in general:\n"
    report += (df["~~group~~"].value_counts()).to_string() + "\n"
    report += "\nTarget values in training:\n"
    report += (y_train.value_counts()).to_string() + "\n"

    report += logit(X_train, X_test, y_train, y_test)  # perform and evaluate Logistic regression
    report += RF(X_train, X_test, y_train, y_test)  # perform and evaluate Random forest classifier
    report += BNB(X_train, X_test, y_train, y_test)  # perform and evaluate Bernoulli Naive Bayes

    return report


def eval_norm_freq(orig_df, resample):  # evaluate and apply ML to the data normalized by frequency
    report = "Data normalized by frequency:\n"

    # first way: true for cutters and false for everyone else
    report += "\nFirst way: making it true for cutters and false for everyone else:\n"
    df = orig_df.copy()  # create a copy bc reference passed to the func
    df["~~group~~"] = df[
                          "~~group~~"] == "Cutters"  # the group column becomes true for cutters and false for everyone else
    report += eval_cont(df, resample)  # evaluate the data with ML models appropriate for continuous data

    # second way: true for cutters and friends, false for fof
    report += "\nSecond way: making it true for cutters and friends, false for fof:\n"
    df = orig_df.copy()
    df["~~group~~"] = df["~~group~~"] != "FoF"  # the group column becomes true for cutters and friends, false for fof
    report += eval_cont(df, resample)  # evaluate the data with ML models appropriate for continuous data
    return report


def eval_norm_pres(orig_df, resample):  # evaluate and apply ML to the data normalized by presence
    report = "Data normalized by presence:\n"

    # first way: true for cutters and false for everyone else
    report += "\nFirst way: making it true for cutters and false for everyone else:\n"
    df = orig_df.copy()  # create a copy bc reference passed to the func
    df["~~group~~"] = df[
                          "~~group~~"] == "Cutters"  # the group column becomes true for cutters and false for everyone else
    report += eval_bool(df, resample)  # evaluate the data with ML models appropriate for boolean data

    # second way: true for cutters and friends, false for fof
    report += "\nSecond way: making it true for cutters and friends, false for fof:\n"
    df = orig_df.copy()
    df["~~group~~"] = df["~~group~~"] != "FoF"  # the group column becomes true for cutters and friends, false for fof
    report += eval_bool(df, resample)  # evaluate the data with ML models appropriate for boolean data
    return report


def eval_norm_med(orig_df, resample):
    report = "Data normalized using median:\n"

    # first way: true for cutters and false for everyone else
    report += "\nFirst way: making it true for cutters and false for everyone else:\n"
    df = orig_df.copy()  # create a copy bc reference passed to the func
    df["~~group~~"] = df[
                          "~~group~~"] == "Cutters"  # the group column becomes true for cutters and false for everyone else
    report += eval_bool(df, resample)  # evaluate the data with ML models appropriate for boolean data

    # second way: true for cutters and friends, false for fof
    report += "\nSecond way: making it true for cutters and friends, false for fof:\n"
    df = orig_df.copy()
    df["~~group~~"] = df["~~group~~"] != "FoF"  # the group column becomes true for cutters and friends, false for fof
    report += eval_bool(df, resample)  # evaluate the data with ML models appropriate for boolean data
    return report


def get_report(resample):
    report = ""

    df1 = pd.read_csv(f"../results/lemmas_normalized/norm_by_freq.csv", keep_default_na=False, index_col=0)
    df1 = df1.drop(columns=["~~n_posts~~", "~~n_words~~"])  # remove these columns cuz we dont need them for ML
    report += eval_norm_freq(df1, resample)  # evaluate and apply ML to the data normalized by frequency

    report += "\n\n"

    df2 = pd.read_csv(f"../results/lemmas_normalized/norm_by_pres.csv", keep_default_na=False, index_col=0)
    df2 = df2.drop(columns=["~~n_posts~~", "~~n_words~~"])  # remove these columns cuz we dont need them for ML
    report += eval_norm_pres(df2, resample)  # evaluate and apply ML to the data normalized by presence

    report += "\n\n"

    df3 = pd.read_csv(f"../results/lemmas_normalized/norm_by_med.csv", keep_default_na=False, index_col=0)
    df3 = df3.drop(columns=["~~n_posts~~", "~~n_words~~"])  # remove these columns cuz we dont need them for ML
    report += eval_norm_med(df3, resample)  # evaluate and apply ML to the data normalized using the median

    return report


def main():
    nd = "../results/ML_reports"  # new directory
    if not os.path.exists(nd):
        os.makedirs(nd)

    # perform a report with no resample
    report = get_report(resample=None)
    with open(f"../results/ML_reports/report_no-fs.txt", "w") as f:
        f.write(report)

    # perform a report with undersample
    report = get_report(resample="undersample")
    with open(f"../results/ML_reports/report_no-fs_undersampled.txt", "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()