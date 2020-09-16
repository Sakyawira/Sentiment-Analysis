import datetime

import praw
import pandas as pd

from keys import client_id, client_secret, username

reddit = praw.Reddit( client_id=client_id,
                      client_secret=client_secret,
                      user_agent=f'web-app:sentimentAnalysis:v1 (by /u/{username})')

def subreddit_posts(_topic, _limit):     
    
    # Get the Sub-Reddit
    topic = reddit.subreddit(_topic)

    # Select the top <limit> posts, with their title, URL, body, upvotes, timestamp, 
    # and an index that serves as a key between the posts and the comments we collect later.
    posts = []
    for index, post in enumerate(topic.top(limit=_limit)):
        posts.append([post.title, "https://www.reddit.com" + post.permalink, post.selftext, post.score, post.created_utc, index])

    # Convert to DataFrame
    posts = pd.DataFrame(posts, columns=['Title', 'URL', 'Body', 'Upvotes', 'Time', 'Key'])

    # Convert from UTC to standard timestamp
    posts.Time = posts.Time.apply(lambda x: pd.to_datetime(datetime.datetime.fromtimestamp(x)))

    # The first post is a sticky, so we can drop it
   ## posts = posts.iloc[1:]
    
    return posts

    
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
    
    keys = posts_dataframe.Key.tolist()
    urls = posts_dataframe.URL.tolist()
    tupules = list(zip(keys, urls))

    # Generate 'Comments' data-frame using list comprehensions
    comments = pd.concat([collect_replies(x[0], x[1]) for x in tupules])
    comments.Time = comments.Time.apply(lambda x: pd.to_datetime(datetime.datetime.fromtimestamp(x)))
    return comments