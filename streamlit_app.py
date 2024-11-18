from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import os

# Set page configuration
st.set_page_config(
    page_title="Game Recommendation System", 
    page_icon="🎮", 
    layout="wide"
)

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

def resize_image(image_path, width=300, height=300):
    """
    Resize an image to a fixed width and height with high quality.
    """
    try:
        image = Image.open(image_path)
        return image.resize((width, height), Image.LANCZOS)
    except FileNotFoundError:
        return None

# App header
st.markdown(
    """
    <div style="text-align: center; background-color: #4CAF50; padding: 20px; border-radius: 10px; color: white;">
        <h1>🎮 Game Recommendation System</h1>
        <p>Find games similar to your favorites based on playtime and votes!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Game selection dropdown
selected_game = st.selectbox(
    "🎯 **Select a Game**",
    data['game'].unique(),
    help="Choose a game to get recommendations based on user votes and total playtime."
)

# Slider for number of recommendations
top_n = st.slider(
    "How many recommendations would you like?", 
    min_value=1, 
    max_value=10, 
    value=5, 
    help="Adjust the number of recommendations displayed."
)

# Path to image folder
image_folder = './'

# Recommendation button
if st.button("🔍 Recommend Games"):
    with st.spinner("Fetching recommendations..."):
        st.markdown("---")
        st.subheader(f"📋 Recommendations for: **{selected_game}**")
        
        recommended_games = recommend_games(selected_game, data, top_n=top_n)
        
        if recommended_games.empty:
            st.warning("No recommendations found for the selected game.")
        else:
            cols_per_row = 3
            cols = st.columns(cols_per_row)  # Adjust columns dynamically
            
            for i, (_, game_row) in enumerate(recommended_games.iterrows()):
                col = cols[i % cols_per_row]  # Wrap columns
                with col:
                    # Resize and display the image
                    recommended_image_path = os.path.join(image_folder, f"{game_row['game'][:3]}.jpg")
                    resized_image = resize_image(recommended_image_path, width=300, height=300)
                    if resized_image:
                        col.image(resized_image, use_container_width=True)
                    else:
                        col.image("https://via.placeholder.com/300x300?text=No+Image", use_container_width=True)

                    # Game name and details
                    background = "linear-gradient(135deg, #74ebd5, #acb6e5);"  # Example gradient
                    col.markdown(
                        f"""
                        <div style="
                            text-align: center; 
                            padding: 10px; 
                            margin-top: 10px; 
                            margin-bottom: 20px; 
                            border-radius: 12px; 
                            background: {background}; 
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
                            color: black;
                        ">
                            <b style="font-size: 16px;">{game_row['game']}</b><br>
                            <span style="font-weight: bold;">👍 Votes Up:</span> {game_row['votes_up_count']}<br>
                            <span style="font-weight: bold;">⏱️ Playtime:</span> {game_row['total_playtime']} hours
                        </div>
                        """,
                        unsafe_allow_html=True
                    )



# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <p>🎲 Made with ❤️ using Streamlit</p>
        <p>Follow me on:
            <a href="https://twitter.com" target="_blank">
                <img src="https://img.icons8.com/color/48/000000/twitter--v1.png" width="24"/>
            </a>
            <a href="https://github.com" target="_blank">
                <img src="https://img.icons8.com/ios-glyphs/30/000000/github.png" width="24"/>
            </a>
            <a href="https://linkedin.com" target="_blank">
                <img src="https://img.icons8.com/ios-glyphs/30/000000/linkedin.png" width="24"/>
            </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
