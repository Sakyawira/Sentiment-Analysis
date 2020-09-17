import datetime

import praw
import pandas as pd

from keys import client_id, client_secret, username

# Initializing a Reddit Instance
reddit = praw.Reddit( client_id=client_id,
                      client_secret=client_secret,
                      user_agent=f'web-app:sentimentAnalysis:v1 (by /u/{username})')

from psaw import PushshiftAPI

def subreddit_posts(_topic, _limit):     
    
    api = PushshiftAPI()
    gen = api.search_submissions(limit=_limit, subreddit=_topic,filter=['created_utc','title', 'full_link', 'selftext', 'upvote_ratio', 'created'])
    #gen = api.search_submissions(limit=100)
    #gen = api.search_submissions(limit=100, subreddit='EpicGamesPC')
    df = pd.DataFrame([obj.d_ for obj in gen])

    # Convert from UTC to standard timestamp
    df["Time"] = df.created_utc.apply(lambda x: pd.to_datetime(datetime.datetime.fromtimestamp(x)))

    return df

    
def collect_replies(key, url):
 
    # params pandas series row: each row of the dataframe we built above in the form of a panda series
    # Returns a pandas DataFrame, where each row represents an individual comment
    
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:] 

    table = {'Reply':[], 'Upvote':[], 'Time':[], 'Key':[]}

    while comment_queue:
        comment = comment_queue.pop(0)
        table['Reply'].append(comment.body)
        table['Time'].append(comment.created_utc)
        table['Upvote'].append(comment.score)
        table['Key'].append(key)
        comment_queue.extend(comment.replies)
    
    return pd.DataFrame.from_dict(table)

    
def replies_to_posts(posts_dataframe):
    # params pandas dataframe posts_dataframe: the posts dataframe created by the function subreddit_posts
    # returns: comments dataframe
    
    keys = posts_dataframe.index.tolist()
    urls = posts_dataframe.URL.tolist()
    tupules = list(zip(keys, urls))

    # Generate 'Comments' data-frame using list comprehensions
    comments = pd.concat([collect_replies(x[0], x[1]) for x in tupules])
    comments.Time = comments.Time.apply(lambda x: pd.to_datetime(datetime.datetime.fromtimestamp(x)))
    return comments