from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import os

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="Game Recommendation System", layout="wide")

# Load data
@st.cache_data
def load_data(filepath):
    """Load the CSV data into a DataFrame."""
    return pd.read_csv(filepath)

data = load_data('recommend.csv')

# Define recommendation function
def recommend_games(selected_game, data, top_n=5):
    """
    Recommend similar games based on votes and playtime.
    """
    selected_game_data = data[data['game'] == selected_game]
    if selected_game_data.empty:
        return pd.DataFrame()
    
    selected_votes = selected_game_data.iloc[0]['votes_up_count']
    selected_playtime = selected_game_data.iloc[0]['total_playtime']
    
    data['similarity'] = np.sqrt(
        (data['votes_up_count'] - selected_votes) ** 2 +
        (data['total_playtime'] - selected_playtime) ** 2
    )
    
    recommendations = (
        data[data['game'] != selected_game]
        .sort_values(by='similarity')
        .head(top_n)
    )
    return recommendations

def resize_image(image_path, width=200, height=200):
    """
    Resize an image to a fixed width and height.
    """
    try:
        image = Image.open(image_path)
        return image.resize((width, height))
    except FileNotFoundError:
        return None

# Streamlit app
st.title("🎮 Game Recommendation System")
st.markdown(
    "Find games similar to your favorites! Select a game from the dropdown below to get tailored recommendations."
)

# Game selection dropdown
selected_game = st.selectbox(
    "🎯 **Select a Game**",
    data['game'].unique(),
    help="Choose a game to get recommendations based on user votes and total playtime."
)

# Path to image folder
image_folder = './'

if st.button("🔍 Recommend Games"):
    st.markdown("---")
    st.subheader(f"📋 Recommendations for: **{selected_game}**")
    
    recommended_games = recommend_games(selected_game, data)
    
    if recommended_games.empty:
        st.warning("No recommendations found for the selected game.")
    else:
        # Columns for recommendations
        cols = st.columns(len(recommended_games))
        for col, (_, game_row) in zip(cols, recommended_games.iterrows()):
            with col:
                # Resize and display the image
                recommended_image_path = os.path.join(image_folder, f"{game_row['game'][:3]}.jpg")
                resized_image = resize_image(recommended_image_path, width=200, height=200)
                if resized_image:
                    col.image(resized_image, use_container_width=True)
                else:
                    col.image("https://via.placeholder.com/200x200?text=No+Image", use_container_width=True)

                # Game name and details (center-aligned)
                col.markdown(
                    f"""
                    <div style="text-align: center; margin-top: 10px;">
                        <b>{game_row['game']}</b><br>
                        👍 Votes Up: {game_row['votes_up_count']}<br>
                        ⏱️ Playtime: {game_row['total_playtime']} hours
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>"
    "🎲 Made with ❤️ using Streamlit | "
    "<a href='https://www.streamlit.io' target='_blank'>Streamlit Documentation</a>"
    "</p>",
    unsafe_allow_html=True
)
