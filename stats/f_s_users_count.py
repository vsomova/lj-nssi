#count the amount of users of type "s" and "f"
import pandas as pd

df = pd.read_csv("../data/community-based-users.csv")
print(df)

mask_f = df["type"] == "F"
mask_s = df["type"] == "S"

arr_f = df[mask_f]["username"].to_numpy()
arr_s = df[mask_s]["username"].to_numpy()

print(arr_f)
print(arr_s)

print(len(arr_f))
print(len(arr_s))