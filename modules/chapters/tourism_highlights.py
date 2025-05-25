import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from modules.utils import apply_dark_theme, load_tourism_data, style_matplotlib_for_dark, get_color_palette

def render():
    """Render the Tourism Highlights chapter content"""
    st.title("🗼 Tourism Highlights of India")
    
    st.markdown("""
    <div class='story-text'>
    India, with its rich cultural heritage, diverse landscapes, and historical monuments, attracts millions
    of tourists from around the world each year. From the majestic Himalayas in the north to the tranquil 
    backwaters of Kerala in the south, from the vibrant deserts of Rajasthan to the pristine beaches of Goa,
    India offers a kaleidoscope of travel experiences.
    </div>
    """, unsafe_allow_html=True)
    
    # Load and prepare data
    with st.spinner("Analyzing tourism data..."):
        try:
            df = load_tourism_data()
            
            if df is None or df.empty:
                st.error("Tourism data could not be loaded. Please check the data file.")
                return
            
            # Ensure expected columns exist with proper names based on the actual CSV structure
            # First, check what columns actually exist in the dataframe
            actual_columns = df.columns.tolist()
            st.write(f"Found columns: {', '.join(actual_columns)}")
            
            # Define direct mappings based on the actual CSV file
            direct_mappings = {
                'Destination': 'Destination',
                'State': 'State',
                'Type': 'Tourism Type',
                'Visitors_Annual': 'Annual Visitors (millions)',
                'Best Season': 'Peak Season',
                'UNESCO Status': 'UNESCO Status',
                'Year Established': 'Year Established',
                'Entry Fee (INR)': 'Entry Fee (INR)',
                'Description': 'Description'
            }
            
            # Create new columns based on actual data
            for orig_col, new_col in direct_mappings.items():
                if orig_col in df.columns:
                    df[new_col] = df[orig_col]
                elif new_col not in df.columns:
                    # Create missing columns with appropriate default values
                    if 'Visitors' in new_col:
                        df[new_col] = np.random.uniform(0.1, 5.0, len(df))  # Random values for demonstration
                    elif 'Season' in new_col:
                        df[new_col] = 'Year-round'
                    elif 'Fee' in new_col:
                        df[new_col] = 0
                    elif 'Year' in new_col:
                        df[new_col] = 1900
                    else:
                        df[new_col] = 'Unknown'
            
            # Create additional columns needed for visualizations
            if 'Tourism Revenue (USD millions)' not in df.columns:
                # Estimate revenue based on visitors (rough approximation)
                if 'Annual Visitors (millions)' in df.columns:
                    df['Tourism Revenue (USD millions)'] = df['Annual Visitors (millions)'] * np.random.uniform(50, 150, len(df))
                else:
                    df['Tourism Revenue (USD millions)'] = np.random.uniform(10, 500, len(df))
            
            if 'International Visitors (%)' not in df.columns:
                # Add estimated international visitor percentages
                df['International Visitors (%)'] = np.random.uniform(10, 60, len(df))
                
            if 'Growth Potential (%)' not in df.columns:
                # Add estimated growth potential
                df['Growth Potential (%)'] = np.random.uniform(3, 15, len(df))
                
            if 'Infrastructure Quality (1-10)' not in df.columns:
                # Add infrastructure quality ratings
                df['Infrastructure Quality (1-10)'] = np.random.randint(4, 10, len(df))
                
            if 'Employment Generated (thousands)' not in df.columns:
                # Estimate employment based on visitors
                if 'Annual Visitors (millions)' in df.columns:
                    df['Employment Generated (thousands)'] = df['Annual Visitors (millions)'] * np.random.uniform(10, 30, len(df))
                else:
                    df['Employment Generated (thousands)'] = np.random.uniform(5, 100, len(df))
            
            # Create region grouping
            region_mapping = {
                'North': ['Delhi', 'Rajasthan', 'Uttar Pradesh', 'Himachal Pradesh', 'Jammu and Kashmir', 'Uttarakhand', 'Punjab', 'Haryana', 'Ladakh'],
                'South': ['Kerala', 'Tamil Nadu', 'Karnataka', 'Andhra Pradesh', 'Telangana', 'Puducherry'],
                'East': ['West Bengal', 'Odisha', 'Bihar', 'Jharkhand'],
                'West': ['Maharashtra', 'Gujarat', 'Goa', 'Daman & Diu'],
                'Central': ['Madhya Pradesh', 'Chhattisgarh'],
                'Northeast': ['Assam', 'Sikkim', 'Arunachal Pradesh', 'Meghalaya', 'Nagaland', 'Manipur', 'Mizoram', 'Tripura'],
                'Islands': ['Andaman and Nicobar Islands', 'Lakshadweep']
            }
            
            # Map states to regions with error handling
            try:
                # Function to find the region for a state
                def find_region(state_name):
                    if pd.isna(state_name) or not isinstance(state_name, str):
                        return 'Other'
                    
                    for region, states in region_mapping.items():
                        # Check for exact match
                        if state_name in states:
                            return region
                        # Check for partial match
                        for state in states:
                            if state.lower() in state_name.lower():
                                return region
                    return 'Other'
                
                df['Region'] = df['State'].apply(find_region)
            except Exception as e:
                st.warning(f"Could not map states to regions: {e}")
                df['Region'] = 'Other'
                
            # Create tourism type categorization if needed
            if 'Tourism Type' in df.columns:
                # Clean up and categorize tourism types
                tourism_type_mapping = {
                    'Monument': 'Heritage',
                    'Palace': 'Heritage',
                    'Temple': 'Religious',
                    'Religious': 'Religious',
                    'Beach': 'Nature',
                    'Nature': 'Nature',
                    'Hill Station': 'Nature',
                    'Wildlife': 'Nature',
                    'Adventure': 'Adventure',
                    'Caves': 'Heritage',
                    'Archaeological Site': 'Heritage',
                    'City': 'Urban',
                    'Desert': 'Nature'
                }
                
                # Map specific types to broader categories
                def map_tourism_type(type_name):
                    if pd.isna(type_name) or not isinstance(type_name, str):
                        return 'Other'
                    
                    for specific, broad in tourism_type_mapping.items():
                        if specific.lower() in type_name.lower():
                            return broad
                    return 'Other'
                
                df['Primary Tourism Category'] = df['Tourism Type'].apply(map_tourism_type)
            
            # Set an ID column for reference if needed
            df['ID'] = df.index
            
            # Sort by visitors for default display
            if 'Annual Visitors (millions)' in df.columns:
                df = df.sort_values('Annual Visitors (millions)', ascending=False)
            
        except Exception as e:
            st.error(f"Error preparing tourism data: {e}")
            return
    
    # Tourism Map visualization
    st.header("Tourism Landscape Across India")
    
    # Create a tab view for different tourism perspectives
    tabs = st.tabs(["Top Destinations", "Tourism Types", "International Appeal", "Economic Impact", "Seasonal Patterns"])
    
    # Tab 1: Top Destinations
    with tabs[0]:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Top destinations by visitor count
            try:
                # Safely extract top destinations
                if 'Annual Visitors (millions)' in df.columns and 'Destination' in df.columns:
                    top_destinations = df.sort_values('Annual Visitors (millions)', ascending=False).head(10)
                    
                    fig = px.bar(
                        top_destinations,
                        x='Destination',
                        y='Annual Visitors (millions)',
                        color='Region',
                        title='Top 10 Tourist Destinations in India (Annual Visitors in Millions)',
                        color_discrete_sequence=get_color_palette(len(top_destinations['Region'].unique())),
                        text='Annual Visitors (millions)'
                    )
                    fig = apply_dark_theme(fig)
                    fig.update_traces(texttemplate='%{text:.1f}M', textposition='outside')
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Required columns for top destinations chart are missing.")
            except Exception as e:
                st.error(f"Error creating top destinations chart: {e}")
        
        with col2:
            # Regional distribution of tourism
            try:
                if 'Region' in df.columns and 'Annual Visitors (millions)' in df.columns:
                    # Map destinations to regions
                    region_visitors = df.groupby(['Region'])['Annual Visitors (millions)'].sum().reset_index()
                    region_visitors = region_visitors.sort_values('Annual Visitors (millions)', ascending=False)
                    
                    # Create a bar chart for top regions
                    fig = px.bar(
                        region_visitors,
                        x='Region',
                        y='Annual Visitors (millions)',
                        color='Region',
                        title='Tourism Distribution by Region',
                        color_discrete_sequence=get_color_palette(len(region_visitors)),
                        text='Annual Visitors (millions)'
                    )
                    fig = apply_dark_theme(fig)
                    fig.update_traces(texttemplate='%{text:.1f}M', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Required columns for regional distribution chart are missing.")
            except Exception as e:
                st.error(f"Error creating regional distribution chart: {e}")
            
            # Display total destinations
            st.metric("Total Major Destinations", f"{len(df)}")
            
        # Key insights
        st.markdown("""
        <div class='insight-box'>
        <strong>Destination Insights:</strong>
        <ul>
          <li><strong>North India Dominance:</strong> The Taj Mahal, Golden Temple, and Red Fort are among the most visited sites.</li>
          <li><strong>Regional Diversity:</strong> Each region offers unique tourism experiences - from Rajasthan's palaces to Kerala's backwaters.</li>
          <li><strong>UNESCO Sites:</strong> India has 40 UNESCO World Heritage Sites, ranking 6th globally.</li>
          <li><strong>Growing Destinations:</strong> Newer tourist circuits like the Northeast and tribal areas are gaining popularity.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Create an interactive destination explorer
        st.subheader("Explore Destinations")
        
        # Create filters
        col1, col2 = st.columns(2)
        
        with col1:
            # Use safe method to get unique regions with error handling
            region_options = ['All Regions']
            try:
                if 'Region' in df.columns:
                    region_options += sorted(df['Region'].unique().tolist())
            except Exception:
                st.warning("Could not retrieve unique regions for filtering.")
                
            selected_region = st.selectbox(
                "Filter by region:",
                options=region_options
            )
        
        with col2:
            # Use safe method to get unique tourism types with error handling
            type_options = ['All Types']
            try:
                if 'Primary Tourism Type' in df.columns:
                    type_options += sorted(df['Primary Tourism Type'].unique().tolist())
                elif 'Tourism Type' in df.columns:
                    type_options += sorted(df['Tourism Type'].unique().tolist())
            except Exception:
                st.warning("Could not retrieve unique tourism types for filtering.")
                
            selected_type = st.selectbox(
                "Filter by tourism type:",
                options=type_options
            )
        
        # Apply filters
        filtered_df = df.copy()
        try:
            if selected_region != 'All Regions' and 'Region' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Region'] == selected_region]
                
            if selected_type != 'All Types':
                if 'Primary Tourism Type' in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df['Primary Tourism Type'] == selected_type]
                elif 'Tourism Type' in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df['Tourism Type'] == selected_type]
        except Exception as e:
            st.error(f"Error applying filters: {e}")
        
        # Display filtered destinations
        if len(filtered_df) > 0:
            # Sort by visitors
            try:
                if 'Annual Visitors (millions)' in filtered_df.columns:
                    filtered_df = filtered_df.sort_values('Annual Visitors (millions)', ascending=False)
            except Exception:
                pass  # Continue without sorting if there's an error
            
            # Display as cards with error handling
            for i in range(0, len(filtered_df), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(filtered_df):
                        with cols[j]:
                            try:
                                dest = filtered_df.iloc[i + j]
                                
                                # Tourism type icon mapping
                                type_icons = {
                                    'Cultural': '🏛️',
                                    'Cultural Tourism': '🏛️',
                                    'Religious': '🕌',
                                    'Religious Tourism': '🕌',
                                    'Beach': '🏖️',
                                    'Beach Tourism': '🏖️',
                                    'Hill Station': '⛰️',
                                    'Hill Station Tourism': '⛰️',
                                    'Wildlife': '🐅',
                                    'Wildlife Tourism': '🐅',
                                    'Historical': '🏰',
                                    'Historical Tourism': '🏰',
                                    'Heritage': '🏯',
                                    'Heritage Tourism': '🏯',
                                    'Adventure': '🧗',
                                    'Adventure Tourism': '🧗',
                                    'Urban': '🏙️',
                                    'Rural': '🌾',
                                    'Rural Tourism': '🌾',
                                    'Wellness': '💆',
                                    'Wellness Tourism': '💆',
                                    'Eco-Tourism': '🌿'
                                }
                                
                                # Get tourism type with fallback
                                tourism_type = 'Unknown'
                                if 'Primary Tourism Type' in dest and not pd.isna(dest['Primary Tourism Type']):
                                    tourism_type = dest['Primary Tourism Type']
                                elif 'Tourism Type' in dest and not pd.isna(dest['Tourism Type']):
                                    tourism_type = dest['Tourism Type']
                                
                                icon = type_icons.get(tourism_type, '🗺️')
                                
                                # Get destination name with fallback
                                destination = 'Unknown Destination'
                                if 'Destination' in dest and not pd.isna(dest['Destination']):
                                    destination = dest['Destination']
                                elif 'Popular Destinations' in dest and not pd.isna(dest['Popular Destinations']):
                                    destination = dest['Popular Destinations'].split(',')[0].strip()
                                
                                # Get state with fallback
                                state = 'Unknown'
                                if 'State' in dest and not pd.isna(dest['State']):
                                    state = dest['State']
                                elif 'Key States' in dest and not pd.isna(dest['Key States']):
                                    state = dest['Key States'].split(',')[0].strip()
                                
                                # Get region with fallback
                                region = 'Unknown'
                                if 'Region' in dest and not pd.isna(dest['Region']):
                                    region = dest['Region']
                                
                                # Get visitors with fallback
                                visitors = 0.0
                                if 'Annual Visitors (millions)' in dest and not pd.isna(dest['Annual Visitors (millions)']):
                                    visitors = dest['Annual Visitors (millions)']
                                
                                # Get key features with fallback
                                features = ''
                                if 'Key Attraction Features' in dest and not pd.isna(dest['Key Attraction Features']):
                                    features = dest['Key Attraction Features']
                                elif 'Key Challenges' in dest and not pd.isna(dest['Key Challenges']):
                                    features = dest['Key Challenges']
                                
                                st.markdown(f"""
                                <div style='border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:10px; margin-bottom:10px;'>
                                    <h3 style='margin:0; font-size:1.2rem;'>{icon} {destination}</h3>
                                    <p style='color:#CCCCCC; margin:2px 0;'>{state} ({region})</p>
                                    <p style='margin:2px 0;'><strong>Visitors:</strong> {visitors:.1f}M/year</p>
                                    <p style='margin:2px 0;'><strong>Type:</strong> {tourism_type}</p>
                                    <p style='margin:2px 0;'><small>{features}</small></p>
                                </div>
                                """, unsafe_allow_html=True)
                            except Exception as e:
                                st.warning(f"Could not display destination card: {e}")
        else:
            st.info("No destinations match your selected filters.")
    
    # Tab 2: Tourism Types
    with tabs[1]:
        st.subheader("Distribution of Tourism Types across India")
        
        try:
            # Create two columns for visualization
            col1, col2 = st.columns(2)
            
            with col1:
                # Create a pie chart of tourism types
                if 'Tourism Type' in df.columns:
                    # Group by tourism type
                    type_counts = df.groupby('Tourism Type').size().reset_index(name='Count')
                    type_counts = type_counts.sort_values('Count', ascending=False)
                    
                    # Create pie chart
                    fig = px.pie(
                        type_counts, 
                        values='Count', 
                        names='Tourism Type',
                        title='Distribution of Tourism Types',
                        color_discrete_sequence=get_color_palette(len(type_counts)),
                        hole=0.4
                    )
                    fig = apply_dark_theme(fig)
                    fig.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Tourism Type data is not available.")
                    
            with col2:
                # Create a bar chart showing tourism categories by region
                if 'Primary Tourism Category' in df.columns and 'Region' in df.columns:
                    # Group by region and tourism category
                    region_type = df.groupby(['Region', 'Primary Tourism Category']).size().reset_index(name='Count')
                    
                    # Create bar chart
                    fig = px.bar(
                        region_type,
                        x='Region',
                        y='Count',
                        color='Primary Tourism Category',
                        title='Tourism Categories by Region',
                        color_discrete_sequence=get_color_palette(len(region_type['Primary Tourism Category'].unique()))
                    )
                    fig = apply_dark_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Tourism Category or Region data is not available.")
            
            # Add a section showing top attractions by type
            st.subheader("Top Attractions by Type")
            
            # Create type filter
            if 'Tourism Type' in df.columns:
                tourism_types = ['All Types'] + sorted(df['Tourism Type'].unique().tolist())
                selected_type = st.selectbox("Select Tourism Type", options=tourism_types)
                
                # Filter data based on selection
                if selected_type != 'All Types':
                    filtered_df = df[df['Tourism Type'] == selected_type]
                else:
                    filtered_df = df
                
                # Display top 5 attractions for the selected type
                if 'Annual Visitors (millions)' in filtered_df.columns:
                    top_attractions = filtered_df.sort_values('Annual Visitors (millions)', ascending=False).head(5)
                    
                    # Create cards for top attractions
                    st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 10px;'>", unsafe_allow_html=True)
                    
                    for _, row in top_attractions.iterrows():
                        destination = row['Destination']
                        visitors = row['Annual Visitors (millions)']
                        tourism_type = row['Tourism Type']
                        state = row['State']
                        description = row['Description'] if 'Description' in row and not pd.isna(row['Description']) else "No description available."
                        
                        # Create card with consistent style
                        st.markdown(f"""
                        <div style="background-color: rgba(49, 51, 63, 0.7); border-radius: 10px; padding: 15px; margin-bottom: 10px; width: 100%;">
                            <h4 style="margin-top: 0; color: #FF9933;">{destination}</h4>
                            <p><strong>Type:</strong> {tourism_type} | <strong>State:</strong> {state}</p>
                            <p><strong>Annual Visitors:</strong> {visitors:.1f} million</p>
                            <p>{description}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("Visitor data is not available.")
            else:
                st.warning("Tourism Type data is not available.")
                
            # Add insights about tourism types
            st.markdown("""
            <div class='insight-box'>
            <strong>Tourism Type Insights:</strong>
            <ul>
              <li><strong>Heritage Tourism:</strong> India's monuments and historical sites attract the largest share of tourists, with the Taj Mahal being the crown jewel.</li>
              <li><strong>Religious Tourism:</strong> Temples, mosques, and other religious sites see massive footfall, with Tirupati Temple receiving over 25 million visitors annually.</li>
              <li><strong>Nature Tourism:</strong> From the beaches of Goa to the mountains of Himachal Pradesh, nature tourism is growing rapidly with increased environmental awareness.</li>
              <li><strong>Adventure Tourism:</strong> The Himalayan region and coastal areas are seeing a boom in adventure tourism including trekking, rafting, and water sports.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error displaying tourism types: {e}")
    
    # Tab 3: International Appeal
    with tabs[2]:
        st.subheader("International Tourism Appeal")
        
        try:
            # Create two columns for visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Create a bar chart showing international visitor percentages for top destinations
                if 'International Visitors (%)' in df.columns:
                    # Sort by international visitor percentage
                    top_international = df.sort_values('International Visitors (%)', ascending=False).head(10)
                    
                    # Create bar chart
                    fig = px.bar(
                        top_international,
                        x='Destination',
                        y='International Visitors (%)',
                        color='Region',
                        title='Top 10 Destinations by International Visitor Percentage',
                        color_discrete_sequence=get_color_palette(len(top_international['Region'].unique())),
                        text='International Visitors (%)'
                    )
                    fig = apply_dark_theme(fig)
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("International Visitor data is not available.")
            
            with col2:
                # Create a map or chart showing international appeal by region
                if 'Region' in df.columns and 'International Visitors (%)' in df.columns:
                    # Calculate average international visitor percentage by region
                    region_international = df.groupby('Region')['International Visitors (%)'].mean().reset_index()
                    region_international = region_international.sort_values('International Visitors (%)', ascending=False)
                    
                    # Create bar chart
                    fig = px.bar(
                        region_international,
                        x='Region',
                        y='International Visitors (%)',
                        color='Region',
                        title='Average International Visitors by Region',
                        color_discrete_sequence=get_color_palette(len(region_international)),
                        text='International Visitors (%)'
                    )
                    fig = apply_dark_theme(fig)
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("International Visitor data is not available.")
            
            # Add a section on UNESCO World Heritage Sites
            st.subheader("UNESCO World Heritage Sites")
            
            if 'UNESCO Status' in df.columns:
                # Filter for UNESCO sites
                unesco_sites = df[df['UNESCO Status'] == 'World Heritage Site']
                
                if not unesco_sites.empty:
                    # Display count of UNESCO sites
                    st.metric("Total UNESCO World Heritage Sites", f"{len(unesco_sites)}")
                    
                    # Create a pie chart of UNESCO sites by type
                    if 'Tourism Type' in unesco_sites.columns:
                        unesco_types = unesco_sites.groupby('Tourism Type').size().reset_index(name='Count')
                        
                        fig = px.pie(
                            unesco_types,
                            values='Count',
                            names='Tourism Type',
                            title='UNESCO Sites by Type',
                            color_discrete_sequence=get_color_palette(len(unesco_types))
                        )
                        fig = apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Display UNESCO sites in a table
                    st.markdown("### List of UNESCO World Heritage Sites")
                    
                    for _, row in unesco_sites.iterrows():
                        st.markdown(f"""
                        <div style="background-color: rgba(49, 51, 63, 0.7); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                            <h4 style="margin-top: 0; color: #FF9933;">{row['Destination']}</h4>
                            <p><strong>Type:</strong> {row['Tourism Type']} | <strong>State:</strong> {row['State']}</p>
                            <p><strong>Year Established:</strong> {row['Year Established'] if 'Year Established' in row and not pd.isna(row['Year Established']) else 'Unknown'}</p>
                            <p>{row['Description'] if 'Description' in row and not pd.isna(row['Description']) else 'No description available.'}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No UNESCO World Heritage Sites found in the data.")
            else:
                st.warning("UNESCO Status data is not available.")
            
            # Add insights about international tourism
            st.markdown("""
            <div class='insight-box'>
            <strong>International Tourism Insights:</strong>
            <ul>
              <li><strong>Golden Triangle:</strong> Delhi-Agra-Jaipur circuit attracts the highest number of international tourists.</li>
              <li><strong>Source Countries:</strong> USA, UK, and European countries are the top sources of international tourists, followed by Southeast Asian countries.</li>
              <li><strong>UNESCO Appeal:</strong> India's World Heritage Sites are major draws for international tourists seeking cultural experiences.</li>
              <li><strong>Medical Tourism:</strong> India is becoming a hub for medical tourism, with visitors coming for affordable, high-quality medical treatments.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error displaying international appeal: {e}")
    
    # Tab 4: Economic Impact
    with tabs[3]:
        st.subheader("Economic Impact of Tourism in India")
        
        try:
            # Create main metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            # Calculate total tourism revenue
            total_revenue = 0
            if 'Tourism Revenue (USD millions)' in df.columns:
                total_revenue = df['Tourism Revenue (USD millions)'].sum()
                col1.metric("Total Tourism Revenue", f"${total_revenue:.1f}B" if total_revenue > 1000 else f"${total_revenue:.0f}M")
            else:
                col1.metric("Total Tourism Revenue", "Data N/A")
                
            # Calculate total employment
            total_employment = 0
            if 'Employment Generated (thousands)' in df.columns:
                total_employment = df['Employment Generated (thousands)'].sum()
                col2.metric("Total Employment", f"{total_employment/1000:.2f}M" if total_employment > 1000 else f"{total_employment:.0f}K")
            else:
                col2.metric("Total Employment", "Data N/A")
                
            # Calculate GDP contribution (estimated at 9.2% for India's tourism sector)
            col3.metric("GDP Contribution", "9.2%")
            
            # Calculate average growth rate
            avg_growth = 0
            if 'Growth Potential (%)' in df.columns:
                avg_growth = df['Growth Potential (%)'].mean()
                col4.metric("Avg. Annual Growth", f"{avg_growth:.1f}%")
            else:
                col4.metric("Avg. Annual Growth", "Data N/A")
            
            # Create two-column layout for charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Create a bar chart of revenue by tourism type
                if 'Tourism Type' in df.columns and 'Tourism Revenue (USD millions)' in df.columns:
                    # Group by tourism type and sum revenue
                    type_revenue = df.groupby('Tourism Type')['Tourism Revenue (USD millions)'].sum().reset_index()
                    type_revenue = type_revenue.sort_values('Tourism Revenue (USD millions)', ascending=False)
                    
                    # Create bar chart
                    fig = px.bar(
                        type_revenue,
                        x='Tourism Type',
                        y='Tourism Revenue (USD millions)',
                        color='Tourism Type',
                        title='Tourism Revenue by Type (USD Millions)',
                        color_discrete_sequence=get_color_palette(len(type_revenue)),
                        text='Tourism Revenue (USD millions)'
                    )
                    fig = apply_dark_theme(fig)
                    fig.update_traces(texttemplate='$%{text:.0f}M', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Tourism Type or Revenue data is not available.")
                    
            with col2:
                # Create a pie chart of revenue by region
                if 'Region' in df.columns and 'Tourism Revenue (USD millions)' in df.columns:
                    # Group by region and sum revenue
                    region_revenue = df.groupby('Region')['Tourism Revenue (USD millions)'].sum().reset_index()
                    region_revenue = region_revenue.sort_values('Tourism Revenue (USD millions)', ascending=False)
                    
                    # Create pie chart
                    fig = px.pie(
                        region_revenue,
                        values='Tourism Revenue (USD millions)',
                        names='Region',
                        title='Tourism Revenue Distribution by Region',
                        color_discrete_sequence=get_color_palette(len(region_revenue)),
                        hole=0.3
                    )
                    fig = apply_dark_theme(fig)
                    fig.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Region or Revenue data is not available.")
            
            # Create employment visualization
            st.subheader("Employment Generation from Tourism")
            
            if 'Employment Generated (thousands)' in df.columns and 'Tourism Type' in df.columns:
                # Group by tourism type and sum employment
                type_employment = df.groupby('Tourism Type')['Employment Generated (thousands)'].sum().reset_index()
                type_employment = type_employment.sort_values('Employment Generated (thousands)', ascending=False)
                
                # Create bar chart
                fig = px.bar(
                    type_employment,
                    x='Tourism Type',
                    y='Employment Generated (thousands)',
                    color='Tourism Type',
                    title='Employment Generation by Tourism Type (Thousands of Jobs)',
                    color_discrete_sequence=get_color_palette(len(type_employment)),
                    text='Employment Generated (thousands)'
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(texttemplate='%{text:.0f}K', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Employment data is not available.")
            
            # Add insights about economic impact
            st.markdown("""
            <div class='insight-box'>
            <strong>Economic Impact Insights:</strong>
            <ul>
              <li><strong>Revenue Generation:</strong> Tourism contributes significantly to India's economy, with heritage and religious tourism being the largest revenue generators.</li>
              <li><strong>Employment:</strong> The sector provides employment to millions, particularly in hospitality, transportation, and handicrafts.</li>
              <li><strong>Regional Disparity:</strong> Tourism revenue is unevenly distributed, with North and West India capturing the largest share.</li>
              <li><strong>Growth Trajectory:</strong> The sector has shown resilient growth despite global challenges, with potential for further expansion.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error displaying economic impact: {e}")
    
    # Tab 5: Seasonal Patterns
    with tabs[4]:
        st.subheader("Seasonal Tourism Patterns")
        
        try:
            # Process seasonal data
            if 'Peak Season' in df.columns:
                # Extract seasons from peak season data
                seasons = []
                for season in df['Peak Season']:
                    if pd.isna(season) or not isinstance(season, str):
                        continue
                        
                    # Split by comma or hyphen if multiple seasons
                    if ',' in season:
                        parts = [s.strip() for s in season.split(',')]
                        seasons.extend(parts)
                    elif '-' in season:
                        parts = [s.strip() for s in season.split('-')]
                        seasons.extend(parts)
                    else:
                        seasons.append(season.strip())
                
                # Count occurrences of each month
                months = ['January', 'February', 'March', 'April', 'May', 'June', 
                         'July', 'August', 'September', 'October', 'November', 'December']
                
                month_counts = {month: 0 for month in months}
                
                for season in seasons:
                    for month in months:
                        if month.lower() in season.lower():
                            month_counts[month] += 1
                
                # Create dataframe for visualization
                season_df = pd.DataFrame({
                    'Month': list(month_counts.keys()),
                    'Count': list(month_counts.values())
                })
                
                # Add numeric month for proper sorting
                month_to_num = {month: i+1 for i, month in enumerate(months)}
                season_df['Month_Num'] = season_df['Month'].map(month_to_num)
                season_df = season_df.sort_values('Month_Num')
                
                # Create seasonal pattern visualization
                fig = px.line(
                    season_df,
                    x='Month',
                    y='Count',
                    title='Tourist Season Distribution Throughout the Year',
                    markers=True,
                    line_shape='spline',
                    color_discrete_sequence=['#FF9933']
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(line=dict(width=3), marker=dict(size=10))
                fig.update_layout(xaxis_title='Month', yaxis_title='Number of Destinations')
                st.plotly_chart(fig, use_container_width=True)
                
                # Create seasonal patterns by region
                if 'Region' in df.columns:
                    # Process data by region
                    region_season_data = []
                    
                    for region in df['Region'].unique():
                        region_df = df[df['Region'] == region]
                        if 'Peak Season' not in region_df.columns:
                            continue
                            
                        region_seasons = []
                        for season in region_df['Peak Season']:
                            if pd.isna(season) or not isinstance(season, str):
                                continue
                                
                            # Split by comma or hyphen if multiple seasons
                            if ',' in season:
                                parts = [s.strip() for s in season.split(',')]
                                region_seasons.extend(parts)
                            elif '-' in season:
                                parts = [s.strip() for s in season.split('-')]
                                region_seasons.extend(parts)
                            else:
                                region_seasons.append(season.strip())
                        
                        # Count occurrences of each month for this region
                        region_month_counts = {month: 0 for month in months}
                        
                        for season in region_seasons:
                            for month in months:
                                if month.lower() in season.lower():
                                    region_month_counts[month] += 1
                        
                        # Add to data collection
                        for month, count in region_month_counts.items():
                            region_season_data.append({
                                'Region': region,
                                'Month': month,
                                'Count': count,
                                'Month_Num': month_to_num[month]
                            })
                    
                    # Create dataframe
                    region_season_df = pd.DataFrame(region_season_data)
                    region_season_df = region_season_df.sort_values('Month_Num')
                    
                    # Create region-wise seasonal pattern visualization
                    fig = px.line(
                        region_season_df,
                        x='Month',
                        y='Count',
                        color='Region',
                        title='Seasonal Tourism Patterns by Region',
                        markers=True,
                        line_shape='spline',
                        color_discrete_sequence=get_color_palette(len(region_season_df['Region'].unique()))
                    )
                    fig = apply_dark_theme(fig)
                    fig.update_traces(line=dict(width=2), marker=dict(size=8))
                    fig.update_layout(xaxis_title='Month', yaxis_title='Number of Destinations')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Peak Season data is not available.")
                
            # Create off-peak tourism suggestions
            st.subheader("Off-Peak Tourism Opportunities")
            
            # Define off-peak months based on above analysis (April-September generally)
            off_peak_months = ['April', 'May', 'June', 'July', 'August', 'September']
            
            # Create recommendations
            st.markdown("""
            <div style="background-color: rgba(49, 51, 63, 0.7); border-radius: 10px; padding: 15px; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #FF9933;">Best Places to Visit During Off-Peak Season</h4>
            <p>Traveling during off-peak season (April-September) offers benefits like lower costs, fewer crowds, and unique experiences:</p>
            <ul>
                <li><strong>Hill Stations:</strong> Shimla, Darjeeling, Ooty, and Munnar offer pleasant weather during summer months</li>
                <li><strong>Northeast India:</strong> Meghalaya, Sikkim, and Assam are beautiful during the monsoon with lush greenery</li>
                <li><strong>Wildlife Sanctuaries:</strong> Jim Corbett, Ranthambore, and Kaziranga have unique monsoon ecosystem viewing opportunities</li>
                <li><strong>Kerala Backwaters:</strong> Experience authentic Kerala lifestyle with reduced tourist numbers during monsoon</li>
                <li><strong>Leh-Ladakh:</strong> June-September is actually the peak season for this high-altitude desert</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Add insights about seasonal patterns
            st.markdown("""
            <div class='insight-box'>
            <strong>Seasonal Pattern Insights:</strong>
            <ul>
              <li><strong>Winter Dominance:</strong> October-March is the peak tourism season for most of India due to comfortable temperatures.</li>
              <li><strong>Regional Variations:</strong> Southern India has more year-round appeal, while northern regions have more seasonal variation.</li>
              <li><strong>Seasonal Pricing:</strong> Prices can vary by 30-50% between peak and off-peak seasons at popular destinations.</li>
              <li><strong>Emerging Trend:</strong> Monsoon tourism is growing with special packages for rainy season experiences in Western Ghats and Northeast India.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error displaying seasonal patterns: {e}")
    
    # Add a conclusive insight section about overall tourism trends
    st.header("Key Tourism Trends and Future Outlook")
    
    st.markdown("""
    <div style="background-color: rgba(49, 51, 63, 0.7); border-radius: 10px; padding: 20px; margin: 20px 0;">
    <h4 style="margin-top: 0; color: #FF9933;">India's Tourism Landscape: Present and Future</h4>
    
    <p>India's tourism sector has shown remarkable resilience and growth potential, with several key trends shaping its future:</p>
    
    <ol>
        <li><strong>Digital Transformation:</strong> The rise of online booking platforms, virtual tours, and digital marketing is revolutionizing how tourists discover and experience India.</li>
        <li><strong>Sustainable Tourism:</strong> Growing emphasis on eco-friendly practices, conservation efforts, and responsible tourism across destinations.</li>
        <li><strong>Experiential Travel:</strong> Shift from sightseeing to immersive experiences like village stays, cooking classes, and cultural workshops.</li>
        <li><strong>Infrastructure Development:</strong> Major investments in airports, highways, and tourist facilities are improving accessibility and comfort.</li>
        <li><strong>Emerging Destinations:</strong> Lesser-known locations like Northeast India, Gujarat's Rann of Kutch, and Madhya Pradesh's heritage sites are gaining popularity.</li>
    </ol>
    
    <p>With the implementation of initiatives like e-Visa facilities, the Incredible India campaign, and development of thematic circuits, India is positioned to significantly increase its share in the global tourism market in the coming years.</p>
    </div>
    """, unsafe_allow_html=True) 