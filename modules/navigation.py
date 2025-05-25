import streamlit as st
from modules.router import CHAPTER_LIST

# Dictionary mapping chapters to their icons
CHAPTER_ICONS = {
    "Introduction": "🏠",
    "Linguistic Diversity": "🗣️",
    "Religious Mosaic": "🕉️",
    "Cultural Heritage": "🏛️",
    "Festivals of India": "🪔",
    "Geographical Diversity": "🏞️",
    "Historical Timeline": "⏳",
    "Tourism Highlights": "🧳",
    "Education Landscape": "🎓",
    "Modern India": "🏙️",
    "Image Gallery": "📷"
}

def create_top_navigation():
    """Creates a modern top navigation bar using st.navigation"""
    
    # Define the Pages using the latest Streamlit navigation API
    pages = {}
    
    # Group chapters into logical sections
    discover_section = ["Introduction", "Linguistic Diversity", "Religious Mosaic"]
    explore_section = ["Cultural Heritage", "Festivals of India", "Geographical Diversity", "Historical Timeline"]
    engage_section = ["Tourism Highlights", "Education Landscape", "Modern India", "Image Gallery"]
    
    # Create Page objects for each section
    discover_pages = []
    for chapter in discover_section:
        if chapter in CHAPTER_LIST:
            # Create a Page that's actually a function that sets navigation target
            page = st.Page(
                lambda c=chapter: st.session_state.update({"navigate_to": c, "rerun": True}),
                title=chapter,
                icon=CHAPTER_ICONS.get(chapter, "📄")
            )
            discover_pages.append(page)
    
    explore_pages = []
    for chapter in explore_section:
        if chapter in CHAPTER_LIST:
            page = st.Page(
                lambda c=chapter: st.session_state.update({"navigate_to": c, "rerun": True}),
                title=chapter,
                icon=CHAPTER_ICONS.get(chapter, "📄")
            )
            explore_pages.append(page)
    
    engage_pages = []
    for chapter in engage_section:
        if chapter in CHAPTER_LIST:
            page = st.Page(
                lambda c=chapter: st.session_state.update({"navigate_to": c, "rerun": True}),
                title=chapter,
                icon=CHAPTER_ICONS.get(chapter, "📄")
            )
            engage_pages.append(page)
    
    # Define the navigation structure
    navigation = {
        "Discover": discover_pages,
        "Explore": explore_pages, 
        "Engage": engage_pages
    }
    
    # Create the navigation component
    nav = st.navigation(navigation)
    
    # Run the navigation
    nav.run()
    
    # Check if we need to rerun to navigate
    if st.session_state.get("rerun", False):
        st.session_state.rerun = False
        st.rerun()
    
    # Return the current chapter name
    return st.session_state.get("current_chapter", "Introduction")

def create_responsive_top_links():
    """Creates clickable page links in a responsive horizontal layout"""
    
    # Create a more responsive horizontal layout
    cols = st.columns(len(CHAPTER_LIST))
    
    # Add page links for each chapter
    for i, chapter in enumerate(CHAPTER_LIST):
        with cols[i]:
            st.page_link(
                "app.py",  # Base app path
                label=CHAPTER_ICONS.get(chapter, "📄"),
                icon=None,  # Already showing icon in label
                help=chapter,  # Show chapter name on hover
                use_container_width=True
            )
            
    # Return the current chapter name
    return st.session_state.get("current_chapter", "Introduction") 