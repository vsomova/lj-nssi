# we want to minimize false negatives so we choose models with high precision

import pandas as pd

df = pd.read_csv(f"../results/ML_reports/all_scores.csv", index_col=[0,1])

df = df[ df["Testing score"] > 0.70] # narrow down to where testing score is more than the value

df = df[ df["Precision score"] > 0.72] # narrow down to where precision score is more than the value

df.to_csv("../results/ML_reports/best_scores.csv")