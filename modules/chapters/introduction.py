import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from modules.utils import load_population_data, load_state_data, load_cultural_data, load_festivals_data, style_matplotlib_for_dark, apply_dark_theme

def render():
    with st.spinner("Preparing Introduction chapter..."):
        st.markdown("<h2 class='chapter-heading'>Introduction to India's Cultural Tapestry</h2>", unsafe_allow_html=True)
        
        # Add centered introductory text
        st.markdown("""
        <div style="text-align: center; margin: 1.5rem auto; max-width: 800px; padding: 1rem; background: linear-gradient(135deg, rgba(255, 153, 51, 0.05), rgba(19, 136, 8, 0.05)); border-radius: 10px;">
            <p style="font-size: 1.4rem; font-weight: 300; line-height: 1.6; color: #FFFFFF; font-style: italic;">
                Experience the vibrant colors, rich traditions, and ancient wisdom of the world's largest democracy
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Fix the Nehru quote styling
        st.markdown("""
        <div style="background-color: rgba(35, 35, 45, 0.7); border-radius: 10px; padding: 2rem; margin: 1.5rem 0; position: relative; border-left: 4px solid #FF9933;">
            <div style="position: absolute; top: 10px; left: 20px; font-family: Georgia, serif; font-size: 4rem; color: #FF9933; opacity: 0.6; line-height: 0;">"</div>
            <p style="font-size: 1.3rem; line-height: 1.6; text-align: center; font-style: italic; margin: 0.5rem 3rem; color: #F5F5F5;">
                India is not a nation, nor a country. It is a subcontinent of nationalities.
            </p>
            <div style="position: absolute; bottom: 10px; right: 20px; font-family: Georgia, serif; font-size: 4rem; color: #FF9933; opacity: 0.6; line-height: 0;">"</div>
            <p style="text-align: right; margin-top: 1rem; color: #FF9933; font-size: 1.1rem;">— Jawaharlal Nehru</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Project Mission Statement - Enhanced with better spacing and visual elements
        st.markdown("""
        <div style="margin: 1.5rem 0; padding: 1.5rem; background-color: rgba(255, 153, 51, 0.05); border-radius: 10px; border-left: 4px solid #FF9933; text-align: center;">
            <div class='tricolor-bar' style="height: 3px; background: linear-gradient(to right, #FF9933, #FFFFFF, #138808); margin: 0 auto 1rem; width: 80%; border-radius: 3px;"></div>
            <div class='story-text fade-in' style="margin: 1rem auto; padding: 0 1rem; max-width: 90%;">
                <span style="font-size: 1.5rem; font-weight: 500; color: #FF9933; display: block; margin-bottom: 0.8rem;">Our Mission</span>
                <p style="font-size: 1.15rem; line-height: 1.8; letter-spacing: 0.2px; text-align: center;">
                    To celebrate, preserve, and visualize India's extraordinary cultural heritage through data storytelling, 
                    creating an immersive journey that bridges ancient traditions with modern analytics.
                </p>
            </div>
            <div class='tricolor-bar' style="height: 3px; background: linear-gradient(to right, #FF9933, #FFFFFF, #138808); margin: 1rem auto 0; width: 80%; border-radius: 3px;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Introduction section with improved formatting - Content moved from header
        st.markdown("""
        <div class='story-text fade-in'>
        India, a land of extraordinary diversity, presents a fascinating tapestry of cultures, languages, religions, and artistic traditions. 
        This data story takes you through a journey across the subcontinent, exploring the rich heritage and vibrant cultural mosaic of 
        Indian society through immersive data visualization and storytelling.

        From the ancient classical dance forms of the south to the intricate handicrafts of the north, from millennia-old temples to contemporary art movements,
        India's cultural expressions reflect both timeless continuity and dynamic evolution, making it one of the world's most culturally rich civilizations.
        </div>
        """, unsafe_allow_html=True)
        
        # Use st.container for better control over layout
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                <div class='story-text'>
                India's artistic and cultural heritage spans over 5,000 years, shaped by diverse civilizations, empires, and traditions. With 28 states and 8 union territories, each region contributes unique artistic expressions, crafts, music, dance, and architectural styles to the nation's cultural identity.
                
                This rich cultural landscape has been recognized globally, with India having 40 UNESCO World Heritage sites and numerous art forms designated as Intangible Cultural Heritage treasures.
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div class='data-insight'>India's cultural diversity is reflected in its 22 officially recognized languages, 1,600+ dialects, 8 major classical dance forms, and thousands of folk art traditions that continue to thrive across the country.</div>", unsafe_allow_html=True)
            
            with col2:
                # Population Growth visualization with better formatting
                with st.spinner("Loading population data visualization..."):
                    try:
                        df_population = load_population_data()
                        
                        with st.container():
                            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                            # Check if data is loaded correctly
                            if df_population is not None and not df_population.empty:
                                # Convert to appropriate types if needed
                                df_population['Year'] = df_population['Year'].astype(int)
                                df_population['Population (millions)'] = df_population['Population (millions)'].astype(float)
                                
                                # Create a responsive figure size
                                fig, ax = plt.subplots(figsize=(8, 6))
                                ax.plot(df_population['Year'], df_population['Population (millions)'], 
                                        marker='o', linestyle='-', color='#FF9933', linewidth=2, markersize=8)
                                ax.set_title('India Population Growth (in millions)')
                                ax.set_xlabel('Year')
                                ax.set_ylabel('Population (millions)')
                                
                                # Add grid for better readability
                                ax.grid(True, linestyle='--', alpha=0.3)
                                
                                # Apply dark theme styling to the matplotlib figure
                                fig, ax = style_matplotlib_for_dark(fig, ax)
                                
                                # Add value labels on points
                                for x, y in zip(df_population['Year'], df_population['Population (millions)']):
                                    # Only label certain years to avoid clutter
                                    if x % 20 == 0 or x in [2021]:
                                        ax.annotate(f'{y:.1f}', 
                                                   (x, y), 
                                                   textcoords="offset points",
                                                   xytext=(0, 10), 
                                                   ha='center',
                                                   color='#FAFAFA')
                                
                                st.pyplot(fig)
                            else:
                                st.error("Failed to load population data. Please check your data files.")
                            st.markdown("</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error in population visualization: {e}")
    
    # Add a cultural heritage highlight section
    st.markdown("<h3 class='section-heading' style='text-align: center;'>The Artistic Soul of India</h3>", unsafe_allow_html=True)
    
    # Add a decorative line
    st.markdown("""
    <div style="display: flex; align-items: center; margin: 1rem 0 1.5rem;">
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to right, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
        <div style="margin: 0 15px; color: #FF9933; font-size: 18px;">❖</div>
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to left, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for cultural highlights with improved card design
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='stat-card hoverable' style="height: 250px; display: flex; flex-direction: column; justify-content: flex-start; transition: all 0.3s ease; border-radius: 10px; border: 1px solid rgba(255, 153, 51, 0.3); background: linear-gradient(135deg, rgba(35, 35, 45, 0.8), rgba(35, 35, 45, 0.6)); overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <div style="background: linear-gradient(90deg, rgba(255, 153, 51, 0.3), rgba(255, 153, 51, 0.1)); padding: 0.8rem; border-bottom: 2px solid rgba(255, 153, 51, 0.3); text-align: center;">
                <h4 style="color:#FF9933; margin: 0; padding: 0.2rem; font-size: 1.4rem; text-align: center; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">Classical Arts</h4>
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-evenly; padding: 1rem; text-align: center;">
                <div style="margin-bottom: 0.5rem;">
                    <span style="font-size: 2.2rem; font-weight: 600; color: #FF9933; text-shadow: 0 1px 2px rgba(0,0,0,0.3); display: block;">8</span>
                    <span style="display: block; font-size: 0.9rem; color: #DDDDDD; margin-top: 0.2rem;">Classical Dance Forms</span>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <span style="font-size: 2.2rem; font-weight: 600; color: #FF9933; text-shadow: 0 1px 2px rgba(0,0,0,0.3); display: block;">2</span>
                    <span style="display: block; font-size: 0.9rem; color: #DDDDDD; margin-top: 0.2rem;">Classical Music Traditions</span>
                </div>
                <p style="margin: 0.5rem 0 0; font-size: 0.85rem; line-height: 1.4; color: #AAAAAA; font-style: italic;">Recognized by Sangeet Natak Akademi</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-card hoverable' style="height: 250px; display: flex; flex-direction: column; justify-content: flex-start; transition: all 0.3s ease; border-radius: 10px; border: 1px solid rgba(255, 153, 51, 0.3); background: linear-gradient(135deg, rgba(35, 35, 45, 0.8), rgba(35, 35, 45, 0.6)); overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <div style="background: linear-gradient(90deg, rgba(255, 153, 51, 0.3), rgba(255, 153, 51, 0.1)); padding: 0.8rem; border-bottom: 2px solid rgba(255, 153, 51, 0.3); text-align: center;">
                <h4 style="color:#FF9933; margin: 0; padding: 0.2rem; font-size: 1.4rem; text-align: center; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">Crafts & Visual Arts</h4>
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-evenly; padding: 1rem; text-align: center;">
                <div style="margin-bottom: 0.5rem;">
                    <span style="font-size: 2.2rem; font-weight: 600; color: #FF9933; text-shadow: 0 1px 2px rgba(0,0,0,0.3); display: block;">3,000+</span>
                    <span style="display: block; font-size: 0.9rem; color: #DDDDDD; margin-top: 0.2rem;">Craft Clusters</span>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <span style="font-size: 2.2rem; font-weight: 600; color: #FF9933; text-shadow: 0 1px 2px rgba(0,0,0,0.3); display: block;">7M</span>
                    <span style="display: block; font-size: 0.9rem; color: #DDDDDD; margin-top: 0.2rem;">Artisans</span>
                </div>
                <p style="margin: 0.5rem 0 0; font-size: 0.85rem; line-height: 1.4; color: #AAAAAA; font-style: italic;">Preserving traditional craftsmanship</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-card hoverable' style="height: 250px; display: flex; flex-direction: column; justify-content: flex-start; transition: all 0.3s ease; border-radius: 10px; border: 1px solid rgba(255, 153, 51, 0.3); background: linear-gradient(135deg, rgba(35, 35, 45, 0.8), rgba(35, 35, 45, 0.6)); overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <div style="background: linear-gradient(90deg, rgba(255, 153, 51, 0.3), rgba(255, 153, 51, 0.1)); padding: 0.8rem; border-bottom: 2px solid rgba(255, 153, 51, 0.3); text-align: center;">
                <h4 style="color:#FF9933; margin: 0; padding: 0.2rem; font-size: 1.4rem; text-align: center; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">Heritage & Architecture</h4>
            </div>
            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-evenly; padding: 1rem; text-align: center;">
                <div style="margin-bottom: 0.5rem;">
                    <span style="font-size: 2.2rem; font-weight: 600; color: #FF9933; text-shadow: 0 1px 2px rgba(0,0,0,0.3); display: block;">40</span>
                    <span style="display: block; font-size: 0.9rem; color: #DDDDDD; margin-top: 0.2rem;">UNESCO World Heritage Sites</span>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <span style="font-size: 2.2rem; font-weight: 600; color: #FF9933; text-shadow: 0 1px 2px rgba(0,0,0,0.3); display: block;">3,650+</span>
                    <span style="display: block; font-size: 0.9rem; color: #DDDDDD; margin-top: 0.2rem;">Protected Monuments</span>
                </div>
                <p style="margin: 0.5rem 0 0; font-size: 0.85rem; line-height: 1.4; color: #AAAAAA; font-style: italic;">Diverse architectural styles</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Project Overview Section
    st.markdown("<h3 class='section-heading' style='text-align: center;'>Project Overview: Code Yatra</h3>", unsafe_allow_html=True)
    
    # Add decorative boundary line
    st.markdown("""
    <div style="display: flex; align-items: center; margin: 1rem 0 1.5rem;">
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to right, rgba(19,136,8,0.1), rgba(19,136,8,0.8), rgba(19,136,8,0.1));"></div>
        <div style="margin: 0 15px; color: #138808; font-size: 18px;">❖</div>
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to left, rgba(19,136,8,0.1), rgba(19,136,8,0.8), rgba(19,136,8,0.1));"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text' style="margin: 1.2rem 0; font-size: 1.15rem; line-height: 1.7; text-align: center;">
    <p><strong style="color: #FF9933; font-size: 1.2rem;">Code Yatra</strong> is a data-driven exploration of India's cultural heritage, designed to showcase the richness and diversity of Indian traditions through interactive visualizations. Our project aims to:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for project goals with improved spacing and visual appeal
    goal_col1, goal_col2 = st.columns(2)
    
    with goal_col1:
        st.markdown("""
        <div class='data-insight' style='height: 300px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background: linear-gradient(135deg, rgba(19, 136, 8, 0.12), rgba(35, 35, 45, 0.3)); border: 1px solid rgba(19, 136, 8, 0.3); display: flex; flex-direction: column;'>
        <h4 style="margin: 0; color: #FF9933; font-size: 1.3rem; border-bottom: 1px solid rgba(255, 255, 255, 0.2); padding: 0.8rem; text-align: center; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">Preserve & Educate</h4>
        <div style="flex-grow: 1; padding: 1rem 0.5rem;">
        <ul style="list-style-type: none; padding-left: 0.5rem; margin-top: 0.5rem;">
            <li style="margin-bottom: 0.8rem; position: relative; padding-left: 1.5rem;">
                <span style="position: absolute; left: 0; color: #FF9933;">▶</span> Document and showcase India's diverse cultural elements
            </li>
            <li style="margin-bottom: 0.8rem; position: relative; padding-left: 1.5rem;">
                <span style="position: absolute; left: 0; color: #FF9933;">▶</span> Make cultural data accessible and engaging
            </li>
            <li style="margin-bottom: 0.8rem; position: relative; padding-left: 1.5rem;">
                <span style="position: absolute; left: 0; color: #FF9933;">▶</span> Create awareness about lesser-known traditions
            </li>
            <li style="margin-bottom: 0.8rem; position: relative; padding-left: 1.5rem;">
                <span style="position: absolute; left: 0; color: #FF9933;">▶</span> Highlight the historical significance of cultural practices
            </li>
        </ul>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with goal_col2:
        st.markdown("""
        <div class='data-insight' style='height: 300px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background: linear-gradient(135deg, rgba(19, 136, 8, 0.12), rgba(35, 35, 45, 0.3)); border: 1px solid rgba(19, 136, 8, 0.3); display: flex; flex-direction: column;'>
        <h4 style="margin: 0; color: #FF9933; font-size: 1.3rem; border-bottom: 1px solid rgba(255, 255, 255, 0.2); padding: 0.8rem; text-align: center; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">Visualize & Connect</h4>
        <div style="flex-grow: 1; padding: 1rem 0.5rem;">
        <ul style="list-style-type: none; padding-left: 0.5rem; margin-top: 0.5rem;">
            <li style="margin-bottom: 0.8rem; position: relative; padding-left: 1.5rem;">
                <span style="position: absolute; left: 0; color: #FF9933;">▶</span> Transform cultural statistics into immersive stories
            </li>
            <li style="margin-bottom: 0.8rem; position: relative; padding-left: 1.5rem;">
                <span style="position: absolute; left: 0; color: #FF9933;">▶</span> Demonstrate regional diversity and interconnections
            </li>
            <li style="margin-bottom: 0.8rem; position: relative; padding-left: 1.5rem;">
                <span style="position: absolute; left: 0; color: #FF9933;">▶</span> Show how traditions evolve over time
            </li>
            <li style="margin-bottom: 0.8rem; position: relative; padding-left: 1.5rem;">
                <span style="position: absolute; left: 0; color: #FF9933;">▶</span> Bridge traditional knowledge with modern analytics
            </li>
        </ul>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Add spacing between sections
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Population urban vs rural breakdown with better styling
    st.markdown("<h3 class='section-heading' style='text-align: center;'>Urban vs Rural Population Trend</h3>", unsafe_allow_html=True)
    
    # Add decorative boundary line
    st.markdown("""
    <div style="display: flex; align-items: center; margin: 1rem 0 1.5rem;">
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to right, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
        <div style="margin: 0 15px; color: #FF9933; font-size: 18px;">❖</div>
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to left, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        try:
            # Ensure df_population is loaded successfully
            if 'df_population' not in locals() or df_population is None or df_population.empty:
                df_population = load_population_data()
                
            if df_population is not None and not df_population.empty:
                # Ensure the required columns exist
                if all(col in df_population.columns for col in ['Year', 'Urban Population (%)', 'Rural Population (%)']):
                    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                    # Filter to recent years only (avoid cluttering with projections)
                    df_plot = df_population[df_population['Year'] <= 2021].copy()
                    
                    # Create enhanced Plotly figure with improved styling
                    fig = px.line(df_plot, x='Year', y=['Urban Population (%)', 'Rural Population (%)'],
                                title='Urban vs Rural Population Trend in India (1960-2021)',
                                color_discrete_sequence=['#FF9933', '#138808'],
                                markers=True,
                                line_shape='spline',  # Smoother lines
                                render_mode='svg')    # Better rendering quality
                    
                    # Improve layout with more styling
                    fig.update_layout(
                        xaxis_title='Year',
                        yaxis_title='Population Percentage (%)',
                        legend_title='Population Type',
                        hovermode="x unified",
                        title_font=dict(size=22),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.3,  # Increased space for legend
                            xanchor="center",
                            x=0.5,
                            font=dict(size=14)
                        ),
                        margin=dict(l=40, r=40, t=60, b=100)  # Increased bottom margin
                    )
                    
                    # Apply dark theme for better visualization
                    fig = apply_dark_theme(fig)
                    
                    # Add value labels at the end of each line
                    last_year = df_plot['Year'].max()
                    for col in ['Urban Population (%)', 'Rural Population (%)']:
                        last_val = df_plot[df_plot['Year'] == last_year][col].values[0]
                        color = '#FF9933' if col == 'Urban Population (%)' else '#138808'
                        fig.add_annotation(
                            x=last_year,
                            y=last_val,
                            text=f"{last_val:.1f}%",
                            showarrow=False,
                            xshift=15,
                            font=dict(
                                family="Arial",
                                size=14,
                                color=color
                            ),
                            bgcolor="rgba(30, 33, 41, 0.7)",
                            bordercolor=color,
                            borderwidth=1,
                            borderpad=4,
                            opacity=0.8
                        )
                    
                    # Add a trend line or annotation to highlight the crossover point
                    crossover_years = []
                    for i in range(1, len(df_plot)-1):
                        if ((df_plot['Urban Population (%)'].iloc[i-1] < df_plot['Rural Population (%)'].iloc[i-1] and
                             df_plot['Urban Population (%)'].iloc[i] > df_plot['Rural Population (%)'].iloc[i]) or
                            (df_plot['Urban Population (%)'].iloc[i] < df_plot['Rural Population (%)'].iloc[i] and
                             df_plot['Urban Population (%)'].iloc[i+1] > df_plot['Rural Population (%)'].iloc[i+1])):
                            crossover_years.append(df_plot['Year'].iloc[i])
                    
                    # If a crossover point is found, add an annotation
                    if crossover_years:
                        crossover_year = crossover_years[0]
                        crossover_value = (df_plot[df_plot['Year'] == crossover_year]['Urban Population (%)'].values[0] +
                                          df_plot[df_plot['Year'] == crossover_year]['Rural Population (%)'].values[0]) / 2
                        
                        fig.add_annotation(
                            x=crossover_year,
                            y=crossover_value,
                            text="Urban-Rural<br>Crossover Point",
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor="#FFFFFF",
                            ax=-50,
                            ay=-40,
                            font=dict(
                                family="Arial",
                                size=12,
                                color="#FFFFFF"
                            ),
                            bgcolor="rgba(68, 68, 68, 0.7)",
                            bordercolor="#FFFFFF",
                            borderwidth=1,
                            borderpad=4,
                            opacity=0.8
                        )
                    
                    # Add shaded regions to highlight different periods
                    periods = [
                        {"name": "Pre-Liberalization", "start": 1960, "end": 1990, "color": "rgba(255, 153, 51, 0.1)"},
                        {"name": "Economic Reforms", "start": 1991, "end": 2000, "color": "rgba(19, 136, 8, 0.1)"},
                        {"name": "Rapid Urbanization", "start": 2001, "end": 2021, "color": "rgba(255, 153, 51, 0.15)"}
                    ]
                    
                    for period in periods:
                        fig.add_vrect(
                            x0=period["start"], 
                            x1=period["end"],
                            fillcolor=period["color"],
                            opacity=0.6,
                            layer="below",
                            line_width=0,
                            annotation_text=period["name"],
                            annotation_position="top left",
                            annotation=dict(
                                font_size=10,
                                font_color="#CCCCCC"
                            )
                        )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("Required columns not found in population data. Please check the CSV format.")
            else:
                st.error("Failed to load population data for urban vs rural trend chart.")
        except Exception as e:
            st.error(f"Error in urban/rural population chart: {e}")
    
    # Add informative text with insights from the data and cultural perspective
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class='story-text'>
        The shift from rural to urban living has transformed India's cultural landscape. While rural areas preserve traditional art forms and crafts passed down through generations, urban centers have become hubs of cultural fusion and innovation, blending ancient traditions with contemporary expressions.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Add a small insight box about cultural preservation
        st.markdown("<div class='data-insight'>Despite rapid urbanization, India's rural communities remain vital custodians of cultural heritage, with over 70% of traditional artisans residing in villages and small towns, preserving centuries-old techniques and knowledge systems.</div>", unsafe_allow_html=True)
    
    # Add spacing between sections
    st.markdown("<br>", unsafe_allow_html=True)
    
    # States data with improved styling
    st.markdown("<h3 class='section-heading'>India's Cultural Diversity Across States</h3>", unsafe_allow_html=True)
    st.markdown("<div class='story-text'>Each state of India has its own distinct cultural identity, contributing unique art forms, crafts, music, dance, cuisine, and traditions to the nation's cultural mosaic. The map below shows the distribution of population across major Indian states.</div>", unsafe_allow_html=True)
    
    # Tabs for different state visualizations
    tab1, tab2 = st.tabs(["Population by State", "Regional Distribution"])
    
    with tab1:
        try:
            df_states = load_state_data()
            
            if df_states is not None and not df_states.empty:
                # Create a horizontal bar chart of state populations with improved styling
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                
                # Sort for better visualization
                sorted_states = df_states.sort_values('Population (millions)', ascending=True)
                
                # Create enhanced bar chart
                fig = px.bar(sorted_states, 
                            y='State', x='Population (millions)', orientation='h',
                            title='Population by State (in millions)',
                            color='Population (millions)',
                            color_continuous_scale=px.colors.sequential.Oranges,
                            hover_data=['Literacy Rate (%)', 'Region'])

                # Improve layout
                fig.update_layout(
                    height=800,
                    yaxis_title="State/Union Territory",
                    xaxis_title="Population (millions)",
                    xaxis=dict(
                        title_font=dict(size=16),
                        tickfont=dict(size=14),
                    ),
                    yaxis=dict(
                        title_font=dict(size=16),
                        tickfont=dict(size=14),
                    ),
                    coloraxis_colorbar=dict(
                        title="Population<br>(millions)",
                        tickfont=dict(size=14),
                        title_font=dict(size=14)
                    )
                )
                
                # Apply dark theme for better visualization
                fig = apply_dark_theme(fig)

                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Failed to load state data.")
        except Exception as e:
            st.error(f"Error in state population chart: {e}")
    
    with tab2:
        try:
            # Add a pie chart showing regional distribution
            if 'df_states' not in locals() or df_states is None or df_states.empty:
                df_states = load_state_data()
            
            if df_states is not None and not df_states.empty:
                # Group by region for population analysis
                region_pop = df_states.groupby(['Region'])['Population (millions)'].sum().reset_index()
                region_pop = region_pop.sort_values('Population (millions)', ascending=False)
                
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                # Create an enhanced pie chart with hover information
                fig = px.pie(region_pop, values='Population (millions)', names='Region',
                            title='Distribution of Population by Region',
                            color_discrete_sequence=px.colors.qualitative.Bold,
                            hover_data=['Population (millions)'],
                            custom_data=['Population (millions)'],
                            hole=0.4)
                
                # Custom hovertemplate to show state count
                fig.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Population: %{value:.1f} million<br>States/UTs: %{customdata[0]}<extra></extra>'
                )
                
                # Improved layout
                fig.update_layout(
                    title_font_size=20,
                    annotations=[dict(text='Regional<br>Distribution', x=0.5, y=0.5, font_size=15, showarrow=False)],
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=14)
                    )
                )
                
                # Apply dark theme for better visualization
                fig = apply_dark_theme(fig)
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Failed to load state data for regional distribution.")
        except Exception as e:
            st.error(f"Error in regional distribution chart: {e}")
    
    # Add a section on cultural heritage
    st.markdown("<h3 class='section-heading' style='text-align: center;'>Cultural Heritage Across India</h3>", unsafe_allow_html=True)
    
    # Add decorative boundary line
    st.markdown("""
    <div style="display: flex; align-items: center; margin: 1rem 0 1.5rem;">
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to right, rgba(19,136,8,0.1), rgba(19,136,8,0.8), rgba(19,136,8,0.1));"></div>
        <div style="margin: 0 15px; color: #138808; font-size: 18px;">❖</div>
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to left, rgba(19,136,8,0.1), rgba(19,136,8,0.8), rgba(19,136,8,0.1));"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    India's cultural heritage is a living tapestry that has evolved over millennia, encompassing diverse elements from classical arts to traditional crafts, from ancient monuments to vibrant festivals. Each element represents a unique facet of India's cultural identity and continues to influence contemporary expressions.
    </div>
    """, unsafe_allow_html=True)
    
    # Try to load cultural data
    try:
        df_culture = load_cultural_data()
        
        if df_culture is not None and not df_culture.empty:
            # Add additional insights about cultural elements
            st.markdown("<div class='data-insight'>India's cultural heritage encompasses over 100 distinct art forms, 8 classical dance styles, 9 classical music traditions, and 40 UNESCO World Heritage Sites, making it one of the most culturally diverse nations in the world.</div>", unsafe_allow_html=True)
            
            # Create tabs for different visualizations
            cult_tab1, cult_tab2 = st.tabs(["Cultural Elements", "Regional Distribution"])
            
            with cult_tab1:
                # Display cultural elements in a visually appealing way
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                
                # Create a horizontal bar chart for cultural elements
                fig = px.bar(df_culture, y='Cultural Element', x='Count', 
                            title='Richness of Indian Cultural Heritage',
                            color='Cultural Element',
                            orientation='h',
                            text='Count',
                            color_discrete_sequence=px.colors.qualitative.Bold)
                
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    yaxis_title="",
                    xaxis_title="Count",
                    title_font_size=20,
                    height=450
                )
                
                # Apply dark theme for better visualization
                fig = apply_dark_theme(fig)
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with cult_tab2:
                # Add a treemap visualization for better hierarchical representation
                st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                
                # Create a treemap chart for cultural elements by region
                fig = px.treemap(df_culture, 
                                path=['Region of Origin', 'Cultural Element'], 
                                values='Count',
                                color='Count',
                                color_continuous_scale='Oranges',
                                title='Cultural Heritage Distribution by Region')
                
                fig.update_layout(
                    height=500,
                    title_font_size=20,
                )
                
                # Apply dark theme for better visualization
                fig = apply_dark_theme(fig)
                
                # Add hover information
                fig.update_traces(
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Add explanatory text
                st.markdown("""
                <div class='story-text'>
                The treemap above shows the distribution of India's cultural heritage elements across different regions. 
                The size of each box represents the relative count of cultural elements, while the color intensity indicates the magnitude.
                Pan-Indian elements represent traditions that are practiced across multiple regions with regional variations.
                </div>
                """, unsafe_allow_html=True)
            
            # Add a section showing historical periods in a visually engaging way
            if 'Historical Period' in df_culture.columns:
                st.markdown("<h4 class='section-heading'>Historical Evolution of Cultural Traditions</h4>", unsafe_allow_html=True)
                
                # Create two columns
                hist_col1, hist_col2 = st.columns([1, 2])
                
                with hist_col1:
                    st.markdown("""
                    <div class='story-text'>
                    India's cultural traditions span multiple historical periods, from ancient Indus Valley Civilization (3300-1300 BCE) through the Classical, Medieval, and Colonial periods to modern times. This timeline shows how different art forms and cultural practices have evolved over millennia while maintaining their core essence.
                    </div>
                    """, unsafe_allow_html=True)
                
                with hist_col2:
                    # Create a timeline-like display of cultural elements by period
                    periods = {
                        "Ancient (pre-500 BCE)": "Foundation of classical traditions, early temple architecture, and ritual arts",
                        "Classical (500 BCE - 500 CE)": "Codification of arts in texts like Natya Shastra, Buddhist and Hindu artistic expressions",
                        "Medieval (500 CE - 1500 CE)": "Regional styles flourish, temple arts reach peak, Islamic influences integrate",
                        "Early Modern (1500 - 1800 CE)": "Mughal court arts, miniature painting traditions, classical music evolution",
                        "Colonial & Modern (1800 CE - Present)": "Fusion of traditional and Western forms, revival movements, new media"
                    }
                    
                    # Create a vertical timeline with better styling and alignment
                    st.markdown("""
                    <div style="position: relative; padding-left: 40px; margin-top: 10px;">
                        <div style="position: absolute; left: 15px; top: 0; bottom: 0; width: 3px; background: linear-gradient(to bottom, #FF9933, #138808); border-radius: 3px;"></div>
                    """, unsafe_allow_html=True)
                    
                    for i, (period, desc) in enumerate(periods.items()):
                        # Add color variation to make it visually interesting
                        dot_color = "#FF9933" if i % 2 == 0 else "#138808"
                        bg_color = f"rgba({255 if i % 2 == 0 else 19}, {153 if i % 2 == 0 else 136}, {51 if i % 2 == 0 else 8}, 0.1)"
                        
                        st.markdown(f"""
                        <div style="position: relative; margin-bottom: 30px; clear: both;">
                            <div style="position: absolute; left: -30px; top: 15px; width: 20px; height: 20px; background-color: {dot_color}; border-radius: 50%; border: 3px solid #1E2129; box-shadow: 0 0 0 2px {dot_color}; z-index: 5;"></div>
                            <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; border-left: 3px solid {dot_color}; margin-left: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-right: 5px;">
                                <h5 style="margin: 0 0 8px 0; color: {dot_color}; font-size: 1.1rem; text-align: left;">{period}</h5>
                                <p style="margin: 0; font-size: 0.95rem; line-height: 1.5; text-align: left;">{desc}</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Add geographical distribution if region data is available
            if 'Region of Origin' in df_culture.columns or 'Associated States' in df_culture.columns:
                region_col = 'Region of Origin' if 'Region of Origin' in df_culture.columns else 'Associated States'
                st.markdown("<h4 class='section-heading'>Geographical Distribution of Cultural Traditions</h4>", unsafe_allow_html=True)
                
                st.markdown("""
                <div class='story-text'>
                India's cultural expressions show distinct regional characteristics while maintaining interconnections across the subcontinent. From the classical dance forms of the South to the textile traditions of the West, each region contributes uniquely to India's cultural tapestry.
                </div>
                """, unsafe_allow_html=True)
        else:
            # If cultural data isn't available, show a placeholder
            st.markdown("""
            <div class='story-text'>
            India's cultural heritage is remarkably diverse, encompassing classical and folk traditions in music, dance, visual arts, crafts, literature, and architecture. These art forms have evolved over millennia, reflecting the country's historical depth and regional diversity.
            </div>
            """, unsafe_allow_html=True)
            
            # Add some backup content if data isn't available
            st.markdown("""
            <div class='data-insight'>
            <h4 style="margin-top: 0;">Key Cultural Elements of India</h4>
            <ul>
                <li><strong>Classical Arts:</strong> Bharatanatyam, Kathak, Hindustani and Carnatic music traditions</li>
                <li><strong>Crafts & Folk Arts:</strong> Madhubani, Kalamkari, Phad painting, Warli art, Pattachitra</li>
                <li><strong>Heritage Sites:</strong> Taj Mahal, Khajuraho Temples, Ellora & Ajanta Caves, Hampi</li>
                <li><strong>Festivals:</strong> Diwali, Holi, Durga Puja, Pongal, Bihu, Onam</li>
                <li><strong>Living Traditions:</strong> Yoga, Ayurveda, Traditional knowledge systems</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Create manual cultural overview
            cultural_elements = {
                "Classical Dance Forms": 8,
                "Classical Music Traditions": 9,
                "UNESCO Heritage Sites": 40,
                "Major Festivals": 30,
                "Traditional Cuisines": 35,
                "Handloom Varieties": 20,
                "Folk Art Forms": 25,
                "Ancient Monuments": 100,
                "Martial Arts": 12
            }
            
            # Convert to DataFrame
            df_manual = pd.DataFrame(list(cultural_elements.items()), columns=['Cultural Element', 'Count'])
            
            # Create a horizontal bar chart
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            fig = px.bar(df_manual, y='Cultural Element', x='Count', 
                        title='Richness of Indian Cultural Heritage',
                        color='Cultural Element',
                        orientation='h',
                        text='Count',
                        color_discrete_sequence=px.colors.qualitative.Bold)
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                yaxis_title="",
                xaxis_title="Count",
                title_font_size=20,
                height=450
            )
            
            # Apply dark theme for better visualization
            fig = apply_dark_theme(fig)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading cultural data: {e}")
        
        # Add a fallback visualization if the cultural data fails to load
        st.markdown("""
        <div class='story-text'>
        India's cultural heritage spans thousands of years, with traditions passed down through generations. Below are some of the key elements that form India's rich cultural landscape.
        </div>
        """, unsafe_allow_html=True)
        
        # Create manual cultural overview for the exception case
        cultural_elements = {
            "Classical Dance Forms": 8,
            "Classical Music Traditions": 9,
            "UNESCO Heritage Sites": 40,
            "Major Festivals": 30,
            "Traditional Cuisines": 35,
            "Handloom Varieties": 20,
            "Folk Art Forms": 25,
            "Ancient Monuments": 100,
            "Martial Arts": 12
        }
        
        # Convert to DataFrame
        df_manual = pd.DataFrame(list(cultural_elements.items()), columns=['Cultural Element', 'Count'])
        
        # Create a horizontal bar chart
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        fig = px.bar(df_manual, y='Cultural Element', x='Count', 
                    title='Richness of Indian Cultural Heritage',
                    color='Cultural Element',
                    orientation='h',
                    text='Count',
                    color_discrete_sequence=px.colors.qualitative.Bold)
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            yaxis_title="",
            xaxis_title="Count",
            title_font_size=20,
            height=450
        )
        
        # Apply dark theme for better visualization
        fig = apply_dark_theme(fig)
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Add a section on Festivals of India
    st.markdown("<h3 class='section-heading' style='text-align: center;'>Festivals of India: Celebrating Diversity</h3>", unsafe_allow_html=True)
    
    # Add decorative boundary line
    st.markdown("""
    <div style="display: flex; align-items: center; margin: 1rem 0 1.5rem;">
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to right, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
        <div style="margin: 0 15px; color: #FF9933; font-size: 18px;">❖</div>
        <div style="flex-grow: 1; height: 1px; background: linear-gradient(to left, rgba(255,153,51,0.1), rgba(255,153,51,0.8), rgba(255,153,51,0.1));"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='story-text'>
    India's festivals are vivid expressions of its cultural diversity, with each celebration reflecting historical traditions, religious practices, seasonal changes, or cultural milestones. These festivals bring communities together, preserving ancient rituals while adapting to contemporary contexts.
    </div>
    """, unsafe_allow_html=True)
    
    # Try to load festivals data
    try:
        df_festivals = load_festivals_data()
        
        if df_festivals is not None and not df_festivals.empty:
            # Show insights about festivals
            st.markdown("<div class='data-insight'>India celebrates over 30 major festivals nationally, with hundreds more observed regionally. These celebrations contribute significantly to cultural tourism and local economies, with major festivals like Diwali generating an estimated economic impact of over $7 billion annually.</div>", unsafe_allow_html=True)
            
            # Create festival highlights in cards
            festival_col1, festival_col2, festival_col3 = st.columns(3)
            
            with festival_col1:
                st.markdown("""
                <div class='stat-card hoverable' style="height: 240px; display: flex; flex-direction: column; background: linear-gradient(135deg, rgba(35, 35, 45, 0.8), rgba(35, 35, 45, 0.6)); border: 1px solid rgba(255, 153, 51, 0.3); border-radius: 10px; transition: all 0.3s ease; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                    <div style="background: linear-gradient(90deg, rgba(255, 153, 51, 0.3), rgba(255, 153, 51, 0.1)); padding: 0.8rem; border-bottom: 2px solid rgba(255, 153, 51, 0.3); text-align: center;">
                        <h4 style="color:#FF9933; margin: 0; text-align: center; font-size: 1.4rem;">Diwali</h4>
                    </div>
                    <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-evenly; padding: 1rem; text-align: center; position: relative;">
                        <div style="position: absolute; top: 5px; right: 5px; font-size: 1.8rem; opacity: 0.2;">✨</div>
                        <p style="margin: 0.4rem 0; text-align: center; font-weight: 600; font-size: 1.3rem; color: #FF9933;">Festival of Lights</p>
                        <p style="margin: 0.4rem 0; text-align: center; color: #DDDDDD;">Celebrated nationwide in October-November</p>
                        <p style="margin: 0.4rem 0; text-align: center; font-style: italic; color: #AAAAAA;">Symbolizes victory of light over darkness</p>
                        <div style="position: absolute; bottom: 5px; left: 0; right: 0; height: 3px; background: linear-gradient(to right, transparent, rgba(255, 153, 51, 0.5), transparent);"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with festival_col2:
                st.markdown("""
                <div class='stat-card hoverable' style="height: 240px; display: flex; flex-direction: column; background: linear-gradient(135deg, rgba(35, 35, 45, 0.8), rgba(35, 35, 45, 0.6)); border: 1px solid rgba(255, 153, 51, 0.3); border-radius: 10px; transition: all 0.3s ease; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                    <div style="background: linear-gradient(90deg, rgba(255, 153, 51, 0.3), rgba(255, 153, 51, 0.1)); padding: 0.8rem; border-bottom: 2px solid rgba(255, 153, 51, 0.3); text-align: center;">
                        <h4 style="color:#FF9933; margin: 0; text-align: center; font-size: 1.4rem;">Holi</h4>
                    </div>
                    <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-evenly; padding: 1rem; text-align: center; position: relative;">
                        <div style="position: absolute; top: 5px; right: 5px; font-size: 1.8rem; opacity: 0.2;">🎨</div>
                        <p style="margin: 0.4rem 0; text-align: center; font-weight: 600; font-size: 1.3rem; color: #FF9933;">Festival of Colors</p>
                        <p style="margin: 0.4rem 0; text-align: center; color: #DDDDDD;">Celebrated across North India in March</p>
                        <p style="margin: 0.4rem 0; text-align: center; font-style: italic; color: #AAAAAA;">Marks the arrival of spring and triumph of good</p>
                        <div style="position: absolute; bottom: 5px; left: 0; right: 0; height: 3px; background: linear-gradient(to right, transparent, rgba(255, 153, 51, 0.5), transparent);"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with festival_col3:
                st.markdown("""
                <div class='stat-card hoverable' style="height: 240px; display: flex; flex-direction: column; background: linear-gradient(135deg, rgba(35, 35, 45, 0.8), rgba(35, 35, 45, 0.6)); border: 1px solid rgba(255, 153, 51, 0.3); border-radius: 10px; transition: all 0.3s ease; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                    <div style="background: linear-gradient(90deg, rgba(255, 153, 51, 0.3), rgba(255, 153, 51, 0.1)); padding: 0.8rem; border-bottom: 2px solid rgba(255, 153, 51, 0.3); text-align: center;">
                        <h4 style="color:#FF9933; margin: 0; text-align: center; font-size: 1.4rem;">Durga Puja</h4>
                    </div>
                    <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-evenly; padding: 1rem; text-align: center; position: relative;">
                        <div style="position: absolute; top: 5px; right: 5px; font-size: 1.8rem; opacity: 0.2;">🙏</div>
                        <p style="margin: 0.4rem 0; text-align: center; font-weight: 600; font-size: 1.3rem; color: #FF9933;">Worship of Divine Mother</p>
                        <p style="margin: 0.4rem 0; text-align: center; color: #DDDDDD;">Major festival in Eastern India</p>
                        <p style="margin: 0.4rem 0; text-align: center; font-style: italic; color: #AAAAAA;">Celebrates feminine divine power</p>
                        <div style="position: absolute; bottom: 5px; left: 0; right: 0; height: 3px; background: linear-gradient(to right, transparent, rgba(255, 153, 51, 0.5), transparent);"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Fallback content if festivals data isn't available
            st.markdown("""
            <div class='data-insight'>
            India celebrates a remarkable diversity of festivals throughout the year, from the pan-Indian celebrations of Diwali and Holi to regional festivals like Pongal in the South, Bihu in the Northeast, and Chhath in the East. These festivals reflect the country's cultural, religious, and seasonal diversity.
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading festivals data: {e}")
        # Provide fallback content in case of error
        st.markdown("""
        <div class='data-insight'>
        India's festival calendar is one of the most diverse and vibrant in the world, with celebrations marking seasonal changes, religious events, historical milestones, and cultural traditions throughout the year.
        </div>
        """, unsafe_allow_html=True)
    
    # Add spacing before Quick Facts section
    st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
    
    # Add quick facts as expandable section with key insights
    with st.expander("Quick Facts About India's Cultural Heritage"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Classical Arts")
            st.markdown("8 Classical Dance Forms")
            st.markdown("2 Classical Music Traditions")
            st.markdown("Thousands of Folk Art Forms")
        
        with col2:
            st.markdown("#### Craft Traditions")
            st.markdown("Over 3,000 Craft Clusters")
            st.markdown("7 Million+ Artisans")
            st.markdown("200+ GI-Tagged Crafts")
        
        with col3:
            st.markdown("#### Heritage Sites")
            st.markdown("40 UNESCO World Heritage Sites")
            st.markdown("3,650+ Protected Monuments")
            st.markdown("15 Biosphere Reserves")
    
    # Add a quote section to inspire readers
    st.markdown("""
    <div class='quote-box' style="position: relative; background: linear-gradient(135deg, rgba(19, 136, 8, 0.05) 0%, rgba(255, 153, 51, 0.1) 100%); border-radius: 12px; padding: 45px 40px 35px; margin: 55px 0 60px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15); border-left: 5px solid #FF9933; font-style: italic; font-size: 1.15rem; line-height: 1.8; color: #F5F5F5; text-align: center; max-width: 100%; overflow: hidden;">
        <div class='quote-marks' style="position: absolute; top: 10px; left: 20px; font-size: 4rem; color: #FF9933; opacity: 0.6; font-family: Georgia, serif; line-height: 0.8;">"</div>
        <div style="position: relative; z-index: 2;">
            India's cultural heritage is not just about the past; it's a living, breathing entity that continues to evolve while maintaining its core essence. Through data visualization and storytelling, we invite you to explore this rich tapestry that has fascinated the world for centuries.
        </div>
        <div class='quote-marks closing-quote' style="position: absolute; bottom: 0; right: 20px; font-size: 4rem; color: #FF9933; opacity: 0.6; font-family: Georgia, serif; line-height: 0.8;">"</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a conclusion and call to action
    st.markdown("<h3 class='section-heading' style='text-align: center;'>Preserving the Past, Enriching the Future</h3>", unsafe_allow_html=True)
    
    conclusion_col1, conclusion_col2 = st.columns([2, 1])
    
    with conclusion_col1:
        st.markdown("""
        <div class='story-text' style="font-size: 1.1rem; line-height: 1.8; letter-spacing: 0.2px; padding: 1rem; background-color: rgba(30, 33, 41, 0.3); border-radius: 8px; height: 100%; box-sizing: border-box; text-align: left;">
        <p style="margin-bottom: 1rem;">As we journey through India's cultural landscape in the following chapters, we'll explore how data can help us understand, preserve, and celebrate this extraordinary heritage. From analyzing the geographical distribution of art forms to tracking the evolution of traditions over time, data storytelling offers new perspectives on India's cultural treasures.</p>
        
        <p>This project aims to bridge traditional knowledge with modern analytics, creating an immersive experience that honors the past while embracing the future. By making cultural data accessible and engaging, we hope to inspire a deeper appreciation for India's artistic and cultural legacy among both Indians and global audiences.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with conclusion_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255, 153, 51, 0.1) 0%, rgba(19, 136, 8, 0.05) 100%); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #FF9933; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); height: 100%; box-sizing: border-box;">
            <h4 style="margin-top:0; color:#FF9933; border-bottom: 1px solid rgba(255, 153, 51, 0.3); padding-bottom: 0.5rem; text-align: center;">Explore Further</h4>
            <ul style="list-style-type: none; padding-left: 0.2rem; margin-top: 1rem;">
                <li style="margin-bottom: 0.7rem; position: relative; padding-left: 1.2rem; text-align: left;">
                    <span style="position: absolute; left: 0; color: #FF9933;">➤</span> Regional cultural diversity
                </li>
                <li style="margin-bottom: 0.7rem; position: relative; padding-left: 1.2rem; text-align: left;">
                    <span style="position: absolute; left: 0; color: #FF9933;">➤</span> Historical evolution of traditions
                </li>
                <li style="margin-bottom: 0.7rem; position: relative; padding-left: 1.2rem; text-align: left;">
                    <span style="position: absolute; left: 0; color: #FF9933;">➤</span> Living heritage practices
                </li>
                <li style="margin-bottom: 0.7rem; position: relative; padding-left: 1.2rem; text-align: left;">
                    <span style="position: absolute; left: 0; color: #FF9933;">➤</span> Contemporary expressions
                </li>
                <li style="margin-bottom: 0.7rem; position: relative; padding-left: 1.2rem; text-align: left;">
                    <span style="position: absolute; left: 0; color: #FF9933;">➤</span> Preservation challenges and solutions
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True) 