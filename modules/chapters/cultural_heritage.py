import streamlit as st
import time
from modules.utils import load_cultural_data, apply_dark_theme

def render():
    with st.spinner("Loading Cultural Heritage content..."):
        # Use shorter delay for data loading
        time.sleep(0.5)
        
        # Enhanced header with dynamic elements and better visual hierarchy
        st.markdown("""
        <div style="text-align: center; margin: 2rem auto; max-width: 900px; padding: 2rem; background: linear-gradient(135deg, rgba(255, 153, 51, 0.1), rgba(19, 136, 8, 0.1)); border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h1 class='chapter-heading' style="color: #FF9933; text-shadow: 0 2px 4px rgba(0,0,0,0.3); font-size: 2.8rem; margin-bottom: 1rem;">Cultural Heritage: The Living Legacy of India</h1>
            <p style="font-size: 1.6rem; font-weight: 300; line-height: 1.8; color: #FFFFFF; font-style: italic; margin-bottom: 1.5rem;">
                Where ancient wisdom meets modern expression, and traditions dance with innovation
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem;">
                <div style="text-align: center;">
                    <span style="font-size: 2.5rem;">🎨</span>
                    <p style="margin: 0.5rem 0; color: #FF9933;">Artistic Excellence</p>
                </div>
                <div style="text-align: center;">
                    <span style="font-size: 2.5rem;">💃</span>
                    <p style="margin: 0.5rem 0; color: #138808;">Cultural Expression</p>
                </div>
                <div style="text-align: center;">
                    <span style="font-size: 2.5rem;">🏛️</span>
                    <p style="margin: 0.5rem 0; color: #FF9933;">Heritage Sites</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Inspirational quote section with enhanced styling
        st.markdown("""
        <div style="background-color: rgba(35, 35, 45, 0.8); border-radius: 15px; padding: 2.5rem; margin: 2rem 0; position: relative; border-left: 5px solid #FF9933; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <div style="position: absolute; top: 10px; left: 20px; font-family: Georgia, serif; font-size: 5rem; color: #FF9933; opacity: 0.4; line-height: 0;">"</div>
            <p style="font-size: 1.5rem; line-height: 1.8; text-align: center; font-style: italic; margin: 0.5rem 3rem; color: #F5F5F5;">
                Culture is the widening of the mind and of the spirit. It is the expression of our inner selves, the mirror of our collective consciousness.
            </p>
            <div style="position: absolute; bottom: 10px; right: 20px; font-family: Georgia, serif; font-size: 5rem; color: #FF9933; opacity: 0.4; line-height: 0;">"</div>
            <p style="text-align: right; margin-top: 1.5rem; color: #FF9933; font-size: 1.2rem;">— Jawaharlal Nehru</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Introduction with enhanced formatting and visual elements
        st.markdown("""
        <div class='story-text fade-in' style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin: 2rem 0; line-height: 1.8;">
            <p style="font-size: 1.2rem; margin-bottom: 1.5rem;">
                India's cultural heritage is a living testament to the country's rich history and diverse traditions. From the intricate dance forms that tell stories of gods and goddesses to the soul-stirring melodies of classical music, from the vibrant handicrafts that preserve ancient techniques to the architectural marvels that stand as silent witnesses to bygone eras - every aspect of Indian culture is a celebration of creativity, spirituality, and human ingenuity.
            </p>
            <p style="font-size: 1.2rem;">
                Our cultural heritage is not just a collection of artifacts and traditions; it's a living, breathing entity that continues to evolve while maintaining its deep-rooted connection to our past. It's a bridge between generations, a source of inspiration for the present, and a foundation for the future.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different aspects of cultural heritage with enhanced styling
        cult_tab1, cult_tab2, cult_tab3, cult_tab4 = st.tabs(["🎨 Arts & Crafts", "💃 Dance & Music", "🏛️ Monuments & Heritage", "🌱 Responsible Tourism"])
        
        # Load cultural data
        df_culture = load_cultural_data()
    
    with cult_tab1:
        with st.spinner("Rendering Arts & Crafts visualizations..."):
            st.markdown("<h3 class='section-heading'>The Artistic Tapestry of India</h3>", unsafe_allow_html=True)
            
            # Add decorative line with enhanced styling
            st.markdown("""
            <div style="display: flex; align-items: center; margin: 1.5rem 0 2rem;">
                <div style="flex-grow: 1; height: 2px; background: linear-gradient(to right, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
                <div style="margin: 0 20px; color: #FF9933; font-size: 24px;">❖</div>
                <div style="flex-grow: 1; height: 2px; background: linear-gradient(to left, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a section about art preservation
            st.markdown("""
            <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
                <h4 style="color: #FF9933; margin-top: 0; margin-bottom: 1rem;">Preserving Our Artistic Heritage</h4>
                <p style="font-size: 1.1rem; line-height: 1.6;">
                    India's traditional art forms are not just beautiful expressions of creativity; they are living links to our cultural past. Each stroke of the brush, each thread woven, and each piece of metal crafted carries forward centuries of wisdom and tradition. Through various initiatives and the dedication of master artisans, we continue to preserve and promote these invaluable art forms for future generations.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            # Create a horizontal bar chart for better readability
            import plotly.express as px
            
            # Create a copy of the dataframe to avoid modifying the original
            plot_df = df_culture.copy()
            
            # Ensure 'Cultural Element' is treated as a category for better visualization
            if 'Cultural Element' in plot_df.columns:
                plot_df['Cultural Element'] = plot_df['Cultural Element'].astype('category')
            
            fig = px.bar(plot_df, y='Cultural Element', x='Count', 
                        title='Richness of Indian Cultural Heritage',
                        color='Cultural Element',
                        orientation='h',
                        text='Count',
                        color_discrete_sequence=px.colors.qualitative.Bold)
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                yaxis_title="",
                xaxis_title="Count",
                title_font_size=24,
                plot_bgcolor='rgba(240, 240, 240, 0.1)',
                height=500,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add craft highlights section with enhanced styling
            st.markdown("<h4 style='color: #FF9933; margin-top: 2rem; margin-bottom: 1.5rem;'>Craft Highlights</h4>", unsafe_allow_html=True)
            
            craft_col1, craft_col2 = st.columns(2)
            
            with craft_col1:
                st.markdown("""
                <div style="background-color: rgba(35, 35, 45, 0.7); padding: 1.8rem; border-radius: 15px; margin-bottom: 1.5rem; height: 100%; border-left: 4px solid #FF9933;">
                    <h5 style="color: #FF9933; margin-top: 0; margin-bottom: 1rem; font-size: 1.2rem;">Textile Arts</h5>
                    <ul style="list-style-type: none; padding-left: 0;">
                        <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Banarasi Silk Weaving - The royal fabric of India</li>
                        <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Kalamkari Painting - Storytelling through natural dyes</li>
                        <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Bandhani Tie & Dye - The art of resist dyeing</li>
                        <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Phulkari Embroidery - The flower work of Punjab</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with craft_col2:
                st.markdown("""
                <div style="background-color: rgba(35, 35, 45, 0.7); padding: 1.8rem; border-radius: 15px; margin-bottom: 1.5rem; height: 100%; border-left: 4px solid #138808;">
                    <h5 style="color: #138808; margin-top: 0; margin-bottom: 1rem; font-size: 1.2rem;">Traditional Crafts</h5>
                    <ul style="list-style-type: none; padding-left: 0;">
                        <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Madhubani Painting - The art of storytelling</li>
                        <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Pattachitra Art - Scroll painting tradition</li>
                        <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Bidri Metal Work - The art of inlay</li>
                        <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Dokra Metal Casting - Ancient metal craft</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    
    with cult_tab2:
        st.markdown("<h3 class='section-heading'>The Rhythmic Heart of India</h3>", unsafe_allow_html=True)
        
        # Add decorative line with enhanced styling
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 1.5rem 0 2rem;">
            <div style="flex-grow: 1; height: 2px; background: linear-gradient(to right, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
            <div style="margin: 0 20px; color: #FF9933; font-size: 24px;">❖</div>
            <div style="flex-grow: 1; height: 2px; background: linear-gradient(to left, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add an introduction to dance and music
        st.markdown("""
        <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem; line-height: 1.8;">
                India's classical dance and music traditions are more than just performing arts; they are spiritual practices that have evolved over thousands of years. Each movement, each note, and each rhythm carries deep philosophical meaning and connects us to our cultural roots. These art forms continue to inspire and influence artists worldwide while maintaining their authentic essence.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a more interactive dance forms section with enhanced styling
        dance_forms = {
            "Bharatanatyam": {
                "region": "Tamil Nadu",
                "origin": "2000+ years old, originated in temples",
                "features": "Characterized by bent knees, precise footwork, and geometric patterns. Uses elaborate eye and hand gestures (mudras).",
                "significance": "One of the oldest classical dance forms, it embodies the essence of Indian classical dance traditions.",
                "preservation": "Regular performances in temples and cultural centers, dedicated training institutions"
            },
            "Kathakali": {
                "region": "Kerala",
                "origin": "17th century, originated in temples of Kerala",
                "features": "Known for elaborate costumes, makeup, and face masks. Performers use their entire body for expression with special emphasis on facial movements.",
                "significance": "A unique blend of dance, drama, and music that brings ancient stories to life.",
                "preservation": "Traditional training centers (kalari), annual festivals, UNESCO recognition"
            },
            "Kathak": {
                "region": "North India",
                "origin": "Mughal courts, blend of Hindu and Islamic influences",
                "features": "Famous for fast, rhythmic footwork and multiple spins (chakkars). Combines storytelling with rhythmic patterns.",
                "significance": "Represents the cultural synthesis of Hindu and Islamic traditions.",
                "preservation": "Guru-shishya parampara, cultural festivals, modern adaptations"
            },
            "Odissi": {
                "region": "Odisha",
                "origin": "2nd century BCE in temples of Odisha",
                "features": "Recognizable by the characteristic tribhangi posture (three bends). Fluid, lyrical movements with sculpture-like poses.",
                "significance": "Known as the dance of divine love and devotion.",
                "preservation": "Temple traditions, government support, international recognition"
            },
            "Kuchipudi": {
                "region": "Andhra Pradesh",
                "origin": "17th century in the village of Kuchipudi",
                "features": "Combines dance with drama. Known for tarangam - dancing on a brass plate and performing with a pot balanced on the head.",
                "significance": "A perfect blend of grace, strength, and storytelling.",
                "preservation": "Village traditions, modern adaptations, global performances"
            },
            "Manipuri": {
                "region": "Manipur",
                "origin": "Ancient tradition linked to indigenous rituals",
                "features": "Characterized by gentle, graceful movements. Performers' feet never strike the ground forcefully out of respect for Earth.",
                "significance": "Celebrates the divine love of Radha and Krishna through gentle, flowing movements.",
                "preservation": "Community participation, religious festivals, cultural institutions"
            },
            "Mohiniyattam": {
                "region": "Kerala",
                "origin": "18th century royal courts of Travancore",
                "features": "Known as the 'dance of the enchantress.' Features gentle, swaying movements resembling palm trees in the Kerala countryside.",
                "significance": "The only classical dance form that exclusively features female performers.",
                "preservation": "Traditional training centers, cultural festivals, modern interpretations"
            },
            "Sattriya": {
                "region": "Assam",
                "origin": "15th century monasteries (sattras)",
                "features": "Combines rhythmic foot movements with hand gestures and facial expressions to convey mythological stories.",
                "significance": "A living tradition that continues to evolve while maintaining its spiritual essence.",
                "preservation": "Monastery traditions, cultural festivals, contemporary adaptations"
            }
        }
        
        # Create columns for dance form selection and display with enhanced styling
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Create a radio selector for dance forms with improved formatting
            selected_dance = st.radio(
                "Select a Classical Dance Form:",
                list(dance_forms.keys()),
                key="dance_selector"
            )
        
        with col2:
            # Display information about the selected dance form in a visually appealing card
            dance_info = dance_forms[selected_dance]
            
            st.markdown(f"""
            <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; border-left: 4px solid #FF9933; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <h4 style="color: #FF9933; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.4rem;">{selected_dance}</h4>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Region:</strong> {dance_info['region']}</p>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Origin:</strong> {dance_info['origin']}</p>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Key Features:</strong> {dance_info['features']}</p>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Cultural Significance:</strong> {dance_info['significance']}</p>
                <p style="margin-bottom: 0;"><strong style="color: #DDDDDD;">Preservation Efforts:</strong> {dance_info['preservation']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a section for classical music traditions with enhanced styling
        st.markdown("<h3 class='section-heading' style='margin-top:40px;'>Classical Music Traditions</h3>", unsafe_allow_html=True)
        
        music_col1, music_col2 = st.columns(2)
        
        with music_col1:
            st.markdown("""
            <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; height:100%; border-left: 4px solid #FF9933; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <h4 style="color: #FF9933; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.4rem;">Hindustani Classical Music</h4>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Region:</strong> North India</p>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Key Forms:</strong> Dhrupad, Khayal, Thumri, Ghazal</p>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Instruments:</strong> Sitar, Tabla, Sarod, Shehnai, Sarangi</p>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Preservation:</strong> Guru-shishya parampara, music festivals, digital archives</p>
                <p style="font-style: italic; color: #AAAAAA; margin-bottom: 0;">Influenced by Persian and Islamic traditions, with emphasis on improvisation within a structured framework.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with music_col2:
            st.markdown("""
            <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; height:100%; border-left: 4px solid #138808; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <h4 style="color: #138808; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.4rem;">Carnatic Classical Music</h4>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Region:</strong> South India</p>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Key Forms:</strong> Kriti, Varnam, Tillana, Javali</p>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Instruments:</strong> Veena, Mridangam, Violin, Flute, Gottuvadyam</p>
                <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Preservation:</strong> Traditional learning, music sabhas, digital documentation</p>
                <p style="font-style: italic; color: #AAAAAA; margin-bottom: 0;">Maintains stronger adherence to traditional compositions, with a different approach to raga and tala systems.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with cult_tab3:
        st.markdown("<h3 class='section-heading'>India's Architectural Heritage</h3>", unsafe_allow_html=True)
        
        # Add decorative line with enhanced styling
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 1.5rem 0 2rem;">
            <div style="flex-grow: 1; height: 2px; background: linear-gradient(to right, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
            <div style="margin: 0 20px; color: #FF9933; font-size: 24px;">❖</div>
            <div style="flex-grow: 1; height: 2px; background: linear-gradient(to left, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add an introduction to heritage sites
        st.markdown("""
        <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem; line-height: 1.8;">
                India's architectural heritage is a testament to the country's rich history and cultural diversity. From ancient cave temples to magnificent palaces, from intricate stepwells to grand forts, each structure tells a unique story of the people, their beliefs, and their way of life. These monuments are not just stone and mortar; they are living witnesses to India's glorious past and continue to inspire awe and wonder in visitors from around the world.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create an interactive exploration of heritage sites with enhanced styling
        heritage_sites = {
            "Taj Mahal": {
                "location": "Agra, Uttar Pradesh",
                "year_listed": 1983,
                "type": "Cultural",
                "description": "An ivory-white marble mausoleum built by Emperor Shah Jahan in memory of his wife Mumtaz Mahal. A symbol of eternal love and architectural perfection.",
                "significance": "One of the Seven Wonders of the World, representing the pinnacle of Mughal architecture.",
                "preservation": "Regular maintenance, visitor management, environmental protection"
            },
            "Ajanta Caves": {
                "location": "Maharashtra",
                "year_listed": 1983,
                "type": "Cultural",
                "description": "Buddhist cave monuments dating from the 2nd century BCE to about 480 CE, featuring paintings and sculptures that depict the life of Buddha.",
                "significance": "Home to some of the finest surviving examples of ancient Indian art.",
                "preservation": "Climate control, visitor restrictions, digital documentation"
            },
            "Ellora Caves": {
                "location": "Maharashtra",
                "year_listed": 1983,
                "type": "Cultural",
                "description": "A complex of 34 caves representing Buddhist, Jain, and Hindu monuments dating from 600-1000 CE, showcasing religious harmony.",
                "significance": "A unique example of religious tolerance and artistic excellence.",
                "preservation": "Structural reinforcement, visitor management, environmental monitoring"
            },
            "Khajuraho Group of Monuments": {
                "location": "Madhya Pradesh",
                "year_listed": 1986,
                "type": "Cultural",
                "description": "Temples known for their nagara-style architectural symbolism and intricate sculptures depicting various aspects of life.",
                "significance": "Celebrates the celebration of life in all its forms through art.",
                "preservation": "Regular conservation, visitor education, cultural events"
            },
            "Hampi": {
                "location": "Karnataka",
                "year_listed": 1986,
                "type": "Cultural",
                "description": "The ruins of Vijayanagara, the former capital of the Vijayanagara Empire, featuring stunning temple complexes and royal structures.",
                "significance": "A testament to the grandeur of one of India's greatest empires.",
                "preservation": "Archaeological conservation, sustainable tourism, community involvement"
            },
            "Jaipur City": {
                "location": "Rajasthan",
                "year_listed": 2019,
                "type": "Cultural",
                "description": "Known as the 'Pink City,' featuring remarkable architecture including palaces, city walls, and streets planned according to Vastu Shastra.",
                "significance": "A living example of urban planning and architectural excellence.",
                "preservation": "Urban conservation, heritage regulations, community participation"
            },
            "Western Ghats": {
                "location": "Multiple states",
                "year_listed": 2012,
                "type": "Natural",
                "description": "One of the world's biodiversity hotspots with exceptional levels of plant and animal diversity, including many endemic species.",
                "significance": "A crucial ecological region that influences India's climate and biodiversity.",
                "preservation": "Ecosystem protection, sustainable development, community conservation"
            },
            "Great Himalayan National Park": {
                "location": "Himachal Pradesh",
                "year_listed": 2014,
                "type": "Natural",
                "description": "Contains high alpine peaks, alpine meadows, and riverine forests with many endangered species, including the snow leopard.",
                "significance": "A vital conservation area for Himalayan biodiversity.",
                "preservation": "Wildlife protection, sustainable tourism, local community involvement"
            }
        }
        
        # Add filtering options with enhanced styling
        st.markdown("""
        <div style="background-color: rgba(35, 35, 45, 0.7); padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <h4 style="color: #FF9933; margin-top: 0; margin-bottom: 1rem; font-size: 1.3rem;">Explore Heritage Sites</h4>
            <p style="color: #DDDDDD; margin-bottom: 1rem;">Discover India's rich heritage through its magnificent monuments and natural wonders. Each site tells a unique story of our cultural and natural heritage.</p>
        """, unsafe_allow_html=True)
        
        site_type = st.radio(
            "Filter by type:",
            ["All", "Cultural", "Natural"],
            horizontal=True
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Filter sites based on selection
        filtered_sites = heritage_sites
        if site_type != "All":
            filtered_sites = {k: v for k, v in heritage_sites.items() if v["type"] == site_type}
        
        # Create a grid layout for the sites with enhanced styling
        num_cols = 2
        cols = st.columns(num_cols)
        
        for i, (site_name, site_info) in enumerate(filtered_sites.items()):
            with cols[i % num_cols]:
                st.markdown(f"""
                <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; height: 100%; border-left: 4px solid #FF9933; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    <h4 style="color: #FF9933; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.4rem;">{site_name}</h4>
                    <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Location:</strong> {site_info['location']}</p>
                    <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Type:</strong> {site_info['type']}</p>
                    <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Year Listed:</strong> {site_info['year_listed']}</p>
                    <p style="margin-bottom: 1rem;">{site_info['description']}</p>
                    <p style="margin-bottom: 1rem;"><strong style="color: #DDDDDD;">Significance:</strong> {site_info['significance']}</p>
                    <p style="margin-bottom: 0;"><strong style="color: #DDDDDD;">Preservation:</strong> {site_info['preservation']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Add metrics section with enhanced styling
        st.markdown("""
        <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin-top: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <h4 style="color: #FF9933; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.3rem;">Heritage Statistics</h4>
            <p style="color: #DDDDDD; margin-bottom: 1.5rem;">India's rich heritage is recognized globally through UNESCO World Heritage Sites, showcasing our commitment to preserving cultural and natural treasures.</p>
        """, unsafe_allow_html=True)
        
        site_metrics_col1, site_metrics_col2, site_metrics_col3 = st.columns(3)
        
        with site_metrics_col1:
            st.metric(
                label="Total UNESCO Sites",
                value="40",
                delta="Ranked 6th globally"
            )
        
        with site_metrics_col2:
            st.metric(
                label="Cultural Sites",
                value="32",
                delta="80% of total"
            )
        
        with site_metrics_col3:
            st.metric(
                label="Natural Sites",
                value="7",
                delta="17.5% of total"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with cult_tab4:
        st.markdown("<h3 class='section-heading'>Responsible Tourism</h3>", unsafe_allow_html=True)
        
        # Add decorative line with enhanced styling
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 1.5rem 0 2rem;">
            <div style="flex-grow: 1; height: 2px; background: linear-gradient(to right, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
            <div style="margin: 0 20px; color: #FF9933; font-size: 24px;">❖</div>
            <div style="flex-grow: 1; height: 2px; background: linear-gradient(to left, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add introduction to responsible tourism
        st.markdown("""
        <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem; line-height: 1.8;">
                Responsible tourism is about making better places for people to live in and better places for people to visit. It's about respecting local cultures, supporting local economies, and preserving our natural and cultural heritage for future generations. As we explore India's rich cultural heritage, let's do so with mindfulness and respect.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for different aspects of responsible tourism
        rt_col1, rt_col2 = st.columns(2)
        
        with rt_col1:
            st.markdown("""
            <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; height: 100%; border-left: 4px solid #FF9933;">
                <h4 style="color: #FF9933; margin-top: 0; margin-bottom: 1.5rem;">Cultural Respect</h4>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Learn about local customs and traditions before visiting</li>
                    <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Dress appropriately for religious and cultural sites</li>
                    <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Respect photography restrictions</li>
                    <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Support local artisans and craftspeople</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with rt_col2:
            st.markdown("""
            <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; height: 100%; border-left: 4px solid #138808;">
                <h4 style="color: #138808; margin-top: 0; margin-bottom: 1.5rem;">Environmental Care</h4>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Minimize waste and use eco-friendly products</li>
                    <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Respect wildlife and natural habitats</li>
                    <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Use water and energy resources wisely</li>
                    <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Support conservation initiatives</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a section about supporting local communities
        st.markdown("""
        <div style="background-color: rgba(35, 35, 45, 0.7); padding: 2rem; border-radius: 15px; margin-top: 2rem;">
            <h4 style="color: #FF9933; margin-top: 0; margin-bottom: 1.5rem;">Supporting Local Communities</h4>
            <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 1.5rem;">
                When visiting cultural sites and heritage locations, consider how your visit can benefit local communities:
            </p>
            <ul style="list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Stay in locally-owned accommodations</li>
                <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Eat at local restaurants and try traditional cuisine</li>
                <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Purchase authentic handicrafts directly from artisans</li>
                <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Engage with local guides and learn from their knowledge</li>
                <li style="margin-bottom: 1rem; font-size: 1.1rem;">• Respect local customs and contribute positively to the community</li>
            </ul>
        </div>
        """, unsafe_allow_html=True) 