import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize database connection
def init_db():
    conn = sqlite3.connect('basketball.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            opponent TEXT NOT NULL,
            score TEXT NOT NULL,
            result TEXT NOT NULL,
            notes TEXT
        )
    ''')
    conn.commit()
    return conn

# Initialize the database
conn = init_db()

# Set page config
st.set_page_config(
    page_title="Basketball Wins Tracker",
    page_icon="🏀",
    layout="wide"
)

# Title
st.title("🏀 Basketball Wins Tracker")

# Sidebar for adding new games
with st.sidebar:
    st.header("Add New Game")
    
    date = st.date_input("Date")
    opponent = st.text_input("Opponent")
    score = st.text_input("Score (e.g., '85-82')")
    result = st.selectbox("Result", ["Win", "Loss"])
    notes = st.text_area("Notes")
    
    if st.button("Add Game"):
        if opponent and score:
            c = conn.cursor()
            c.execute('''
                INSERT INTO games (date, opponent, score, result, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (date.isoformat(), opponent, score, result, notes))
            conn.commit()
            st.success("Game added successfully!")
        else:
            st.error("Please fill in all required fields.")

# Main content
st.header("Game History")

# Fetch and display games
c = conn.cursor()
c.execute('SELECT * FROM games ORDER BY date DESC')
games = c.fetchall()

if games:
    # Convert to DataFrame for better display
    df = pd.DataFrame(games, columns=['ID', 'Date', 'Opponent', 'Score', 'Result', 'Notes'])
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    # Display the data
    st.dataframe(df, use_container_width=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Games", len(df))
    with col2:
        wins = len(df[df['Result'] == 'Win'])
        st.metric("Wins", wins)
    with col3:
        win_percentage = (wins / len(df)) * 100 if len(df) > 0 else 0
        st.metric("Win Percentage", f"{win_percentage:.1f}%")
else:
    st.info("No games recorded yet. Add your first game using the sidebar!") 