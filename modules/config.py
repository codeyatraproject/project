import streamlit as st
import os
from pathlib import Path

# Constants
APP_VERSION = "1.0.0"
APP_NAME = "Incredible India | A Data-Driven Journey"
DATA_DIR = Path("data")

# Chapter configuration
CHAPTER_CONFIG = {
    "Introduction": {
        "icon": "🇮🇳",
        "color": "#FF9933",
        "datasets": ["population", "state"]
    },
    "Linguistic Diversity": {
        "icon": "🗣️",
        "color": "#3776AB",
        "datasets": ["linguistic", "state"]
    },
    "Religious Mosaic": {
        "icon": "🕉️",
        "color": "#FF5722",
        "datasets": ["religious", "state"]
    },
    "Cultural Heritage": {
        "icon": "🏛️",
        "color": "#9C27B0",
        "datasets": ["cultural", "state"]
    },
    "Festivals of India": {
        "icon": "🪔",
        "color": "#FFC107",
        "datasets": ["festivals", "state"]
    },
    "Geographical Diversity": {
        "icon": "🏔️",
        "color": "#4CAF50",
        "datasets": ["geography", "state"]
    },
    "Historical Timeline": {
        "icon": "⏳",
        "color": "#795548",
        "datasets": ["historical"]
    },
    "Tourism Highlights": {
        "icon": "🧳",
        "color": "#2196F3",
        "datasets": ["tourism"]
    },
    "Education Landscape": {
        "icon": "📚",
        "color": "#607D8B",
        "datasets": ["education", "state"]
    },
    "Modern India": {
        "icon": "🏙️",
        "color": "#E91E63",
        "datasets": ["economic", "population"]
    },
    "Image Gallery": {
        "icon": "🖼️",
        "color": "#9E9E9E",
        "datasets": []
    }
}

def init_config():
    """Initialize application configuration and session state"""
    # Set up session state variables if they don't exist
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_chapter = "Introduction"
        st.session_state.visited_chapters = set(["Introduction"])
        st.session_state.favorites = set()
        st.session_state.error_count = 0
        st.session_state.data_loaded = False
        st.session_state.dark_mode = True
        st.session_state.animations_enabled = True
        st.session_state.high_quality = True
        
    # Check if data directories exist
    for dataset in os.listdir(DATA_DIR) if os.path.exists(DATA_DIR) else []:
        dataset_path = DATA_DIR / dataset
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
            
    return True 