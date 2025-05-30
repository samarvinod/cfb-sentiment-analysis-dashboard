import streamlit as st
import pandas as pd
from sentiment_utils import process_team_sentiment
import plotly.express as px
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="CFB Sentiment Dashboard",
    page_icon="🏈",
    layout="wide"
)

# Title and description
st.title("College Football Sentiment Dashboard")
st.markdown("""
This dashboard tracks public sentiment toward college football teams based on Reddit posts.
Select a team and season to see how fan sentiment changed throughout the season.
""")

# Sidebar for team and season selection
st.sidebar.header("Select Parameters")

# Team selection
teams = [
    "Alabama", "Arizona", "Arizona State", "Arkansas", "Auburn", "Baylor", "Boston College", "BYU", 
    "California", "Cincinnati", "Clemson", "Colorado", "Duke", "Florida", "Florida State", "Georgia", 
    "Georgia Tech", "Houston", "Illinois", "Indiana", "Iowa", "Iowa State", "Kansas", "Kansas State", 
    "Kentucky", "Louisville", "LSU", "Maryland", "Miami (FL)", "Michigan", "Michigan State", "Minnesota", 
    "Mississippi State", "Missouri", "NC State", "Nebraska", "North Carolina", "Northwestern", "Notre Dame", 
    "Ohio State", "Oklahoma State", "Ole Miss", "Oregon", "Penn State", "Pittsburgh", "Purdue", "Rutgers", 
    "SMU", "South Carolina", "Stanford", "Syracuse", "TCU", "Tennessee", "Texas", "Texas A&M", "Texas Tech", 
    "UCF", "UCLA", "USC", "Utah", "Vanderbilt", "Virginia", "Virginia Tech", "Wake Forest", "Washington", 
    "West Virginia", "Wisconsin"
]
selected_team = st.sidebar.selectbox("Select Team", teams)

# Get current season year
current_date = datetime.now()
current_year = current_date.year
if current_date.month < 8:
    current_year -= 1

# Main content
if st.sidebar.button("Analyze Sentiment"):
    with st.spinner("Analyzing Reddit posts... This may take a few minutes."):
        # Get sentiment data
        sentiment_data = process_team_sentiment(selected_team, current_year)
        
        if sentiment_data.empty:
            st.error(f"No data found for {selected_team} in {current_year}")
        else:            
            # Create sentiment plot using Matplotlib
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(sentiment_data['week_start'], sentiment_data['sentiment'], marker='o', linestyle='-')
            ax.axhline(0, color='gray', linestyle='--')
            ax.set_title(f"{selected_team} Fan Sentiment - {current_year} Season")
            ax.set_xlabel("Week of Season")
            ax.set_ylabel("Sentiment Score")
            ax.set_ylim(-1, 1)
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)
            
            # Calculate and display key metrics
            st.subheader("Key Sentiment Metrics")
            
            # Calculate metrics
            if sentiment_data['sentiment'].isna().all():
                st.error("No valid sentiment data available for the selected period.")
            else:
                # Filter out values for calculations
                valid_data = sentiment_data.dropna(subset=['sentiment'])
                
                highest_week = valid_data.loc[valid_data['sentiment'].idxmax()]
                lowest_week = valid_data.loc[valid_data['sentiment'].idxmin()]
                mean_sentiment = valid_data['sentiment'].mean()
                median_sentiment = valid_data['sentiment'].median()
                
                # Calculate week-over-week changes
                valid_data['change'] = valid_data['sentiment'].diff()
                biggest_increase = valid_data.loc[valid_data['change'].idxmax()]
                biggest_decrease = valid_data.loc[valid_data['change'].idxmin()]
                
                # Display metrics in columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Highest Sentiment", 
                             f"{highest_week['sentiment']:.3f}",
                             f"Week of {highest_week['week_start'].strftime('%Y-%m-%d')}",
                             delta_color="off")
                    st.metric("Mean Sentiment", f"{mean_sentiment:.3f}")
                
                with col2:
                    st.metric("Lowest Sentiment", 
                             f"{lowest_week['sentiment']:.3f}",
                             f"Week of {lowest_week['week_start'].strftime('%Y-%m-%d')}",
                             delta_color="off")
                    st.metric("Median Sentiment", f"{median_sentiment:.3f}")
                
                with col3:
                    st.metric("Biggest Increase", 
                             f"{biggest_increase['change']:.3f}",
                             f"Week of {biggest_increase['week_start'].strftime('%Y-%m-%d')}",
                             delta_color="off")
                    st.metric("Biggest Decrease", 
                             f"{biggest_decrease['change']:.3f}",
                             f"Week of {biggest_decrease['week_start'].strftime('%Y-%m-%d')}",
                             delta_color="off")
            
            # Display raw data (all weeks, including none)
            st.subheader("Weekly Sentiment Data")
            sentiment_data['week_start'] = sentiment_data['week_start'].dt.strftime('%Y-%m-%d')
            st.dataframe(
                sentiment_data.style.format({'sentiment': '{:.3f}'}),
                use_container_width=True
            )
            
            st.markdown("""
            ### How to Interpret the Data
            - **Sentiment Score**: Ranges from -1 (very negative) to +1 (very positive)
            - **Trends**: Look for patterns around game days and major events
            - **Spikes**: Sudden changes often indicate significant wins or losses
            """)

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Data source: Reddit (r/CFB, r/cfbmemes, r/CFBAnalysis, r/American_Football) | Sentiment Analysis: VADER</p>
</div>
""", unsafe_allow_html=True) 
