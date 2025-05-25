import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.utils import load_linguistic_data, apply_dark_theme, get_color_palette

def render():
    st.markdown("<h2 class='chapter-heading'>Linguistic Diversity: The Many Voices of India</h2>", unsafe_allow_html=True)
    
    # Introduction with better formatting and more positive framing
    with st.container():
        st.markdown("""
        <div class='story-text'>
        India's extraordinary linguistic diversity stands as one of the world's greatest cultural treasures. The country embraces hundreds of languages from multiple language families, creating a vibrant tapestry of expression that has evolved over thousands of years.
        
        With 22 officially recognized languages and over 19,500 dialects spoken across its regions, India represents a unique linguistic ecosystem where ancient classical languages coexist with modern innovations. This remarkable diversity doesn't divide India—it unites the nation through a shared appreciation for multilingual heritage.
        </div>
        """, unsafe_allow_html=True)
    
    # Add a key insight at the top with more positive framing
    st.info("🔍 **Linguistic Treasure:** India ranks fourth globally in linguistic diversity after Papua New Guinea, Indonesia, and Nigeria, with its languages representing all major language families. This diversity has fostered one of the world's richest literary traditions spanning over 3,500 years.")
    
    # Create tabs for different aspects of language data with more comprehensive organization
    lang_tab1, lang_tab2, lang_tab3, lang_tab4 = st.tabs(["Language Landscape", "Cultural Significance", "Regional Brilliance", "Global Influence"])
    
    # Load language data once for all tabs
    df_languages = load_linguistic_data()
    
    with lang_tab1:
        st.markdown("<h3 class='section-heading'>India's Linguistic Mosaic</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Create a more visually appealing chart
            fig = px.pie(df_languages, 
                        values='Speakers', 
                        names='Language',
                        title='Major Indian Languages by Speaker Population',
                        color_discrete_sequence=px.colors.qualitative.Prism,
                        hole=0.4)
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                legend_title='Language', 
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                margin=dict(l=20, r=20, t=40, b=20),
                height=500,
                autosize=True
            )
            fig = apply_dark_theme(fig)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("<div class='data-insight'>India's linguistic diversity is unparalleled, with the top 10 languages alone spoken by over 90% of the population. This creates a natural multilingualism where citizens often speak 3+ languages fluently.</div>", unsafe_allow_html=True)
        
        with col2:
            # Create a more engaging visualization of language status
            classical_languages = df_languages[df_languages['UNESCO Status'].str.contains('Classical', na=False)]
            
            st.markdown("<h4>India's Classical Languages</h4>", unsafe_allow_html=True)
            st.markdown("""
            <div class='story-text'>
            India has officially designated 6 languages as Classical Languages, recognizing their rich heritage, ancient origins, and substantial body of literature:
            </div>
            """, unsafe_allow_html=True)
            
            # Create a more visually appealing display of classical languages
            for idx, row in classical_languages.iterrows():
                st.markdown(f"""
                <div style="padding: 10px; margin-bottom: 10px; border-radius: 5px; background-color: rgba(255, 153, 51, 0.1); border-left: 3px solid #FF9933;">
                    <span style="font-weight: bold; color: #FF9933;">{row['Language']}</span>: {row['UNESCO Status']}
                    <div style="font-size: 0.9em; margin-top: 5px;">Notable texts: {row['Ancient Texts']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    with lang_tab2:
        st.markdown("<h3 class='section-heading'>Cultural Treasures in Every Tongue</h3>", unsafe_allow_html=True)
        
        # Create a visualization of cultural significance
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create a visualization showing cultural significance
            fig = go.Figure()
            
            languages = df_languages['Language'].tolist()[:10]  # Top 10 languages
            cultural_sig = [len(str(sig)) for sig in df_languages['Cultural Significance'].tolist()[:10]]  # Using length as a proxy for richness
            ancient_texts = [len(str(texts)) for texts in df_languages['Ancient Texts'].tolist()[:10]]  # Using length as a proxy for literary heritage
            
            fig.add_trace(go.Bar(
                x=languages,
                y=cultural_sig,
                name='Cultural Significance',
                marker_color='indianred'
            ))
            
            fig.add_trace(go.Bar(
                x=languages,
                y=ancient_texts,
                name='Literary Heritage',
                marker_color='lightsalmon'
            ))
            
            fig.update_layout(
                title='Cultural and Literary Richness by Language',
                xaxis_tickangle=-45,
                barmode='group',
                xaxis_title='Language',
                yaxis_title='Cultural Richness Score',
                height=500,
                margin=dict(l=20, r=20, t=50, b=100),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
            )
            
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class='story-text'>
            <h4>Linguistic Cultural Heritage</h4>
            Each Indian language carries unique cultural treasures:
            
            <ul>
                <li><strong>Sanskrit:</strong> The "perfect language" with mathematical precision, foundation of ancient sciences and philosophy</li>
                <li><strong>Tamil:</strong> World's oldest continuously spoken language with unbroken literary tradition</li>
                <li><strong>Bengali:</strong> Language of the first Asian Nobel laureate in Literature (Rabindranath Tagore)</li>
                <li><strong>Malayalam:</strong> Highest literacy rate among all language speakers in India</li>
                <li><strong>Hindi:</strong> Foundation of world's largest film industry (Bollywood)</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
        # Add a section on literary achievements
        st.markdown("<h4>Literary Excellence Across Languages</h4>", unsafe_allow_html=True)
        
        # Create columns for Jnanpith Award winners by language
        jnanpith_data = {
            'Language': ['Hindi', 'Malayalam', 'Bengali', 'Kannada', 'Telugu', 'Urdu', 'Odia', 'Marathi', 'Gujarati', 'Tamil'],
            'Awards': [11, 6, 6, 8, 3, 2, 3, 4, 3, 2]
        }
        
        jnanpith_df = pd.DataFrame(jnanpith_data)
        
        fig = px.bar(jnanpith_df, 
                    x='Language', 
                    y='Awards',
                    title='Jnanpith Awards by Language (India\'s Highest Literary Honor)',
                    color='Awards',
                    color_continuous_scale=px.colors.sequential.Oranges)
        
        fig.update_layout(
            xaxis_title='Language', 
            yaxis_title='Number of Awards',
            height=450,
            margin=dict(l=20, r=20, t=50, b=50),
            xaxis_tickangle=-45
        )
        fig = apply_dark_theme(fig)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div class='data-insight'>The Jnanpith Award, India's highest literary honor, has been awarded to authors writing in 12 different languages, showcasing the literary excellence across India's linguistic landscape.</div>", unsafe_allow_html=True)
    
    with lang_tab3:
        st.markdown("<h3 class='section-heading'>Regional Language Brilliance</h3>", unsafe_allow_html=True)
        
        # Create a map of India's linguistic regions
        st.markdown("""
        <div class='story-text'>
        Each region of India contributes uniquely to the nation's linguistic tapestry:
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(255, 153, 51, 0.1); margin-bottom: 15px;">
                <h4 style="color: #FF9933; margin-top: 0;">Northern Brilliance</h4>
                <p>Home to Hindi, Urdu, Punjabi, and Kashmiri, the northern languages blend Sanskrit heritage with Persian influences, creating rich poetic traditions like Urdu's ghazals and Hindi's dohas.</p>
                <p><strong>Unique Feature:</strong> The Devanagari script used for Hindi is scientifically designed to represent all possible speech sounds.</p>
            </div>
            
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(19, 136, 8, 0.1); margin-bottom: 15px;">
                <h4 style="color: #138808; margin-top: 0;">Eastern Treasures</h4>
                <p>Bengali, Odia, and Assamese languages have produced Nobel laureates and countless literary giants. Bengali literature's global recognition through Rabindranath Tagore showcases the region's intellectual depth.</p>
                <p><strong>Unique Feature:</strong> Assamese is the easternmost Indo-European language in the world.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(0, 0, 128, 0.1); margin-bottom: 15px;">
                <h4 style="color: #0000FF; margin-top: 0;">Southern Linguistic Heritage</h4>
                <p>The Dravidian languages (Tamil, Telugu, Kannada, Malayalam) preserve some of the world's oldest literary traditions. Tamil's 2000+ year literary continuity stands unmatched globally.</p>
                <p><strong>Unique Feature:</strong> Malayalam has the highest consonant-to-vowel ratio among Indian languages, enabling remarkable linguistic precision.</p>
            </div>
            
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(255, 223, 0, 0.1); margin-bottom: 15px;">
                <h4 style="color: #FFD700; margin-top: 0;">Western Linguistic Innovation</h4>
                <p>Marathi, Gujarati, and Konkani have pioneered modern literature and theater in India. Marathi theater tradition dates back 150+ years and remains vibrant today.</p>
                <p><strong>Unique Feature:</strong> Gujarati was home to the first printed book in India (1797).</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a section on Northeast languages
        st.markdown("""
        <div style="padding: 15px; border-radius: 10px; background-color: rgba(128, 0, 128, 0.1); margin-bottom: 15px;">
            <h4 style="color: #800080; margin-top: 0;">Northeastern Linguistic Diversity</h4>
            <p>The "Seven Sisters" states host over 220 languages from multiple language families, creating one of the world's most linguistically dense regions. Languages like Bodo, Manipuri, and Khasi preserve unique cultural knowledge and indigenous wisdom.</p>
            <p><strong>Unique Feature:</strong> Manipuri's ancient Meitei Mayek script was successfully revived after near extinction, representing one of the world's most successful script revival stories.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add a section on tribal languages
        st.markdown("<h4>Tribal Language Preservation Success Stories</h4>", unsafe_allow_html=True)
        st.markdown("""
        <div class='story-text'>
        India has pioneered efforts to preserve its tribal and indigenous languages:
        
        - <strong>Santali:</strong> First tribal language to receive official recognition in the Constitution
        - <strong>Gondi:</strong> Dictionary and children's literature development has revitalized this central Indian language
        - <strong>Great Andamanese:</strong> Preservation efforts for this critically endangered language have documented its unique knowledge systems
        - <strong>Toda:</strong> Digital documentation has preserved this ancient Nilgiri Hills language with fewer than 1,500 speakers
        </div>
        """, unsafe_allow_html=True)
    
    with lang_tab4:
        st.markdown("<h3 class='section-heading'>Global Influence & Future Potential</h3>", unsafe_allow_html=True)
        
        # Create a visualization of global reach
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create a horizontal bar chart showing global reach
            top_global = df_languages.nlargest(8, 'Speakers')
            
            fig = px.bar(top_global, 
                        y='Language', 
                        x='Speakers',
                        title='Indian Languages with Global Presence',
                        text='Global Reach',
                        color='Speakers',
                        orientation='h',
                        color_continuous_scale=px.colors.sequential.Viridis)
            
            fig.update_traces(textposition='inside')
            fig.update_layout(
                yaxis_title='Language', 
                xaxis_title='Speakers (millions)',
                height=500,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            fig = apply_dark_theme(fig)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class='story-text'>
            <h4>Global Impact</h4>
            Indian languages have spread worldwide through diaspora communities and cultural influence:
            
            <ul>
                <li><strong>Hindi-Urdu:</strong> 4th most spoken language globally with growing international interest</li>
                <li><strong>Sanskrit:</strong> Studied in 250+ universities worldwide for linguistics and AI applications</li>
                <li><strong>Tamil:</strong> Official status in Singapore, Sri Lanka, and Malaysia</li>
                <li><strong>Punjabi:</strong> Official language in parts of Canada</li>
                <li><strong>Bengali:</strong> 7th most spoken language worldwide</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a section on language technology
        st.markdown("<h4>Language Technology Innovation</h4>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='story-text'>
        India leads in developing language technology for linguistic diversity:
        
        - <strong>Bhashini Platform:</strong> AI-powered translation between 22+ Indian languages
        - <strong>Indic Keyboards:</strong> Input methods for all official languages on digital devices
        - <strong>Speech Recognition:</strong> Advanced systems for 9 major Indian languages
        - <strong>NLP Research:</strong> Leading computational linguistics research for low-resource languages
        </div>
        """, unsafe_allow_html=True)
        
        # Add interactive element - language greeting translator with improved design
        st.markdown("<h4 style='margin-top:30px;'>Experience India's Linguistic Diversity: Greetings Across Languages</h4>", unsafe_allow_html=True)
        
        greetings = {
            "Hindi": "नमस्ते (Namaste) - The divine in me bows to the divine in you",
            "Bengali": "নমস্কার (Nomoshkar) - I bow to the divine in you",
            "Telugu": "నమస్కారం (Namaskaram) - Respectful greetings to you",
            "Tamil": "வணக்கம் (Vanakkam) - My respect to you",
            "Marathi": "नमस्कार (Namaskar) - I bow to you with respect",
            "Gujarati": "નમસ્તે (Namaste) - Respectful greetings",
            "Kannada": "ನಮಸ್ಕಾರ (Namaskara) - I bow to you",
            "Malayalam": "നമസ്കാരം (Namaskaram) - I bow to you with respect",
            "Punjabi": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ (Sat Sri Akal) - God is the Ultimate Truth",
            "Assamese": "নমস্কাৰ (Nomoskar) - I bow to you",
            "Odia": "ନମସ୍କାର (Namaskara) - I bow to you",
            "Kashmiri": "आदाब (Adaab) - I offer my respect",
            "Sanskrit": "नमस्ते (Namaste) - I bow to the divine in you",
            "Manipuri": "ꯀꯨꯝꯖꯔꯤ (Kumjari) - Greetings to you"
        }
        
        # Create a more visually appealing selectbox for language selection
        selected_lang = st.selectbox("Select a language to learn its greeting:", list(greetings.keys()))
        
        st.markdown(f"""
        <div style="text-align:center; padding:20px; background: linear-gradient(135deg, rgba(255, 153, 51, 0.2), rgba(19, 136, 8, 0.2)); border-radius:10px; margin:20px 0;">
            <div style="font-size:32px; margin-bottom:10px; color:#FF9933;">{selected_lang}</div>
            <div style="font-size:24px; margin-bottom:15px;">{greetings[selected_lang].split(' - ')[0]}</div>
            <div style="font-size:18px; font-style:italic; color:#e0e0e0;">{greetings[selected_lang].split(' - ')[1]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a collapsible section for additional language facts with more positive framing
    with st.expander("📚 Fascinating Facts About Indian Languages"):
        st.markdown("""
        ### Ancient Wisdom in Modern Times
        - **Sanskrit:** Often called "the perfect language," its grammar was codified by Panini in 500 BCE with a precision that modern computer scientists admire. NASA has considered Sanskrit the most suitable language for AI due to its unambiguous structure.
        
        - **Tamil:** With literature dating back to 300 BCE, Tamil is the only ancient classical language that has survived into the modern age as a living language with unbroken literary tradition.
        
        ### Script Innovation
        - India has developed 11 major script systems, most derived from the ancient Brahmi script.
        - The Nagari script family (used for Hindi, Marathi, and Sanskrit) is considered one of the world's most scientifically designed writing systems.
        - The Tamil script has evolved continuously for over 2,000 years while maintaining readability.
        
        ### Multilingual Excellence
        - The average Indian speaks 3+ languages fluently, making India one of the world's most naturally multilingual societies.
        - Code-switching (mixing languages mid-sentence) is a sophisticated linguistic skill common among Indian speakers.
        - India's linguistic diversity has created natural translation abilities, with many Indians serving as "language bridges" between different communities.
        
        ### Literary Achievements
        - Indian languages have produced 10 Jnanpith Awards (India's highest literary honor) and a Nobel Prize in Literature.
        - The world's longest epic poem, the Mahabharata (100,000 verses), was composed in Sanskrit and has been translated into every major Indian language.
        - Indian languages have some of the world's richest collections of folk literature, with over 100,000 documented folk tales.
        """)
        
        # Add a chart showing script diversity
        script_data = {
            'Script': ['Devanagari', 'Bengali', 'Tamil', 'Telugu', 'Kannada', 'Malayalam', 'Gujarati', 'Gurmukhi', 'Odia', 'Urdu'],
            'Languages': [5, 2, 1, 1, 1, 1, 1, 1, 1, 3]
        }
        
        script_df = pd.DataFrame(script_data)
        
        fig = px.bar(script_df, 
                    x='Script', 
                    y='Languages',
                    title='Major Script Systems of India',
                    color='Languages',
                    color_continuous_scale=px.colors.sequential.Viridis)
        
        fig.update_layout(
            xaxis_title='Script', 
            yaxis_title='Number of Languages Using Script',
            height=450,
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_tickangle=-45
        )
        fig = apply_dark_theme(fig)
        
        st.plotly_chart(fig, use_container_width=True) 