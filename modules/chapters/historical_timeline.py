import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.utils import apply_dark_theme, load_historical_data, get_color_palette
import re

def render():
    """Render the Historical Timeline chapter content"""
    st.title("📜 Historical Timeline of India")
    
    st.markdown("""
    <div class='story-text'>
    India's rich history spans over 5,000 years, from the ancient Indus Valley Civilization to the modern republic. 
    This journey through time showcases the rise and fall of powerful empires, cultural and scientific achievements, 
    religious movements, and social transformations that have shaped the world's largest democracy.
    </div>
    """, unsafe_allow_html=True)
    
    # Load and prepare data
    with st.spinner("Analyzing historical data..."):
        try:
            df = load_historical_data()
            
            if df is None or df.empty:
                st.error("Failed to load historical data. Please check your data files.")
                return
                
            # Check for required columns
            required_columns = ['Era', 'Time Period']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"Missing required columns in historical data: {', '.join(missing_columns)}")
                return
            
            # Extract start years from time period for timeline ordering
            df['Start Year'] = df['Time Period'].str.extract(r'(\d+)').astype(int)
            
            # Create BCE flag and adjust years for timeline visualization
            df['BCE'] = df['Time Period'].str.contains('BCE')
            df['Timeline Year'] = df.apply(lambda x: -x['Start Year'] if x['BCE'] else x['Start Year'], axis=1)
            
            # Sort by timeline year for chronological order
            df = df.sort_values('Timeline Year')
            
            # Create era colors for consistent visualization
            era_colors = {}
            color_palette = get_color_palette(len(df['Era'].unique()))
            for i, era in enumerate(df['Era'].unique()):
                era_colors[era] = color_palette[i]
        except Exception as e:
            st.error(f"Error preparing historical data: {e}")
            return
    
    # Interactive Timeline
    st.header("Interactive Timeline of Indian History")
    
    try:
        # Add timeline description
        st.markdown("""
        <div class='story-text'>
        Use the slider below to explore key eras in Indian history. Each period represents a major 
        historical era with unique cultural, political, and social characteristics.
        </div>
        """, unsafe_allow_html=True)
        
        # Create a slider for timeline navigation
        selected_index = st.slider(
            "Explore Historical Periods",
            min_value=0,
            max_value=len(df) - 1,
            value=0,
            format=None
        )
        
        selected_era = df.iloc[selected_index]
        
        # Display era information in two columns
        col1, col2 = st.columns([1, 2])
        
        # Time period and basic info in first column
        with col1:
            # Create a container for consistent styling
            with st.container():
                # Era name with appropriate styling
                st.markdown(f"<h2 style='color:{era_colors[selected_era['Era']]}'>{selected_era['Era']}</h2>", unsafe_allow_html=True)
                
                # Time period with BCE/CE notation
                time_period = selected_era['Time Period']
                st.markdown(f"**Period:** {time_period}")
                
                # Key rulers/leaders if available
                if 'Key Rulers/Leaders' in selected_era and not pd.isna(selected_era['Key Rulers/Leaders']):
                    st.markdown(f"**Key Rulers/Leaders:** {selected_era['Key Rulers/Leaders']}")
                
                # Capital cities if available
                if 'Capital Cities' in selected_era and not pd.isna(selected_era['Capital Cities']):
                    st.markdown(f"**Capital Cities:** {selected_era['Capital Cities']}")
                
                # Create era badge
                era_periods = {
                    'Ancient': ['Indus Valley Civilization', 'Vedic Period', 'Mahajanapadas', 'Ancient India'],
                    'Classical': ['Mauryan Empire', 'Post-Mauryan Period', 'Gupta Empire'],
                    'Medieval': ['Post-Gupta Period', 'Medieval India', 'Delhi Sultanate', 'Vijayanagara Empire', 'Mughal Empire', 'Maratha Empire'],
                    'Modern': ['Colonial Era', 'British Raj', 'Independence Movement', 'Independence', 'Republic of India', 'Post-Independence', 'Economic Reforms', 'Modern India', 'Age of Exploration']
                }
                
                # Determine era category for badge
                era_category = next((category for category, eras in era_periods.items() if selected_era['Era'] in eras), "Other")
                
                # Display era category badge
                badge_colors = {
                    'Ancient': '#9C6644',
                    'Classical': '#4C9900',
                    'Medieval': '#9966CC',
                    'Modern': '#3366CC',
                    'Other': '#888888'  # Default color for any era not in the mapping
                }
                
                st.markdown(f"""
                <div style='margin-top:20px;'>
                    <span style='background-color:{badge_colors[era_category]}33;color:{badge_colors[era_category]};
                    padding:5px 15px;border-radius:20px;font-size:0.9rem;'>
                    {era_category} Period
                    </span>
                </div>
                """, unsafe_allow_html=True)
        
        # Detailed information in second column
        with col2:
            # Create tabs for different aspects
            tabs = st.tabs(["Major Events", "Culture & Society", "Economy & Technology"])
            
            # Tab 1: Major Events
            with tabs[0]:
                st.markdown(f"### Key Historical Events")
                if 'Major Events' in selected_era and not pd.isna(selected_era['Major Events']):
                    st.markdown(f"{selected_era['Major Events']}")
                else:
                    st.info("No major events information available for this period.")
                
                if 'Territorial Extent' in selected_era and not pd.isna(selected_era['Territorial Extent']):
                    st.markdown("#### Territorial Extent")
                    st.markdown(f"{selected_era['Territorial Extent']}")
                
                if 'Military Developments' in selected_era and not pd.isna(selected_era['Military Developments']):
                    st.markdown("#### Military")
                    st.markdown(f"{selected_era['Military Developments']}")
                    
                if 'Foreign Relations' in selected_era and not pd.isna(selected_era['Foreign Relations']):
                    st.markdown("#### Foreign Relations")
                    st.markdown(f"{selected_era['Foreign Relations']}")
            
            # Tab 2: Culture & Society
            with tabs[1]:
                if 'Cultural Developments' in selected_era and not pd.isna(selected_era['Cultural Developments']):
                    st.markdown("### Cultural Developments")
                    st.markdown(f"{selected_era['Cultural Developments']}")
                
                if 'Religious Trends' in selected_era and not pd.isna(selected_era['Religious Trends']):
                    st.markdown("### Religious Trends")
                    st.markdown(f"{selected_era['Religious Trends']}")
                
                if 'Art & Architecture' in selected_era and not pd.isna(selected_era['Art & Architecture']):
                    st.markdown("### Art & Architecture")
                    st.markdown(f"{selected_era['Art & Architecture']}")
                
                if 'Social Structure' in selected_era and not pd.isna(selected_era['Social Structure']):
                    st.markdown("### Social Structure")
                    st.markdown(f"{selected_era['Social Structure']}")
                
                if all(pd.isna(selected_era.get(col, np.nan)) for col in ['Cultural Developments', 'Religious Trends', 'Art & Architecture', 'Social Structure']):
                    st.info("No cultural and social information available for this period.")
            
            # Tab 3: Economy & Technology
            with tabs[2]:
                if 'Economic Systems' in selected_era and not pd.isna(selected_era['Economic Systems']):
                    st.markdown("### Economic Systems")
                    st.markdown(f"{selected_era['Economic Systems']}")
                
                if 'Scientific Advances' in selected_era and not pd.isna(selected_era['Scientific Advances']):
                    st.markdown("### Scientific Advances")
                    st.markdown(f"{selected_era['Scientific Advances']}")
                
                if 'Technological Innovations' in selected_era and not pd.isna(selected_era['Technological Innovations']):
                    st.markdown("### Technological Innovations")
                    st.markdown(f"{selected_era['Technological Innovations']}")
                
                if all(pd.isna(selected_era.get(col, np.nan)) for col in ['Economic Systems', 'Scientific Advances', 'Technological Innovations']):
                    st.info("No economic and technological information available for this period.")
        
        # Historical legacy
        if 'Historical Legacy' in selected_era and not pd.isna(selected_era['Historical Legacy']):
            st.markdown("### Historical Legacy")
            st.info(f"{selected_era['Historical Legacy']}")
    except Exception as e:
        st.error(f"Error displaying historical era information: {e}")
    
    # Visual timeline representation
    st.header("Visual Timeline of Indian History")
    
    try:
        # Create a more reliable visualization for the timeline
        st.markdown("""
        <div style='margin-bottom:15px;'>
        Explore India's historical journey through time, from the ancient Indus Valley Civilization to the modern republic.
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different time periods
        timeline_tabs = st.tabs([
            "Ancient (Before 600 CE)", 
            "Medieval (600-1757 CE)", 
            "Colonial (1757-1947)",
            "Modern (1947-Present)"
        ])
        
        # Define color scheme for different time periods
        period_colors = {
            "Ancient": "#E3663E",
            "Medieval": "#6C8CBF",
            "Colonial": "#4D9078",
            "Modern": "#FFC857"
        }
        
        # ANCIENT PERIOD TAB
        with timeline_tabs[0]:
            st.markdown(f"<h3 style='color:{period_colors['Ancient']}'>Ancient India</h3>", unsafe_allow_html=True)
            
            # Filter data for ancient period
            ancient_df = df[(df['Timeline Year'] < 600)]
            if not ancient_df.empty:
                # Sort by timeline year
                ancient_df = ancient_df.sort_values('Timeline Year')
                
                # Create an enhanced timeline visualization
                fig = go.Figure()
                
                # Add events as scatter points
                fig.add_trace(go.Scatter(
                    x=ancient_df['Timeline Year'],
                    y=[1] * len(ancient_df),
                    mode='markers+text',
                    marker=dict(
                        symbol='circle',
                        size=16,
                        color=period_colors['Ancient'],
                        line=dict(width=2, color='white')
                    ),
                    text=ancient_df['Era'],
                    textposition="top center",
                    hovertemplate='<b>%{text}</b><br>Year: %{x}<extra></extra>'
                ))
                
                # Add a line connecting all points
                fig.add_trace(go.Scatter(
                    x=ancient_df['Timeline Year'],
                    y=[1] * len(ancient_df),
                    mode='lines',
                    line=dict(color=period_colors['Ancient'], width=3),
                    hoverinfo='skip'
                ))
                
                # Update layout
                fig.update_layout(
                    title="Ancient Indian Timeline",
                    showlegend=False,
                    yaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False,
                        range=[0.5, 1.5]
                    ),
                    xaxis=dict(
                        title="Year (Negative values represent BCE)",
                        gridcolor='rgba(255,255,255,0.2)'
                    ),
                    height=250,
                    margin=dict(l=10, r=10, t=50, b=30),
                )
                
                # Apply dark theme
                fig = apply_dark_theme(fig)
                
                # Display timeline
                st.plotly_chart(fig, use_container_width=True)
                
                # Display key events in a formatted table
                st.subheader("Key Events in Ancient India")
                for _, row in ancient_df.iterrows():
                    time_label = f"{row['Time Period']}"
                    
                    # Format year for BCE/CE display
                    year_display = f"{abs(row['Timeline Year'])} {'BCE' if row['Timeline Year'] < 0 else 'CE'}"
                    
                    st.markdown(f"""
                    <div style='margin-bottom:15px; padding:10px; border-radius:5px; background-color:rgba(227, 102, 62, 0.1);'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='font-weight:bold; color:{period_colors["Ancient"]};'>{row['Era']}</span>
                            <span style='color:#AAAAAA;'>{year_display}</span>
                        </div>
                        <div style='margin-top:5px;'>
                            <span>{row['Event'] if 'Event' in row and not pd.isna(row['Event']) else 'Major historical era'}</span>
                        </div>
                        <div style='margin-top:5px; font-size:0.9em;'>
                            {row['Significance'] if 'Significance' in row and not pd.isna(row['Significance']) else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No data available for the ancient period.")
        
        # MEDIEVAL PERIOD TAB
        with timeline_tabs[1]:
            st.markdown(f"<h3 style='color:{period_colors['Medieval']}'>Medieval India</h3>", unsafe_allow_html=True)
            
            # Filter data for medieval period
            medieval_df = df[(df['Timeline Year'] >= 600) & (df['Timeline Year'] < 1757)]
            if not medieval_df.empty:
                # Sort by timeline year
                medieval_df = medieval_df.sort_values('Timeline Year')
                
                # Create an enhanced timeline visualization
                fig = go.Figure()
                
                # Add events as scatter points
                fig.add_trace(go.Scatter(
                    x=medieval_df['Timeline Year'],
                    y=[1] * len(medieval_df),
                    mode='markers+text',
                    marker=dict(
                        symbol='circle',
                        size=16,
                        color=period_colors['Medieval'],
                        line=dict(width=2, color='white')
                    ),
                    text=medieval_df['Era'],
                    textposition="top center",
                    hovertemplate='<b>%{text}</b><br>Year: %{x}<extra></extra>'
                ))
                
                # Add a line connecting all points
                fig.add_trace(go.Scatter(
                    x=medieval_df['Timeline Year'],
                    y=[1] * len(medieval_df),
                    mode='lines',
                    line=dict(color=period_colors['Medieval'], width=3),
                    hoverinfo='skip'
                ))
                
                # Update layout
                fig.update_layout(
                    title="Medieval Indian Timeline",
                    showlegend=False,
                    yaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False,
                        range=[0.5, 1.5]
                    ),
                    xaxis=dict(
                        title="Year (CE)",
                        gridcolor='rgba(255,255,255,0.2)'
                    ),
                    height=250,
                    margin=dict(l=10, r=10, t=50, b=30),
                )
                
                # Apply dark theme
                fig = apply_dark_theme(fig)
                
                # Display timeline
                st.plotly_chart(fig, use_container_width=True)
                
                # Display key events in a formatted table
                st.subheader("Key Events in Medieval India")
                for _, row in medieval_df.iterrows():
                    # Format year for CE display
                    year_display = f"{row['Timeline Year']} CE"
                    
                    st.markdown(f"""
                    <div style='margin-bottom:15px; padding:10px; border-radius:5px; background-color:rgba(108, 140, 191, 0.1);'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='font-weight:bold; color:{period_colors["Medieval"]};'>{row['Era']}</span>
                            <span style='color:#AAAAAA;'>{year_display}</span>
                        </div>
                        <div style='margin-top:5px;'>
                            <span>{row['Event'] if 'Event' in row and not pd.isna(row['Event']) else 'Major historical era'}</span>
                        </div>
                        <div style='margin-top:5px; font-size:0.9em;'>
                            {row['Significance'] if 'Significance' in row and not pd.isna(row['Significance']) else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No data available for the medieval period.")
        
        # COLONIAL PERIOD TAB
        with timeline_tabs[2]:
            st.markdown(f"<h3 style='color:{period_colors['Colonial']}'>Colonial Period</h3>", unsafe_allow_html=True)
            
            # Filter data for colonial period
            colonial_df = df[(df['Timeline Year'] >= 1757) & (df['Timeline Year'] < 1947)]
            if not colonial_df.empty:
                # Sort by timeline year
                colonial_df = colonial_df.sort_values('Timeline Year')
                
                # Create an enhanced timeline visualization
                fig = go.Figure()
                
                # Add events as scatter points
                fig.add_trace(go.Scatter(
                    x=colonial_df['Timeline Year'],
                    y=[1] * len(colonial_df),
                    mode='markers+text',
                    marker=dict(
                        symbol='circle',
                        size=16,
                        color=period_colors['Colonial'],
                        line=dict(width=2, color='white')
                    ),
                    text=colonial_df['Era'],
                    textposition="top center",
                    hovertemplate='<b>%{text}</b><br>Year: %{x}<extra></extra>'
                ))
                
                # Add a line connecting all points
                fig.add_trace(go.Scatter(
                    x=colonial_df['Timeline Year'],
                    y=[1] * len(colonial_df),
                    mode='lines',
                    line=dict(color=period_colors['Colonial'], width=3),
                    hoverinfo='skip'
                ))
                
                # Update layout
                fig.update_layout(
                    title="Colonial Indian Timeline",
                    showlegend=False,
                    yaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False,
                        range=[0.5, 1.5]
                    ),
                    xaxis=dict(
                        title="Year (CE)",
                        gridcolor='rgba(255,255,255,0.2)'
                    ),
                    height=250,
                    margin=dict(l=10, r=10, t=50, b=30),
                )
                
                # Apply dark theme
                fig = apply_dark_theme(fig)
                
                # Display timeline
                st.plotly_chart(fig, use_container_width=True)
                
                # Display key events in a formatted table
                st.subheader("Key Events in Colonial India")
                for _, row in colonial_df.iterrows():
                    year_display = f"{row['Timeline Year']} CE"
                    
                    st.markdown(f"""
                    <div style='margin-bottom:15px; padding:10px; border-radius:5px; background-color:rgba(77, 144, 120, 0.1);'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='font-weight:bold; color:{period_colors["Colonial"]};'>{row['Era']}</span>
                            <span style='color:#AAAAAA;'>{year_display}</span>
                        </div>
                        <div style='margin-top:5px;'>
                            <span>{row['Event'] if 'Event' in row and not pd.isna(row['Event']) else 'Major historical era'}</span>
                        </div>
                        <div style='margin-top:5px; font-size:0.9em;'>
                            {row['Significance'] if 'Significance' in row and not pd.isna(row['Significance']) else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No data available for the colonial period.")
        
        # MODERN PERIOD TAB
        with timeline_tabs[3]:
            st.markdown(f"<h3 style='color:{period_colors['Modern']}'>Modern India</h3>", unsafe_allow_html=True)
            
            # Filter data for modern period
            modern_df = df[df['Timeline Year'] >= 1947]
            if not modern_df.empty:
                # Sort by timeline year
                modern_df = modern_df.sort_values('Timeline Year')
                
                # Create an enhanced timeline visualization
                fig = go.Figure()
                
                # Add events as scatter points
                fig.add_trace(go.Scatter(
                    x=modern_df['Timeline Year'],
                    y=[1] * len(modern_df),
                    mode='markers+text',
                    marker=dict(
                        symbol='circle',
                        size=16,
                        color=period_colors['Modern'],
                        line=dict(width=2, color='white')
                    ),
                    text=modern_df['Era'],
                    textposition="top center",
                    hovertemplate='<b>%{text}</b><br>Year: %{x}<extra></extra>'
                ))
                
                # Add a line connecting all points
                fig.add_trace(go.Scatter(
                    x=modern_df['Timeline Year'],
                    y=[1] * len(modern_df),
                    mode='lines',
                    line=dict(color=period_colors['Modern'], width=3),
                    hoverinfo='skip'
                ))
                
                # Update layout
                fig.update_layout(
                    title="Modern Indian Timeline",
                    showlegend=False,
                    yaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False,
                        range=[0.5, 1.5]
                    ),
                    xaxis=dict(
                        title="Year (CE)",
                        gridcolor='rgba(255,255,255,0.2)'
                    ),
                    height=250,
                    margin=dict(l=10, r=10, t=50, b=30),
                )
                
                # Apply dark theme
                fig = apply_dark_theme(fig)
                
                # Display timeline
                st.plotly_chart(fig, use_container_width=True)
                
                # Display key events in a formatted table
                st.subheader("Key Events in Modern India")
                for _, row in modern_df.iterrows():
                    year_display = f"{row['Timeline Year']} CE"
                    
                    st.markdown(f"""
                    <div style='margin-bottom:15px; padding:10px; border-radius:5px; background-color:rgba(255, 200, 87, 0.1);'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='font-weight:bold; color:{period_colors["Modern"]};'>{row['Era']}</span>
                            <span style='color:#AAAAAA;'>{year_display}</span>
                        </div>
                        <div style='margin-top:5px;'>
                            <span>{row['Event'] if 'Event' in row and not pd.isna(row['Event']) else 'Major historical era'}</span>
                        </div>
                        <div style='margin-top:5px; font-size:0.9em;'>
                            {row['Significance'] if 'Significance' in row and not pd.isna(row['Significance']) else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No data available for the modern period.")
        
        # Add an explanatory text below the timeline
        st.markdown("""
        <div class='info-card' style='margin-top:20px;'>
        <strong>About the Timeline:</strong> The interactive timeline above organizes Indian history into four major periods.
        Each tab shows key events and developments within that timeframe. Click on different tabs to explore India's journey 
        from ancient civilizations to the modern nation-state.
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating visual timeline: {e}")
        
        # Provide fallback content
        st.markdown("""
        <div style='background-color:rgba(49, 51, 63, 0.7);padding:20px;border-radius:5px;margin:15px 0;'>
        <h4>Major Periods in Indian History</h4>
        
        <div style='margin-bottom:15px;'>
            <h5 style='color:#E3663E;'>Ancient India (Before 600 CE)</h5>
            <p>From the emergence of the Indus Valley Civilization around 2600 BCE through the Vedic Period, 
            Mauryan Empire, and Gupta Empire - establishing foundations of Indian culture, philosophy, and science.</p>
        </div>
        
        <div style='margin-bottom:15px;'>
            <h5 style='color:#6C8CBF;'>Medieval India (600-1757 CE)</h5>
            <p>Rise of regional kingdoms, introduction of Islam, establishment of Delhi Sultanate and Mughal Empire, 
            creating a synthesis of Indo-Islamic culture, art, and governance.</p>
        </div>
        
        <div style='margin-bottom:15px;'>
            <h5 style='color:#4D9078;'>Colonial India (1757-1947)</h5>
            <p>British East India Company rule followed by direct British Crown control, development of Indian nationalism, 
            freedom struggle under Gandhi and other leaders, ultimately leading to independence.</p>
        </div>
        
        <div style='margin-bottom:15px;'>
            <h5 style='color:#FFC857;'>Modern India (1947-Present)</h5>
            <p>From independence and partition, through economic reforms of the 1990s, to India's emergence as a 
            major global player in technology, space exploration, and international affairs.</p>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Historical Evolution Analysis
    st.header("Key Developments Through History")
    
    try:
        # Introduction text to give more soul to this section
        st.markdown("""
        <div style='margin-bottom:20px;'>
        <p>India's historical journey has witnessed remarkable achievements across many domains. 
        Select the aspects below to explore how different eras contributed to India's evolution in these areas.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a multi-select for user to choose aspects to explore
        aspects = st.multiselect(
            "Select historical aspects to explore:",
            options=['Cultural Developments', 'Religious Trends', 'Economic Systems', 
                    'Scientific Advances', 'Art & Architecture', 'Social Structure',
                    'Military Developments', 'Technological Innovations'],
            default=['Cultural Developments', 'Scientific Advances', 'Art & Architecture', 'Technological Innovations']
        )
        
        if aspects:
            # Create a DataFrame for selected aspects
            evolution_data = []
            
            for _, row in df.iterrows():
                for aspect in aspects:
                    # Skip empty entries
                    if aspect not in row or pd.isna(row[aspect]) or row[aspect] == '':
                        continue
                        
                    # Try to split by periods or semicolons first, then commas
                    if '. ' in row[aspect]:
                        key_points = row[aspect].split('. ')
                    elif ';' in row[aspect]:
                        key_points = row[aspect].split(';')
                    else:
                        key_points = row[aspect].split(', ')
                    
                    for point in key_points:
                        # Skip empty points
                        if not point.strip():
                            continue
                            
                        # Add a period if needed
                        clean_point = point.strip()
                        if not clean_point.endswith('.') and len(clean_point) > 20:  # Only add period for longer points
                            clean_point += '.'
                            
                        evolution_data.append({
                            'Era': row['Era'],
                            'Aspect': aspect,
                            'Development': clean_point,
                            'Timeline Year': row['Timeline Year']
                        })
            
            evolution_df = pd.DataFrame(evolution_data)
            
            # Create visualization for evolution of selected aspects
            if not evolution_df.empty:
                # Group by era and aspect, count developments
                aspect_counts = evolution_df.groupby(['Era', 'Aspect']).size().reset_index(name='Count')
                
                # Create pivot table for radar chart
                aspect_pivot = aspect_counts.pivot(index='Era', columns='Aspect', values='Count').fillna(0)
                
                # Prepare data for radar chart
                categories = aspects
                
                # Make sure all categories exist in pivot table
                for category in categories:
                    if category not in aspect_pivot.columns:
                        aspect_pivot[category] = 0
                
                fig = go.Figure()
                
                # Add a trace for each era
                for era in df['Era'].unique():
                    if era in aspect_pivot.index:
                        values = [aspect_pivot.loc[era, aspect] if aspect in aspect_pivot.columns else 0 for aspect in categories]
                        
                        # Ensure non-zero values for better visualization
                        values = [max(0.5, v) for v in values]
                        
                        # Close the polygon by repeating the first value
                        values.append(values[0])
                        categories_closed = categories + [categories[0]]
                        
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=categories_closed,
                            fill='toself',
                            name=era,
                            line_color=era_colors[era]
                        ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, max(aspect_counts['Count']) + 1]
                        )),
                    title="Evolution of Key Developments Across Historical Periods",
                    height=600,
                    margin=dict(l=10, r=10, t=50, b=10),
                )
                
                # Apply dark theme
                fig = apply_dark_theme(fig)
                
                # Display the polar chart
                st.plotly_chart(fig, use_container_width=True)
                
                # Add an explanation of the radar chart
                st.markdown("""
                <div style='background-color:rgba(49, 51, 63, 0.7);padding:15px;border-radius:5px;margin:15px 0;'>
                <h4>Understanding the Radar Chart</h4>
                <p>This visualization shows the relative emphasis each historical era placed on different aspects of development.
                Larger areas indicate eras with more significant developments across multiple domains.</p>
                
                <p>For example, you can see which eras emphasized cultural advancements versus technological innovations,
                or which periods made balanced contributions across all selected aspects.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Development table with filtering
                st.subheader("Detailed Developments Table")
                
                st.markdown("""
                <div style='margin-bottom:15px;'>
                This table displays specific developments from the selected historical eras. 
                Use the filters below to explore developments in different periods and aspects of Indian history.
                </div>
                """, unsafe_allow_html=True)
                
                # Create a two-column layout for filters
                filter_col1, filter_col2 = st.columns(2)
                
                with filter_col1:
                    # Get available eras from the dataframe
                    available_eras = sorted(df['Era'].unique().tolist())
                    
                    # Define preferred default eras (in order of preference)
                    preferred_defaults = ['Mughal Empire', 'Gupta Empire', 'Republic of India', 
                                        'Ancient India', 'British Raj', 'Modern India', 
                                        'Mauryan Empire', 'Delhi Sultanate']
                    
                    # Find which preferred eras exist in the dataset (up to 3)
                    default_eras = [era for era in preferred_defaults if era in available_eras][:3]
                    
                    # If we couldn't find any of our preferred defaults, take the first 3 eras from available
                    if not default_eras and len(available_eras) > 0:
                        default_eras = available_eras[:min(3, len(available_eras))]
                    
                    # Era filter
                    selected_eras = st.multiselect(
                        "Filter by historical era:",
                        options=available_eras,
                        default=default_eras
                    )
                
                with filter_col2:
                    # Get available aspects from the evolution dataframe
                    if not evolution_df.empty:
                        available_aspects = sorted(evolution_df['Aspect'].unique().tolist())
                        
                        # Aspect filter (with all selected by default)
                        selected_aspects = st.multiselect(
                            "Filter by aspect:",
                            options=available_aspects,
                            default=available_aspects
                        )
                    else:
                        selected_aspects = aspects  # Use the aspects selected earlier if no data
                
                # Apply filters
                if selected_eras or selected_aspects:
                    # Start with all data
                    filtered_df = evolution_df.copy()
                    
                    # Apply era filter if any eras are selected
                    if selected_eras:
                        filtered_df = filtered_df[filtered_df['Era'].isin(selected_eras)]
                    
                    # Apply aspect filter if any aspects are selected and they're available
                    if selected_aspects and 'Aspect' in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df['Aspect'].isin(selected_aspects)]
                else:
                    # If no filters are selected, show all data
                    filtered_df = evolution_df
                
                # Sort by timeline year for chronological order
                filtered_df = filtered_df.sort_values('Timeline Year')
                
                # Display as formatted table with scrollable container
                st.markdown("""
                <style>
                .development-table {
                    max-height: 400px;
                    overflow-y: auto;
                    padding: 10px;
                    border: 1px solid #333;
                    border-radius: 5px;
                }
                </style>
                """, unsafe_allow_html=True)
                
                if not filtered_df.empty:
                    st.markdown("<div class='development-table'>", unsafe_allow_html=True)
                    for idx, row in filtered_df.iterrows():
                        st.markdown(f"""
                        <div style='border-left: 3px solid {era_colors[row['Era']]}; padding-left: 10px; margin-bottom: 15px;'>
                            <span style='color:{era_colors[row['Era']]}; font-weight:bold;'>{row['Era']}</span> • 
                            <span style='color:#AAAAAA;'>{row['Aspect']}</span><br>
                            <span style='font-size:1.05em;'>{row['Development']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("No detailed development data available for the selected filters. Try selecting different aspects or eras.")
            else:
                st.warning("No detailed development data is available for the selected aspects. Try selecting different aspects.")
                
                # Provide alternative content
                st.markdown("""
                <div style='background-color:rgba(49, 51, 63, 0.7);padding:15px;border-radius:5px;margin:15px 0;'>
                <h4>Key Historical Developments in India</h4>
                
                <p>While detailed data visualization isn't available for your selection, here are some key developments across India's history:</p>
                
                <ul>
                  <li><strong>Scientific Innovations:</strong> From Aryabhata's astronomical calculations to the development of steel and the concept of zero</li>
                  <li><strong>Architectural Marvels:</strong> From the precisely engineered cities of the Indus Valley to the Taj Mahal</li>
                  <li><strong>Cultural Achievements:</strong> Sanskrit literature, classical music, dance forms, and art traditions that have continued for millennia</li>
                  <li><strong>Religious Thought:</strong> Development of philosophical schools within Hinduism, Buddhism, Jainism and later synthesis with Islam</li>
                  <li><strong>Administrative Systems:</strong> Innovations from the Arthashastra's statecraft to the Mughals' administrative systems and modern democracy</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Please select historical aspects to explore using the multi-select box above.")
            
            # Provide some guidance
            st.markdown("""
            <div style='background-color:rgba(49, 51, 63, 0.7);padding:15px;border-radius:5px;margin:15px 0;'>
            <h4>Suggested Combinations to Explore</h4>
            
            <ul>
              <li><strong>Cultural & Religious Developments:</strong> See how India's spiritual and cultural evolution unfolded across time periods</li>
              <li><strong>Scientific & Technological Innovations:</strong> Track India's contributions to global knowledge and technical progress</li>
              <li><strong>Economic Systems & Social Structure:</strong> Understand how India's society and economic organization evolved</li>
              <li><strong>Military & Foreign Relations:</strong> Explore India's defensive capabilities and international connections throughout history</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error analyzing historical developments: {e}")
        
        # Provide fallback content
        st.markdown("""
        <div style='background-color:rgba(49, 51, 63, 0.7);padding:15px;border-radius:5px;margin:15px 0;'>
        <h4>The Evolution of Indian Civilization</h4>
        
        <p>While we're having technical difficulties displaying detailed development data, here are key patterns in India's historical evolution:</p>
        
        <ul>
          <li><strong>Cultural Synthesis:</strong> Throughout history, India has absorbed outside influences and transformed them into uniquely Indian expressions</li>
          <li><strong>Technological Innovation:</strong> From metallurgy to mathematics, India has contributed fundamental technological advances</li>
          <li><strong>Religious Diversity:</strong> India birthed multiple major world religions while also accommodating faiths from elsewhere</li>
          <li><strong>Artistic Continuity:</strong> Many art forms and architectural traditions show remarkable continuity across thousands of years</li>
          <li><strong>Political Adaptation:</strong> India's political systems have evolved from tribal republics to empires to the world's largest democracy</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Legacy analysis and impact
    st.header("The Legacy of Indian History")
    
    try:
        # Legacy analysis and impact
        legacy_data = df[['Era']].copy()
        
        # Check if legacy data is available
        if 'Historical Legacy' in df.columns and not df['Historical Legacy'].isna().all():
            legacy_data['Historical Legacy'] = df['Historical Legacy']
            
            # Extract key themes from legacy
            common_themes = [
                'Cultural', 'Religious', 'Administrative', 'Scientific', 
                'Architectural', 'Political', 'Social', 'Economic'
            ]
            
            # Create theme columns with proper NaN handling
            for theme in common_themes:
                # Convert to string first to avoid NaN issues, then perform contains check
                legacy_data[theme] = legacy_data['Historical Legacy'].fillna('').astype(str).str.contains(theme, case=False).astype(int)
            
            # Create heatmap of themes by era
            theme_matrix = legacy_data[['Era'] + common_themes].set_index('Era')
            
            # Ensure there are no NaN values in the matrix before visualization
            theme_matrix = theme_matrix.fillna(0)
            
            # Create the heatmap
            fig = px.imshow(
                theme_matrix.values,
                x=common_themes,
                y=theme_matrix.index,
                color_continuous_scale='Viridis',
                title='Historical Legacy Themes Across Eras',
                height=500
            )
            
            # Apply dark theme
            fig = apply_dark_theme(fig)
            
            # Improve axes labels
            fig.update_layout(
                xaxis_title="Legacy Themes", 
                yaxis_title="Historical Eras",
                margin=dict(l=10, r=10, t=50, b=30)
            )
            
            # Display the heatmap
            st.plotly_chart(fig, use_container_width=True)
            
            # Add more engaging description
            st.markdown("""
            <div style='background-color:rgba(49, 51, 63, 0.7);padding:15px;border-radius:5px;margin-bottom:20px;'>
            <h4>What This Legacy Heatmap Shows:</h4>
            <p>The visualization above illustrates how different historical eras of India contributed to various aspects 
            of the nation's legacy. Brighter areas indicate stronger influences in that particular theme.</p>
            
            <p>India's historical narrative isn't simply a sequence of events but rather a tapestry of interconnected cultural, 
            religious, political, and scientific developments that have profoundly shaped not just the subcontinent but global civilization.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display alternative content if legacy data is not available
            st.info("Detailed historical legacy data visualization is not available, but here's what you should know:")
            
            st.markdown("""
            <div style='background-color:rgba(49, 51, 63, 0.7);padding:15px;border-radius:5px;margin:15px 0;'>
            <h4>The Enduring Legacy of Indian History</h4>
            
            <p>India's historical legacy is remarkably multifaceted and has influenced global civilization in profound ways:</p>
            
            <ul>
              <li><strong>Cultural Continuity:</strong> Few civilizations can claim the continuous cultural development that India has maintained 
              for over 5,000 years, from the Indus Valley through today's republic.</li>
              
              <li><strong>Religious Innovation:</strong> As the birthplace of Hinduism, Buddhism, Jainism, and Sikhism, India has shaped the 
              spiritual beliefs of billions worldwide throughout history.</li>
              
              <li><strong>Scientific Contributions:</strong> From the concept of zero and decimal system to early astronomical observations 
              and surgical techniques, Indian scientific thought has been fundamental to human knowledge.</li>
              
              <li><strong>Architectural Heritage:</strong> From the precision of Indus cities to the splendor of Mughal monuments, 
              India's architectural traditions represent some of humanity's greatest achievements.</li>
              
              <li><strong>Philosophical Depth:</strong> Indian philosophical traditions have explored the nature of consciousness, 
              reality, and ethics with remarkable sophistication from ancient times to the present day.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error analyzing historical legacy: {e}")
        
        # Provide fallback content
        st.markdown("""
        <div style='background-color:rgba(49, 51, 63, 0.7);padding:15px;border-radius:5px;margin:15px 0;'>
        <h4>The Essence of Indian Historical Legacy</h4>
        
        <p>Despite technical difficulties displaying the legacy analysis, it's important to understand that India's 
        historical contributions have been monumental:</p>
        
        <ul>
          <li>The world's oldest continuous civilization with urban planning dating back to 2600 BCE</li>
          <li>Pioneering mathematics including the concept of zero, decimal system, and algebra</li>
          <li>Advanced metallurgy that produced the rust-resistant Iron Pillar of Delhi in the 4th century</li>
          <li>Sophisticated philosophical schools that contemplated the nature of reality millennia ago</li>
          <li>Cultural adaptability that allowed diverse traditions to coexist and intermingle</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Key insights about historical continuity
    st.markdown("""
    <div class='insight-box'>
    <strong>Historical Continuity Insights:</strong>
    <ul>
      <li><strong>Cultural Synthesis:</strong> Throughout India's history, incoming cultures were absorbed and integrated rather than replaced, creating layers of cultural influence.</li>
      <li><strong>Administrative Patterns:</strong> Many modern Indian administrative structures have roots in historical systems from the Mauryan, Mughal, and British periods.</li>
      <li><strong>Religious Evolution:</strong> India witnessed the birth of major religions (Hinduism, Buddhism, Jainism) and the adaptation of others (Islam, Christianity) into its cultural fabric.</li>
      <li><strong>Scientific Legacy:</strong> Indian contributions to mathematics, astronomy, and medicine have fundamentally shaped global scientific development.</li>
      <li><strong>Architectural Continuity:</strong> Each era added to India's architectural heritage, creating a timeline of styles that showcases technical and artistic evolution.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Final summary
    st.markdown("""
    <div class='story-text'>
    India's historical journey represents one of humanity's most remarkable continuous civilizational stories. 
    From the urban planning of Harappa to the democratic institutions of modern India, the nation's history 
    demonstrates remarkable adaptability and cultural synthesis. Each historical period has left lasting legacies 
    that continue to shape contemporary Indian society, politics, art, and thought.
    
    This tapestry of historical experiences - empires rising and falling, religious movements spreading, cultural 
    and scientific achievements flourishing - forms the foundation for understanding the complexity and resilience 
    of modern India.
    </div>
    """, unsafe_allow_html=True) 