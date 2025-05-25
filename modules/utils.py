import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os
import requests
from io import BytesIO
import re
import numpy as np

# Function to style Matplotlib figures for dark theme
def style_matplotlib_for_dark(fig, ax):
    # Set figure facecolor
    fig.patch.set_facecolor('#1E2129')
    
    # Set axes facecolor
    ax.set_facecolor('#0E1117')
    
    # Set grid color
    ax.grid(True, linestyle='--', alpha=0.3, color='#CCCCCC')
    
    # Set spine colors
    for spine in ax.spines.values():
        spine.set_color('#555555')
    
    # Set title and label colors
    ax.title.set_color('#FF9933')
    ax.xaxis.label.set_color('#FAFAFA')
    ax.yaxis.label.set_color('#FAFAFA')
    
    # Set tick colors
    ax.tick_params(axis='x', colors='#FAFAFA')
    ax.tick_params(axis='y', colors='#FAFAFA')
    
    return fig, ax

# Function to apply consistent dark mode styling to Plotly charts
def apply_dark_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(30, 33, 41, 0.7)',
        paper_bgcolor='rgba(30, 33, 41, 0.0)',
        font_color='#FAFAFA',
        title_font_color='#FF9933',
        legend_title_font_color='#FAFAFA',
        legend_font_color='#FAFAFA',
        hoverlabel=dict(
            bgcolor='#1E2129',
            font_color='white',
            font_size=14
        )
    )
    # Add grid lines for better readability
    if 'xaxis' in fig.layout:
        fig.update_xaxes(
            gridcolor='rgba(255, 255, 255, 0.1)',
            zerolinecolor='rgba(255, 255, 255, 0.2)'
        )
    if 'yaxis' in fig.layout:
        fig.update_yaxes(
            gridcolor='rgba(255, 255, 255, 0.1)',
            zerolinecolor='rgba(255, 255, 255, 0.2)'
        )
    return fig

# Function to preload common datasets to avoid redundancy
@st.cache_data
def preload_data(datasets=None):
    """
    Preload and cache datasets for faster access across different chapters
    
    Args:
        datasets (list): List of dataset names to load. If None, loads all datasets.
                        Options: 'linguistic', 'religious', 'state', 'cultural', 
                                'population', 'economic', 'historical', 'festivals',
                                'tourism', 'education', 'geography'
    
    Returns:
        dict: Dictionary containing all loaded datasets
    """
    all_datasets = [
        'linguistic', 'religious', 'state', 'cultural', 'population', 
        'economic', 'historical', 'festivals', 'tourism', 'education', 'geography'
    ]
    
    # If no specific datasets are requested, load all of them
    if datasets is None:
        datasets = all_datasets
    
    # Initialize data container
    data = {}
    
    # Load requested datasets
    with st.spinner("Preloading data for faster navigation..."):
        for dataset in datasets:
            if dataset == 'linguistic':
                data['linguistic'] = load_linguistic_data()
            elif dataset == 'religious':
                data['religious'] = load_religious_data()
            elif dataset == 'state':
                data['state'] = load_state_data()
            elif dataset == 'cultural':
                data['cultural'] = load_cultural_data()
            elif dataset == 'population':
                data['population'] = load_population_data()
            elif dataset == 'economic':
                data['economic'] = load_economic_data()
            elif dataset == 'historical':
                data['historical'] = load_historical_data()
            elif dataset == 'festivals':
                data['festivals'] = load_festivals_data()
            elif dataset == 'tourism':
                data['tourism'] = load_tourism_data()
            elif dataset == 'education':
                data['education'] = load_education_data()
            elif dataset == 'geography':
                data['geography'] = load_geography_data()
    
    return data

# Function to load image from URL with caching
@st.cache_data
def load_image_from_url(url):
    try:
        with st.spinner(f"Loading image..."):
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            return img
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Function to load local SVG image as base64 data URL
@st.cache_data
def load_svg_as_base64(file_path):
    """Load an SVG file and return it as a base64 data URL for embedding in HTML"""
    try:
        full_path = os.path.join(os.getcwd(), file_path)
        if not os.path.exists(full_path):
            st.error(f"SVG file not found: {full_path}")
            return None
            
        import base64
        with open(full_path, "rb") as f:
            svg_data = f.read()
            b64 = base64.b64encode(svg_data).decode("utf-8")
            return f"data:image/svg+xml;base64,{b64}"
    except Exception as e:
        st.error(f"Error loading SVG: {e}")
        return None

