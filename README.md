# LiveJournal NSSI

*To access the files for data and results, check the [OneDrive Link](https://1drv.ms/f/s!Aq-NQwt8EWd2grBlZGmX_qQzILUlig?e=ThTWL4).*


## Introduction and agenda

We are given a dataset of 25,000+ LiveJournal users who were, directly or indirectly, involved in non-suicidal self-injury (NSSI). They participated in around 130 NSSI communities on LiveJournal but also had their personal journals. We have their community posts and would like to compare them with the personal posts to see if there are any hints revealing their predisposition to NSSI.

## Given: 
1. Three files containing people from three groups within NSSI community: a list of cutters (14948 users), a list of friends (13670 users), and a list of friends of friends (11672); files being named after the groups they are representing (list-of-cutters.csv, list-of-friends.csv, list-of-fofs.csv). 
2. CSV file (community-based-users.csv) containing the usernames for 3292 community-based users. For 693 of them, we are going to use all of their community-based posts (indicated by “F” - full in the second column), and for the remaining 2599, we are going to sample 2.5% of their posts.

## Actions taken:

### 00-get-links
Gather all links to dates (posts) from 2000 to 2010 of all users. 

Input: list-of-cutters.csv, list-of-friends.csv, list-of-fofs.csv

Output: posts_links.csv

Notes: since there are 3758497 links, it would take approximately 254 days to go through them (we have to introduce an artificial delay between each link to avoid getting banned by the website). We could solve this problem either by parallelizing the job or getting a sample instead of the full dataset. However, even if we could use all of our team’s computers, it would still take too much time to get the results. Thus, we decided to use the sampling approach.

### 01-get-comm-based-links
Gather all links to all posts of users that we have in community-based-users.csv. 

Input: community-based-users.csv, posts_links.csv (to get full links)

Output: links-community-based-users.csv (376718 links)

### 02-get-F-S-links
Create two separate csv files, one of them containing all links to the posts of the users of type “S” and one of them containing all links to the posts of the users of type “F”.

Input: community-based-users.csv, links-community-based-users.csv

Output: type_F_links.csv (76455 links), type_S_links.csv (300010 links)

### 03-sample-S
Randomly choose 2.5% of posts for people of type S and create a separate csv file for chosen posts.

Input: type_S_links.csv

Output: type_S_links_sample.csv (8637 links)

Notes: some people have a very small number of posts so that 2.5% of the number of their posts would be zero posts. For them, we randomly choose one of their posts.

### 04-sum-comm-based
Put all links to posts of type F and chosen posts of type S into one file.

Input: type_S_links_sample.csv, type_F_links.csv

Output: F_and_Ssample_links.csv (85092 links)

### 05-get-html-files
Download html pages of users’ posts we have chosen.

Input: F_and_Ssample_links.csv

Output: html_pages folder containing 85092 html pages of posts needed.

Notes: some posts contain too much text, and in order to show the complete version of the post, the user has to interact with “cut” (click on the “Read more” button). We want to see the full text, so we are going to deal with it next.

### 06-save-posts-with-cut
Go through our saved pages, see if they have any “cut” and if so, put the link into csv file.

Input: html_pages folder

Output: posts_with_cut.csv (11082 links)

### 07-posts-with-cut-to-html
Download html pages of full posts with “cut”.

Input: posts_with_cut.csv

Output: 11082 files in html_pages_of_posts _with_cut folder
 
### 08-get-json-files
Analyze html files (downloaded pages) and create json files with summarized information. One json file corresponds to one html page and contains an array representing all posts within a specific date. For each post, we have the following entries: author, title, time, tags, number of comments, userpic, is repost (is it a repost of the other post?), is answer (is it an answer to “question of the day”?), text (the text of the post). For reposts, we also have original_post_link field. For answers, we have question_url and question_text fields.

Input: html_pages folder

Output: json_files folder (85092 files)

### 09-add-language
Go through “text” fields of json objects and check if the post is written in English language and if so, add “language” field. We assume that the post is written in English if at least 50% words are English.

Input: json_files folder

Output: updated json_files folder

### 10-three-groups-csv-to-sets
For programming purposes, create three Python Pickle files (sets) from the csv files of three groups: cutters, friends, friends of friends.

Input: list-of-cutters.csv, list-of-friends.csv, list-of-fofs.csv

Output: list_of_cutters.p, list_of_friends.p, list_of_fofs.p

### 11-english-posts-stats
Collect statistics on English posts within three groups: how many posts in English belong to each group; how many posts belong to each group in general; what is the percentage of English posts for each group?

Input: list-of-cutters.p, list-of-friends.p, list-of-fofs.p, json_files folder

Output: english-posts-stats.csv

Notes: percentage of posts in English for each group is as follows: cutters - 94.547%, friends - 91.8369%, friends of friends - 87.2507%. Since the percentage is high, we can feel free to examine the posts in English only. 

### 12-extract-english-posts
We want to focus only on posts in English. Create a table: the first column represents the link to the date (file), the second column tells which posts on that date are in English.

Input: json_files folder

Output: posts_in_english.csv

### 13-get-users-vectors
Create a “vector” for each user. One vector represents summary of the posts of a particular user. The vector for each user contains:
1. All lemmas (words and signs (including punctuation) (ex., “!”, “,”, “)))”) used by the user)
2. Colors used in a text (start with “#”)
3. Metalemmas:

~\~n_b_strong~~ - total number of words within “b” or “strong” tags used by the author

~\~n_font_size~~ - total number of words for which the font size was changed by the author

~\~n_has_title~~ - now many posts have a title

~\~n_i_em~~ - total number words within “i” or “em” tags used by the author

~\~n_imgs~~ - total number of images included by the author

~\~n_posts~~ - total number of posts that have a title

~\~n_strike~~ - total number of words within “strike” tags used by the author

~\~n_u~~ - total number of words within “u” tags used by the author

~\~n_words~~ - total number of words, includes number of lemmas (words and punctuation), number of colors within the text and number of images used

~\~percent_uppercase~~ - average percent of uppercase letters in a post for the author

Input: posts_in_english.csv; json_files folder; html_pages folder 

Output: lemmas_dataframes folder containing csv files containing a “vector” for each user. 

### 14-get-lemmas-frequencies
Count the frequency for each lemma, get the csv file with each lemma and how often it was used

Input: lemmas_dataframes folder

Output: lemmas_frequencies.csv

### 15-get-most-freq
Go through all lemmas with their frequencies and choose the most frequently used lemmas that represent 95% of the corpus. Therefore, we are going to get rid of the huge amount of insignificant lemmas (lemmas that had a low frequency). The program also builds a plot showing the number of lemmas vs the fraction of the corpus they constitute, with the red line representing the 95%. Thus, we used to have 225289 lemmas, and after choosing those representing 95% of the corpus we are left with 6920 lemmas, getting rid of 218369 lemmas (with frequencies from 1 to 143), therefore improving the performance for classification later. 

Input: lemmas_frequencies.csv

Output: 95_percent_words.p (a python set with chosen lemmas), 95_percent.png (the plot)

### 16-choose-95-percent
Go through lemmas_dataframes folder and for each file leave only significant lemmas using results from the previous step.

Input: 95_percent_words.p, lemmas_dataframes folder

Output: lemmas_dataframes_95 folder (with the smaller files)

### 17-get-95-df
Collect all lemmas from the previous steps into one csv file. 

Input: lemmas_dataframes_95 folder

Output: sum_df.csv (inside lemmas_dataframes_95 folder)

### 18-add-group
Finish up the previous step. To the table from the previous task, add a column “group”: Cutter/Friend/FoF (friend of friend). Sort the table. 

Input: list_of_cutters.p, list_of_friends.p, list_of_fofs.p, sum_df.csv

Output: users-vs-lemmas.csv

### 19-norm-freq
Normalize the table by frequency: divide all lemmas, and ```~~n_b_strong~~```, ```~~n_i_em~~```, ```~~n_strike~~```, ```~~n_u~~```, ```~~n_font_size~~```, ```~~n_imgs~~``` in metalemmas by ```~~n_words~~``` to count the frequency, since if the person is writing more in general, then they are gonna use more of those lemmas. Normalize ```~~n_has_title~~``` by dividing it by the number of posts, include a new column - ```~~inv_avg_post_len~~``` - inverse average post length, which is the total number of posts divided by the total number of words.

Input: users-vs-lemmas.csv

Output: lemmas_normalized/norm_by_freq.csv

### 20-norm-pres
Normalize the table by the presence: use binary mode for whether a lemma/metalemma is used by the user (true - 1) or not (false - 0) (exclude group, n_posts and n_words).

Input: users-vs-lemmas.csv

Output: lemmas_normalized/norm_by_pres.csv

### 21-norm-med
Normalize the table using the median: use binary mode for whether a lemma is above the median (true - 1) or not (below or equal to) (false - 0). Find the median for each lemma, assign 1 if an author uses the lemma the number of times higher than the median for that lemma, assign 0 for equal or lower than the median.

Input: users-vs-lemmas.csv

Output: lemmas_normalized/norm_by_med.csv

### 22-apply-ML
Apply machine learning to explore the data obtained from the last three steps. Each table that we have has 2988 rows and 6932 columns. The objective is to explore this data with predictive models and evaluate the results. This step does not use feature selection. Evaluating the confusion tables, one could see class imbalance, therefore we also perform two ways of resampling: undersample and oversample. Write report on each evaluation.

Input: norm_by_freq.csv, norm_by_pres.csv, norm_by_med.csv

Output: ML_reports/report_no-fs.txt, ML_reports/report_no-fs_undersampled.txt, ML_reports/report_no-fs_oversampled.txt

### 23-feature-analysis
Apply feature selection to the data and display on the screen the best features for lemmas normalized by frequency, by presence, and by median.

Input: norm_by_freq.csv, norm_by_pres.csv, norm_by_med.csv

Output: N best features are displayed on the screen.


### 24-feat-sel
Apply feature selection to the data (using half the features, then 1000, then 100) and write report on each evaluation with each way of feature selection (including using resampling techniques).

Input: norm_by_freq.csv, norm_by_pres.csv, norm_by_med.csv

Output: ML_reports/report_{N_features}.txt, ML_reports/report_{N_features}_undersampled.txt, ML_reports/report_{N_features}_oversampled.txt

### 25-scores-to-csv
Go through all the reports in ML_reports directory and make one csv file comparing the testing scores from each report

Input: ML_reports directory

Output: ML_reports/testing_scores.csv

### 26-get-all-scores
Get testing, f1, precision and recall scores for ML and put them into one csv file.

Input: ML_reports directory

Output: ML_reports/all_scores.csv

### 27-get-best-models
Evaluate ML models based on their scores. Narrow them down to where testing score is more than 0.70 and where precision score is more than 0.72.

Input: ML_reports/all_scores.csv

Output: Show the best models and their scores
