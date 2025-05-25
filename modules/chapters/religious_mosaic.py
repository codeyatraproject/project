import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.utils import load_religious_data, apply_dark_theme

def render():
    """
    Renders the Religious Mosaic chapter content with enhanced visualization and positive framing
    """
    st.markdown("<h2 class='chapter-heading'>Religious Mosaic: India's Spiritual Symphony</h2>", unsafe_allow_html=True)
    
    # Introduction with more positive framing
    st.markdown("""
    <div class='story-text'>
    India stands as a living testament to religious harmony and spiritual diversity, where multiple faith traditions have not just coexisted but flourished for millennia. This extraordinary tapestry of beliefs represents one of humanity's most successful experiments in pluralism, where ancient wisdom traditions continue to thrive alongside newer spiritual paths.
    
    From the snow-capped Himalayan monasteries to the sacred riverbanks of Varanasi, from the golden domes of gurudwaras to the intricate architecture of mosques, India's landscape is adorned with expressions of devotion that have inspired the world. This spiritual diversity has enriched every aspect of Indian culture—from art and architecture to philosophy and daily life.
    </div>
    """, unsafe_allow_html=True)
    
    # Key insight with positive framing
    st.info("🔍 **Spiritual Treasure:** India is the birthplace of four major world religions—Hinduism, Buddhism, Jainism, and Sikhism—and has provided sanctuary to persecuted religious communities throughout history. It's the only country where every major world religion has thrived continuously for centuries.")
    
    # Load religious data
    df_religions = load_religious_data()
    
    # Create tabs for different aspects of religious data
    rel_tab1, rel_tab2, rel_tab3, rel_tab4 = st.tabs(["Diversity Landscape", "Sacred Geography", "Cultural Contributions", "Living Traditions"])
    
    with rel_tab1:
        st.markdown("<h3 class='section-heading'>India's Spiritual Diversity</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create a more visually appealing pie chart
            fig = px.pie(df_religions, 
                        values='Population', 
                        names='Religion',
                        title='Religious Communities of India',
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        hole=0.4)
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(legend_title='Religion', legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
            fig = apply_dark_theme(fig)
            
            st.plotly_chart(fig, use_container_width=True)
    
        with col2:
            st.markdown("""
            <div class='story-text'>
            <h4>Harmony in Diversity</h4>
            India's religious landscape represents a unique achievement in human civilization—a place where:
            
            <ul>
                <li>Multiple faith traditions have coexisted for thousands of years</li>
                <li>Syncretic practices bridge different religious communities</li>
                <li>Religious minorities have preserved their traditions for centuries</li>
                <li>New spiritual movements continue to emerge and flourish</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a metric highlighting religious diversity
            st.metric(
                label="Active Religious Traditions",
                value="9+",
                delta="Thriving continuously",
                delta_color="normal"
            )
        
        # Historical timeline of religions in India
        st.markdown("<h4>Spiritual Timeline: Ancient Origins to Modern Flourishing</h4>", unsafe_allow_html=True)
        
        # Create timeline data
        timeline_data = {
            'Religion': ['Hinduism', 'Jainism', 'Buddhism', 'Judaism', 'Christianity', 'Islam', 'Sikhism', 'Zoroastrianism', 'Bahai Faith'],
            'Year': [-3000, -800, -600, -100, 52, 700, 1469, 936, 1844],
            'Event': ['Vedic traditions established', 'Mahavira revitalizes Jain teachings', 'Buddha attains enlightenment', 'Jewish settlers arrive in India', 'St. Thomas brings Christianity', 'First mosque built in Kerala', 'Guru Nanak begins teachings', 'Parsis arrive in Gujarat', 'Bahai Faith introduced to India']
        }
        
        timeline_df = pd.DataFrame(timeline_data)
        timeline_df['Year_Display'] = timeline_df['Year'].apply(lambda x: f"{abs(x)} BCE" if x < 0 else f"{x} CE")
        
        fig = px.scatter(timeline_df, 
                       x='Year', 
                       y='Religion',
                       size=[20]*len(timeline_df),
                       text='Year_Display',
                       color='Religion',
                       title='Timeline of Religious Traditions in India')
        
        fig.update_traces(textposition='top center', mode='markers+text')
        fig.update_layout(xaxis_title='Year (BCE/CE)', yaxis_title='Religion')
        fig.update_xaxes(range=[-3500, 2000])
        fig = apply_dark_theme(fig)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<div class='data-insight'>India's spiritual landscape has continuously evolved over millennia, with each tradition finding space to flourish while contributing to a shared cultural heritage.</div>", unsafe_allow_html=True)
    
    with rel_tab2:
        st.markdown("<h3 class='section-heading'>Sacred Geography: Spiritual Landmarks</h3>", unsafe_allow_html=True)
        
        # Create a visualization of sacred sites
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class='story-text'>
            <h4>Northern Sacred Circuit</h4>
            The Himalayan region and Gangetic plains host some of humanity's most revered spiritual sites:
            </div>
            """, unsafe_allow_html=True)
            
            # Create cards for northern sacred sites
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(255, 153, 51, 0.1); margin-bottom: 15px;">
                <h5 style="color: #FF9933; margin-top: 0;">Varanasi (Hindu)</h5>
                <p>One of the world's oldest continuously inhabited cities, Varanasi's ghats along the sacred Ganges River have witnessed spiritual seekers for over 3,500 years.</p>
            </div>
            
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(255, 223, 0, 0.1); margin-bottom: 15px;">
                <h5 style="color: #FFD700; margin-top: 0;">Golden Temple, Amritsar (Sikh)</h5>
                <p>The holiest shrine in Sikhism exemplifies the religion's principles of equality and service, feeding up to 100,000 visitors daily regardless of faith.</p>
            </div>
            
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(19, 136, 8, 0.1); margin-bottom: 15px;">
                <h5 style="color: #138808; margin-top: 0;">Bodh Gaya (Buddhist)</h5>
                <p>Where the Buddha attained enlightenment under the Bodhi Tree, now a UNESCO World Heritage site drawing pilgrims from across Asia.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='story-text'>
            <h4>Southern & Western Sacred Treasures</h4>
            The southern and western regions preserve some of India's most architecturally stunning and historically significant religious sites:
            </div>
            """, unsafe_allow_html=True)
            
            # Create cards for southern sacred sites
            st.markdown("""
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(0, 0, 128, 0.1); margin-bottom: 15px;">
                <h5 style="color: #0000FF; margin-top: 0;">Meenakshi Temple, Madurai (Hindu)</h5>
                <p>A breathtaking example of Dravidian architecture with 14 gateway towers, this temple complex receives over 25,000 visitors daily.</p>
            </div>
            
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(128, 0, 128, 0.1); margin-bottom: 15px;">
                <h5 style="color: #800080; margin-top: 0;">Ajmer Sharif Dargah (Islamic)</h5>
                <p>Sufi shrine visited by people of all faiths, representing India's syncretic traditions where spiritual boundaries blur.</p>
            </div>
            
            <div style="padding: 15px; border-radius: 10px; background-color: rgba(255, 99, 71, 0.1); margin-bottom: 15px;">
                <h5 style="color: #FF6347; margin-top: 0;">Paradesi Synagogue, Kochi (Jewish)</h5>
                <p>One of the oldest active synagogues in the Commonwealth, symbolizing India's unique history of welcoming Jewish communities without persecution.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Create a section on multi-faith pilgrimage sites
        st.markdown("<h4>Shared Sacred Spaces: Where Faiths Converge</h4>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='story-text'>
        India features numerous sites revered by multiple faith traditions, exemplifying the country's syncretic spiritual heritage:
        
        - <strong>Shrine of Khwaja Moinuddin Chishti:</strong> Visited by Muslims, Hindus, Christians and Sikhs
        - <strong>Shirdi Sai Baba Temple:</strong> Draws devotees from Hindu, Muslim, and other communities
        - <strong>Sabrimala:</strong> Hindu pilgrimage site that welcomes people of all faiths
        - <strong>Naina Devi Temple:</strong> Sacred to both Hindus and Sikhs
        - <strong>St. Mary's Church, Chennai:</strong> Visited by Christians, Hindus and Muslims for healing prayers
        </div>
        """, unsafe_allow_html=True)
        
        # Add a map visualization placeholder (in production this would be an actual map)
        st.image("https://www.mapsofindia.com/maps/india/religious-map.jpg", caption="India's Religious Geography", use_container_width=True)
    
    with rel_tab3:
        st.markdown("<h3 class='section-heading'>Cultural Treasures: Faith's Creative Legacy</h3>", unsafe_allow_html=True)
        
        # Create a visualization of cultural contributions
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create a horizontal bar chart showing cultural contributions
            # Extract and count cultural contributions from each religion
            df_religions['Contribution_Count'] = df_religions['Cultural Contributions'].str.count(',') + 1
            
            fig = px.bar(df_religions.sort_values('Contribution_Count', ascending=False).head(8), 
                        y='Religion', 
                        x='Contribution_Count',
                        title='Cultural Contributions by Religious Traditions',
                        text='Cultural Contributions',
                        color='Contribution_Count',
                        orientation='h',
                        color_continuous_scale=px.colors.sequential.Viridis)
            
            fig.update_traces(textposition='outside')
            fig.update_layout(yaxis_title='Religion', xaxis_title='Number of Major Cultural Contributions')
            fig = apply_dark_theme(fig)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class='story-text'>
            <h4>Artistic & Intellectual Heritage</h4>
            Religious traditions have inspired India's greatest cultural achievements:
            
            <ul>
                <li><strong>Architecture:</strong> From the intricate temples of Khajuraho to the perfect symmetry of the Taj Mahal</li>
                <li><strong>Literature:</strong> Epic works like the Mahabharata and Ramayana, Sufi poetry, and Buddhist philosophical texts</li>
                <li><strong>Performing Arts:</strong> Classical dance forms with spiritual foundations, devotional music traditions</li>
                <li><strong>Sciences:</strong> Ancient mathematical, astronomical, and medical knowledge preserved in religious institutions</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a section on architectural marvels
        st.markdown("<h4>Architectural Splendors: Faith in Stone and Structure</h4>", unsafe_allow_html=True)
        
        # Create columns for different architectural traditions
        arch_col1, arch_col2, arch_col3, arch_col4 = st.columns(4)
        
        with arch_col1:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <h5>Hindu Temple Architecture</h5>
                <p>Nagara (North), Dravida (South), and Vesara (Central) styles created mathematical marvels like Kandariya Mahadeva Temple</p>
            </div>
            """, unsafe_allow_html=True)
            
        with arch_col2:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <h5>Indo-Islamic Architecture</h5>
                <p>Synthesis of Persian, Turkish and Indian styles creating masterpieces like Taj Mahal, Qutub Minar, and Gol Gumbaz</p>
            </div>
            """, unsafe_allow_html=True)
            
        with arch_col3:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <h5>Sikh Architecture</h5>
                <p>Distinctive style featuring domes, open spaces, and community halls seen in historic gurudwaras across North India</p>
            </div>
            """, unsafe_allow_html=True)
            
        with arch_col4:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <h5>Colonial-Era Churches</h5>
                <p>Gothic, Portuguese, and uniquely Indian Christian architectural styles in churches like Se Cathedral and St. Thomas Basilica</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a section on philosophical contributions
        st.markdown("<h4>Philosophical Treasures: India's Gift to World Thought</h4>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='story-text'>
        India's religious traditions have contributed foundational philosophical concepts that continue to influence global thought:
        
        - <strong>Ahimsa (Non-violence):</strong> Core principle from Jainism, Hinduism and Buddhism that inspired global peace movements
        - <strong>Karma:</strong> Concept of cosmic causality and ethical responsibility that has entered global vocabulary
        - <strong>Dharma:</strong> Complex notion of cosmic order, duty, and righteousness that underpins Indian ethical systems
        - <strong>Seva:</strong> Selfless service emphasized in Sikhism that created the world's largest free community kitchens
        - <strong>Meditation:</strong> Practices from multiple traditions now scientifically validated and adopted worldwide
        </div>
        """, unsafe_allow_html=True)
    
    with rel_tab4:
        st.markdown("<h3 class='section-heading'>Living Traditions: Faith in Daily Life</h3>", unsafe_allow_html=True)
        
        # Create a visualization of festivals
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create a visualization of festivals throughout the year
            months = ['January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December']
            
            # Count of major festivals by month (approximate)
            festival_counts = [3, 4, 5, 6, 3, 2, 3, 4, 5, 7, 5, 3]
            
            # Create a polar chart for festivals through the year
            fig = px.line_polar(r=festival_counts, 
                               theta=months, 
                               line_close=True,
                               title="Festival Calendar: Year-Round Celebrations",
                               color_discrete_sequence=px.colors.sequential.Plasma_r)
            
            fig.update_traces(fill='toself')
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 8])))
            fig = apply_dark_theme(fig)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("<div class='data-insight'>India celebrates over 50 major religious festivals throughout the year, with many becoming pan-Indian celebrations that transcend religious boundaries.</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='story-text'>
            <h4>Festival Highlights</h4>
            Religious festivals in India often become nationwide celebrations:
            
            <ul>
                <li><strong>Diwali:</strong> Hindu festival of lights celebrated across religions</li>
                <li><strong>Eid:</strong> Islamic celebrations marked by community feasts open to all</li>
                <li><strong>Christmas:</strong> Celebrated with Indian cultural elements across the country</li>
                <li><strong>Holi:</strong> Spring color festival that transcends religious boundaries</li>
                <li><strong>Baisakhi:</strong> Sikh harvest festival with nationwide participation</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a section on unique religious practices
        st.markdown("<h4>Unique Religious Practices: India's Spiritual Innovation</h4>", unsafe_allow_html=True)
        
        # Create tabs for different religious practices
        practice_tab1, practice_tab2, practice_tab3 = st.tabs(["Daily Devotions", "Pilgrimages", "Community Traditions"])
        
        with practice_tab1:
            st.markdown("""
            <div class='story-text'>
            <h5>Daily Spiritual Practices</h5>
            Religious devotion is woven into everyday Indian life:
            
            - <strong>Hindu Puja:</strong> Daily home worship rituals with offerings to deities
            - <strong>Islamic Namaz:</strong> Five daily prayers observed by Muslims
            - <strong>Sikh Path:</strong> Daily readings from the Guru Granth Sahib
            - <strong>Christian Prayer:</strong> Morning and evening devotions adapted to Indian contexts
            - <strong>Buddhist Meditation:</strong> Daily mindfulness practices
            - <strong>Jain Pratikraman:</strong> Daily reflection and repentance ritual
            </div>
            """, unsafe_allow_html=True)
            
        with practice_tab2:
            st.markdown("""
            <div class='story-text'>
            <h5>Pilgrimage Traditions</h5>
            India hosts some of the world's largest and most diverse pilgrimage traditions:
            
            - <strong>Kumbh Mela:</strong> World's largest religious gathering with up to 120 million participants
            - <strong>Char Dham:</strong> Hindu circuit of four sacred sites in the Himalayas
            - <strong>Hajj Preparation:</strong> Special training centers for Indian Muslims preparing for Hajj
            - <strong>Buddhist Circuit:</strong> Path following Buddha's life events across northern India
            - <strong>Jain Pilgrimage:</strong> Complex system of temple circuits like the Shatrunjaya hills with 863 temples
            </div>
            """, unsafe_allow_html=True)
            
        with practice_tab3:
            st.markdown("""
            <div class='story-text'>
            <h5>Community Traditions</h5>
            Religious communities have developed unique social innovations:
            
            - <strong>Langar:</strong> Sikh tradition of free community kitchens serving millions daily
            - <strong>Iftar:</strong> Muslim tradition of breaking fast during Ramadan, often shared with neighbors of all faiths
            - <strong>Bhajan & Kirtan:</strong> Hindu devotional music gatherings building community bonds
            - <strong>Christian Charity:</strong> Schools, hospitals and social services open to all communities
            - <strong>Parsi Philanthropy:</strong> Tradition of community service and charitable foundations
            </div>
            """, unsafe_allow_html=True)
        
        # Add a section on interfaith initiatives
        st.markdown("<h4>Interfaith Harmony: Building Bridges</h4>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='story-text'>
        India has pioneered numerous interfaith initiatives that promote harmony:
        
        - <strong>Sarva Dharma Samabhava:</strong> Constitutional principle of "equal respect for all religions"
        - <strong>Interfaith Celebrations:</strong> Joint celebration of festivals across religious communities
        - <strong>Shared Sacred Sites:</strong> Places like Shirdi where multiple faiths worship together
        - <strong>Community Peace Committees:</strong> Local interfaith groups that promote dialogue and cooperation
        - <strong>Spiritual Tourism:</strong> Programs encouraging visitors to experience diverse religious traditions
        </div>
        """, unsafe_allow_html=True)
    
    # Add a collapsible section for religious facts
    with st.expander("📚 Fascinating Facts About India's Religious Heritage"):
        st.markdown("""
        ### Unique Achievements
        - **Religious Sanctuary:** India is the only country where Judaism has existed for 2,000+ years without experiencing antisemitism
        - **Parsi Preservation:** India enabled Zoroastrians to preserve their ancient faith when it declined elsewhere
        - **Syrian Christians:** One of the world's oldest Christian communities has thrived in Kerala since 52 CE
        - **Tibetan Buddhism:** India provided refuge for Tibetan Buddhism, enabling its preservation and global spread
        
        ### Architectural Wonders
        - The Brihadeeswara Temple was built 1000 years ago with a 80-ton granite capstone raised to 66 meters without modern technology
        - The Iron Pillar of Delhi has stood for 1600+ years without rusting, demonstrating ancient metallurgical knowledge
        - The Kailasa Temple at Ellora was carved from a single rock, with sculptors removing 400,000 tons of stone
        - The Golden Temple's foundation was laid by a Muslim saint at the invitation of a Sikh Guru, symbolizing interfaith harmony
        
        ### Modern Continuity
        - India maintains the world's oldest continuously operating religious traditions and institutions
        - Ancient Sanskrit schools (gurukuls) continue teaching using methods established over 3,000 years ago
        - Traditional religious art forms like Thanjavur painting and Madhubani art continue to evolve while preserving core techniques
        - Religious festivals documented in ancient texts are still celebrated with the same core rituals thousands of years later
        """)
        
        # Add a chart showing religious diversity by region
        region_data = {
            'Region': ['North', 'South', 'East', 'West', 'Central', 'Northeast'],
            'Number of Active Religions': [8, 7, 6, 9, 6, 7]
        }
        
        region_df = pd.DataFrame(region_data)
        
        fig = px.bar(region_df, 
                    x='Region', 
                    y='Number of Active Religions',
                    title='Religious Diversity Across Indian Regions',
                    color='Number of Active Religions',
                    color_continuous_scale=px.colors.sequential.Viridis)
        
        fig.update_layout(xaxis_title='Region', yaxis_title='Number of Active Religious Traditions')
        fig = apply_dark_theme(fig)
        
        st.plotly_chart(fig, use_container_width=True)