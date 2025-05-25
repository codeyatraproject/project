import streamlit as st


def load_css():
    # Add all CSS styles in a more organized way
    
    # Import fonts and base styles
    base_styles = """
    /* Modern font improvements */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #FAFAFA;
        -webkit-font-smoothing: antialiased;
        letter-spacing: -0.01em;
    }

    /* Override Streamlit's default styling for cleaner UI */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Clean up streamlit header/footer */
    header {
        background-color: rgba(14,17,23,0.8) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    
    footer {
        visibility: hidden;
    }
    
    /* Hide hamburger menu, it's distracting */
    .st-emotion-cache-1egq4bb {
        visibility: hidden;
    }

    /* Cleaner buttons */
    .stButton > button {
        background-color: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 4px;
        color: white;
        padding: 0.25rem 1rem;
        font-size: 0.85rem;
    }
    
    .stButton > button:hover {
        background-color: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    """
    
    # Responsive design fixes
    responsive_styles = """
    /* Fix for mobile responsiveness */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem !important;
        }
        .subtitle {
            font-size: 1.3rem !important;
        }
        .story-text {
            font-size: 1rem !important;
            text-align: left !important;
        }
        .stat-card {
            padding: 10px !important;
        }
        .data-insight {
            font-size: 0.9rem !important;
            padding: 10px !important;
        }
    }
    """
    
    # Animation styles
    animation_styles = """
    /* Apple-style loading animation */
    .loader {
        border: 2px solid rgba(30, 33, 41, 0.3);
        border-radius: 50%;
        border-top: 2px solid #FF9933;
        width: 24px;
        height: 24px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Fade-in animation for content */
    .fade-in {
        animation: fadeIn 0.8s ease forwards;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Pulse animation for tricolor bar */
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 153, 51, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(255, 153, 51, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 153, 51, 0); }
    }
    """
    
    # UI component styles
    component_styles = """
    /* Navigation button styles - Apple-inspired */
    .stButton > button {
        background-color: rgba(19, 136, 8, 0.1);
        color: #FAFAFA;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 0.9rem;
        font-weight: 500;
        letter-spacing: 0.3px;
        transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        width: 100%;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        position: relative;
        z-index: 1;
    }
    
    .stButton > button:hover {
        background-color: rgba(255, 153, 51, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        background-color: rgba(255, 153, 51, 0.4);
    }
    
    /* Apple-style tricolor bar */
    .tricolor-bar {
        height: 3px;
        background: linear-gradient(to right, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%);
        margin-bottom: 10px;
        border-radius: 2px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        position: relative;
        z-index: 1;
    }
    
    /* Radio buttons - Apple style */
    .stRadio [data-baseweb="radio"] {
        color: #FAFAFA !important;
        transition: all 0.2s ease;
    }
    
    .stRadio [data-baseweb="radio"] div:first-child {
        border-color: rgba(255, 153, 51, 0.5) !important;
        transition: all 0.2s ease;
    }
    
    .stRadio [data-baseweb="radio"][aria-checked="true"] div:first-child {
        border-color: #FF9933 !important;
        border-width: 2px !important;
    }
    
    .stRadio [data-baseweb="radio"][aria-checked="true"] div:nth-child(2) {
        background-color: #FF9933 !important;
        transform: scale(0.7) !important;
    }
    """
    
    # Typography styles
    typography_styles = """
    /* Main title styles - Apple inspired */
    .main-title {
        font-size: 3.8rem;
        font-weight: 600;
        color: #FF9933;
        text-align: center;
        margin-bottom: 0.7rem;
        padding-top: 10px;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #FF9933, #FFC786);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 2;
        text-shadow: 0 2px 10px rgba(255, 153, 51, 0.3);
        animation: titleGlow 3s infinite alternate;
    }
    
    @keyframes titleGlow {
        0% { text-shadow: 0 0 5px rgba(255, 153, 51, 0.3); }
        100% { text-shadow: 0 0 15px rgba(255, 153, 51, 0.6); }
    }
    
    /* Enhanced Incredible India header with 3D effect */
    .incredible-india-header {
        font-size: 3.2rem;
        font-weight: 700;
        text-align: center;
        margin: 0.8rem 0 0.6rem;
        background: linear-gradient(45deg, #FF9933, #FFBF00, #FF9933);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient 5s ease infinite;
        text-shadow: 0 5px 15px rgba(255, 153, 51, 0.2);
        letter-spacing: -0.5px;
        transform: perspective(500px) rotateX(5deg);
        padding: 0.2rem 0;
        position: relative;
    }
    
    .title-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 130px;
        padding: 0;
        position: relative;
        top: -5px;
    }
    
    .india-emblem {
        width: 120px;
        height: auto;
        filter: drop-shadow(0px 0px 8px rgba(255, 153, 51, 0.5));
        transition: all 0.3s ease;
    }
    
    /* Flambeau SVG styling */
    .flambeau-left, .flambeau-right {
        filter: invert(1) brightness(1.5) drop-shadow(0px 0px 8px rgba(255, 153, 51, 0.7));
        transition: all 0.5s ease;
    }
    
    .flambeau-left:hover, .flambeau-right:hover {
        filter: invert(1) brightness(1.5) drop-shadow(0px 0px 12px rgba(255, 153, 51, 1));
        transform: scale(1.05);
    }
    
    .flambeau-left {
        animation: flambeauGlowLeft 3s infinite alternate;
    }
    
    .flambeau-right {
        animation: flambeauGlowRight 3s infinite alternate;
    }
    
    @keyframes flambeauGlowLeft {
        0% { filter: invert(1) brightness(1.5) drop-shadow(0px 0px 5px rgba(255, 153, 51, 0.5)); transform: rotate(-2deg); }
        100% { filter: invert(1) brightness(1.5) drop-shadow(0px 0px 12px rgba(255, 153, 51, 0.8)); transform: rotate(2deg); }
    }
    
    @keyframes flambeauGlowRight {
        0% { filter: invert(1) brightness(1.5) drop-shadow(0px 0px 5px rgba(255, 153, 51, 0.5)); transform: scaleX(-1) rotate(2deg); }
        100% { filter: invert(1) brightness(1.5) drop-shadow(0px 0px 12px rgba(255, 153, 51, 0.8)); transform: scaleX(-1) rotate(-2deg); }
    }
    
    .incredible-india-header::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 50%;
        height: 3px;
        background: linear-gradient(to right, rgba(255, 153, 51, 0), rgba(255, 153, 51, 0.7), rgba(255, 153, 51, 0));
        border-radius: 3px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Enhanced subtitle style */
    .subtitle {
        font-size: 1.7rem;
        font-weight: 300;
        color: #FAFAFA;
        text-align: center;
        margin-top: 0;
        margin-bottom: 1.5rem;
        letter-spacing: 0.2px;
        line-height: 1.3;
        position: relative;
        z-index: 2;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    /* Discover section styling with enhanced effects */
    .discover-section {
        background: linear-gradient(135deg, rgba(35, 35, 45, 0.7) 0%, rgba(20, 20, 30, 0.8) 100%);
        border-radius: 15px;
        padding: 1.8rem 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), 0 0 30px rgba(255, 153, 51, 0.1);
        border: 1px solid rgba(255, 153, 51, 0.2);
        text-align: center;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
        animation: subtlePulse 5s infinite alternate;
    }
    
    @keyframes subtlePulse {
        0% {
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), 0 0 30px rgba(255, 153, 51, 0.1);
        }
        100% {
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), 0 0 50px rgba(255, 153, 51, 0.2);
        }
    }
    
    .discover-section::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(to right, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%);
        z-index: 2;
    }
    
    .discover-section::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(to right, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%);
        z-index: 2;
    }
    
    .discover-heading {
        font-size: 2.2rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 1rem;
        letter-spacing: -0.3px;
        background: linear-gradient(135deg, #FFFFFF, #F5F5F5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px 10px rgba(255, 255, 255, 0.2);
    }
    
    .discover-subheading {
        font-size: 1.2rem;
        font-weight: 300;
        color: #F0F0F0;
        margin-bottom: 1.5rem;
        letter-spacing: 0.2px;
        line-height: 1.5;
        max-width: 80%;
        margin-left: auto;
        margin-right: auto;
    }
    
    .experience-buttons {
        display: flex;
        justify-content: center;
        gap: 1.2rem;
        margin-top: 1.2rem;
        flex-wrap: wrap;
    }
    
    .experience-button {
        background-color: rgba(255, 153, 51, 0.15);
        color: #FF9933;
        padding: 0.6rem 1.2rem;
        border-radius: 30px;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        border: 1px solid rgba(255, 153, 51, 0.3);
        cursor: pointer;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        position: relative;
        overflow: hidden;
        z-index: 1;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        min-width: 120px;
        text-align: center;
    }
    
    .experience-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, rgba(255, 153, 51, 0.1), rgba(255, 153, 51, 0.3));
        z-index: -1;
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
    }
    
    .experience-button:hover {
        background-color: rgba(255, 153, 51, 0.25);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(255, 153, 51, 0.2);
        color: #FFF;
    }
    
    .experience-button:hover::before {
        transform: scaleX(1);
    }
    
    .experience-button:active {
        transform: translateY(-1px);
        box-shadow: 0 3px 10px rgba(255, 153, 51, 0.1);
    }
    
    /* Chapter heading styles */
    .chapter-heading {
        font-size: 2.5rem;
        font-weight: 500;
        color: #FF9933;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
        border-bottom: 1px solid rgba(255, 153, 51, 0.2);
        padding-bottom: 0.8rem;
    }
    
    /* Section heading styles */
    .section-heading {
        font-size: 1.8rem;
        font-weight: 500;
        color: #FFFFFF;
        margin-top: 2rem;
        margin-bottom: 1rem;
        letter-spacing: -0.3px;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 153, 51, 0.15);
    }
    
    /* Story text styling */
    .story-text {
        font-size: 1.1rem;
        line-height: 1.7;
        letter-spacing: 0.2px;
        color: #EAEAEA;
        font-weight: 300;
        margin-bottom: 1.5rem;
    }
    
    /* Data insight boxes */
    .data-insight {
        background-color: rgba(19, 136, 8, 0.15);
        padding: 15px 20px;
        border-radius: 8px;
        border-left: 3px solid #138808;
        font-size: 1rem;
        color: #FAFAFA;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    """
    
    # Card and container styles
    container_styles = """
    /* Improved sidebar styling for Apple-like feel */
    .stSidebar {
        background-color: rgba(30, 33, 41, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 999;
        position: relative;
    }
    
    /* Chapter indicator styles - Apple inspired */
    .chapter-indicator {
        text-align: center;
        color: #AAAAAA;
        font-size: 0.85rem;
        margin: 0 auto;
        padding: 8px 15px;
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        letter-spacing: 0.5px;
        z-index: 1;
        position: relative;
    }
    
    /* Apple-like cards */
    .stat-card {
        text-align: center;
        padding: 20px;
        transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
        background-color: rgba(30, 33, 41, 0.7);
        border-radius: 12px;
        border: none;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        position: relative;
        z-index: 1;
    }
    
    .hoverable:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        background-color: rgba(255, 153, 51, 0.15);
    }
    
    /* Chart container styling */
    .chart-container {
        background-color: rgba(14, 17, 23, 0.5);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin: 1rem 0 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    """

    # Combine all style sections
    all_styles = "\n".join([
        "<style>",
        base_styles,
        responsive_styles,
        animation_styles,
        component_styles,
        typography_styles,
        container_styles,
        "</style>"
    ])
    
    # Apply all styles at once for better performance
    st.markdown(all_styles, unsafe_allow_html=True)

    # Add meta tags for better mobile responsiveness
    st.markdown("""
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    """, unsafe_allow_html=True)

    # Enhanced CSS for better styling and alignment with dark mode compatibility
    st.markdown("""
    <style>
        /* Base styles for dark mode */
        html, body, [class*="st-"] {
            color: #FAFAFA;
        }
        
        /* Main title styles */
        .main-title {
            font-size: 3.8rem;
            font-weight: 700;
            color: #FF9933;
            text-align: center;
            margin-bottom: 0.5rem;
            padding-top: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            background: linear-gradient(45deg, #FF9933, #FFC786);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 1px;
        }
        
        /* For smaller screens */
        @media screen and (max-width: 768px) {
            .main-title {
                font-size: 2.5rem;
            }
        }
        
        .subtitle {
            font-size: 1.7rem;
            color: #FAFAFA;
            text-align: center;
            margin-top: 0;
            margin-bottom: 1rem;
            font-style: italic;
        }
        
        /* For smaller screens */
        @media screen and (max-width: 768px) {
            .subtitle {
                font-size: 1.3rem;
            }
        }
        
        /* Enhanced title container with animations */
        .title-container {
            padding: 10px 0;
            text-align: center;
        }
        
        /* Indian monument styling */
        .emblem-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            margin: 0;
        }
        
        .india-emblem {
            width: 110px;
            height: auto;
            filter: drop-shadow(0px 0px 8px rgba(255, 153, 51, 0.5));
            transition: all 0.3s ease;
        }
        
        /* Color styling for the Taj Mahal SVG */
        .india-emblem g {
            stroke: #FFFFFF !important;
        }
        
        .india-emblem path, .india-emblem rect, .india-emblem line {
            stroke: #FFFFFF;
            stroke-width: 1.5px;
        }
        
        .emblem-container:hover .india-emblem {
            filter: drop-shadow(0px 0px 10px rgba(255, 153, 51, 0.7));
            transform: scale(1.05);
        }
        
        /* Header image container with parallax effect */
        .header-image-container {
            position: relative;
            overflow: hidden;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .image-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.6));
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10;
        }
        
        .image-overlay h2 {
            color: white;
            font-size: 2.5rem;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            padding: 0 20px;
        }
        
        /* Hero banner with enhanced styling */
        .hero-banner-container {
            margin: 30px 0;
            position: relative;
            overflow: hidden;
            border-radius: 15px;
        }
        
        .hero-banner {
            background: linear-gradient(135deg, rgba(255, 153, 51, 0.15) 0%, rgba(19, 136, 8, 0.15) 100%);
            padding: 40px 20px;
            text-align: center;
            position: relative;
            border: 1px solid rgba(255, 153, 51, 0.3);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }
        
        .banner-content {
            position: relative;
            z-index: 2;
        }
        
        .banner-heading {
            color: #FF9933;
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 15px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
            animation: fadeIn 1.2s;
        }
        
        .banner-subheading {
            color: #EEE;
            font-size: 1.3rem;
            font-style: italic;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto 20px;
            animation: fadeIn 1.2s 0.3s both;
        }
        
        .banner-highlight-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 25px;
        }
        
        .banner-highlight {
            background-color: rgba(255, 153, 51, 0.2);
            color: #FFF;
            padding: 8px 20px;
            border-radius: 30px;
            font-size: 1.1rem;
            font-weight: 500;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 153, 51, 0.3);
            animation: fadeIn 1.2s 0.6s both;
        }
        
        @media screen and (max-width: 768px) {
            .banner-heading {
                font-size: 2rem;
            }
            
            .banner-subheading {
                font-size: 1.1rem;
            }
            
            .banner-highlight {
                font-size: 0.9rem;
            }
        }
        
        /* Enhanced quote box styling */
        .quote-box {
            position: relative;
            background: linear-gradient(135deg, rgba(30, 33, 41, 0.6) 0%, rgba(25, 28, 36, 0.8) 100%);
            border-radius: 15px;
            padding: 2.5rem 3rem 2rem;
            margin: 1.5rem 0 2rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            border-left: 5px solid #FF9933;
            font-style: italic;
            font-size: 1.2rem;
            line-height: 1.7;
            color: #F5F5F5;
            text-align: center;
            max-width: 100%;
            overflow: hidden;
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
        }
        
        .quote-marks {
            position: absolute;
            top: 15px;
            left: 20px;
            font-size: 5rem;
            color: #FF9933;
            opacity: 0.5;
            font-family: Georgia, serif;
            line-height: 0.6;
            transform: rotate(180deg);
            text-shadow: 0 0 10px rgba(255, 153, 51, 0.3);
        }
        
        .quote-content {
            position: relative;
            z-index: 2;
            font-weight: 300;
            letter-spacing: 0.3px;
        }
        
        .closing-quote {
            position: absolute;
            bottom: 10px;
            right: 20px;
            transform: rotate(0deg);
        }
        
        .shine-border {
            position: relative;
        }
        
        .shine-border::after {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 200%;
            height: 100%;
            background: linear-gradient(90deg, 
                rgba(255,255,255,0) 0%, 
                rgba(255,255,255,0.05) 25%, 
                rgba(255,255,255,0.2) 50%,
                rgba(255,255,255,0.05) 75%,
                rgba(255,255,255,0) 100%);
            transform: translateX(-100%);
            animation: shine 5s infinite linear;
            pointer-events: none;
        }
        
        @keyframes shine {
            to {
                transform: translateX(50%);
            }
        }
        
        /* Enhanced stats banner */
        .stats-banner {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 1rem;
            margin: 1.5rem 0;
            padding: 0.8rem;
        }
        
        .stat-card {
            background: linear-gradient(135deg, rgba(35, 35, 45, 0.7) 0%, rgba(25, 28, 36, 0.8) 100%);
            border-radius: 10px;
            padding: 1.2rem 1rem;
            min-width: 180px;
            flex: 1;
            text-align: center;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 153, 51, 0.15);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2);
            border-color: rgba(255, 153, 51, 0.3);
        }
        
        .stat-value {
            font-size: 2.2rem;
            font-weight: 600;
            color: #FF9933;
            margin: 0.3rem 0;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        
        .stat-label {
            font-size: 0.9rem;
            font-weight: 400;
            color: #FAFAFA;
            margin: 0;
            letter-spacing: 0.5px;
        }
        
        .stat-icon {
            font-size: 1.8rem;
            margin-bottom: 0.8rem;
            color: rgba(255, 153, 51, 0.8);
            text-shadow: 0 0 10px rgba(255, 153, 51, 0.3);
        }
        
        /* Minimal chapter header styles */
        .mini-tricolor-bar {
            height: 4px;
            background: linear-gradient(to right, #FF9933 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%);
            margin-bottom: 10px;
            border-radius: 2px;
        }
        
        .chapter-header-container {
            display: flex;
            align-items: center;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        
        .chapter-header-logo {
            margin-right: 15px;
        }
        
        .mini-emblem {
            width: 40px;
            height: auto;
            filter: drop-shadow(0px 0px 3px rgba(255, 153, 51, 0.5));
        }
        
        .chapter-header-content {
            flex-grow: 1;
        }
        
        .chapter-title {
            font-size: 2rem;
            font-weight: 600;
            color: #FF9933;
            margin: 0;
            padding: 0;
        }
        
        .chapter-subtitle {
            font-size: 1rem;
            color: #CCC;
            margin: 0;
            padding: 0;
        }
        
        .breadcrumb-container {
            margin-bottom: 30px;
            background-color: rgba(30, 33, 41, 0.3);
            padding: 10px 15px;
            border-radius: 5px;
        }
        
        .breadcrumb-path {
            font-size: 0.9rem;
            color: #CCC;
        }
        
        .breadcrumb-link {
            color: #AAA;
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .breadcrumb-link:hover {
            color: #FF9933;
        }
        
        .breadcrumb-separator {
            margin: 0 8px;
            color: #666;
        }
        
        .breadcrumb-current {
            color: #FF9933;
            font-weight: 500;
        }
        
        /* Enhanced footer wave separator */
        .footer-wave-separator {
            height: 100px;
            margin-top: 50px;
            overflow: hidden;
            position: relative;
        }
        
        .footer-wave-separator svg {
            width: 100%;
            height: 100%;
        }
        
        /* Enhanced footer container */
        .footer-container {
            background-color: #1A1D24;
            padding: 40px 20px 20px;
            margin-top: 0;
            border-top: 1px solid #333;
            position: relative;
        }
        
        .footer-section {
            margin-bottom: 30px;
        }
        
        .footer-heading {
            color: #FF9933;
            font-size: 1.3rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255, 153, 51, 0.3);
            position: relative;
        }
        
        .footer-heading::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 60px;
            height: 2px;
            background-color: #FF9933;
        }
        
        .footer-text {
            color: #AAA;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        
        .contact-item {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .contact-item i {
            color: #FF9933;
            margin-right: 10px;
            font-size: 1rem;
        }
        
        /* Enhanced footer links */
        .footer-links {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .footer-links li {
            margin-bottom: 12px;
        }
        
        .animated-link {
            color: #CCC;
            text-decoration: none;
            transition: all 0.3s;
            padding-left: 12px;
            position: relative;
            font-size: 0.95rem;
            display: inline-block;
        }
        
        .animated-link:before {
            content: "▹";
            color: #FF9933;
            position: absolute;
            left: 0;
            transition: transform 0.3s;
        }
        
        .animated-link:hover {
            color: #FF9933;
            text-decoration: none;
            padding-left: 15px;
        }
        
        .animated-link:hover:before {
            transform: translateX(3px);
        }
        
        .footer-badge {
            background-color: rgba(19, 136, 8, 0.2);
            border: 1px solid rgba(19, 136, 8, 0.5);
            padding: 8px 12px;
            border-radius: 20px;
            display: inline-block;
            margin-top: 10px;
            transition: all 0.3s;
        }
        
        .pulsing {
            animation: badge-pulse 2s infinite;
        }
        
        @keyframes badge-pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .footer-badge p {
            margin: 0;
            color: #FAFAFA;
            font-size: 0.85rem;
        }
        
        /* Enhanced social icons */
        .social-icons {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }
        
        .social-icon {
            transition: all 0.3s;
            opacity: 0.8;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: rgba(255, 255, 255, 0.1);
            color: #CCC;
            font-size: 1.2rem;
        }
        
        .social-icon:hover {
            transform: translateY(-3px) scale(1.1);
            opacity: 1;
            background-color: rgba(255, 153, 51, 0.2);
            color: #FF9933;
        }
        
        /* Enhanced copyright section */
        .copyright-section {
            text-align: center;
            padding: 20px 0;
            background-color: #161820;
            color: #888;
            font-size: 0.85rem;
        }
        
        .copyright-content {
            padding: 10px 0;
        }
        
        .copyright-section p {
            margin: 8px 0;
        }
        
        .copyright-links {
            margin-top: 10px;
        }
        
        .footer-policy-link {
            color: #AAA;
            text-decoration: none;
            transition: color 0.2s;
            font-size: 0.8rem;
        }
        
        .footer-policy-link:hover {
            color: #FF9933;
        }
        
        .footer-link-separator {
            margin: 0 8px;
            color: #666;
        }
        
        .copyright-section .tricolor-bar {
            height: 4px;
            margin: 10px auto;
            max-width: 200px;
        }
        
        /* Navigation button styles */
        .stButton > button {
            background-color: rgba(19, 136, 8, 0.1);
            color: #FAFAFA;
            border: 1px solid rgba(255, 153, 51, 0.5);
            border-radius: 30px;
            padding: 8px 16px;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            background-color: rgba(255, 153, 51, 0.2);
            border-color: #FF9933;
            color: #FF9933;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255, 153, 51, 0.3);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(255, 153, 51, 0.3);
        }
        
        /* Chapter navigation container */
        .chapter-navigation {
            margin-top: 2rem;
            padding: 1rem;
            border-top: 1px solid rgba(255, 153, 51, 0.3);
            display: flex;
            justify-content: space-between;
        }
        
        /* Chapter indicator styles */
        .chapter-indicator {
            text-align: center;
            color: #AAAAAA;
            font-size: 0.8rem;
            margin: 0 auto;
            padding: 5px 10px;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.05);
        }
    </style>
    """, unsafe_allow_html=True) 