# Helper function to safely read CSV files with various encodings
def safe_read_csv(file_path):
    """Safely read a CSV file with encoding fallbacks"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
        except Exception as e:
            st.error(f"Error reading file {file_path}: {str(e)}")
            return None
    
    st.error(f"Failed to read {file_path} with any encoding.")
    return None

# Improved data loading functions with better error handling
@st.cache_data
def load_linguistic_data():
    try:
        with st.spinner("Loading linguistic data..."):
            file_path = "data/languages.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist
            required_columns = ['Language', 'Speakers', 'Percentage']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in linguistic data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'Language':
                        df[col] = [f"Language {i+1}" for i in range(len(df))]
                    elif col == 'Speakers':
                        df[col] = 0
                    elif col == 'Percentage':
                        df[col] = 0.0
            
            return df
    except Exception as e:
        st.error(f"Error loading linguistic data: {e}")
        return None

@st.cache_data
def load_religious_data():
    try:
        with st.spinner("Loading religious data..."):
            file_path = "data/religions.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist
            required_columns = ['Religion', 'Percentage', 'Population']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in religious data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'Religion':
                        df[col] = [f"Religion {i+1}" for i in range(len(df))]
                    elif col == 'Percentage':
                        df[col] = 0.0
                    elif col == 'Population':
                        df[col] = 0
            
            return df
    except Exception as e:
        st.error(f"Error loading religious data: {e}")
        return None

@st.cache_data
def load_state_data():
    try:
        with st.spinner("Loading state data..."):
            file_path = "data/states.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist
            required_columns = ['State', 'Population (millions)', 'Area (sq km)', 'Literacy Rate (%)', 'Region']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in state data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'State':
                        df[col] = [f"State {i+1}" for i in range(len(df))]
                    elif col == 'Population (millions)':
                        df[col] = 0.0
                    elif col == 'Area (sq km)':
                        df[col] = 0
                    elif col == 'Literacy Rate (%)':
                        df[col] = 0.0
                    elif col == 'Region':
                        df[col] = 'Unknown'
            
            # Add HDI column if it doesn't exist (Human Development Index)
            if 'HDI' not in df.columns:
                # HDI values by state (approximations based on 2021-22 data)
                hdi_values = {
                    'Kerala': 0.782,
                    'Delhi': 0.746,
                    'Goa': 0.761,
                    'Punjab': 0.723,
                    'Tamil Nadu': 0.708,
                    'Himachal Pradesh': 0.725,
                    'Maharashtra': 0.696,
                    'Karnataka': 0.682,
                    'Telangana': 0.669,
                    'Gujarat': 0.672,
                    'Haryana': 0.708,
                    'Uttarakhand': 0.684,
                    'West Bengal': 0.641,
                    'Andhra Pradesh': 0.649,
                    'Rajasthan': 0.629,
                    'Odisha': 0.606,
                    'Assam': 0.613,
                    'Jharkhand': 0.599,
                    'Chhattisgarh': 0.613,
                    'Madhya Pradesh': 0.603,
                    'Uttar Pradesh': 0.596,
                    'Bihar': 0.574,
                    'Manipur': 0.697,
                    'Tripura': 0.658,
                    'Meghalaya': 0.636,
                    'Nagaland': 0.679,
                    'Sikkim': 0.716,
                    'Mizoram': 0.705,
                    'Arunachal Pradesh': 0.662,
                    'Jammu and Kashmir': 0.688,
                    'Chandigarh': 0.775,
                    'Puducherry': 0.738,
                    'Andaman and Nicobar Islands': 0.74,
                    'Lakshadweep': 0.712,
                    'Dadra and Nagar Haveli': 0.663,
                    'Daman and Diu': 0.681,
                    'Ladakh': 0.674
                }
                
                # Apply HDI values based on state name
                df['HDI'] = df['State'].map(lambda x: hdi_values.get(x, 0.65))  # Default to 0.65 if state not found
            
            # Add Urbanization (%) if it doesn't exist
            if 'Urbanization (%)' not in df.columns:
                # Urbanization rates by state (approximations)
                urbanization_values = {
                    'Delhi': 97.5,
                    'Chandigarh': 97.3,
                    'Puducherry': 68.3,
                    'Goa': 62.2,
                    'Mizoram': 52.1,
                    'Tamil Nadu': 48.4,
                    'Kerala': 47.7,
                    'Maharashtra': 45.2,
                    'Gujarat': 42.6,
                    'Karnataka': 38.6,
                    'Telangana': 38.9,
                    'Punjab': 37.5,
                    'Haryana': 34.8,
                    'Andhra Pradesh': 33.5,
                    'West Bengal': 31.9,
                    'Uttarakhand': 30.2,
                    'Jammu and Kashmir': 27.4,
                    'Nagaland': 28.9,
                    'Manipur': 29.2,
                    'Jharkhand': 24.1,
                    'Rajasthan': 24.9,
                    'Chhattisgarh': 23.2,
                    'Madhya Pradesh': 27.6,
                    'Odisha': 16.7,
                    'Assam': 14.1,
                    'Bihar': 11.3,
                    'Himachal Pradesh': 10.0,
                    'Sikkim': 25.1,
                    'Tripura': 26.2,
                    'Meghalaya': 20.1,
                    'Arunachal Pradesh': 22.9,
                    'Uttar Pradesh': 22.3,
                    'Andaman and Nicobar Islands': 37.7,
                    'Dadra and Nagar Haveli': 47.2,
                    'Daman and Diu': 75.2,
                    'Lakshadweep': 78.1,
                    'Ladakh': 21.4
                }
                
                # Apply urbanization values based on state name
                df['Urbanization (%)'] = df['State'].map(lambda x: urbanization_values.get(x, 35.0))  # Default to 35%
            
            # Add additional state information if it doesn't exist
            additional_columns = ['Capital', 'Official Languages', 'Major Crops', 'Key Industries', 'Famous Destinations']
            
            # Example data for capitals
            if 'Capital' not in df.columns:
                capitals = {
                    'Andhra Pradesh': 'Amaravati',
                    'Arunachal Pradesh': 'Itanagar',
                    'Assam': 'Dispur',
                    'Bihar': 'Patna',
                    'Chhattisgarh': 'Raipur',
                    'Goa': 'Panaji',
                    'Gujarat': 'Gandhinagar',
                    'Haryana': 'Chandigarh',
                    'Himachal Pradesh': 'Shimla',
                    'Jharkhand': 'Ranchi',
                    'Karnataka': 'Bengaluru',
                    'Kerala': 'Thiruvananthapuram',
                    'Madhya Pradesh': 'Bhopal',
                    'Maharashtra': 'Mumbai',
                    'Manipur': 'Imphal',
                    'Meghalaya': 'Shillong',
                    'Mizoram': 'Aizawl',
                    'Nagaland': 'Kohima',
                    'Odisha': 'Bhubaneswar',
                    'Punjab': 'Chandigarh',
                    'Rajasthan': 'Jaipur',
                    'Sikkim': 'Gangtok',
                    'Tamil Nadu': 'Chennai',
                    'Telangana': 'Hyderabad',
                    'Tripura': 'Agartala',
                    'Uttar Pradesh': 'Lucknow',
                    'Uttarakhand': 'Dehradun',
                    'West Bengal': 'Kolkata',
                    'Andaman and Nicobar Islands': 'Port Blair',
                    'Chandigarh': 'Chandigarh',
                    'Dadra and Nagar Haveli': 'Silvassa',
                    'Daman and Diu': 'Daman',
                    'Delhi': 'New Delhi',
                    'Jammu and Kashmir': 'Srinagar/Jammu',
                    'Ladakh': 'Leh',
                    'Lakshadweep': 'Kavaratti',
                    'Puducherry': 'Puducherry'
                }
                df['Capital'] = df['State'].map(lambda x: capitals.get(x, 'Unknown'))
            
            # Add languages if missing
            if 'Official Languages' not in df.columns:
                languages = {
                    'Andhra Pradesh': 'Telugu',
                    'Arunachal Pradesh': 'English',
                    'Assam': 'Assamese',
                    'Bihar': 'Hindi, Urdu',
                    'Chhattisgarh': 'Hindi',
                    'Goa': 'Konkani, Marathi',
                    'Gujarat': 'Gujarati',
                    'Haryana': 'Hindi',
                    'Himachal Pradesh': 'Hindi, Sanskrit',
                    'Jharkhand': 'Hindi',
                    'Karnataka': 'Kannada',
                    'Kerala': 'Malayalam',
                    'Madhya Pradesh': 'Hindi',
                    'Maharashtra': 'Marathi',
                    'Manipur': 'Manipuri',
                    'Meghalaya': 'English',
                    'Mizoram': 'Mizo, English',
                    'Nagaland': 'English',
                    'Odisha': 'Odia',
                    'Punjab': 'Punjabi',
                    'Rajasthan': 'Hindi',
                    'Sikkim': 'Nepali, English',
                    'Tamil Nadu': 'Tamil',
                    'Telangana': 'Telugu, Urdu',
                    'Tripura': 'Bengali, English',
                    'Uttar Pradesh': 'Hindi, Urdu',
                    'Uttarakhand': 'Hindi, Sanskrit',
                    'West Bengal': 'Bengali',
                    'Delhi': 'Hindi, English',
                    'Jammu and Kashmir': 'Urdu, Kashmiri, Dogri',
                    'Ladakh': 'Ladakhi, Hindi, English'
                }
                df['Official Languages'] = df['State'].map(lambda x: languages.get(x, 'Unknown'))
            
            # Add crops if missing
            if 'Major Crops' not in df.columns:
                crops = {
                    'Punjab': 'Wheat, Rice, Maize, Sugarcane',
                    'Haryana': 'Wheat, Rice, Sugarcane, Cotton',
                    'Uttar Pradesh': 'Wheat, Rice, Sugarcane, Pulses',
                    'Bihar': 'Rice, Wheat, Maize, Pulses',
                    'West Bengal': 'Rice, Jute, Tea, Pulses',
                    'Assam': 'Rice, Tea, Jute, Oilseeds',
                    'Gujarat': 'Cotton, Groundnut, Tobacco, Cumin',
                    'Maharashtra': 'Jowar, Cotton, Sugarcane, Pulses',
                    'Karnataka': 'Coffee, Silk, Ragi, Jowar',
                    'Tamil Nadu': 'Rice, Sugarcane, Banana, Cotton',
                    'Andhra Pradesh': 'Rice, Cotton, Sugarcane, Tobacco',
                    'Kerala': 'Coconut, Rubber, Cardamom, Pepper',
                    'Rajasthan': 'Bajra, Pulses, Oilseeds, Wheat',
                    'Madhya Pradesh': 'Soybean, Wheat, Rice, Maize'
                }
                df['Major Crops'] = df['State'].map(lambda x: crops.get(x, 'Various food and cash crops'))
            
            # Add industries if missing
            if 'Key Industries' not in df.columns:
                industries = {
                    'Maharashtra': 'Automotive, IT, Textiles, Finance',
                    'Gujarat': 'Petrochemicals, Textiles, Pharmaceuticals',
                    'Tamil Nadu': 'Automotive, Textiles, Electronics',
                    'Karnataka': 'IT, Aerospace, Biotechnology',
                    'Delhi': 'IT, Media, Tourism, Retail',
                    'Telangana': 'IT, Pharmaceuticals, Biotechnology',
                    'Haryana': 'Automotive, IT, Agriculture',
                    'Uttar Pradesh': 'Food Processing, Cement, Handicrafts',
                    'West Bengal': 'Jute, Tea, Leather, Steel',
                    'Andhra Pradesh': 'Pharmaceuticals, Food Processing, Textiles',
                    'Kerala': 'Tourism, Coir, Spices, Seafood',
                    'Goa': 'Tourism, Pharmaceuticals, Mining',
                    'Punjab': 'Textiles, Food Processing, Sports Goods'
                }
                df['Key Industries'] = df['State'].map(lambda x: industries.get(x, 'Agriculture, Services, Small-scale industries'))
            
            # Add tourist destinations if missing
            if 'Famous Destinations' not in df.columns:
                destinations = {
                    'Rajasthan': 'Jaipur, Udaipur, Jaisalmer, Jodhpur',
                    'Kerala': 'Alleppey, Munnar, Kochi, Thekkady',
                    'Goa': 'Baga Beach, Calangute, Anjuna, Old Goa',
                    'Himachal Pradesh': 'Shimla, Manali, Dharamshala, Dalhousie',
                    'Maharashtra': 'Mumbai, Ajanta & Ellora, Lonavala',
                    'Tamil Nadu': 'Chennai, Ooty, Kodaikanal, Mahabalipuram',
                    'Uttar Pradesh': 'Agra, Varanasi, Lucknow, Allahabad',
                    'Delhi': 'Red Fort, Qutub Minar, India Gate, Humayun\'s Tomb',
                    'Karnataka': 'Bangalore, Mysore, Hampi, Coorg',
                    'Uttarakhand': 'Rishikesh, Haridwar, Nainital, Mussoorie',
                    'Jammu and Kashmir': 'Srinagar, Gulmarg, Pahalgam, Leh',
                    'Ladakh': 'Leh, Pangong Lake, Nubra Valley, Zanskar'
                }
                df['Famous Destinations'] = df['State'].map(lambda x: destinations.get(x, 'Various historical and natural attractions'))
            
            return df
    except Exception as e:
        st.error(f"Error loading state data: {e}")
        return None

@st.cache_data
def load_cultural_data():
    try:
        with st.spinner("Loading cultural data..."):
            file_path = "data/cultural_heritage.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist based on actual file structure
            required_columns = ['Cultural Element', 'Count', 'Description', 'Historical Period', 'Region of Origin']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in cultural data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'Cultural Element':
                        df[col] = [f"Element {i+1}" for i in range(len(df))]
                    elif col == 'Count':
                        df[col] = 0
                    elif col == 'Description':
                        df[col] = 'No description available'
                    elif col == 'Historical Period':
                        df[col] = 'Unknown period'
                    elif col == 'Region of Origin':
                        df[col] = 'All India'
            
            # For backward compatibility, add the old expected columns if they're needed elsewhere
            if 'Heritage_Type' not in df.columns and 'Cultural Element' in df.columns:
                df['Heritage_Type'] = df['Cultural Element']
            
            if 'Name' not in df.columns:
                df['Name'] = [f"Heritage {i+1}" for i in range(len(df))]
                
            if 'State' not in df.columns and 'Associated States' in df.columns:
                df['State'] = df['Associated States']
            elif 'State' not in df.columns and 'Region of Origin' in df.columns:
                df['State'] = df['Region of Origin']
            elif 'State' not in df.columns:
                df['State'] = 'Unknown'
                
            if 'Year' not in df.columns and 'Historical Period' in df.columns:
                # Extract the earliest year from Historical Period if possible
                df['Year'] = df['Historical Period'].apply(lambda x: 
                    int(re.search(r'-?\d+', str(x)).group()) if re.search(r'-?\d+', str(x)) else 0)
            elif 'Year' not in df.columns:
                df['Year'] = 0
            
            return df
    except Exception as e:
        st.error(f"Error loading cultural data: {e}")
        return None

@st.cache_data
def load_population_data():
    try:
        with st.spinner("Loading population data..."):
            file_path = "data/population_growth.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist
            required_columns = ['Year', 'Population (millions)', 'Urban Population (%)', 'Rural Population (%)']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in population data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'Year':
                        df[col] = list(range(1950, 1950 + len(df)))
                    elif col == 'Population (millions)':
                        df[col] = 0.0
                    elif col == 'Urban Population (%)':
                        df[col] = 0.0
                    elif col == 'Rural Population (%)':
                        df[col] = 0.0
            
            # Ensure numeric types
            for col in ['Year', 'Population (millions)', 'Urban Population (%)', 'Rural Population (%)']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Filter out projections - only include years up to current year
            current_year = pd.Timestamp.now().year
            df = df[df['Year'] <= current_year]
            
            return df
    except Exception as e:
        st.error(f"Error loading population data: {e}")
        return None

@st.cache_data
def load_economic_data():
    try:
        with st.spinner("Loading economic data..."):
            file_path = "data/economic_sectors.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist
            required_columns = ['Year', 'Agriculture', 'Industry', 'Services']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in economic data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'Year':
                        df[col] = list(range(1950, 1950 + len(df)))
                    else:
                        df[col] = 0.0
            
            return df
    except Exception as e:
        st.error(f"Error loading economic data: {e}")
        return None

# Additional data loading functions with improved error handling
@st.cache_data
def load_historical_data():
    try:
        with st.spinner("Loading historical timeline data..."):
            file_path = "data/historical_timeline.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Verify required columns exist
            required_columns = ['Year', 'Era', 'Event', 'Significance']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in historical data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'Year':
                        df[col] = 0
                    elif col == 'Era':
                        df[col] = 'Unknown'
                    elif col == 'Event':
                        df[col] = 'Unknown Event'
                    elif col == 'Significance':
                        df[col] = 'Unknown significance'
            
            # Add Time Period column if it doesn't exist
            if 'Time Period' not in df.columns:
                # Function to format year to time period
                def format_time_period(year):
                    # Convert to integer
                    year = int(year)
                    
                    # If it's a BCE year (negative)
                    if year < 0:
                        # For BCE years, we need to negate and add BCE
                        return f"{abs(year)} BCE"
                    # For CE years
                    else:
                        # For years after 1 CE
                        return f"{year} CE"
                
                # Create Time Period column based on Year column
                df['Time Period'] = df['Year'].apply(format_time_period)
                
                # For specific eras, add a year range
                era_ranges = {
                    'Indus Valley Civilization': '2600-1900 BCE',
                    'Vedic Period': '1500-600 BCE',
                    'Mauryan Empire': '322-185 BCE',
                    'Post-Mauryan Period': '185 BCE-320 CE',
                    'Gupta Empire': '320-550 CE',
                    'Post-Gupta Period': '550-1206 CE',
                    'Delhi Sultanate': '1206-1526 CE',
                    'Vijayanagara Empire': '1336-1646 CE',
                    'Mughal Empire': '1526-1857 CE',
                    'Maratha Empire': '1674-1818 CE',
                    'Colonial Era': '1757-1947 CE',
                    'British Raj': '1858-1947 CE',
                    'Independence Movement': '1885-1947 CE',
                    'Republic of India': '1950-Present',
                    'Post-Independence': '1950-1991 CE',
                    'Economic Reforms': '1991-2014 CE',
                    'Modern India': '2014-Present',
                    'Ancient India': '600-320 BCE',
                    'Medieval India': '712-1757 CE',
                    'Age of Exploration': '1498-1600 CE',
                    'Independence': '1947-1950 CE'
                }
                
                # Map era ranges to specific eras where applicable
                for i, row in df.iterrows():
                    for era, time_range in era_ranges.items():
                        if era == row['Era']:  # Use exact match instead of substring
                            df.at[i, 'Time Period'] = time_range
                            break
            
            # Add Timeline Year for sorting events chronologically in visualizations
            if 'Timeline Year' not in df.columns:
                df['Timeline Year'] = df['Year']
            
            # Add Major Events column if it doesn't exist
            if 'Major Events' not in df.columns:
                # Combine Event and Significance as Major Events
                df['Major Events'] = df.apply(
                    lambda row: f"**{row['Event']}**: {row['Significance']}" if not pd.isna(row['Event']) and not pd.isna(row['Significance']) else 
                    (row['Event'] if not pd.isna(row['Event']) else 
                    (row['Significance'] if not pd.isna(row['Significance']) else "No event information available")),
                    axis=1
                )
            
            # Add Capital Cities column if it doesn't exist
            if 'Capital Cities' not in df.columns:
                capital_cities = {
                    'Indus Valley Civilization': 'Harappa, Mohenjo-daro',
                    'Vedic Period': 'Various tribal capitals',
                    'Mauryan Empire': 'Pataliputra (modern Patna)',
                    'Gupta Empire': 'Pataliputra (modern Patna)',
                    'Delhi Sultanate': 'Delhi',
                    'Vijayanagara Empire': 'Hampi',
                    'Mughal Empire': 'Agra, Delhi, Fatehpur Sikri',
                    'Maratha Empire': 'Raigad, Pune',
                    'Colonial Era': 'Calcutta, Delhi',
                    'British Raj': 'Calcutta (until 1911), Delhi',
                    'Republic of India': 'New Delhi',
                    'Post-Independence': 'New Delhi',
                    'Modern India': 'New Delhi',
                    'Ancient India': 'Various regional capitals',
                    'Medieval India': 'Various regional capitals',
                    'Post-Mauryan Period': 'Various regional capitals',
                    'Post-Gupta Period': 'Kannauj, Thanesar',
                    'Independence Movement': 'N/A (political movement)',
                    'Independence': 'New Delhi',
                    'Economic Reforms': 'New Delhi',
                    'Age of Exploration': 'European trading posts'
                }
                
                # Map capital cities to eras
                df['Capital Cities'] = df['Era'].map(lambda x: capital_cities.get(x, 'Unknown'))
            
            # Add Key Rulers/Leaders column if it doesn't exist
            if 'Key Rulers/Leaders' not in df.columns and 'Key Figures' in df.columns:
                df['Key Rulers/Leaders'] = df['Key Figures']
            elif 'Key Rulers/Leaders' not in df.columns:
                df['Key Rulers/Leaders'] = 'Various'
            
            # Add additional historical information columns
            additional_columns = {
                'Cultural Developments': {
                    'Indus Valley Civilization': 'Advanced urban planning, standardized weights and measures, sophisticated drainage systems, and possibly the development of the Indus script.',
                    'Vedic Period': 'Composition of the Vedas, development of Sanskrit, early Hindu rituals and practices, and emergence of the caste system.',
                    'Mauryan Empire': 'Buddhist art and architecture, rock-cut edicts, development of political philosophy through Arthashastra.',
                    'Gupta Empire': 'Golden Age of art, literature, and science. Sanskrit literature flourished with works of Kalidasa. Development of classical Indian music and dance forms.',
                    'Delhi Sultanate': 'Indo-Islamic fusion in art, architecture, and music. Introduction of Persian literary traditions.',
                    'Mughal Empire': 'Height of Indo-Islamic cultural synthesis. Miniature painting, Mughal architecture, Urdu poetry, and music flourished.',
                    'Colonial Era': 'Western influence on Indian culture, English education, modern literature, Bengal Renaissance.',
                    'Independence Movement': 'Revival of traditional arts as part of swadeshi movement, development of nationalist literature and music.',
                    'Republic of India': 'Constitutional framework, democratic institutions, secularism, and cultural pluralism.',
                    'Modern India': 'Digital revolution, global cultural influence through cinema and technology, fusion of traditional and modern art forms.'
                },
                'Religious Trends': {
                    'Indus Valley Civilization': 'Evidence of nature worship, ritual baths, and possibly proto-Shiva worship.',
                    'Vedic Period': 'Vedic religion with fire sacrifices, nature deities, and ritual practices that evolved into early Hinduism.',
                    'Ancient India': 'Rise of heterodox traditions like Buddhism and Jainism as reactions to Brahmanical orthodoxy.',
                    'Mauryan Empire': 'State patronage of Buddhism under Ashoka, spread of Buddhist missionaries to South and Southeast Asia.',
                    'Gupta Empire': 'Revival of Hinduism, particularly Vaishnavism and Shaivism, with continued Buddhist and Jain influence.',
                    'Medieval India': 'Introduction of Islam, development of Bhakti and Sufi movements emphasizing devotion and mysticism.',
                    'Mughal Empire': 'Syncretic religious policies under Akbar, attempts at creating Din-i-Ilahi, followed by more orthodox Islamic policies under Aurangzeb.',
                    'Colonial Era': 'Religious reform movements in Hinduism, Islam, and Sikhism; Christian missionary activities.',
                    'Independence Movement': 'Religious identities becoming intertwined with nationalist politics, ultimately leading to partition.',
                    'Republic of India': 'Constitutional secularism, religious pluralism, and legal reforms of religious practices.'
                },
                'Economic Systems': {
                    'Indus Valley Civilization': 'Trade-based economy with standardized weights and measures, agriculture, crafts, and long-distance trade with Mesopotamia.',
                    'Vedic Period': 'Pastoral and agricultural economy, barter system, and emergence of occupational specialization.',
                    'Mauryan Empire': 'Centralized economy with royal ownership of mines and forests, taxation system, and trade regulations described in Arthashastra.',
                    'Gupta Empire': 'Guild-based manufacturing, extensive trade networks, agricultural surplus, and sophisticated monetary system.',
                    'Delhi Sultanate': 'Feudal system, iqta land grants, agricultural taxation, and state monopolies on certain trades.',
                    'Mughal Empire': 'Sophisticated revenue system under Akbar (zabti), extensive international trade, and growth of urban manufacturing centers.',
                    'Colonial Era': 'Extractive colonial economy, deindustrialization, plantation agriculture, and integration into British imperial economic system.',
                    'Independence Movement': 'Emphasis on economic self-sufficiency, boycott of British goods, and promotion of indigenous industries.',
                    'Republic of India': 'Mixed economy with five-year plans, public sector dominance, agricultural reforms, and later economic liberalization.',
                    'Economic Reforms': 'Liberalization, privatization, and globalization of the Indian economy, rapid growth in services sector.',
                    'Modern India': 'Digital economy, startup ecosystem, service sector dominance, and integration into global supply chains.'
                },
                'Art & Architecture': {
                    'Indus Valley Civilization': 'Planned cities with grid layouts, advanced drainage systems, Great Bath at Mohenjo-daro, and small sculptures like the Dancing Girl.',
                    'Mauryan Empire': 'Pillars with animal capitals, especially the Sarnath Lion Capital, rock-cut architecture, and early Buddhist stupas.',
                    'Gupta Empire': 'Temple architecture, Ajanta and Ellora caves, sophisticated metal sculptures, and refined painting techniques.',
                    'Delhi Sultanate': 'Indo-Islamic architecture with arches and domes, Qutub Minar, and fortress construction.',
                    'Vijayanagara Empire': 'Temple complexes at Hampi with elaborate sculptural programs, musical pillars, and water systems.',
                    'Mughal Empire': 'Taj Mahal, Red Fort, Humayun\'s Tomb, miniature painting, intricate carpets, and jewelry craftsmanship.',
                    'Colonial Era': 'Indo-Saracenic architecture, Company School painting, and fusion of European and Indian artistic traditions.',
                    'Republic of India': 'Modernist architecture in Chandigarh by Le Corbusier, Bengal School of Art, and post-independence artistic movements.'
                },
                'Territorial Extent': {
                    'Mauryan Empire': 'At its peak under Ashoka, extended from Afghanistan to Bengal and from the Himalayas to modern Karnataka.',
                    'Gupta Empire': 'Northern India, from the Indus River to Bengal, and from the Himalayas to the Narmada River.',
                    'Delhi Sultanate': 'Varying control over Northern India, with brief expansion into the Deccan under Muhammad bin Tughlaq.',
                    'Vijayanagara Empire': 'Most of South India, particularly modern Karnataka, Andhra Pradesh, Tamil Nadu, and parts of Kerala.',
                    'Mughal Empire': 'At its height under Aurangzeb, controlled almost the entire subcontinent except the southernmost regions.',
                    'Maratha Empire': 'Central India, with influence extending from Delhi in the north to Tamil Nadu in the south.',
                    'British Raj': 'Direct rule over most of the subcontinent, with princely states as protectorates, Burma (until 1937), and parts of Southeast Asia.'
                },
                'Social Structure': {
                    'Vedic Period': 'Emergence of varna system (Brahmin, Kshatriya, Vaishya, Shudra), patriarchal family structure, and tribal organization.',
                    'Ancient India': 'Crystallization of the caste system, urban merchant classes, guilds of artisans, and monastic communities.',
                    'Gupta Empire': 'Complex caste-based society, powerful Brahmin class, guild organizations, and village self-governance.',
                    'Medieval India': 'Feudal relationships, emergence of Rajput clans, strengthening of caste boundaries, and status of women declining in upper castes.',
                    'Mughal Empire': 'Mansabdari system of nobles, religious pluralism under Akbar, complex court hierarchy, and urban merchant communities.',
                    'Colonial Era': 'Codification of caste, emergence of Western-educated elite, and new professional classes.',
                    'Republic of India': 'Constitutional protections for disadvantaged groups, affirmative action, urbanization, and changing family structures.'
                },
                'Scientific Advances': {
                    'Indus Valley Civilization': 'Advanced drainage systems, standardized weights and measures, and knowledge of astronomy for agricultural calendars.',
                    'Vedic Period': 'Early astronomical observations, mathematical concepts in Vedic rituals, and medicinal knowledge in Atharvaveda.',
                    'Gupta Empire': 'Aryabhata\'s work on astronomy and mathematics, concept of zero, decimal system, calculation of pi, and trigonometry.',
                    'Medieval India': 'Advancements in algebra, astronomy, and medicine through scholars like Brahmagupta and Bhaskara II.',
                    'Mughal Empire': 'Astronomical observatories (Jantar Mantar), metallurgy, and synthesis of Indian and Persian medical traditions.',
                    'Colonial Era': 'Introduction of Western scientific education, establishment of scientific institutions, and early Indian participation in modern science.',
                    'Republic of India': 'Development of nuclear and space programs, biotechnology, pharmaceutical industry, and information technology.'
                },
                'Technological Innovations': {
                    'Indus Valley Civilization': 'Precise standardized weights and measures, advanced metallurgy, sophisticated urban planning, and possibly docks for water transport.',
                    'Ancient India': 'Iron technology, steel production (wootz steel), shipbuilding, textile techniques, and water management systems.',
                    'Gupta Empire': 'Advanced metallurgy (Iron Pillar of Delhi), medical procedures described by Sushruta, and sophisticated textile production.',
                    'Medieval India': 'Paper manufacturing, water wheels, irrigation systems, and fortress construction techniques.',
                    'Mughal Empire': 'Advances in textile production, metalworking, gunpowder weapons, and architectural engineering.',
                    'Colonial Era': 'Railways, telegraph, modern irrigation systems, and mechanized industries.',
                    'Post-Independence': 'Green Revolution agricultural technologies, nuclear power, space program, and early computer systems.',
                    'Modern India': 'Software development, pharmaceutical manufacturing, renewable energy technologies, and digital payment systems.'
                },
                'Military Developments': {
                    'Mauryan Empire': 'Large standing army with specialized divisions for infantry, cavalry, chariots, and elephants, described in detail in Arthashastra.',
                    'Gupta Empire': 'Skilled cavalry and elephant corps, development of the composite bow, and fortress defense strategies.',
                    'Delhi Sultanate': 'Introduction of heavy cavalry tactics, siege engines, and Turkish military organization.',
                    'Mughal Empire': 'Gunpowder weapons including artillery, matchlock infantry (Banduqchi), and sophisticated cavalry tactics.',
                    'Maratha Empire': 'Guerrilla warfare techniques, swift cavalry movements, and hill fort defense systems.',
                    'Colonial Era': 'Creation of British Indian Army, modern military organization, and incorporation of Indian martial traditions.',
                    'Republic of India': 'Development of modern military with indigenous defense production, nuclear weapons, and professional armed forces.'
                },
                'Foreign Relations': {
                    'Ancient India': 'Diplomatic and trade contacts with Greek states following Alexander\'s invasion, embassy exchanges with the Roman Empire.',
                    'Mauryan Empire': 'Diplomatic relations with Hellenistic kingdoms, especially the Seleucids, embassy of Megasthenes, and Buddhist missions abroad.',
                    'Gupta Empire': 'Trade and cultural exchanges with Southeast Asia, China, and the Byzantine Empire.',
                    'Medieval India': 'Arab trade networks, diplomatic contacts with China, and influences from Central Asia.',
                    'Mughal Empire': 'Diplomatic relations with Safavid Persia, Ottoman Empire, and various European powers.',
                    'British Raj': 'India as part of the British imperial system, participation in World Wars, and colonial foreign policy.',
                    'Republic of India': 'Non-alignment policy during Cold War, leadership in Non-Aligned Movement, and later strategic partnerships.'
                },
                'Historical Legacy': {
                    'Indus Valley Civilization': 'Urban planning concepts, possible continuities in religious iconography, and early standardization systems.',
                    'Vedic Period': 'Foundational texts of Hinduism, Sanskrit language and literature, and early philosophical concepts.',
                    'Mauryan Empire': 'Concepts of imperial governance, Ashoka\'s principles of dharma and non-violence, and Buddhist heritage.',
                    'Gupta Empire': 'Classical traditions in art, literature, and science, Hindu temple architecture, and mathematical innovations.',
                    'Delhi Sultanate': 'Indo-Islamic cultural synthesis, architectural traditions, and administrative systems.',
                    'Mughal Empire': 'Architectural monuments, miniature painting tradition, Urdu language, and administrative systems adopted by later states.',
                    'Colonial Era': 'Modern educational institutions, legal system, railways and infrastructure, and English language.',
                    'Independence Movement': 'Principles of non-violent resistance, democratic aspirations, and anti-colonial ideology.',
                    'Republic of India': 'Constitutional democracy, pluralistic society, and principles of secularism and federalism.'
                }
            }
            
            # Add all additional columns
            for column, data_dict in additional_columns.items():
                if column not in df.columns:
                    df[column] = df['Era'].map(lambda x: data_dict.get(x, np.nan))
            
            # For key events not covered by the era mapping, add specific details
            for i, row in df.iterrows():
                event = row['Event'] if not pd.isna(row['Event']) else ""
                
                # Add specific Military Developments
                if "Battle of Plassey" in event and pd.isna(df.at[i, 'Military Developments']):
                    df.at[i, 'Military Developments'] = "British victory through superior artillery and infantry tactics, showcasing European military advantage over traditional Indian armies."
                
                # Add specific Cultural Developments
                if "Gandhi returns" in event and pd.isna(df.at[i, 'Cultural Developments']):
                    df.at[i, 'Cultural Developments'] = "Introduction of Gandhian principles of simplicity, self-sufficiency, and non-violence that profoundly influenced Indian cultural values."
                
                # Add specific Economic Systems info
                if "Economic liberalization" in event and pd.isna(df.at[i, 'Economic Systems']):
                    df.at[i, 'Economic Systems'] = "Dismantling of License Raj, reduction of import tariffs, opening to foreign investment, and currency devaluation to address balance of payments crisis."
            
            return df
    except Exception as e:
        st.error(f"Error loading historical data: {e}")
        return None

@st.cache_data
def load_festivals_data():
    try:
        with st.spinner("Loading festivals data..."):
            file_path = "data/festivals.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Create mappings from actual columns to expected columns
            column_mappings = {
                'Religion/Type': 'Religion',
                'Primary States': 'Region',
                'Season': 'Month'
            }
            
            # Rename columns based on mappings if they exist
            for actual_col, expected_col in column_mappings.items():
                if actual_col in df.columns and expected_col not in df.columns:
                    df[expected_col] = df[actual_col]
            
            # Verify required columns exist
            required_columns = ['Festival', 'Religion', 'Region', 'Month']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in festivals data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'Festival':
                        df[col] = [f"Festival {i+1}" for i in range(len(df))]
                    elif col == 'Religion':
                        df[col] = 'Unknown'
                    elif col == 'Region':
                        df[col] = 'All India'
                    elif col == 'Month':
                        df[col] = 'January'
            
            # Process Season to extract just the month
            if 'Season' in df.columns and 'Month' in df.columns:
                # Extract the first month from Season if it's a range (October-November)
                df['Month'] = df['Season'].str.extract(r'([A-Za-z]+)(?:-[A-Za-z]+)?')[0]
            
            # Add Environmental Impact column if it doesn't exist
            if 'Environmental Impact' not in df.columns:
                # Default environmental impact values based on festival characteristics
                environmental_impact = {
                    'Diwali': 'High - Air pollution from fireworks, increased waste from packaging, and energy consumption from lights',
                    'Holi': 'Moderate to High - Water usage and chemical colors can contaminate water bodies, though natural colors are increasingly used',
                    'Durga Puja': 'Moderate - Idol immersion impacts water bodies, though eco-friendly materials are increasingly used',
                    'Ganesh Chaturthi': 'Moderate to High - Water pollution from idol immersion, though eco-friendly clay idols are being promoted',
                    'Navratri/Dussehra': 'Moderate - Burning of effigies causes air pollution, increased waste from decorations',
                    'Onam': 'Low - Primarily uses biodegradable materials like flowers and leaves for decorations',
                    'Pongal/Makar Sankranti': 'Low to Moderate - Generally eco-friendly with some waste from kite materials in certain regions',
                    'Bihu': 'Low - Mostly uses natural and biodegradable materials',
                    'Eid al-Fitr': 'Low to Moderate - Primarily food waste and packaging waste from new items',
                    'Eid al-Adha': 'Moderate - Animal sacrifice creates biological waste, though usually well-managed',
                    'Muharram': 'Low - Limited environmental impact from processions',
                    'Christmas': 'Moderate - Tree cutting (though artificial trees are common), packaging waste from gifts',
                    'Easter': 'Low - Minimal environmental impact from celebrations',
                    'Baisakhi': 'Low - Agricultural festival with minimal environmental footprint',
                    'Guru Nanak Jayanti': 'Low - Minimal waste due to community meals using reusable plates',
                    'Buddha Purnima': 'Low - Emphasis on non-violence extends to environmental consciousness',
                    'Mahavir Jayanti': 'Low - Jain principles emphasize environmental protection',
                    'Parsi New Year (Nowruz)': 'Low - Small community with limited environmental impact',
                    'Raksha Bandhan': 'Low to Moderate - Waste from packaging of gifts and rakhis',
                    'Karva Chauth': 'Low - Minimal environmental impact',
                    'Chhath Puja': 'Moderate - Water pollution from offerings and waste near riverbanks',
                    'Gudi Padwa/Ugadi': 'Low - Uses mostly biodegradable traditional materials',
                    'Puthandu/Vishu': 'Low - Primarily uses natural materials like flowers and fruits',
                    'Teej': 'Low - Minimal environmental impact from celebrations',
                    'Hornbill Festival': 'Moderate - Increased waste and carbon footprint from tourism',
                    'Hemis Festival': 'Low - Small scale with traditional materials',
                    'Pushkar Camel Fair': 'Moderate - Large gathering creating waste and strain on local resources',
                    'Thrissur Pooram': 'Moderate - Fireworks cause noise and air pollution',
                    'Kumbh Mela': 'High - Massive gathering creating waste management challenges, water pollution, though improved management in recent years'
                }
                
                # Add environmental impact column with default "Moderate" for any festival not in the mapping
                df['Environmental Impact'] = df['Festival'].map(lambda x: environmental_impact.get(x, 'Moderate - General waste generation and energy usage common to mid-sized gatherings'))
            
            # Add Economic Impact data if it doesn't exist
            if 'Economic Impact (Millions USD)' not in df.columns and 'Economic Impact (USD millions)' not in df.columns:
                # Realistic economic impact values based on festival importance and scale
                economic_impact = {
                    'Diwali': 7200,  # Major national festival with highest economic impact
                    'Holi': 1500,    # Major festival with significant spending
                    'Durga Puja': 1200,  # Major regional festival with significant economic activity
                    'Ganesh Chaturthi': 950,  # Important regional festival with substantial economic impact
                    'Navratri/Dussehra': 1700,  # Nine-day festival with substantial economic activity
                    'Onam': 500,     # Major Kerala festival with regional economic impact
                    'Pongal/Makar Sankranti': 650,  # Important harvest festival
                    'Bihu': 320,     # Regional festival with moderate economic impact
                    'Eid al-Fitr': 920,   # Major Islamic festival with substantial spending
                    'Eid al-Adha': 750,   # Important Islamic festival with significant economic activity
                    'Muharram': 220,      # Religious observance with moderate economic impact
                    'Christmas': 780,     # Major festival with significant retail impact
                    'Easter': 180,        # Moderate economic impact in Christian regions
                    'Baisakhi': 350,      # Important Punjabi harvest festival
                    'Guru Nanak Jayanti': 290,  # Important Sikh festival
                    'Buddha Purnima': 150,      # Buddhist festival with moderate impact
                    'Mahavir Jayanti': 130,     # Jain festival with moderate economic impact
                    'Parsi New Year (Nowruz)': 80,  # Smaller community festival
                    'Raksha Bandhan': 620,      # Gift-giving festival with significant economic impact
                    'Karva Chauth': 410,        # Gift-giving observance with moderate economic impact
                    'Chhath Puja': 280,         # Regional festival with moderate economic impact
                    'Gudi Padwa/Ugadi': 380,    # New Year festival with moderate economic impact
                    'Puthandu/Vishu': 270,      # Regional New Year with moderate economic impact
                    'Teej': 230,                # Regional festival with moderate economic impact
                    'Hornbill Festival': 170,   # Tourism-focused festival with growing impact
                    'Hemis Festival': 90,       # Smaller regional festival
                    'Pushkar Camel Fair': 310,  # Tourism-focused festival with significant impact
                    'Thrissur Pooram': 250,     # Regional festival with moderate economic impact
                    'Kumbh Mela': 2200          # Massive gathering with substantial economic impact
                }
                
                # Add economic impact column with reasonable default value for any festival not in the mapping
                df['Economic Impact (Millions USD)'] = df['Festival'].map(lambda x: economic_impact.get(x, 250))
            
            # Add Participants data if it doesn't exist
            if 'Participants (millions)' not in df.columns:
                # Realistic participant numbers based on festival scale
                participants = {
                    'Diwali': 800,        # Nationwide celebration
                    'Holi': 400,          # Widespread celebration
                    'Durga Puja': 120,    # Major regional celebration
                    'Ganesh Chaturthi': 100,  # Major regional celebration
                    'Navratri/Dussehra': 350,  # Widespread celebration
                    'Onam': 35,           # Kerala-focused celebration
                    'Pongal/Makar Sankranti': 200,  # Widespread harvest festival
                    'Bihu': 25,           # Assam-focused celebration
                    'Eid al-Fitr': 180,   # Major Islamic celebration
                    'Eid al-Adha': 170,   # Major Islamic celebration
                    'Muharram': 80,       # Moderate participation
                    'Christmas': 60,      # Christian and secular participation
                    'Easter': 30,         # Primarily Christian participation
                    'Baisakhi': 45,       # Punjabi harvest festival
                    'Guru Nanak Jayanti': 40,  # Sikh celebration
                    'Buddha Purnima': 20,      # Buddhist celebration
                    'Mahavir Jayanti': 15,     # Jain celebration
                    'Parsi New Year (Nowruz)': 0.5,  # Small community celebration
                    'Raksha Bandhan': 250,     # Widespread celebration
                    'Karva Chauth': 120,       # North India-focused
                    'Chhath Puja': 70,         # Bihar and eastern UP focused
                    'Gudi Padwa/Ugadi': 80,    # Regional celebration
                    'Puthandu/Vishu': 40,      # Tamil Nadu/Kerala focused
                    'Teej': 60,                # Regional celebration
                    'Hornbill Festival': 0.8,  # Smaller tourism-focused festival
                    'Hemis Festival': 0.5,     # Smaller regional festival
                    'Pushkar Camel Fair': 2,   # Tourism-focused festival
                    'Thrissur Pooram': 3,      # Regional festival
                    'Kumbh Mela': 220          # Massive religious gathering
                }
                
                # Add participants column with reasonable default value for any festival not in the mapping
                df['Participants (millions)'] = df['Festival'].map(lambda x: participants.get(x, 30))
            
            # Add Tourist Attraction Level if it doesn't exist
            if 'Tourist Attraction Level' not in df.columns:
                # Tourist attraction levels (1-10 scale)
                tourist_levels = {
                    'Diwali': 9,           # Major tourist attraction
                    'Holi': 10,            # Extremely popular with foreign tourists
                    'Durga Puja': 8,       # Major regional attraction
                    'Ganesh Chaturthi': 8, # Major regional attraction
                    'Navratri/Dussehra': 7, # Significant tourist attraction
                    'Onam': 7,             # Regional attraction
                    'Pongal/Makar Sankranti': 6, # Moderate tourist attraction
                    'Bihu': 5,             # Growing tourist interest
                    'Eid al-Fitr': 5,      # Moderate tourist interest
                    'Eid al-Adha': 4,      # Some tourist interest
                    'Muharram': 3,         # Limited tourist attraction
                    'Christmas': 6,        # Moderate tourist attraction (Goa, etc.)
                    'Easter': 4,           # Limited tourist attraction
                    'Baisakhi': 6,         # Moderate tourist attraction
                    'Guru Nanak Jayanti': 5, # Some tourist interest
                    'Buddha Purnima': 6,   # Buddhist tourist interest
                    'Mahavir Jayanti': 3,  # Limited tourist attraction
                    'Parsi New Year (Nowruz)': 2, # Minimal tourist attraction
                    'Raksha Bandhan': 4,   # Limited tourist attraction
                    'Karva Chauth': 3,     # Minimal tourist attraction
                    'Chhath Puja': 4,      # Some tourist interest
                    'Gudi Padwa/Ugadi': 4, # Some tourist interest
                    'Puthandu/Vishu': 4,   # Some tourist interest
                    'Teej': 5,             # Growing tourist interest
                    'Hornbill Festival': 9, # Major tourism focus
                    'Hemis Festival': 8,   # Major Ladakh attraction
                    'Pushkar Camel Fair': 10, # Major international tourist attraction
                    'Thrissur Pooram': 9,  # Major Kerala attraction
                    'Kumbh Mela': 10       # Major international attraction
                }
                
                # Add tourist attraction level with reasonable default value for any festival not in the mapping
                df['Tourist Attraction Level'] = df['Festival'].map(lambda x: tourist_levels.get(x, 5))
            
            # Add Global Celebrations data if it doesn't exist
            if 'Global Celebrations' not in df.columns:
                # Global reach data - number of countries with significant celebrations
                global_celebrations = {
                    'Diwali': 'Celebrated in 30+ countries across North America, Europe, Asia, Africa, and Australia',
                    'Holi': 'Celebrated in 40+ countries, with growing popularity as "color festivals" globally',
                    'Durga Puja': 'Celebrated in 15+ countries with significant Bengali diaspora communities',
                    'Ganesh Chaturthi': 'Celebrated in 12+ countries with significant Maharashtrian communities',
                    'Navratri/Dussehra': 'Celebrated in 20+ countries with significant Indian diaspora',
                    'Onam': 'Celebrated in 8+ countries with Malayali diaspora communities',
                    'Pongal/Makar Sankranti': 'Celebrated in 10+ countries with Tamil and Indian diaspora',
                    'Bihu': 'Celebrated in 5+ countries with Assamese communities',
                    'Eid al-Fitr': 'Celebrated in 25+ countries with Indian Muslim communities',
                    'Eid al-Adha': 'Celebrated in 22+ countries with Indian Muslim communities',
                    'Muharram': 'Observed in 15+ countries with Shia Muslim communities',
                    'Christmas': 'Celebrated in 30+ countries with Indian Christian communities',
                    'Easter': 'Celebrated in 20+ countries with Indian Christian communities',
                    'Baisakhi': 'Celebrated in 18+ countries with significant Sikh diaspora',
                    'Guru Nanak Jayanti': 'Celebrated in 15+ countries with Sikh communities',
                    'Buddha Purnima': 'Celebrated in 10+ countries with Buddhist connections',
                    'Mahavir Jayanti': 'Celebrated in 7+ countries with Jain diaspora',
                    'Parsi New Year (Nowruz)': 'Celebrated in 5+ countries with Parsi communities',
                    'Raksha Bandhan': 'Celebrated in 14+ countries with Indian diaspora',
                    'Karva Chauth': 'Celebrated in 8+ countries with North Indian diaspora',
                    'Chhath Puja': 'Celebrated in 6+ countries with Bihari diaspora',
                    'Gudi Padwa/Ugadi': 'Celebrated in 7+ countries with South Indian diaspora',
                    'Puthandu/Vishu': 'Celebrated in 6+ countries with Tamil and Malayalam diaspora',
                    'Teej': 'Celebrated in 5+ countries with North Indian communities',
                    'Hornbill Festival': 'Recognized in 3+ countries through cultural exchanges',
                    'Hemis Festival': 'Recognized in 4+ countries with Tibetan Buddhist communities',
                    'Pushkar Camel Fair': 'Attracts tourists from 25+ countries annually',
                    'Thrissur Pooram': 'Recognized in 5+ countries through cultural showcases',
                    'Kumbh Mela': 'Attracts pilgrims and tourists from 20+ countries'
                }
                
                # Add global celebrations data with a reasonable default value for any festival not in the mapping
                df['Global Celebrations'] = df['Festival'].map(lambda x: global_celebrations.get(x, 'Celebrated in 3+ countries with Indian diaspora communities'))
            
            return df
    except Exception as e:
        st.error(f"Error loading festivals data: {e}")
        return None

@st.cache_data
def load_tourism_data():
    try:
        with st.spinner("Loading tourism data..."):
            file_path = "data/tourism.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Create mappings from actual columns to expected columns
            column_mappings = {
                'Destination': 'Popular Destinations',
                'State': 'Key States',
                'Type': 'Tourism Type',
                'Visitors_Annual': 'Annual Visitors (millions)'
            }
            
            # Create expected columns from actual columns if they exist
            for expected_col, actual_col in column_mappings.items():
                if actual_col in df.columns and expected_col not in df.columns:
                    if expected_col == 'Destination':
                        # Create a list to store the destinations
                        destinations = []
                        for i, val in enumerate(df[actual_col]):
                            if isinstance(val, str):
                                # Extract first destination from comma-separated list
                                destinations.append(val.split(',')[0].strip())
                            else:
                                # Use default name if value is not a string
                                destinations.append(f"Destination {i+1}")
                        df[expected_col] = destinations
                    elif expected_col == 'State':
                        # Create a list to store the states
                        states = []
                        for val in df[actual_col]:
                            if isinstance(val, str):
                                # Extract first state from comma-separated list
                                states.append(val.split(',')[0].strip())
                            else:
                                # Use default value if not a string
                                states.append('Unknown')
                        df[expected_col] = states
                    else:
                        # Direct mapping for other columns
                        df[expected_col] = df[actual_col]
            
            # Verify required columns exist
            required_columns = ['Destination', 'State', 'Type', 'Visitors_Annual']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in tourism data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'Destination':
                        df[col] = [f"Destination {i+1}" for i in range(len(df))]
                    elif col == 'State':
                        df[col] = 'Unknown'
                    elif col == 'Type':
                        df[col] = 'Monument'
                    elif col == 'Visitors_Annual':
                        df[col] = 0
            
            return df
    except Exception as e:
        st.error(f"Error loading tourism data: {e}")
        return None

@st.cache_data
def load_education_data():
    try:
        with st.spinner("Loading education data..."):
            file_path = "data/education.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # Define expected columns and their fallback values
            expected_columns = {
                # Overall metrics
                'National Literacy Rate (%)': 78.7,
                'Primary Enrollment Rate (%)': 94.2,
                'Number of Universities': 1047,
                'Higher Education Enrollment (millions)': 38.5,
                
                # State data
                'State Names': 'Kerala, Delhi, Tamil Nadu, Himachal Pradesh, Maharashtra',
                'State Literacy Rates (%)': '96.2, 93.2, 90.4, 89.5, 88.9',
                'State Primary Enrollment (%)': '98.5, 97.2, 97.0, 96.3, 96.0',
                'State Secondary Enrollment (%)': '90.9, 88.7, 85.9, 91.5, 87.2',
                'State Higher Ed Enrollment (%)': '36.9, 36.0, 49.0, 30.8, 32.2',
                
                # Historical data
                'Literacy Rate Years': '1951, 1961, 1971, 1981, 1991, 2001, 2011, 2021',
                'Literacy Rate History': '18.3, 28.3, 34.5, 43.6, 52.2, 64.8, 74.0, 78.7',
                
                # Infrastructure data
                'Number of Primary Schools': '848,712',
                'Number of Secondary Schools': '271,385',
                'Number of Colleges': '42,343',
                'Number of Universities': '1,047',
                'Number of Technical Institutions': '10,827',
                
                # Regional data
                'Regional Names': 'North, South, East, West, Central, Northeast',
                'Regional Primary Schools': '196,000, 187,000, 142,000, 164,000, 91,000, 68,712',
                'Regional Secondary Schools': '62,500, 71,350, 47,000, 53,535, 23,000, 14,000',
                'Regional Colleges': '10,650, 13,960, 5,500, 8,233, 2,500, 1,500',
                'Regional Population (millions)': '365, 252, 230, 213, 115, 46',
                
                # Teacher-student ratios
                'Teacher-Student Ratio Primary': '1:26',
                'Teacher-Student Ratio Secondary': '1:22',
                'Teacher-Student Ratio Higher Ed': '1:24',
                
                # Quality metrics
                'PISA Reading Score': '415',
                'PISA Math Score': '428',
                'PISA Science Score': '419',
                'Global Innovation Index': '37.2/100',
                'Higher Education Quality Rank': '16/50',
                
                # PISA comparisons
                'PISA Comparison Countries': 'India, China, UK, USA, Brazil',
                'PISA Comparison Reading': '415, 555, 504, 505, 413',
                'PISA Comparison Math': '428, 591, 502, 478, 384',
                'PISA Comparison Science': '419, 590, 505, 502, 404',
                
                # University rankings
                'Top Universities': 'IIT Bombay, IISc Bangalore, IIT Delhi, IIT Madras, IIT Kanpur',
                'University World Ranks': '177, 185, 193, 255, 264',
                
                # Gender parity
                'Gender Parity Primary': '1.03',
                'Gender Parity Secondary': '1.01',
                'Gender Parity Higher Ed': '1.05',
                'State Female Literacy (%)': '92.0, 89.6, 86.4, 83.7, 83.1',
                'State Male Literacy (%)': '97.4, 95.7, 93.1, 93.6, 92.9'
            }
            
            # Check for missing columns and add them with default values
            for col, default_value in expected_columns.items():
                if col not in df.columns:
                    df[col] = default_value
            
            # Verify required columns exist (legacy check)
            required_columns = ['State', 'Literacy_Rate', 'Primary_Enrollment', 'Higher_Education_GER']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.warning(f"Missing columns in education data: {', '.join(missing_columns)}")
                
                # Add missing columns with default values if needed
                for col in missing_columns:
                    if col == 'State':
                        df[col] = [f"State {i+1}" for i in range(len(df))]
                    else:
                        df[col] = 0.0
            
            return df
    except Exception as e:
        st.error(f"Error loading education data: {e}")
        # Create a minimal dataframe with expected columns
        return pd.DataFrame({col: [val] for col, val in expected_columns.items()})

@st.cache_data
def load_geography_data():
    try:
        with st.spinner("Loading geography data..."):
            file_path = "data/geography.csv"
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return None
            
            df = safe_read_csv(file_path)
            
            # If terrain data is missing, create a sample dataset
            if 'Terrain_Type' not in df.columns or 'Percentage' not in df.columns:
                st.warning("Missing terrain columns in geography data. Using sample data.")
                
                # Create sample terrain data
                terrain_data = {
                    'Terrain_Type': ['Mountains', 'Plains', 'Plateaus', 'Deserts', 'Coastlines', 'Forests'],
                    'Percentage': [15.3, 43.2, 27.8, 7.9, 3.5, 2.3],
                    'Area_sq_km': [502000, 1419000, 914000, 260000, 115000, 77000]
                }
                df = pd.DataFrame(terrain_data)
            
            return df
    except Exception as e:
        st.error(f"Error loading geography data: {e}")
        # Create a minimal dataframe with sample data as fallback
        terrain_data = {
            'Terrain_Type': ['Mountains', 'Plains', 'Plateaus', 'Deserts', 'Coastlines', 'Forests'],
            'Percentage': [15.3, 43.2, 27.8, 7.9, 3.5, 2.3],
            'Area_sq_km': [502000, 1419000, 914000, 260000, 115000, 77000]
        }
        return pd.DataFrame(terrain_data)

# Helper function to get a color palette
def get_color_palette(n, palette_type="qualitative"):
    """Generate a color palette with n colors"""
    if palette_type == "qualitative":
        if n <= 10:
            return px.colors.qualitative.Plotly[:n]
        else:
            return px.colors.qualitative.Alphabet[:n]
    elif palette_type == "sequential":
        return px.colors.sequential.Plasma[:n]
    else:
        return px.colors.sequential.Viridis[:n] 