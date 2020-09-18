# Sentiment-Analysis

## Business Case
My Business case is a particular game company wishes to investigate the popularity of Epic Games Store. The video game company plans to use the results of the investigation to inform future business decisions (whether they will make an exclusivity deal with Epic Games Store for their upcoming title). We approached the problem by analysing sentiments of posts in the Epic Games Store subreddit (r/EpicGamesPC: https://www.reddit.com/r/EpicGamesPC/ ).

## Data Collection
Data collection is done using Reddit API. PushShift API was also used to bypass the 1000 submissions limit of the Reddit API. A total of 9727 posts are collected, and from those 64311 comments are collected.

## Data Exploration
A word-cloud was used to illustrate the most common words in the whole data-frame. An interesting thing to note is that the word "Steam" is the top 5 words in the whole data-frame.

## Data Cleaning
Characters that do not help with prediction are discarded. Characters like \n, \t, might link two words together and make them indistinguishable from one another. Any links are also discarded.

## Sentiment Analysis

- ### __Vader packaged__

- ### __Textblob package__

- ### __Self-Trained Classifier__

## Analysis
- ### __Positive / Negative Sentiments Ratio__

Using our own trained classification module, there seems to be more Negative sentiments compared to Positive ones. 23% Negative response and 18% Positive sentimes. But if we set aside the Neutral Sentimes, this looks like a very mixed sentiment.

Using the Textblob package, we can see that the Epic Games Store reddit has a mixed sentiment response on posts. 36% bad sentimes and 63% good sentiment.

- ### Analysing Compound Sentiment Score Overtime