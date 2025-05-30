# College Football Sentiment Analysis Dashboard

This Streamlit application analyzes public sentiment toward college football teams and conferences based on Reddit posts. It provides visualizations and metrics to track how fan sentiment changes throughout the season.

## Features

- **Team Analysis**: Select any college football team to see their sentiment trends
- **Conference Analysis**: View aggregated sentiment data for major conferences (SEC, Big Ten, Big 12, ACC, Pac-12)
- **Interactive Visualizations**: 
  - Weekly sentiment trends
  - Key metrics including highest/lowest sentiment and biggest changes
  - Raw data table with weekly sentiment scores
- **Automatic Season Detection**: Automatically uses the current season year (August to January)

## Key Metrics

The dashboard displays several important metrics:
- Highest and Lowest Sentiment scores with corresponding weeks
- Mean and Median sentiment values
- Biggest week-over-week sentiment changes
- Weekly sentiment data table

## Data Sources

- Reddit posts from r/CFB and related subreddits
- Sentiment analysis using VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Posts are filtered to the current season (August through January)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Reddit API credentials:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent
   ```
4. Run the dashboard:
   ```bash
   streamlit run app.py
   ```

## Getting Reddit API Credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "create app" or "create another app"
3. Fill in the required information:
   - Name: CFB Sentiment Dashboard
   - Type: Script
   - Description: College Football Sentiment Analysis Tool
   - About URL: (can be left blank)
   - Redirect URI: http://localhost:8080

## Usage

1. Select a team from the dropdown menu
2. Click "Analyze Sentiment"
3. View the sentiment trend chart and raw data

## Technical Details

- Frontend: Streamlit
- Backend: Python with PRAW (Reddit API wrapper)
- Sentiment Analysis: VADER (NLTK)
- Data Processing: Pandas
- Visualization: Plotly Express

## Limitations

- Limited data to work with from subreddits
- Subject to Reddit API rate limits, especially since it limits to the past 1-2 years.
- No integration with game schedules/scores
- Sentiment analysis may not capture all nuances of sports commentary

## Future Improvements

- Add team-specific subreddits
- Implement caching for better performance
- Integrate game schedules and scores
- Add more visualization options
- Expand team selection
- Add historical data analysis
- Implement sentiment comparison between teams
- Add conference-specific metrics and trends

## Contributing

Feel free to submit issues and enhancement requests!
