import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from modules.utils import load_state_data, apply_dark_theme, load_geography_data

def render():
    st.markdown("<h2 class='chapter-heading'>Geographical Diversity: The Varied Landscapes of India</h2>", unsafe_allow_html=True)
    
    # Introduction with better formatting
    st.markdown("""
    <div class='story-text'>
    India's geography is as diverse as its culture. From the snow-capped Himalayas in the north to the tropical beaches 
    of the south, from the arid Thar Desert in the west to the lush rainforests of the northeast, India encompasses a wide 
    range of ecosystems and landscapes, making it one of the most geographically diverse countries in the world.
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different geographical aspects
    geo_tab1, geo_tab2, geo_tab3 = st.tabs(["Landscapes & Ecosystems", "Population & Regions", "Biodiversity"])
    
    with geo_tab1:
        try:
            # Geographical diversity data with better visualization
            geo_features = {
                "Feature": ["Mountain Ranges", "River Systems", "Deserts", "Forests", "Coastline", "Islands"],
                "Count": [7, 7, 1, 4, 1, 1],
                "Examples": [
                    "Himalayas, Western Ghats, Eastern Ghats, Aravalli, Vindhya, Satpura, Karakoram",
                    "Ganga, Brahmaputra, Yamuna, Godavari, Krishna, Narmada, Kaveri",
                    "Thar Desert",
                    "Tropical Rainforests, Deciduous Forests, Alpine Forests, Mangroves",
                    "7,516 km coastline along the Arabian Sea, Bay of Bengal, and Indian Ocean",
                    "Andaman and Nicobar Islands, Lakshadweep Islands"
                ]
            }
            
            df_geo = pd.DataFrame(geo_features)
            
            # Split the display into columns for better organization
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("<h3 class='section-heading'>Major Geographical Features</h3>", unsafe_allow_html=True)
                
                # Create a horizontal bar chart for better visualization
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                fig = px.bar(df_geo, y='Feature', x='Count', 
                            orientation='h',
                            title='Geographical Features of India',
                            color='Feature',
                            text='Count',
                            color_discrete_sequence=px.colors.qualitative.Bold)
                
                fig.update_traces(textposition='outside')
                # Apply dark theme
                fig = apply_dark_theme(fig)
                fig.update_layout(
                    yaxis_title="",
                    xaxis_title="Count",
                    title_font_size=20,
                    showlegend=False,  # Hide legend as it's redundant
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("<h3 class='section-heading'>Details of Geographical Features</h3>", unsafe_allow_html=True)
                
                # Make the dataframe more visually appealing
                st.dataframe(
                    df_geo[['Feature', 'Examples']],
                    use_container_width=True,
                    height=400
                )
            
            # Try to load geography data
            try:
                geo_data = load_geography_data()
                if geo_data is not None and not geo_data.empty:
                    # Display a terrain distribution chart if data is available
                    st.markdown("<h3 class='section-heading' style='margin-top:30px;'>Terrain Distribution</h3>", unsafe_allow_html=True)
                    
                    if 'Terrain_Type' in geo_data.columns and 'Percentage' in geo_data.columns:
                        # Create pie chart for terrain distribution
                        fig = px.pie(
                            geo_data, 
                            values='Percentage', 
                            names='Terrain_Type',
                            title='Distribution of Terrain Types in India',
                            color_discrete_sequence=px.colors.qualitative.Bold,
                            hole=0.4
                        )
                        
                        # Apply dark theme
                        fig = apply_dark_theme(fig)
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        fig.update_layout(
                            title_font_size=20,
                            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Geography data found but missing required columns.")
            except Exception as e:
                # Silently handle missing geography data - it's optional
                pass
            
            # Create an interactive section to explore different landscapes
            st.markdown("<h3 class='section-heading' style='margin-top:30px;'>Explore India's Diverse Landscapes</h3>", unsafe_allow_html=True)
            
            landscape_types = {
                "Himalayan Mountains": {
                    "region": "Northern India",
                    "states": "Jammu & Kashmir, Himachal Pradesh, Uttarakhand, Sikkim, Arunachal Pradesh",
                    "features": "Home to some of the world's highest peaks, alpine meadows, glaciers, and unique biodiversity. Serves as the water source for major Indian rivers.",
                    "color": "#8A9A5B"  # Mountain green
                },
                "Indo-Gangetic Plains": {
                    "region": "Northern & Eastern India",
                    "states": "Punjab, Haryana, Uttar Pradesh, Bihar, West Bengal",
                    "features": "Fertile alluvial plains formed by the Ganges and its tributaries. One of the most densely populated and agriculturally productive regions in the world.",
                    "color": "#9ACD32"  # Yellowgreen
                },
                "Thar Desert": {
                    "region": "Western India",
                    "states": "Rajasthan, Gujarat, Punjab, Haryana",
                    "features": "The 17th largest desert in the world, with unique desert ecology, sand dunes, and oasis settlements. Home to distinctive cultural traditions adapted to the arid environment.",
                    "color": "#DAA520"  # Goldenrod
                },
                "Deccan Plateau": {
                    "region": "Central & Southern India",
                    "states": "Maharashtra, Karnataka, Telangana, Andhra Pradesh, Tamil Nadu",
                    "features": "Ancient triangular plateau bounded by the Western and Eastern Ghats. Rich in minerals and characterized by black soil regions ideal for cotton cultivation.",
                    "color": "#B87333"  # Copper
                },
                "Western Ghats": {
                    "region": "Western India",
                    "states": "Maharashtra, Goa, Karnataka, Tamil Nadu, Kerala",
                    "features": "UNESCO World Heritage Site and one of the world's biodiversity hotspots. Contains tropical rainforests, rivers, and endemic species. Older than the Himalayas.",
                    "color": "#228B22"  # Forest green
                },
                "Eastern Ghats": {
                    "region": "Eastern India",
                    "states": "Odisha, Andhra Pradesh, Tamil Nadu",
                    "features": "Discontinuous mountain range running parallel to the eastern coast. Lower in elevation than the Western Ghats but rich in minerals and tribal cultures.",
                    "color": "#6B8E23"  # Olive drab
                },
                "Coastal Regions": {
                    "region": "Peninsular India",
                    "states": "Gujarat, Maharashtra, Goa, Karnataka, Kerala, Tamil Nadu, Andhra Pradesh, Odisha, West Bengal",
                    "features": "7,516 km of coastline featuring beaches, lagoons, estuaries, and mangrove forests. Distinct coastal cultures and economies based on fishing and maritime trade.",
                    "color": "#00CED1"  # Dark turquoise
                }
            }
            
            # Create a selectbox for landscape selection
            selected_landscape = st.selectbox("Select a landscape to explore:", list(landscape_types.keys()))
            
            # Display information about the selected landscape
            landscape_info = landscape_types[selected_landscape]
            
            # Use the custom color for the selected landscape
            bg_color = landscape_info['color']
            text_color = "#FFFFFF" if landscape_info['color'] in ["#228B22", "#6B8E23", "#8A9A5B"] else "#000000"
            
            st.markdown(f"""
            <div style="background-color:{bg_color}; padding:20px; border-radius:10px; margin-top:15px; color:{text_color};">
                <h4 style="margin-top:0;">{selected_landscape}</h4>
                <p><strong>Region:</strong> {landscape_info['region']}</p>
                <p><strong>States:</strong> {landscape_info['states']}</p>
                <p><strong>Features:</strong> {landscape_info['features']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error in Landscapes & Ecosystems tab: {e}")
    
    with geo_tab2:
        try:
            # State populations by region with better layout
            df_states = load_state_data()
            
            if df_states is not None and not df_states.empty:
                st.markdown("<h3 class='section-heading'>Population Distribution by Region</h3>", unsafe_allow_html=True)
                
                # Group by region and sum population
                region_population = df_states.groupby('Region')['Population (millions)'].sum().reset_index()
                region_population = region_population.sort_values('Population (millions)', ascending=False)
                
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    # Create a pie chart with better styling
                    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                    fig = px.pie(region_population, values='Population (millions)', names='Region',
                                title='Population Distribution by Region',
                                color='Region',
                                color_discrete_sequence=px.colors.qualitative.Bold,
                                hole=0.4)
                    
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(
                        title_font_size=20,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                        annotations=[dict(text='1.3+ Billion<br>People', x=0.5, y=0.5, font_size=15, showarrow=False)]
                    )
                    
                    # Apply dark theme
                    fig = apply_dark_theme(fig)
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    # Add a dataframe showing population by region
                    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)  # Add spacing for alignment
                    
                    # Format population values with commas
                    df_display = region_population.copy()
                    df_display['Population (millions)'] = df_display['Population (millions)'].apply(lambda x: f"{x:.1f} M")
                    
                    st.dataframe(
                        df_display,
                        use_container_width=True
                    )
                    
                    # Add key insight
                    st.markdown("<div class='data-insight'>The North and East regions together account for nearly 60% of India's population, with the highest population density in the Indo-Gangetic plains.</div>", unsafe_allow_html=True)
                
                # State literacy rates with improved visualization
                st.markdown("<h3 class='section-heading' style='margin-top:30px;'>Literacy Rates Across States</h3>", unsafe_allow_html=True)
                
                # Create a map-like visualization of literacy by state
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                
                # Sort by literacy rate for better visualization
                sorted_literacy = df_states.sort_values('Literacy Rate (%)', ascending=False)
                
                # Use a color-blind friendly palette
                fig = px.bar(sorted_literacy, 
                            x='State', y='Literacy Rate (%)',
                            title='Literacy Rates by State',
                            color='Region',
                            color_discrete_sequence=px.colors.qualitative.Bold,
                            hover_data=['Population (millions)'])
                
                # Apply dark theme
                fig = apply_dark_theme(fig)
                
                # Add a horizontal line for the national average
                national_avg = df_states['Literacy Rate (%)'].mean()
                fig.add_shape(
                    type="line",
                    x0=-0.5,
                    y0=national_avg,
                    x1=len(df_states)-0.5,
                    y1=national_avg,
                    line=dict(
                        color="red",
                        width=2,
                        dash="dash",
                    )
                )
                fig.add_annotation(
                    x=len(df_states)/2,
                    y=national_avg + 2,
                    text=f"National Average: {national_avg:.1f}%",
                    showarrow=False,
                    font=dict(color="red")
                )
                
                fig.update_layout(
                    title_font_size=20,
                    xaxis_title="",
                    yaxis_title="Literacy Rate (%)",
                    xaxis={'categoryorder':'total descending', 'tickangle': 45},
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='data-insight'>Kerala has consistently maintained the highest literacy rate in India, often above 90%, which is comparable to many developed nations. There's a notable correlation between literacy rates and human development indicators across states.</div>", unsafe_allow_html=True)
                
                # Add a state comparison tool
                st.markdown("<h3 class='section-heading' style='margin-top:30px;'>Compare States</h3>", unsafe_allow_html=True)
                
                # Allow users to select states to compare
                col1, col2 = st.columns(2)
                with col1:
                    state1 = st.selectbox("Select first state:", df_states['State'].tolist(), index=0)
                with col2:
                    # Default to a different state for comparison
                    default_idx = 1 if len(df_states) > 1 else 0
                    state2 = st.selectbox("Select second state:", df_states['State'].tolist(), index=default_idx)
                
                # Get data for selected states
                state1_data = df_states[df_states['State'] == state1].iloc[0]
                state2_data = df_states[df_states['State'] == state2].iloc[0]
                
                # Create comparison dataframe
                comparison_data = pd.DataFrame({
                    'Metric': ['Population (millions)', 'Area (sq km)', 'Literacy Rate (%)', 'HDI', 'Urbanization (%)'],
                    state1: [state1_data['Population (millions)'], state1_data['Area (sq km)'], 
                            state1_data['Literacy Rate (%)'], state1_data['HDI'], state1_data['Urbanization (%)']],
                    state2: [state2_data['Population (millions)'], state2_data['Area (sq km)'], 
                            state2_data['Literacy Rate (%)'], state2_data['HDI'], state2_data['Urbanization (%)']],
                })
                
                # Create visual comparison
                fig = px.bar(comparison_data, x='Metric', y=[state1, state2], barmode='group',
                            title=f'Comparison: {state1} vs {state2}',
                            color_discrete_sequence=['#FF9933', '#138808'])
                
                # Apply dark theme
                fig = apply_dark_theme(fig)
                
                fig.update_layout(
                    xaxis_title="",
                    yaxis_title="Value",
                    legend_title="State"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show additional state info
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div style="background-color:rgba(255, 153, 51, 0.2); padding:15px; border-radius:5px;">
                        <h4>{state1}</h4>
                        <p><strong>Capital:</strong> {state1_data['Capital']}</p>
                        <p><strong>Region:</strong> {state1_data['Region']}</p>
                        <p><strong>Official Languages:</strong> {state1_data['Official Languages']}</p>
                        <p><strong>Major Crops:</strong> {state1_data['Major Crops']}</p>
                        <p><strong>Key Industries:</strong> {state1_data['Key Industries']}</p>
                        <p><strong>Famous Destinations:</strong> {state1_data['Famous Destinations']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background-color:rgba(19, 136, 8, 0.2); padding:15px; border-radius:5px;">
                        <h4>{state2}</h4>
                        <p><strong>Capital:</strong> {state2_data['Capital']}</p>
                        <p><strong>Region:</strong> {state2_data['Region']}</p>
                        <p><strong>Official Languages:</strong> {state2_data['Official Languages']}</p>
                        <p><strong>Major Crops:</strong> {state2_data['Major Crops']}</p>
                        <p><strong>Key Industries:</strong> {state2_data['Key Industries']}</p>
                        <p><strong>Famous Destinations:</strong> {state2_data['Famous Destinations']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Failed to load state data. Please check your data files.")
        except Exception as e:
            st.error(f"Error in Population & Regions tab: {e}")
    
    with geo_tab3:
        try:
            st.markdown("<h3 class='section-heading'>India's Biodiversity</h3>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class='story-text'>
            India is one of the 17 megadiverse countries in the world, hosting 7-8% of all recorded species
            including over 45,000 plant species and 91,000 animal species. The country has diverse ecosystems
            ranging from the Himalayas to coastal systems, each hosting unique flora and fauna.
            </div>
            """, unsafe_allow_html=True)
            
            # Biodiversity hotspots data
            biodiversity_data = {
                "Hotspot": [
                    "Western Ghats", 
                    "Eastern Himalayas", 
                    "Indo-Burma Region", 
                    "Sundaland (Nicobar Islands)"
                ],
                "Plant Species": [5000, 5800, 13500, 10000],
                "Endemic Plant Species": [1500, 3500, 7000, 6500],
                "Vertebrate Species": [1022, 1500, 2185, 1800],
                "Endemic Vertebrate Species": [355, 528, 518, 649],
                "Remaining Habitat %": [23, 32, 5, 7]
            }
            
            df_biodiversity = pd.DataFrame(biodiversity_data)
            
            # Create a visually appealing bar chart for biodiversity hotspots
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            fig = px.bar(
                df_biodiversity, 
                x='Hotspot', 
                y=['Endemic Plant Species', 'Endemic Vertebrate Species'],
                title='Endemic Species in India\'s Biodiversity Hotspots',
                barmode='group',
                color_discrete_sequence=['#4CAF50', '#FFC107']
            )
            
            # Apply dark theme
            fig = apply_dark_theme(fig)
            
            fig.update_layout(
                xaxis_title="Biodiversity Hotspot",
                yaxis_title="Number of Endemic Species",
                legend_title="Species Type"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Protected areas information
            st.markdown("<h3 class='section-heading' style='margin-top:30px;'>Protected Areas</h3>", unsafe_allow_html=True)
            
            protected_data = {
                "Type": ["National Parks", "Wildlife Sanctuaries", "Conservation Reserves", "Community Reserves", "Tiger Reserves", "Elephant Reserves", "Biosphere Reserves"],
                "Count": [103, 566, 97, 214, 53, 33, 18]
            }
            
            df_protected = pd.DataFrame(protected_data)
            
            # Split into columns for better layout
            col1, col2 = st.columns([3, 2])
            
            with col1:
                # Create a horizontal bar chart for protected areas
                fig = px.bar(
                    df_protected.sort_values('Count', ascending=True), 
                    y='Type', 
                    x='Count',
                    title='Protected Areas in India',
                    orientation='h',
                    color='Count',
                    color_continuous_scale='Viridis',
                    text='Count'
                )
                
                # Apply dark theme
                fig = apply_dark_theme(fig)
                
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    yaxis_title="",
                    xaxis_title="Number of Protected Areas",
                    coloraxis_showscale=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Add key insight about protected areas
                st.markdown("""
                <div class='data-insight'>
                India has established a comprehensive network of protected areas covering approximately 5% of the total
                geographical area of the country. These protected areas are crucial for conservation of the country's
                rich biodiversity.
                </div>
                """, unsafe_allow_html=True)
                
                # Total protected areas
                total_protected = df_protected['Count'].sum()
                
                st.markdown(f"""
                <div style="background-color:rgba(76, 175, 80, 0.3); padding:20px; border-radius:10px; margin-top:20px; text-align:center;">
                    <h2 style="margin:0;">{total_protected}</h2>
                    <p style="margin:5px 0 0 0;">Total Protected Areas</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Interesting biodiversity facts
            st.markdown("<h3 class='section-heading' style='margin-top:30px;'>Biodiversity Highlights</h3>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div style="background-color:rgba(255, 193, 7, 0.2); padding:15px; border-radius:10px; height:100%;">
                    <h4 style="margin-top:0;">Flora</h4>
                    <p>India has over 45,000 plant species</p>
                    <p>33% of Indian flora are endemic</p>
                    <p>Home to 6,500 medicinal plant species</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color:rgba(33, 150, 243, 0.2); padding:15px; border-radius:10px; height:100%;">
                    <h4 style="margin-top:0;">Fauna</h4>
                    <p>91,000 animal species recorded</p>
                    <p>The only country with both lions and tigers</p>
                    <p>12.6% of world's bird species found here</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="background-color:rgba(233, 30, 99, 0.2); padding:15px; border-radius:10px; height:100%;">
                    <h4 style="margin-top:0;">Conservation</h4>
                    <p>53 dedicated tiger reserves</p>
                    <p>Home to 75% of world's wild tigers</p>
                    <p>Over 100 national parks established</p>
                </div>
                """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error in Biodiversity tab: {e}") 