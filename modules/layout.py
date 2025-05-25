import streamlit as st
import time
from modules.utils import load_image_from_url, load_svg_as_base64
import random
from modules.router import CHAPTER_LIST  # Import the chapter list from router

def create_sidebar():
    with st.sidebar:
        # Minimalist modern sidebar header with Taj Mahal emblem
        taj_mahal_svg = load_svg_as_base64("data/images/tajmahal.svg")
        
        st.markdown(f"""
        <div style="padding: 1.2rem 0.5rem; text-align: center; background: linear-gradient(135deg, rgba(30,33,41,0.6) 0%, rgba(25,28,36,0.8) 100%); 
             border-radius: 8px; margin-bottom: 1.2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2); 
             backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.08);">
            <img src="{taj_mahal_svg}" style="width: 56px; margin-bottom: 12px; filter: drop-shadow(0 0 8px rgba(255, 153, 51, 0.5));">
            <h1 style="font-size: 1.7rem; font-weight: 600; margin: 0; background: linear-gradient(45deg, #FF9933, #FFC786); 
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; 
                 letter-spacing: -0.2px; text-shadow: 0 2px 8px rgba(255, 153, 51, 0.2);">Journey Chapters</h1>
            <div style="width: 50px; height: 3px; background: linear-gradient(to right, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%); 
                 margin: 12px auto 0; border-radius: 2px;" class="pulse-animation"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Elegant divider with enhanced visual appeal
        st.markdown("""
        <div style="height: 2px; 
             background: linear-gradient(to right, rgba(255,153,51,0.01), rgba(255,153,51,0.3), rgba(19,136,8,0.3), rgba(19,136,8,0.01)); 
             margin: 0.8rem 0 1.8rem 0; border-radius: 2px; box-shadow: 0 1px 5px rgba(0,0,0,0.1);"></div>
        """, unsafe_allow_html=True)
        
        # Check if we need to navigate to a new chapter via button navigation
        initial_index = 0
        if 'navigate_to' in st.session_state and st.session_state.navigate_to is not None:
            # Find the index of the chapter we want to navigate to
            try:
                initial_index = CHAPTER_LIST.index(st.session_state.navigate_to)
                # Reset the navigate_to session state now that we've used it
                st.session_state.navigate_to = None
            except ValueError:
                pass  # If chapter not found, default to first chapter
        
        # Create chapter selection with enhanced styling
        st.markdown("""
        <div style="margin-bottom: 12px; font-size: 0.95rem; color: #FF9933; letter-spacing: 0.8px; font-weight: 600; 
             text-transform: uppercase; display: flex; align-items: center;">
            <span style="background: linear-gradient(135deg, rgba(255,153,51,0.3), rgba(255,153,51,0.1)); 
                 width: 24px; height: 24px; display: flex; justify-content: center; align-items: center; 
                 border-radius: 50%; margin-right: 10px; font-size: 0.8rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                 border: 1px solid rgba(255,153,51,0.3);">📖</span>
            Choose your path
        </div>
        """, unsafe_allow_html=True)
        
        # Create a minimal container for the radio buttons with a subtle background
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(30,33,41,0.3) 0%, rgba(25,28,36,0.4) 100%); 
             border-radius: 8px; padding: 10px 8px 6px; margin-bottom: 12px; 
             box-shadow: 0 2px 10px rgba(0,0,0,0.1); backdrop-filter: blur(10px); 
             -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05);">
        """, unsafe_allow_html=True)
        
        chapter = st.radio(
            "Choose your path",  # Add a label for accessibility
            CHAPTER_LIST,
            key="navigation",
            index=initial_index,
            label_visibility="collapsed"  # Hide label but still provide it for accessibility
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Minimalist chapter selection indicator
        st.markdown(f"""
        <div style='text-align:center; margin: 1rem 0 1.5rem 0;'>
            <span style='background: rgba(30,33,41,0.5); 
                 color:#FFFFFF; padding:8px 16px; border-radius:6px; font-size:0.9rem; letter-spacing: 0.3px; 
                 font-weight: 500; box-shadow: 0 2px 8px rgba(0,0,0,0.15); backdrop-filter: blur(10px); 
                 -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.08);
                 transition: all 0.2s ease; display: inline-block;' class='chapter-indicator'>
                <svg style="width: 14px; height: 14px; margin-right: 6px; vertical-align: -2px; filter: drop-shadow(0 1px 1px rgba(0,0,0,0.1));" 
                     viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9,16.17L4.83,12l-1.42,1.41L9,19 21,7l-1.41-1.41L9,16.17z"/>
                </svg>
                {chapter}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple loading indicator for chapter change
        if 'loaded_chapter' not in st.session_state:
            st.session_state.loaded_chapter = None
            
        if st.session_state.loaded_chapter != chapter:
            with st.spinner(f"Loading {chapter}..."):
                time.sleep(0.2)  # Brief delay for visual feedback
                st.session_state.loaded_chapter = chapter
        
        # Elegant divider with enhanced styling
        st.markdown("""
        <div style="height: 2px; 
             background: linear-gradient(to right, rgba(19,136,8,0.01), rgba(19,136,8,0.3), rgba(255,153,51,0.3), rgba(255,153,51,0.01)); 
             margin: 1.2rem 0 2rem 0; border-radius: 2px; box-shadow: 0 1px 5px rgba(0,0,0,0.1);"></div>
        """, unsafe_allow_html=True)
        
        # About section with minimal typography and styling
        st.markdown("""
        <div style="margin-bottom: 10px; font-size: 0.85rem; color: #FF9933; font-weight: 500; 
             display: flex; align-items: center;">
            <span style="width: 20px; height: 20px; display: flex; justify-content: center; align-items: center; 
                 margin-right: 6px; font-size: 0.8rem;">ℹ️</span>
            About
        </div>
        <p style="font-size: 0.9rem; line-height: 1.6; font-weight: 300; color: #F5F5F5; margin: 10px 0 15px; 
             padding: 0 4px; text-shadow: 0 1px 1px rgba(0,0,0,0.1);">
            Interactive visualization of India's cultural, linguistic, religious, and geographical diversity.
        </p>
        """, unsafe_allow_html=True)
        
        # Add information container with minimal styling
        with st.container():
            st.markdown("""
            <div style="margin-bottom: 15px; background: rgba(30,33,41,0.4);
                 border-radius: 6px; padding: 12px 10px; border: 1px solid rgba(255,255,255,0.05);
                 box-shadow: 0 2px 10px rgba(0,0,0,0.15); backdrop-filter: blur(10px);">
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; padding: 5px;">
                <p style="color: #FAFAFA; margin: 0; font-size: 0.9rem;">Explore India's vibrant cultural tapestry</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick navigation with minimal design
        st.markdown("""
        <div style="height: 1px; 
             background: rgba(255,255,255,0.1); 
             margin: 1rem 0 1rem 0;"></div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-bottom: 10px; font-size: 0.85rem; color: #FF9933; font-weight: 500; 
             display: flex; align-items: center;">
            <span style="width: 20px; height: 20px; display: flex; justify-content: center; align-items: center; 
                 margin-right: 6px; font-size: 0.8rem;">🔍</span>
            Quick Access
        </div>
        """, unsafe_allow_html=True)
        
        # Modern quick access buttons with minimal styling
        st.markdown("""
        <div style="background: rgba(30,33,41,0.4); 
             border-radius: 6px; padding: 10px 8px 6px; margin-bottom: 15px; 
             box-shadow: 0 2px 8px rgba(0,0,0,0.1); backdrop-filter: blur(10px); 
             -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05);">
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        with cols[0]:
            st.button("🏛️", help="Cultural Heritage", key="shortcut_culture", use_container_width=True)
        with cols[1]:
            st.button("🏞️", help="Tourism", key="shortcut_tourism", use_container_width=True) 
        with cols[2]:
            st.button("🔮", help="3D Experience", key="shortcut_3d", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Handle button clicks to change chapter using the navigate_to approach
        if st.session_state.get("shortcut_culture", False):
            st.session_state.navigate_to = "Cultural Heritage"
            st.rerun()
        if st.session_state.get("shortcut_tourism", False):
            st.session_state.navigate_to = "Tourism Highlights"
            st.rerun()
        if st.session_state.get("shortcut_3d", False):
            st.session_state.navigate_to = "Explore India in 3D"
            st.rerun()
        
        # Show favorites in an elegantly styled expander
        if 'favorites' in st.session_state and len(st.session_state.favorites) > 0:
            st.markdown("""
            <div style="height: 2px; 
                 background: linear-gradient(to right, rgba(19,136,8,0.01), rgba(19,136,8,0.3), rgba(255,153,51,0.3), rgba(255,153,51,0.01)); 
                 margin: 1.2rem 0 2rem 0; border-radius: 2px; box-shadow: 0 1px 5px rgba(0,0,0,0.1);"></div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="margin-bottom: 12px; font-size: 0.95rem; color: #FF9933; letter-spacing: 0.8px; font-weight: 600; 
                 text-transform: uppercase; display: flex; align-items: center;">
                <span style="background: linear-gradient(135deg, rgba(255,153,51,0.3), rgba(255,153,51,0.1)); 
                     width: 24px; height: 24px; display: flex; justify-content: center; align-items: center; 
                     border-radius: 50%; margin-right: 10px; font-size: 0.8rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                     border: 1px solid rgba(255,153,51,0.3);">⭐</span>
                Favorites
            </div>
            """, unsafe_allow_html=True)
            
            # Create a styled container for favorites
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(30,33,41,0.5) 0%, rgba(25,28,36,0.7) 100%); 
                 border-radius: 12px; padding: 18px 15px 12px; margin-bottom: 25px; 
                 box-shadow: 0 5px 15px rgba(0,0,0,0.15); backdrop-filter: blur(10px); 
                 -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1);">
            """, unsafe_allow_html=True)
            
            with st.expander("⭐ Favorites", expanded=True):
                for fav_chapter in st.session_state.favorites:
                    if st.button(fav_chapter, key=f"fav_{fav_chapter}", use_container_width=True):
                        st.session_state.navigate_to = fav_chapter
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Recently visited chapters with modern styling
        if 'visited_chapters' in st.session_state and len(st.session_state.visited_chapters) > 1:  # More than current
            st.markdown("""
            <div style="height: 2px; 
                 background: linear-gradient(to right, rgba(255,153,51,0.01), rgba(255,153,51,0.3), rgba(19,136,8,0.3), rgba(19,136,8,0.01)); 
                 margin: 1.2rem 0 2rem 0; border-radius: 2px; box-shadow: 0 1px 5px rgba(0,0,0,0.1);"></div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="margin-bottom: 12px; font-size: 0.95rem; color: #FF9933; letter-spacing: 0.8px; font-weight: 600; 
                 text-transform: uppercase; display: flex; align-items: center;">
                <span style="background: linear-gradient(135deg, rgba(255,153,51,0.3), rgba(255,153,51,0.1)); 
                     width: 24px; height: 24px; display: flex; justify-content: center; align-items: center; 
                     border-radius: 50%; margin-right: 10px; font-size: 0.8rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
                     border: 1px solid rgba(255,153,51,0.3);">🕒</span>
                Recently Visited
            </div>
            """, unsafe_allow_html=True)
            
            # Only show recent 5 chapters other than current
            recent_chapters = [ch for ch in st.session_state.visited_chapters if ch != chapter][-5:]
            
            if recent_chapters:
                # Create a styled container for recently visited
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(30,33,41,0.5) 0%, rgba(25,28,36,0.7) 100%); 
                     border-radius: 12px; padding: 18px 15px 12px; margin-bottom: 25px; 
                     box-shadow: 0 5px 15px rgba(0,0,0,0.15); backdrop-filter: blur(10px); 
                     -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1);">
                """, unsafe_allow_html=True)
                
                with st.expander("🕒 Recently Visited", expanded=False):
                    for recent_ch in recent_chapters:
                        if st.button(recent_ch, key=f"recent_{recent_ch}", use_container_width=True):
                            st.session_state.navigate_to = recent_ch
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Add a random fact with enhanced card design
        india_facts = [
            "India has the world's largest postal network with over 155,000 post offices.",
            "Chess was invented in India around the 6th century AD.",
            "India's film industry, Bollywood, produces over 1,000 films annually.",
            "The concept of zero originated in India by mathematician Aryabhata.",
            "India has 36 UNESCO World Heritage Sites.",
            "Sanskrit is considered the mother of all European languages.",
            "India has the second largest population of English speakers after the USA.",
            "The 'Indian Railways' is the world's 8th largest employer.",
            "India is the world's largest democracy.",
            "The Kumbh Mela festival is the largest peaceful gathering on Earth."
        ]
        
        st.markdown("""
        <div style="height: 2px; 
             background: linear-gradient(to right, rgba(19,136,8,0.01), rgba(19,136,8,0.3), rgba(255,153,51,0.3), rgba(255,153,51,0.01)); 
             margin: 1.2rem 0 2rem 0; border-radius: 2px; box-shadow: 0 1px 5px rgba(0,0,0,0.1);"></div>
        """, unsafe_allow_html=True)
        
        if 'random_fact' not in st.session_state:
            st.session_state.random_fact = random.choice(india_facts)
            
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(255,153,51,0.2) 0%, rgba(255,153,51,0.1) 100%); 
             padding:22px; border-radius:16px; margin-top: 1.5rem; box-shadow: 0 8px 25px rgba(0,0,0,0.2); 
             backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); border: 1px solid rgba(255,153,51,0.3);
             transform: translateY(0); transition: transform 0.3s ease; animation: cardFloat 3s ease-in-out infinite alternate;'>
            <div style='font-size:1rem; letter-spacing: 0.5px; font-weight: 600; color: #FF9933; margin-bottom: 15px; 
                 display: flex; align-items: center; text-shadow: 0 1px 2px rgba(0,0,0,0.2);'>
                <span style='margin-right: 10px; font-size: 1.3rem; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));'>🪔</span> DID YOU KNOW?
            </div>
            <p style='font-size:1.05rem; line-height: 1.7; font-weight: 300; color: #FAFAFA; margin: 0; 
                 border-left: 3px solid rgba(255,153,51,0.7); padding-left: 15px; text-shadow: 0 1px 2px rgba(0,0,0,0.1);'>
                {st.session_state.random_fact}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced footer with floating animation
        st.markdown("""
        <style>
        @keyframes footerFloat {
            0% { transform: translateY(0); }
            100% { transform: translateY(-5px); }
        }
        @keyframes cardFloat {
            0% { transform: translateY(0); }
            100% { transform: translateY(-8px); }
        }
        </style>
        
        <div style='position: absolute; bottom: 20px; left: 0; right: 0; padding: 18px; text-align: center; 
             animation: footerFloat 3s ease-in-out infinite alternate;'>
            <div style="width: 50px; height: 4px; background: linear-gradient(to right, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%); 
                 margin: 0 auto 15px; border-radius: 3px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);" class="pulse-animation"></div>
            <div style='font-size: 0.9rem; color: #BBB; letter-spacing: 0.5px; font-weight: 500; text-shadow: 0 1px 2px rgba(0,0,0,0.2);'>
                🇮🇳 Made with pride in India
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    return chapter

