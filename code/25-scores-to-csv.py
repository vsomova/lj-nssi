# extract the testing scores from reports and put them into csv file for easier comparison

import os
import re
import pandas as pd

dir = "../results/ML_reports"
sum_df = pd.DataFrame()

for filename in os.scandir(dir):
    f = open(f'{dir}/{filename.name}', 'r')
    report = f.read()
    x = re.findall("Testing: (.+)\n", report)
    df = pd.DataFrame(x, columns=[filename.name], index=["freq LR 1", "freq RFC 1", "freq MNB 1", "freq LR 2", "freq RFC 2", "freq MNB 2",
                                                         "pres LR 1", "pres RFC 1", "pres BNB 1", "pres LR 2", "pres RFC 2", "pres BNB 2",
                                                         "med LR 1", "med RFC 1", "med BNB 1", "med LR 2", "med RFC 2", "med BNB 2"]) # short labels for scores
    sum_df = pd.concat([sum_df, df], axis=1)

sum_df.to_csv("../results/ML_reports/testing_scores.csv")