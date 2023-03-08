import pickle
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../results/lemmas_frequencies.csv", keep_default_na=False, names=["lemma", "frequency"], header=None)

# orig_df = df

df = df.set_index('lemma')

cumulative = df['frequency'].sort_values(ascending=False).cumsum()
cumulative /= cumulative.max() # 225289 lemmas and puncts
cumulative = cumulative[cumulative <= 0.95] # 6920 lemmas that constitute 95% of the corpus

selected_words = set(cumulative.index)

####################
# print(orig_df.lemma.isin(selected_words)) #0 False, 1 False etc
# print(orig_df[orig_df.lemma.isin(selected_words)].sort_values("frequency"))
# print(orig_df[~orig_df.lemma.isin(selected_words)].sort_values("frequency"))
####################


pickle.dump(selected_words, open("../results/95_percent_words.p", "wb"))


# cumulative[cumulative <= 0.95]

ax = cumulative.plot()
ax.hlines(0.95, 0, cumulative.shape[0], colors=['red'])
ax.set_xscale('log')
ax.grid()
ax.set_xlabel('# of lemmas')

plt.savefig("../results/95_percent.png")
plt.show()

# the first ~7000 most frequently used lemmas represent 95% of the corpus. We can use them as the features for classification.