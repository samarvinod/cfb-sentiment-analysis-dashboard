import praw
import pandas as pd
from datetime import datetime, timedelta
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

# Download VADER lexicon if not already downloaded
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

def get_team_subreddits(team):
    """
    Returns a list of relevant subreddits for a given team.
    Currently only includes r/CFB, but can be expanded.
    """
    return ['CFB', 'cfbmemes', 'CFBAnalysis', 'American_Football']

def get_season_dates(year):
    """
    Returns start and end dates for a given college football season.
    Season typically runs from late August to early January.
    """
    # Season starts in August of the given year
    start_date = datetime(year, 8, 1)
    # Season ends in January of the next year
    end_date = datetime(year + 1, 1, 31)
    return start_date, end_date

def fetch_reddit_posts(team, year):
    """
    Fetches Reddit posts mentioning the team during the specified season.
    """
    start_date, end_date = get_season_dates(year)
    posts = []
    
    for subreddit_name in get_team_subreddits(team):
        subreddit = reddit.subreddit(subreddit_name)
        
        # Search for posts containing team name
        search_query = f"{team} football"
        for submission in subreddit.search(search_query, time_filter='year', limit=1000):
            post_date = datetime.fromtimestamp(submission.created_utc)
            if start_date <= post_date <= end_date:
                posts.append({
                    'date': post_date,
                    'title': submission.title,
                    'text': submission.selftext,
                    'score': submission.score,
                    'url': submission.url
                })

    return pd.DataFrame(posts)

def analyze_sentiment(text):
    """
    Analyzes sentiment of text using VADER.
    Returns compound score (-1 to 1).
    """
    if not isinstance(text, str):
        return 0
    return sia.polarity_scores(text)['compound']

def process_team_sentiment(team, year):
    """
    Main function to process sentiment analysis for a team in a given season.
    Returns weekly sentiment averages.
    """
    # Define the date range for the season
    start_date, end_date = get_season_dates(year)
    week_starts = pd.date_range(start=start_date, end=end_date, freq='W-THU')

    # Fetch posts
    df = fetch_reddit_posts(team, year)
    if df.empty:
        return pd.DataFrame({'week_start': week_starts, 'sentiment': [np.nan]*len(week_starts)})

    df['date'] = pd.to_datetime(df['date'])

    # Only keep posts within the season window
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Calculate sentiment for title and text, then average
    def combined_sentiment(row):
        title_sent = analyze_sentiment(row['title'])
        text_sent = analyze_sentiment(row['text'])
        return np.mean([title_sent, text_sent])

    df['sentiment'] = df.apply(combined_sentiment, axis=1)

    # Assign each post to the correct week
    df['week_start'] = pd.cut(
        df['date'],
        bins=list(week_starts) + [end_date + pd.Timedelta(days=7)],
        labels=week_starts,
        right=False
    )

    # Group by week_start
    weekly_sentiment = df.groupby('week_start')['sentiment'].mean()
    weekly_sentiment = weekly_sentiment.reindex(week_starts, fill_value=np.nan)
    weekly_sentiment = weekly_sentiment.reset_index()
    weekly_sentiment.columns = ['week_start', 'sentiment']
    weekly_sentiment['week_start'] = pd.to_datetime(weekly_sentiment['week_start'])
    
    return weekly_sentiment 
