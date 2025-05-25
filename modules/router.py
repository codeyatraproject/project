import streamlit as st
from modules.chapters import introduction, linguistic_diversity, religious_mosaic, cultural_heritage, geographical_diversity, modern_india
from modules.chapters import festivals_india, historical_timeline, tourism_highlights, education_landscape

# Define a mapping of chapter names to their render functions
CHAPTER_MAPPING = {
    "Introduction": introduction.render,
    "Linguistic Diversity": linguistic_diversity.render,
    "Religious Mosaic": religious_mosaic.render,
    "Cultural Heritage": cultural_heritage.render,
    "Festivals of India": festivals_india.render,
    "Geographical Diversity": geographical_diversity.render,
    "Historical Timeline": historical_timeline.render,
    "Tourism Highlights": tourism_highlights.render,
    "Education Landscape": education_landscape.render,
    "Modern India": modern_india.render
}

# Maintain the same chapter order for navigation
CHAPTER_LIST = [
    "Introduction", "Linguistic Diversity", "Religious Mosaic", "Cultural Heritage", 
    "Festivals of India", "Geographical Diversity", "Historical Timeline", 
    "Tourism Highlights", "Education Landscape", "Modern India"
]

# Function to get next and previous chapter navigation
def get_chapter_navigation(current_chapter):
    """
    Returns the previous and next chapter names based on the current chapter
    
    Args:
        current_chapter (str): The name of the current chapter
    
    Returns:
        tuple: (previous_chapter, next_chapter) - names of the previous and next chapters
               If there is no previous/next chapter, returns None for that position
    """
    try:
        current_index = CHAPTER_LIST.index(current_chapter)
        
        # Get previous chapter (if not first chapter)
        previous_chapter = CHAPTER_LIST[current_index - 1] if current_index > 0 else None
        
        # Get next chapter (if not last chapter)
        next_chapter = CHAPTER_LIST[current_index + 1] if current_index < len(CHAPTER_LIST) - 1 else None
        
        return previous_chapter, next_chapter
    except ValueError:
        # If the current chapter is not in the list (shouldn't happen)
        return None, None

def render_chapter(chapter_name):
    """Renders the appropriate chapter based on the selected name"""
    
    # Store current chapter name in session state for reference by other components
    if 'current_chapter' not in st.session_state:
        st.session_state.current_chapter = chapter_name
    else:
        st.session_state.current_chapter = chapter_name
    
    # Track visited chapters
    if 'visited_chapters' in st.session_state:
        st.session_state.visited_chapters.add(chapter_name)
    
    # Render the chapter content
    chapter_container = st.container()
    with chapter_container:
        if chapter_name in CHAPTER_MAPPING:
            CHAPTER_MAPPING[chapter_name]()
        else:
            st.error(f"Unknown chapter: {chapter_name}")
    
    # Add navigation buttons after rendering the chapter
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create a container for the navigation section
    nav_container = st.container()
    
    with nav_container:
        # Get chapter list and current index
        total_chapters = len(CHAPTER_LIST)
        try:
            current_index = CHAPTER_LIST.index(chapter_name) + 1
        except ValueError:
            current_index = -1
        
        # Add favorite button and chapter info
        favorite_col, info_col = st.columns([1, 5])
        
        with favorite_col:
            # Add ability to favorite a chapter
            if 'favorites' in st.session_state:
                is_favorite = chapter_name in st.session_state.favorites
                
                if st.button("★" if is_favorite else "☆", key="favorite_btn", help="Add to favorites"):
                    if is_favorite:
                        st.session_state.favorites.remove(chapter_name)
                    else:
                        st.session_state.favorites.add(chapter_name)
                    st.rerun()
                
        with info_col:
            # Show visited status
            visited_count = len(st.session_state.visited_chapters) if 'visited_chapters' in st.session_state else 0
            visited_percent = int((visited_count / total_chapters) * 100)
            
            if visited_count == total_chapters:
                st.success(f"🎉 You've visited all {total_chapters} chapters! Well done!")
            else:
                st.info(f"You've visited {visited_count} of {total_chapters} chapters ({visited_percent}% complete)")
        
        # Add a subtle divider
        st.divider()
        
        # Get previous and next chapters
        prev_chapter, next_chapter = get_chapter_navigation(chapter_name)
        
        # Create columns for navigation buttons with Apple-inspired styling
        col1, col2, col3 = st.columns([1, 2, 1])
        
        # Initialize navigate_to in session state if it doesn't exist
        if 'navigate_to' not in st.session_state:
            st.session_state.navigate_to = None
        
        # Previous chapter button (left-aligned) with Apple-style
        with col1:
            if prev_chapter:
                if st.button("« Previous", key="prev_chapter_btn"):
                    # Instead of directly modifying the widget value, store the target chapter name
                    st.session_state.navigate_to = prev_chapter
                    st.rerun()
        
        # Center area - with Apple-style chapter indicator
        with col2:
            st.markdown(f"""
            <div style='text-align: center;'>
                <div style='color: #999; font-size: 0.8rem; margin-bottom: 5px; font-weight: 300; letter-spacing: 0.5px;'>CHAPTER {current_index} OF {total_chapters}</div>
                <div style='color: #FF9933; font-size: 0.95rem; font-weight: 500;'>{chapter_name}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Next chapter button (right-aligned) with Apple-style
        with col3:
            if next_chapter:
                if st.button("Next »", key="next_chapter_btn"):
                    # Instead of directly modifying the widget value, store the target chapter name
                    st.session_state.navigate_to = next_chapter
                    st.rerun()
        
        # Add a Streamlit-native progress bar for chapter navigation
        if current_index > 0:
            progress_percentage = current_index / total_chapters
            # Use Streamlit's native progress bar
            st.progress(progress_percentage)
            
            # Add chapter exploration status text
            if current_index < total_chapters:
                remaining = total_chapters - current_index
                st.caption(f"You've explored {current_index} chapters. {remaining} more to go!") 