import os
import re
import pandas as pd

dir = "../results/ML_reports"
sum_df = pd.DataFrame()

for filename in os.scandir(dir):
    if ".csv" not in filename.name: # this program's output file, in case of rerun
        f = open(f'{dir}/{filename.name}', 'r')
        report = f.read()
        testing_scores = re.findall("Testing: (.+)\n", report)
        f1_scores = re.findall("f1 score: (.+)\n", report)
        precision_scores = re.findall("Precision score: (.+)\n", report)
        recall_scores = re.findall("Recall score: (.+)\n", report)

        # create the base dataframe
        testing_scores_df = pd.DataFrame(testing_scores, columns=["Testing score"], index=["freq LR 1", "freq RFC 1", "freq MNB 1", "freq LR 2", "freq RFC 2", "freq MNB 2",
                                                             "pres LR 1", "pres RFC 1", "pres BNB 1", "pres LR 2", "pres RFC 2", "pres BNB 2",
                                                             "med LR 1", "med RFC 1", "med BNB 1", "med LR 2", "med RFC 2", "med BNB 2"]) # short labels for scores
        testing_scores_df.index.name = "Model" # first index
        testing_scores_df["Data"] = filename.name # second index
        testing_scores_df.set_index(["Data", testing_scores_df.index], inplace=True) # set multiindex

        testing_scores_df["f1 score"] = f1_scores
        testing_scores_df["Precision score"] = precision_scores
        testing_scores_df["Recall score"] = recall_scores
        sum_df = pd.concat([sum_df, testing_scores_df], axis=0)

sum_df.to_csv("../results/ML_reports/all_scores.csv")