def create_main_header():
    """Creates the impressive main header for the website - used on the introduction page"""
    # Set the Matplotlib style to work well with dark theme
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
    
    # Animated loading screen with progress bar for initial app load
    progress_bar = st.progress(0)
    with st.spinner("Loading Incredible India experience..."):
        for percent_complete in range(100):
            time.sleep(0.003)  # Use a shorter delay
            progress_bar.progress(percent_complete + 1)
    progress_bar.empty()  # Remove progress bar when done
    
    # Enhanced header with animated pulsing tricolor bar
    st.markdown("<div class='tricolor-bar animated-bar pulse-animation'></div>", unsafe_allow_html=True)
    
    # Load the flambeau SVG image
    flambeau_svg = load_svg_as_base64("data/images/flambeau.svg")
    
    # Create visually striking header with flambeau on both sides and title in middle
    header_cols = st.columns([1, 3, 1])
    
    # Left flambeau
    with header_cols[0]:
        if flambeau_svg:
            st.markdown(f"""
            <div class='emblem-container rotating-emblem' style="background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; padding: 0; display: flex; align-items: center; justify-content: center; height: 130px; margin: 0; position: relative; top: -5px;">
                <img src='{flambeau_svg}' class='india-emblem flambeau-left' style="width: 100%; max-width: 85px; filter: drop-shadow(0 0 6px rgba(255, 153, 51, 0.4)); position: relative; top: 1px;">
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback if SVG loading fails
            st.markdown("""
            <div class='emblem-container rotating-emblem'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg' class='india-emblem' style="width: 100%; max-width: 85px;">
            </div>
            """, unsafe_allow_html=True)
    
    # Middle title
    with header_cols[1]:
        st.markdown("""
        <div class='title-container' style="text-align: center;">
            <h1 class='incredible-india-header'>Incredible India</h1>
            <p class='subtitle fade-in-text'>A Data-Driven Journey Through India's Diversity</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Right flambeau
    with header_cols[2]:
        if flambeau_svg:
            st.markdown(f"""
            <div class='emblem-container rotating-emblem' style="background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; padding: 0; display: flex; align-items: center; justify-content: center; height: 130px; margin: 0; position: relative; top: -5px;">
                <img src='{flambeau_svg}' class='india-emblem flambeau-right' style="width: 100%; max-width: 85px; filter: drop-shadow(0 0 6px rgba(255, 153, 51, 0.4)); position: relative; top: 1px; transform: scaleX(-1);">
            </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback if SVG loading fails
            st.markdown("""
            <div class='emblem-container rotating-emblem'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg' class='india-emblem' style="width: 100%; max-width: 85px;">
            </div>
            """, unsafe_allow_html=True)
    
    # Bottom tricolor bar with animation
    st.markdown("<div class='tricolor-bar animated-bar pulse-animation'></div>", unsafe_allow_html=True)
    
    # Add a dynamic banner with parallax effect and enhanced styling
    st.markdown("""
    <div class='discover-section'>
        <h2 class='discover-heading'>Discover the Wonder that is India</h2>
        <p class='discover-subheading'>Experience the vibrant colors, rich traditions, and ancient wisdom of the world's largest democracy</p>
        <div class='experience-buttons'>
            <div class='experience-button'>One Land</div>
            <div class='experience-button'>Many Worlds</div>
            <div class='experience-button'>Infinite Experiences</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add an elegant quote with decorative elements
    st.markdown("""
    <div class='quote-box shine-border' style="margin: 1rem 0 1rem;">
        <div class='quote-marks'>"</div>
        <div class='quote-content'>
            India is not a nation, nor a country. It is a subcontinent of nationalities.
            <span style='display:block; text-align:right; margin-top:1rem; font-size: 1rem; color: #FF9933;'>— Jawaharlal Nehru</span>
        </div>
        <div class='quote-marks closing-quote'>"</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a visually impressive statistics banner with reduced spacing
    st.markdown("<div class='stats-banner' style='margin: 1.5rem 0 1.5rem;'>", unsafe_allow_html=True)
    stats_cols = st.columns(4)
    
    with stats_cols[0]:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-icon'>🏰</div>
            <div class='stat-value'>40</div>
            <div class='stat-label'>UNESCO Heritage Sites</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[1]:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-icon'>🗣️</div>
            <div class='stat-value'>22</div>
            <div class='stat-label'>Official Languages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[2]:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-icon'>💃</div>
            <div class='stat-value'>8</div>
            <div class='stat-label'>Classical Dance Forms</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stats_cols[3]:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-icon'>🎭</div>
            <div class='stat-value'>3000+</div>
            <div class='stat-label'>Craft Traditions</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def create_chapter_header(chapter_name):
    """Creates a minimal but visually appealing header for non-introduction chapters"""
    # Add minimal chapter header with tricolor accent
    st.markdown("<div class='mini-tricolor-bar'></div>", unsafe_allow_html=True)
    
    # Create compact header with elegant styling
    st.markdown(f"""
    <div class='chapter-header-container'>
        <div class='chapter-header-logo'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg' class='mini-emblem'>
        </div>
        <div class='chapter-header-content'>
            <h1 class='chapter-title'>{chapter_name}</h1>
            <p class='chapter-subtitle'>Incredible India</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add bottom separator
    st.markdown("<div class='mini-tricolor-bar'></div>", unsafe_allow_html=True)
    
    # Add chapter navigation breadcrumb
    st.markdown(f"""
    <div class='breadcrumb-container'>
        <div class='breadcrumb-path'>
            <a href='#' class='breadcrumb-link'>Home</a>
            <span class='breadcrumb-separator'>›</span>
            <span class='breadcrumb-current'>{chapter_name}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_header(chapter_name=None):
    """
    Creates the appropriate header based on the chapter
    If chapter_name is None or 'Introduction', creates the main header,
    otherwise creates a minimal chapter header
    """
    if chapter_name is None or chapter_name == "Introduction":
        create_main_header()
    else:
        create_chapter_header(chapter_name)

def create_footer():
    # Add an impressive wave separator above footer
    st.markdown("""
    <div class='footer-wave-separator'>
        <svg viewBox='0 0 1200 120' preserveAspectRatio='none'>
            <path d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='#FF9933'/>
            <path d='M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z' opacity='.5' fill='#138808'/>
            <path d='M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z' fill='#FFFFFF'/>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    
    # Add an enhanced footer with multiple sections and visual improvements
    st.markdown("<div class='footer-container'>", unsafe_allow_html=True)
    
    # Create footer columns with better arrangement
    footer_cols = st.columns([2, 1, 1])
    
    # About section with animated elements
    with footer_cols[0]:
        st.markdown("""
        <div class='footer-section'>
            <h3 class='footer-heading'>About CodeYatra</h3>
            <p class='footer-text'>
                Discover India's rich cultural heritage, traditions, and diversity through 
                interactive data visualizations. Our platform offers a comprehensive journey through 
                the many facets of incredible India.
            </p>
            <div class='social-icons'>
                <a href="#" class='social-icon' aria-label="Facebook">
                    <i class="fab fa-facebook-f"></i>
                </a>
                <a href="#" class='social-icon' aria-label="Instagram">
                    <i class="fab fa-instagram"></i>
                </a>
                <a href="#" class='social-icon' aria-label="Twitter">
                    <i class="fab fa-twitter"></i>
                </a>
                <a href="#" class='social-icon' aria-label="LinkedIn">
                    <i class="fab fa-linkedin-in"></i>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick links with hover effects
    with footer_cols[1]:
        st.markdown("""
        <div class='footer-section'>
            <h3 class='footer-heading'>Quick Links</h3>
            <ul class='footer-links'>
                <li><a href="#" class="animated-link">Home</a></li>
                <li><a href="#" class="animated-link">Culture</a></li>
                <li><a href="#" class="animated-link">Education</a></li>
                <li><a href="#" class="animated-link">Tourism</a></li>
                <li><a href="#" class="animated-link">History</a></li>
                <li><a href="#" class="animated-link">Gallery</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact info with interactive elements
    with footer_cols[2]:
        st.markdown("""
        <div class='footer-section'>
            <h3 class='footer-heading'>Contact Us</h3>
            <p class='footer-text contact-item'><i class="fas fa-envelope"></i> info@codeyatra.org</p>
            <p class='footer-text contact-item'><i class="fas fa-globe"></i> www.codeyatra.org</p>
            <div class='footer-badge pulsing'>
                <p>Made with ❤️ in India</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Copyright section with improved styling
    st.markdown("""
    <div class='copyright-section'>
        <div class='tricolor-bar animated-bar'></div>
        <div class='copyright-content'>
            <p>© 2023-2024 CodeYatra India Data Story. All rights reserved.</p>
            <div class='copyright-links'>
                <a href="#" class="footer-policy-link">Privacy Policy</a>
                <span class="footer-link-separator">|</span>
                <a href="#" class="footer-policy-link">Terms of Service</a>
                <span class="footer-link-separator">|</span>
                <a href="https://streamlit.io" target="_blank" class="footer-policy-link">Powered by Streamlit</a>
            </div>
        </div>
        <div class='tricolor-bar animated-bar'></div>
    </div>
    """, unsafe_allow_html=True) 