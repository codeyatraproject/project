# Main app entry point - modular version
import streamlit as st
import os
import sys
import traceback
from modules.config import init_config
from modules.styles import load_css
from modules.layout import create_sidebar, create_header, create_footer
from modules.router import render_chapter
from modules.utils import preload_data

# Error handling function
def handle_error(e, critical=False):
    """Handle errors with appropriate messages based on severity"""
    if critical:
        st.error("Critical application error")
    
    st.error(f"An error occurred: {str(e)}")
    
    if os.environ.get('STREAMLIT_DEBUG', 'false').lower() == 'true':
        st.error(traceback.format_exc())
    
    st.warning("Please try refreshing the page or contact support.")
    
    # Track error count for better user guidance
    if 'error_count' in st.session_state:
        st.session_state.error_count += 1
        
        # If multiple errors occur, provide additional guidance
        if st.session_state.error_count > 2:
            st.warning("Multiple errors detected. Try clearing your browser cache or using incognito mode.")

# Set page configuration
try:
    st.set_page_config(
        page_title="Incredible India | A Data-Driven Journey",
        page_icon="🇮🇳",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "# Incredible India\nA data-driven journey through India's diverse cultural landscape.",
            'Get Help': 'https://github.com/yourusername/codeyatra',
            'Report a bug': "https://github.com/yourusername/codeyatra/issues",
        }
    )
except Exception as e:
    st.error(f"Error in page configuration: {str(e)}")
    sys.exit(1)

try:
    # Initialize app configuration and session state
    init_config()

    # Load CSS styles
    load_css()
    
    # Preload common datasets for better performance
    # Only preload on first load or when data_loaded is False
    if not st.session_state.get('data_loaded', False):
        # Get the current chapter to determine which datasets to load upfront
        current_chapter = st.session_state.get('current_chapter', 'Introduction')
        
        # Map chapters to required datasets for smarter preloading
        chapter_datasets = {
            'Introduction': ['population', 'state'],
            'Linguistic Diversity': ['linguistic', 'state'],
            'Religious Mosaic': ['religious', 'state'],
            'Cultural Heritage': ['cultural', 'state'],
            'Festivals of India': ['festivals', 'state'],
            'Geographical Diversity': ['geography', 'state'],
            'Historical Timeline': ['historical'],
            'Tourism Highlights': ['tourism'],
            'Education Landscape': ['education', 'state'],
            'Modern India': ['economic', 'population']
        }
        
        # Get datasets for the current chapter and preload them
        datasets_to_load = chapter_datasets.get(current_chapter, []) + ['state']  # Always load state data
        if datasets_to_load:
            st.session_state['preloaded_data'] = preload_data(datasets_to_load)
            st.session_state.data_loaded = True

    # Create a loading state for better user experience
    with st.spinner("Loading the Incredible India experience..."):
        # Create sidebar and get selected chapter
        selected_chapter = create_sidebar()
        
        # Main content area
        main_container = st.container()
        
        with main_container:
            # Create header with chapter information
            create_header(selected_chapter)
            
            # Render the selected chapter
            render_chapter(selected_chapter)
            
            # Add footer
            create_footer()

except Exception as e:
    handle_error(e, critical=True)