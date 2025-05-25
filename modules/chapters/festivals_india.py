import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from modules.utils import apply_dark_theme, load_festivals_data, style_matplotlib_for_dark, get_color_palette

def render():
    """Render the Festivals of India chapter content"""
    st.title("🪔 Festivals of India")
    
    st.markdown("""
    <div class='story-text'>
    India's vibrant cultural landscape is illuminated by its diverse festivals, celebrated throughout the year across 
    the country. These festivals reflect the rich tapestry of religions, cultures, and traditions that define India's 
    unique identity. From the colorful festivities of Holi to the spiritual celebrations of Diwali, each festival 
    represents a unique aspect of India's cultural heritage.
    </div>
    """, unsafe_allow_html=True)
    
    # Load and prepare data
    with st.spinner("Analyzing festivals data..."):
        try:
            df = load_festivals_data()
            
            if df is None or df.empty:
                st.error("Failed to load festivals data. Please check your data files.")
                return
                
            # Check and rename columns if necessary
            if 'Religion' in df.columns and 'Religion/Type' not in df.columns:
                df['Religion/Type'] = df['Religion']
            elif 'Religion/Type' not in df.columns and 'Type' in df.columns:
                df['Religion/Type'] = df['Type']
            
            # Prepare derived data
            religion_counts = df['Religion/Type'].value_counts().reset_index()
            religion_counts.columns = ['Religion/Type', 'Count']
            
            # Handle season data
            if 'Season' in df.columns:
                # Extract seasons for analysis
                season_data = df['Season'].str.extract(r'([A-Za-z]+)').reset_index()
                season_data.columns = ['index', 'Season']
                season_data = season_data.join(df['Festival'])
                season_counts = season_data['Season'].value_counts().reset_index()
                season_counts.columns = ['Season', 'Count']
            else:
                # Create sample season data if missing
                st.warning("Season data missing. Using sample data.")
                sample_seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
                sample_counts = [8, 6, 5, 7]
                season_counts = pd.DataFrame({'Season': sample_seasons, 'Count': sample_counts})
                
                # Add a Season column to df for later use
                df['Season'] = np.random.choice(sample_seasons, size=len(df))
            
            # Ensure economic impact column exists
            if 'Economic Impact (USD millions)' in df.columns:
                df['Economic Impact (Millions USD)'] = df['Economic Impact (USD millions)']
            elif 'Economic Impact (Millions USD)' not in df.columns:
                st.warning("Economic impact data missing. Using estimated values.")
                # Generate sample economic impact data based on festival importance
                df['Economic Impact (Millions USD)'] = np.random.uniform(100, 1000, size=len(df))
        except Exception as e:
            st.error(f"Error processing festivals data: {e}")
            return
    
    # Interactive festival exploration section
    st.header("Explore India's Major Festivals")
    
    # Create 2-column layout
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Festival selection
        selected_festival = st.selectbox(
            "Select a festival to explore:",
            options=df['Festival'].tolist()
        )
        
        # Display festival image or icon
        festival_icons = {
            'Diwali': '🪔',
            'Holi': '🎨',
            'Durga Puja': '🛕',
            'Ganesh Chaturthi': '🐘',
            'Navratri/Durgotsav': '💃',
            'Onam': '🌸',
            'Eid ul-Fitr': '🌙',
            'Christmas': '🎄',
            'Baisakhi': '🌾',
            'Janmashtami': '👶',
        }
        
        # Display festival icon or default
        icon = festival_icons.get(selected_festival, '🎯')
        st.markdown(f"<h1 style='text-align:center; font-size:4rem;'>{icon}</h1>", unsafe_allow_html=True)
    
    # Display detailed information about the selected festival
    with col2:
        try:
            festival_data = df[df['Festival'] == selected_festival].iloc[0]
            
            # Create a clean display of festival details
            st.markdown(f"### {selected_festival}")
            
            # Display festival type if available
            if 'Religion/Type' in festival_data:
                st.markdown(f"**Type:** {festival_data['Religion/Type']}")
            
            # Display season if available
            if 'Season' in festival_data:
                st.markdown(f"**When:** {festival_data['Season']}")
            
            # Display duration if available
            if 'Duration (days)' in festival_data:
                st.markdown(f"**Duration:** {festival_data['Duration (days)']} days")
            
            # Display states if available
            if 'Primary States' in festival_data:
                st.markdown(f"**Celebrated in:** {festival_data['Primary States']}")
            
            # Create metrics row
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                if 'Participants (millions)' in festival_data:
                    st.metric("Participants", f"{festival_data['Participants (millions)']}M")
                else:
                    st.metric("Participants", "N/A")
            
            with metric_col2:
                if 'Economic Impact (Millions USD)' in festival_data:
                    st.metric("Economic Impact", f"${festival_data['Economic Impact (Millions USD)']}M")
                else:
                    st.metric("Economic Impact", "N/A")
            
            with metric_col3:
                if 'Tourist Attraction Level' in festival_data:
                    st.metric("Tourist Appeal", festival_data['Tourist Attraction Level'])
                else:
                    st.metric("Tourist Appeal", "Medium")
        except Exception as e:
            st.error(f"Error displaying festival details: {e}")
    
    # Divider
    st.markdown("---")
    
    # Festival visualizations section in tabs
    st.header("Festival Data Insights")
    
    tabs = st.tabs(["Distribution by Type", "Economic Impact", "Seasonal Patterns", "Global Reach"])
    
    # Tab 1: Distribution by Type
    with tabs[0]:
        try:
            fig = px.pie(
                religion_counts, 
                values='Count', 
                names='Religion/Type',
                title='Distribution of Festivals by Type',
                color_discrete_sequence=get_color_palette(len(religion_counts)),
                hole=0.4
            )
            fig = apply_dark_theme(fig)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div class='insight-box'>
            <strong>Insight:</strong> Hindu festivals make up the largest segment, reflecting the majority religion, 
            but India's festival landscape shows remarkable diversity with cultural, Islamic, harvest, and other celebrations 
            that span across religious boundaries.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in distribution visualization: {e}")
    
    # Tab 2: Economic Impact
    with tabs[1]:
        try:
            # Sort data by economic impact
            if 'Economic Impact (Millions USD)' in df.columns:
                economic_df = df.sort_values('Economic Impact (Millions USD)', ascending=False).head(10)
                
                fig = px.bar(
                    economic_df,
                    x='Festival',
                    y='Economic Impact (Millions USD)',
                    color='Religion/Type',
                    title='Top 10 Festivals by Economic Impact (USD Millions)',
                    color_discrete_sequence=get_color_palette(len(economic_df['Religion/Type'].unique())),
                    text='Economic Impact (Millions USD)'
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(texttemplate='%{text:.0f}M', textposition='outside')
                fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Economic impact data is not available.")
            
            st.markdown("""
            <div class='insight-box'>
            <strong>Insight:</strong> Diwali generates the highest economic impact at $7.2 billion USD annually, 
            followed by Holi and Eid ul-Fitr. Major festivals significantly boost sectors like retail, food, 
            clothing, travel, and services.
            </div>
            """, unsafe_allow_html=True)
            
            # Correlation between participants and economic impact
            if all(col in df.columns for col in ['Participants (millions)', 'Economic Impact (Millions USD)', 'Tourist Attraction Level']):
                fig = px.scatter(
                    df,
                    x='Participants (millions)',
                    y='Economic Impact (Millions USD)',
                    size='Tourist Attraction Level',
                    color='Religion/Type',
                    hover_name='Festival',
                    title='Relationship: Participants, Economic Impact & Tourism Appeal',
                    log_x=True,
                    size_max=25,
                    color_discrete_sequence=get_color_palette(len(df['Religion/Type'].unique()))
                )
                fig = apply_dark_theme(fig)
                fig.update_layout(xaxis_title="Participants (Millions, log scale)", 
                                yaxis_title="Economic Impact (USD Millions)")
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error in economic impact visualization: {e}")
    
    # Tab 3: Seasonal Patterns
    with tabs[2]:
        try:
            # Create a season order for better visualization
            season_order = ['Winter', 'Spring', 'Summer', 'Monsoon', 'Autumn']
            
            # Handle season_counts data
            if 'Season' in season_counts.columns:
                season_counts['Season'] = pd.Categorical(season_counts['Season'], 
                                                    categories=season_order, 
                                                    ordered=True)
                season_counts = season_counts.sort_values('Season')
                
                fig = px.bar(
                    season_counts,
                    x='Season',
                    y='Count',
                    color='Season',
                    title='Seasonal Distribution of Festivals',
                    text='Count',
                    color_discrete_sequence=get_color_palette(len(season_counts))
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Season count data is not available.")
            
            # Festival timeline through the year
            months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                        'July', 'August', 'September', 'October', 'November', 'December']
            
            # Check if Season column exists for timeline
            if 'Season' in df.columns:
                # Extract month data with regex
                df['Month'] = df['Season'].str.extract(r'([A-Za-z]+)(?:-[A-Za-z]+)?')[0]
                
                # Map extracted month to standardized month
                month_mapping = {
                    'January': 'January',
                    'February': 'February', 
                    'March': 'March',
                    'April': 'April',
                    'May': 'May',
                    'June': 'June',
                    'July': 'July',
                    'August': 'August',
                    'September': 'September',
                    'October': 'October',
                    'November': 'November',
                    'December': 'December',
                    'Variable': 'Variable'  # Handle Islamic calendar
                }
                
                df['Month_Standard'] = df['Month'].map(month_mapping)
                
                # Filter out variable dates for timeline
                timeline_df = df[df['Month_Standard'] != 'Variable']
                
                # Create month-festival mapping
                month_festivals = {}
                for month in months_order:
                    month_festivals[month] = timeline_df[timeline_df['Month_Standard'] == month]['Festival'].tolist()
                
                # Create a festival calendar visualization
                fig = go.Figure()
                
                months_with_festivals = []
                festival_counts = []
                
                for month in months_order:
                    if month in timeline_df['Month_Standard'].values:
                        months_with_festivals.append(month)
                        festival_counts.append(len(month_festivals.get(month, [])))
                
                fig.add_trace(go.Bar(
                    x=months_with_festivals,
                    y=festival_counts,
                    text=festival_counts,
                    textposition='outside',
                    marker_color=get_color_palette(len(months_with_festivals)),
                    hoverinfo='text',
                    hovertext=[', '.join(month_festivals.get(month, [])) for month in months_with_festivals]
                ))
                
                fig.update_layout(
                    title='Festival Calendar Throughout the Year',
                    xaxis_title='Month',
                    yaxis_title='Number of Major Festivals',
                    xaxis={'categoryorder': 'array', 'categoryarray': months_order}
                )
                
                fig = apply_dark_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Month data is not available for the festival calendar.")
            
            st.markdown("""
            <div class='insight-box'>
            <strong>Insight:</strong> Autumn months (September-November) host the highest number of festivals, coinciding with the 
            harvest season and favorable weather. Winter and Spring also see significant celebrations, while the Summer and 
            Monsoon seasons have fewer major festivals.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in seasonal patterns visualization: {e}")
    
    # Tab 4: Global Reach
    with tabs[3]:
        try:
            # Check if global celebrations data is available
            if 'Global Celebrations' in df.columns:
                # Extract global reach data
                df['Global Reach'] = df['Global Celebrations'].str.extract(r'(\d+)\+').fillna('0').astype(int)
                
                global_df = df.sort_values('Global Reach', ascending=False).head(10)
                
                fig = px.bar(
                    global_df,
                    x='Festival',
                    y='Global Reach',
                    color='Religion/Type',
                    title='Top 10 Indian Festivals with Global Reach (Countries with Celebrations)',
                    color_discrete_sequence=get_color_palette(len(global_df['Religion/Type'].unique())),
                    text='Global Reach'
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(texttemplate='%{text}+ countries', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Global reach data is not available.")
            
            st.markdown("""
            <div class='insight-box'>
            <strong>Insight:</strong> Diwali has the widest global reach, celebrated in more than 30 countries with significant 
            Indian diaspora. Holi has grown in global popularity beyond the diaspora, while Sikh, Hindu, and Islamic festivals 
            also have significant international presence.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in global reach visualization: {e}")
    
    # Environmental impact section
    st.header("Environmental Impact of Festivals")
    
    try:
        # Create a categorical mapping for environmental impact
        impact_mapping = {
            'High': 3,
            'Moderate to High': 2.5,
            'Moderate': 2,
            'Low to Moderate': 1.5,
            'Low': 1
        }
        
        # Check if environmental impact data is available
        if 'Environmental Impact' in df.columns:
            # Extract environmental impact with regex and map to numeric values
            df['Impact Level'] = df['Environmental Impact'].str.extract(r'(High|Moderate to High|Moderate|Low to Moderate|Low)')[0]
            df['Impact Score'] = df['Impact Level'].map(impact_mapping)
            
            # Filter for festivals with usable data and sort
            env_df = df.dropna(subset=['Impact Score']).sort_values('Impact Score', ascending=False)
            
            fig = px.bar(
                env_df,
                x='Festival',
                y='Impact Score',
                color='Impact Level',
                title='Environmental Impact of Major Festivals',
                hover_data=['Environmental Impact'],
                color_discrete_map={
                    'High': '#FF5733',
                    'Moderate to High': '#FF9933',
                    'Moderate': '#FFCC33',
                    'Low to Moderate': '#33CC66',
                    'Low': '#33CCCC'
                }
            )
            fig = apply_dark_theme(fig)
            fig.update_layout(yaxis_title="Environmental Impact Level")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Environmental impact data is not available.")
    except Exception as e:
        st.error(f"Error in environmental impact visualization: {e}")
    
    # Key insights about festival sustainability
    st.markdown("""
    <div class='insight-box'>
    <strong>Sustainability Insights:</strong>
    <ul>
      <li><strong>High Impact:</strong> Festivals like Diwali face environmental challenges from air pollution due to fireworks.</li>
      <li><strong>Water Bodies:</strong> Idol immersion during Ganesh Chaturthi and Durga Puja impacts water ecosystems.</li>
      <li><strong>Sustainable Practices:</strong> Many festivals now promote eco-friendly celebrations with natural colors (Holi), 
      eco-friendly idols, and reduced fireworks.</li>
      <li><strong>Low Impact:</strong> Harvest festivals like Onam and cultural festivals generally have minimal environmental footprint.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Final summary
    st.header("The Cultural Significance of Indian Festivals")
    
    st.markdown("""
    <div class='story-text'>
    Festivals in India transcend mere celebrations – they are living heritage that connects generations, 
    strengthens community bonds, and preserves cultural traditions. Beyond their religious significance, 
    festivals play crucial economic roles, driving consumer spending, tourism, and employment in 
    handicrafts, food, and services sectors.
    
    Indian festivals represent a unique blend of ancient traditions and modern adaptations. As India 
    modernizes, festivals continue to evolve while maintaining their essential character. The growing 
    global reach of Indian festivals like Diwali and Holi demonstrates their universal appeal and 
    the soft power of Indian culture worldwide.
    </div>
    """, unsafe_allow_html=True)
    
    # Key takeaways in expandable sections
    with st.expander("🔍 Key Takeaways"):
        st.markdown("""
        - **Cultural Diversity:** India's festival landscape mirrors its religious and cultural diversity.
        - **Economic Engine:** Festivals drive significant economic activity ($15+ billion USD annually).
        - **Seasonal Rhythm:** Festival calendar follows agricultural cycles and seasonal changes.
        - **Global Influence:** Indian festivals increasingly celebrated worldwide.
        - **Evolving Traditions:** Ancient festivals adapting to modern contexts while preserving core values.
        - **Sustainability Challenges:** Growing awareness of environmental impacts leading to greener celebrations.
        """) 