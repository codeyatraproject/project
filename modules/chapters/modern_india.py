import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.utils import apply_dark_theme, load_economic_data, load_population_data, get_color_palette

def render():
    """
    Renders the Modern India chapter content with comprehensive data visualizations
    """
    st.title("🌆 Modern India")
    
    st.markdown("""
    <div class='story-text'>
    Modern India represents a fascinating blend of ancient traditions and contemporary 
    development, emerging as a significant global player in various fields. From rapid 
    economic growth to technological advancements, India's journey since independence 
    has been remarkable and continues to evolve in the 21st century.
    </div>
    """, unsafe_allow_html=True)
    
    # Load economic and population data
    with st.spinner("Analyzing modern India data..."):
        try:
            economic_data = load_economic_data()
            population_data = load_population_data()
            
            if economic_data is None or economic_data.empty:
                st.warning("Economic data could not be loaded.")
                economic_data = pd.DataFrame()
                
            if population_data is None or population_data.empty:
                st.warning("Population data could not be loaded.")
                population_data = pd.DataFrame()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            economic_data = pd.DataFrame()
            population_data = pd.DataFrame()
    
    # Create a tab view for different aspects of Modern India
    tabs = st.tabs(["Economic Transformation", "Demographic Trends", "Digital Revolution", "Global Position", "Future Outlook"])
    
    # Tab 1: Economic Transformation
    with tabs[0]:
        st.header("Economic Transformation")
        
        try:
            if not economic_data.empty and 'Year' in economic_data.columns:
                # Add overview
                st.markdown("""
                <div class='story-text'>
                Since the liberalization reforms of 1991, India has transformed from a closed, 
                socialist economy to one of the world's fastest-growing major economies. 
                The reforms opened up the economy to foreign investment and reduced government 
                controls on private enterprise, leading to significant changes in India's economic landscape.
                </div>
                """, unsafe_allow_html=True)
                
                # Create columns for visualizations
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    # GDP Growth Trend
                    fig = px.line(
                        economic_data,
                        x='Year',
                        y='GDP (billion USD)',
                        title='India\'s GDP Growth (1951-2023)',
                        markers=True,
                        color_discrete_sequence=['#FF9933'],
                    )
                    fig.update_layout(
                        xaxis_title="Year",
                        yaxis_title="GDP (Billion USD)",
                        hovermode="x unified"
                    )
                    fig = apply_dark_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # GDP Growth Rate
                    recent_data = economic_data[economic_data['Year'] >= 2000].copy()
                    fig = px.bar(
                        recent_data,
                        x='Year',
                        y='GDP Growth Rate (%)',
                        title='Annual GDP Growth Rate (2000-2023)',
                        color='GDP Growth Rate (%)',
                        color_continuous_scale='RdYlGn',
                        text='GDP Growth Rate (%)'
                    )
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                    fig = apply_dark_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Sectoral Composition
                st.subheader("Evolution of Economic Sectors")
                
                # Prepare data for sectors visualization
                sectors_data = economic_data.melt(
                    id_vars=['Year'],
                    value_vars=['Agriculture', 'Industry', 'Services'],
                    var_name='Sector',
                    value_name='Percentage'
                )
                
                # Filter for specific years to show the evolution
                milestone_years = [1951, 1971, 1991, 2001, 2011, 2023]
                # Make sure we only use milestone years that actually exist in the data
                available_years = economic_data['Year'].unique()
                valid_milestone_years = [year for year in milestone_years if year in available_years]
                
                milestone_data = sectors_data[sectors_data['Year'].isin(valid_milestone_years)]
                
                # Create the sectoral evolution chart
                fig = px.bar(
                    milestone_data,
                    x='Year',
                    y='Percentage',
                    color='Sector',
                    title='Sectoral Composition of Indian Economy (1951-2023)',
                    barmode='stack',
                    color_discrete_map={
                        'Agriculture': '#7CB342',
                        'Industry': '#5C6BC0',
                        'Services': '#FF9933'
                    },
                    text='Percentage'
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
                fig = apply_dark_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
                
                # Per Capita Income Growth
                st.subheader("Per Capita Income Growth")
                
                fig = px.line(
                    economic_data,
                    x='Year',
                    y='Per Capita Income (USD)',
                    title='Per Capita Income Growth (1951-2023)',
                    markers=True,
                    color_discrete_sequence=['#4CAF50'],
                )
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="Per Capita Income (USD)",
                    hovermode="x unified"
                )
                fig = apply_dark_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
                
                # Key economic insights
                st.markdown("""
                <div class='insight-box'>
                <strong>Economic Transformation Insights:</strong>
                <ul>
                  <li><strong>Sectoral Shift:</strong> India's economy has transitioned from agriculture-dominated to services-led, with the services sector now contributing over 55% of GDP.</li>
                  <li><strong>Growth Resilience:</strong> Despite global economic challenges, India has maintained robust growth rates, becoming the 5th largest economy globally by 2023.</li>
                  <li><strong>Income Growth:</strong> Per capita income has increased substantially, particularly since liberalization, though income inequality remains a challenge.</li>
                  <li><strong>COVID Impact:</strong> The pandemic caused India's only GDP contraction in recent decades (-6.6% in 2020), followed by a strong recovery.</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Economic data is not available for visualization.")
                
                # Provide some static content as fallback
                st.markdown("""
                ### Economic Milestones
                
                - **1991:** Economic liberalization - removing industrial licensing, reducing import tariffs
                - **2000s:** Emergence as an IT powerhouse and outsourcing destination
                - **2016:** Implementation of Goods and Services Tax (GST) to unify India's market
                - **2020-21:** Economic recovery package of ₹20 lakh crore ($266 billion) to combat COVID-19 impact
                - **2023:** Becomes 5th largest economy globally, surpassing the United Kingdom
                """)
        except Exception as e:
            st.error(f"Error displaying economic data: {e}")
    
    # Tab 2: Demographic Trends
    with tabs[1]:
        st.header("Demographic Trends")
        
        try:
            if not population_data.empty and 'Year' in population_data.columns:
                # Add overview
                st.markdown("""
                <div class='story-text'>
                India is home to over 1.4 billion people, making it the most populous country in the world. 
                The demographic landscape has evolved significantly since independence, with changing growth rates, 
                urbanization patterns, and age distributions that present both opportunities and challenges.
                </div>
                """, unsafe_allow_html=True)
                
                # Create columns for visualizations
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    # Population Growth Trend
                    fig = px.line(
                        population_data,
                        x='Year',
                        y='Population (millions)',
                        title='India\'s Population Growth (1951-2023)',
                        markers=True,
                        color_discrete_sequence=['#FF9933'],
                    )
                    fig.update_layout(
                        xaxis_title="Year",
                        yaxis_title="Population (Millions)",
                        hovermode="x unified"
                    )
                    fig = apply_dark_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Population Growth Rate
                    fig = px.line(
                        population_data,
                        x='Year',
                        y='Growth Rate (%)',
                        title='Population Growth Rate (1951-2023)',
                        markers=True,
                        color_discrete_sequence=['#5C6BC0'],
                    )
                    fig.update_layout(
                        xaxis_title="Year",
                        yaxis_title="Annual Growth Rate (%)",
                        hovermode="x unified"
                    )
                    fig = apply_dark_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Urbanization Trend
                st.subheader("Urbanization Trend")
                
                # Prepare data for urban-rural visualization
                urban_rural_data = population_data.melt(
                    id_vars=['Year'],
                    value_vars=['Urban Population (%)', 'Rural Population (%)'],
                    var_name='Type',
                    value_name='Percentage'
                )
                
                # Create a more visually appealing representation
                urban_rural_data['Type'] = urban_rural_data['Type'].apply(lambda x: 'Urban' if 'Urban' in x else 'Rural')
                
                # Filter for specific milestone years
                milestone_years = [1951, 1971, 1991, 2001, 2011, 2023]
                # Make sure we only use milestone years that actually exist in the data
                available_years = population_data['Year'].unique()
                valid_milestone_years = [year for year in milestone_years if year in available_years]
                
                milestone_urban_rural = urban_rural_data[urban_rural_data['Year'].isin(valid_milestone_years)]
                
                # Create the urban-rural evolution chart
                fig = px.bar(
                    milestone_urban_rural,
                    x='Year',
                    y='Percentage',
                    color='Type',
                    title='Urban-Rural Population Distribution (1951-2023)',
                    barmode='stack',
                    color_discrete_map={
                        'Urban': '#5C6BC0',
                        'Rural': '#7CB342'
                    },
                    text='Percentage'
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
                fig = apply_dark_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
                
                # Gender Distribution
                st.subheader("Gender Distribution")
                
                # Prepare data for gender distribution visualization
                gender_data = population_data.melt(
                    id_vars=['Year'],
                    value_vars=['Male Population (%)', 'Female Population (%)'],
                    var_name='Gender',
                    value_name='Percentage'
                )
                
                # Clean up labels
                gender_data['Gender'] = gender_data['Gender'].apply(lambda x: 'Male' if 'Male' in x else 'Female')
                
                # Create the gender distribution chart
                fig = px.line(
                    gender_data,
                    x='Year',
                    y='Percentage',
                    color='Gender',
                    title='Gender Distribution in India (1951-2023)',
                    color_discrete_map={
                        'Male': '#3F51B5',
                        'Female': '#E91E63'
                    },
                    markers=True
                )
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="Percentage (%)",
                    hovermode="x unified"
                )
                fig = apply_dark_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
                
                # Key demographic insights
                st.markdown("""
                <div class='insight-box'>
                <strong>Demographic Trend Insights:</strong>
                <ul>
                  <li><strong>Demographic Dividend:</strong> India has one of the world's youngest populations, with a median age of about 29 years, creating a potential demographic dividend.</li>
                  <li><strong>Declining Growth Rate:</strong> Population growth rate has declined from 2.2% in 1971 to below 1% in recent years, indicating demographic transition.</li>
                  <li><strong>Urbanization:</strong> Urban population has grown from 17.3% in 1951 to over 36% in 2023, transforming India's social and economic landscape.</li>
                  <li><strong>Gender Balance:</strong> The gender ratio has shown marginal improvement in recent years, though still favors males at approximately 51.1% male to 48.9% female.</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.warning("Population data is not available for visualization.")
                
                # Provide some static content as fallback
                st.markdown("""
                ### Demographic Highlights
                
                - **Population Growth:** India became the world's most populous country in 2023, surpassing China
                - **Demographic Dividend:** Over 65% of the population is under 35 years old
                - **Urbanization:** Seven cities with populations over 5 million, with 40% projected urban population by 2030
                - **Regional Variations:** Southern states have reached replacement-level fertility, while northern states still have higher growth rates
                - **Gender Ratio:** 943 females per 1000 males, with gradual improvement over decades
                """)
        except Exception as e:
            st.error(f"Error displaying demographic data: {e}")
    
    # Tab 3: Digital Revolution
    with tabs[2]:
        st.header("Digital Revolution")
        
        # Add overview
        st.markdown("""
        <div class='story-text'>
        The digital revolution has transformed everyday life in India. With over 800 million 
        internet users, India has the second-largest internet user base globally. Digital 
        initiatives like UPI payments, Aadhaar identity system, and e-governance have changed 
        how Indians interact with services, businesses, and each other.
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for content
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Digital India Initiatives visualization
            st.subheader("Digital India Initiatives")
            
            # Create a visual representation of key digital initiatives
            digital_initiatives = {
                'UPI Payments': 8700,  # Monthly transactions in millions
                'Aadhaar': 1300,      # Users in millions
                'Direct Benefit Transfer': 450,  # Amount in billion USD
                'DigiLocker': 180,    # Users in millions
                'CoWIN': 1020,        # Vaccinations in millions
                'Digital Village': 2.5 # Villages in hundred thousands
            }
            
            initiatives_df = pd.DataFrame({
                'Initiative': list(digital_initiatives.keys()),
                'Value': list(digital_initiatives.values())
            })
            
            fig = px.bar(
                initiatives_df,
                y='Initiative',
                x='Value',
                orientation='h',
                title='Impact of Key Digital Initiatives',
                color='Value',
                color_continuous_scale='Viridis',
                text='Value'
            )
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(xaxis_title="Scale of Impact (varies by initiative)")
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Internet and Mobile Penetration
            st.subheader("Internet & Mobile Growth")
            
            # Create sample data for visualization
            years = list(range(2010, 2024))
            internet_users = [100, 125, 160, 190, 240, 330, 420, 490, 560, 630, 695, 750, 790, 830]
            smartphone_users = [20, 40, 70, 120, 170, 240, 300, 350, 400, 480, 520, 590, 660, 700]
            
            digital_growth = pd.DataFrame({
                'Year': years,
                'Internet Users': internet_users,
                'Smartphone Users': smartphone_users
            })
            
            fig = px.line(
                digital_growth,
                x='Year',
                y=['Internet Users', 'Smartphone Users'],
                title='Digital Adoption (in millions)',
                markers=True,
                color_discrete_map={
                    'Internet Users': '#FF9933',
                    'Smartphone Users': '#4CAF50'
                }
            )
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Users (Millions)",
                hovermode="x unified",
                legend_title=None
            )
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        # Digital Startups and Innovation
        st.subheader("Digital Startups and Innovation")
        
        # Create columns for startup ecosystem
        col3, col4 = st.columns(2)
        
        with col3:
            # Startup funding chart
            startup_years = list(range(2015, 2024))
            funding_amounts = [7.9, 4.2, 13.5, 37.2, 14.5, 11.5, 42.0, 25.0, 16.0]
            deals = [936, 953, 1000, 1266, 1185, 1153, 1583, 1247, 1050]
            
            startup_funding = pd.DataFrame({
                'Year': startup_years,
                'Funding (USD Billion)': funding_amounts
            })
            
            fig = px.bar(
                startup_funding,
                x='Year',
                y='Funding (USD Billion)',
                title='Startup Funding in India',
                color='Funding (USD Billion)',
                color_continuous_scale='Viridis',
                text='Funding (USD Billion)'
            )
            fig.update_traces(texttemplate='$%{text:.1f}B', textposition='outside')
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            # Unicorn growth chart
            unicorn_years = list(range(2015, 2024))
            unicorn_count = [1, 3, 5, 8, 10, 15, 44, 108, 111]
            
            unicorn_data = pd.DataFrame({
                'Year': unicorn_years,
                'Number of Unicorns': unicorn_count
            })
            
            fig = px.line(
                unicorn_data,
                x='Year',
                y='Number of Unicorns',
                title='Growth of Unicorn Startups in India',
                markers=True,
                color_discrete_sequence=['#FF9933']
            )
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Cumulative Unicorns",
                hovermode="x unified"
            )
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        # Digital revolution insights
        st.markdown("""
        <div class='insight-box'>
        <strong>Digital Revolution Insights:</strong>
        <ul>
          <li><strong>UPI Transformation:</strong> Unified Payments Interface (UPI) processes over 8.7 billion transactions monthly, revolutionizing digital payments.</li>
          <li><strong>Mobile Internet:</strong> Over 700 million smartphone users, with affordable data (lowest rates globally) driving digital adoption.</li>
          <li><strong>Startup Ecosystem:</strong> Over 100 unicorn startups valued at more than $1 billion each, covering fintech, edtech, e-commerce, and more.</li>
          <li><strong>Digital Governance:</strong> Aadhaar biometric ID system covering 1.3 billion people, enabling targeted service delivery and financial inclusion.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Tab 4: Global Position
    with tabs[3]:
        st.header("India on the Global Stage")
        
        # Add overview
        st.markdown("""
        <div class='story-text'>
        Modern India has established itself as an important voice in global affairs, with growing
        economic, political, and cultural influence. From active participation in international
        forums to leadership on climate action and south-south cooperation, India's global
        footprint continues to expand in multiple dimensions.
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for content
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Global Economic Position
            st.subheader("Global Economic Position")
            
            # Create data for top economies
            economies = ['USA', 'China', 'Japan', 'Germany', 'India', 'UK', 'France', 'Italy', 'Brazil', 'Canada']
            gdp_values = [26954, 19910, 4231, 4072, 3730, 3164, 2782, 2010, 1920, 1988]
            
            economies_df = pd.DataFrame({
                'Country': economies,
                'GDP (Billion USD)': gdp_values
            }).sort_values('GDP (Billion USD)', ascending=True)
            
            fig = px.bar(
                economies_df,
                y='Country',
                x='GDP (Billion USD)',
                orientation='h',
                title='Top 10 Economies by GDP (2023)',
                color='GDP (Billion USD)',
                color_continuous_scale='Viridis',
                text='GDP (Billion USD)'
            )
            fig.update_traces(texttemplate='$%{text:,}B', textposition='outside')
            fig = apply_dark_theme(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Major Global Roles
            st.subheader("Major Global Roles")
            
            st.markdown("""
            <div style="background-color: rgba(49, 51, 63, 0.7); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #FF9933;">G20 Presidency (2023)</h4>
                <p>India's G20 presidency focused on inclusive growth, climate financing, and digital public infrastructure, with the theme "One Earth, One Family, One Future".</p>
            </div>
            
            <div style="background-color: rgba(49, 51, 63, 0.7); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #FF9933;">BRICS Leadership</h4>
                <p>Active member driving South-South cooperation and advocating for reformed multilateralism in global governance.</p>
            </div>
            
            <div style="background-color: rgba(49, 51, 63, 0.7); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #FF9933;">Climate Action</h4>
                <p>Committed to achieving net-zero emissions by 2070, while leading the International Solar Alliance and Coalition for Disaster Resilient Infrastructure.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # International Trade and Relations
        st.subheader("International Trade and Relations")
        
        # Create columns for trade and diplomatic influence
        col3, col4 = st.columns(2)
        
        with col3:
            # Trade visualization
            trade_years = list(range(2000, 2024, 4))
            exports = [42.3, 163.0, 305.9, 317.8, 322.5, 447.5, 775.0]
            imports = [51.5, 252.3, 489.3, 448.0, 478.3, 573.6, 892.0]
            
            # Ensure arrays are of the same length
            min_length = min(len(trade_years), len(exports), len(imports))
            trade_years = trade_years[:min_length]
            exports = exports[:min_length]
            imports = imports[:min_length]
            
            trade_data = pd.DataFrame({
                'Year': trade_years,
                'Exports': exports,
                'Imports': imports
            })
            
            trade_fig = px.line(
                trade_data,
                x='Year',
                y=['Exports', 'Imports'],
                title='India\'s International Trade (in USD Billion)',
                markers=True,
                color_discrete_map={
                    'Exports': '#4CAF50',
                    'Imports': '#2196F3'
                }
            )
            trade_fig.update_layout(
                xaxis_title="Year",
                yaxis_title="USD Billion",
                hovermode="x unified",
                legend_title=None
            )
            trade_fig = apply_dark_theme(trade_fig)
            st.plotly_chart(trade_fig, use_container_width=True)
        
        with col4:
            # Soft Power elements
            st.markdown("""
            ### Soft Power Elements
            
            India's global influence extends beyond economics and politics to cultural soft power:
            
            - **Yoga & Ayurveda:** Global following with International Day of Yoga observed worldwide
            - **Cinema & Entertainment:** Bollywood reaches over 90 countries; OTT platforms expanding reach
            - **Cuisine:** Indian restaurants in virtually every major city globally
            - **Diaspora Influence:** 32+ million strong Indian diaspora in leadership positions worldwide
            - **Technology Talent:** CEOs of major tech companies including Google, Microsoft, IBM
            """)
        
        # Global position insights
        st.markdown("""
        <div class='insight-box'>
        <strong>Global Position Insights:</strong>
        <ul>
          <li><strong>Economic Rise:</strong> Projected to become the world's 3rd largest economy by 2027, with expanding trade relationships across regions.</li>
          <li><strong>Strategic Partnerships:</strong> Balancing relationships with USA, Russia, Europe, and neighbors while maintaining strategic autonomy.</li>
          <li><strong>Development Partner:</strong> Shifted from aid recipient to provider of development assistance to neighboring and African countries.</li>
          <li><strong>Global Governance:</strong> Advocate for reformed multilateralism and greater representation of developing nations in international institutions.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Tab 5: Future Outlook
    with tabs[4]:
        st.header("Looking Ahead: India@2047")
        
        # Add overview
        st.markdown("""
        <div class='story-text'>
        As India moves towards the centenary of its independence in 2047, it faces both unprecedented 
        opportunities and significant challenges. The country's trajectory over the next decades will 
        be shaped by how it navigates economic transformation, technological advancement, demographic shifts,
        environmental pressures, and geopolitical dynamics.
        </div>
        """, unsafe_allow_html=True)
        
        # Opportunities and Challenges
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Key Opportunities")
            
            st.markdown("""
            <div style="background-color: rgba(76, 175, 80, 0.2); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #4CAF50;">Demographic Dividend</h4>
                <p>Leveraging the young workforce (average age 29) for economic growth through education, skilling, and employment generation.</p>
            </div>
            
            <div style="background-color: rgba(76, 175, 80, 0.2); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #4CAF50;">Digital Leadership</h4>
                <p>Building on digital public infrastructure to create inclusive growth models and become a global hub for digital innovation.</p>
            </div>
            
            <div style="background-color: rgba(76, 175, 80, 0.2); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #4CAF50;">Manufacturing Expansion</h4>
                <p>Potential to become a global manufacturing hub through Production Linked Incentive schemes and infrastructure development.</p>
            </div>
            
            <div style="background-color: rgba(76, 175, 80, 0.2); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #4CAF50;">Green Growth</h4>
                <p>Leading in renewable energy adoption and sustainable development practices, with 500 GW non-fossil energy capacity targeted by 2030.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Key Challenges")
            
            st.markdown("""
            <div style="background-color: rgba(244, 67, 54, 0.2); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #F44336;">Job Creation</h4>
                <p>Creating 10-12 million quality jobs annually to absorb the growing workforce and reduce informal employment.</p>
            </div>
            
            <div style="background-color: rgba(244, 67, 54, 0.2); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #F44336;">Environmental Pressures</h4>
                <p>Addressing air and water pollution, climate change impacts, and balancing growth with environmental sustainability.</p>
            </div>
            
            <div style="background-color: rgba(244, 67, 54, 0.2); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #F44336;">Infrastructure Gaps</h4>
                <p>Bridging the $1.5 trillion infrastructure gap, particularly in urban housing, transportation, and logistics.</p>
            </div>
            
            <div style="background-color: rgba(244, 67, 54, 0.2); border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <h4 style="margin-top: 0; color: #F44336;">Inequality</h4>
                <p>Reducing income, regional, and social disparities to ensure inclusive development across all segments of society.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Vision for India@2047
        st.subheader("Vision for India@2047")
        
        # Create potential GDP projection
        projection_years = list(range(2023, 2048, 5))
        projected_gdp = [3.7, 5.5, 8.2, 12.0, 17.5]  # In trillion USD
        
        projection_df = pd.DataFrame({
            'Year': projection_years,
            'Projected GDP (Trillion USD)': projected_gdp
        })
        
        fig = px.line(
            projection_df,
            x='Year',
            y='Projected GDP (Trillion USD)',
            title='Potential Economic Trajectory Towards India@2047',
            markers=True,
            color_discrete_sequence=['#FF9933'],
        )
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="GDP (Trillion USD)",
            hovermode="x unified"
        )
        fig.add_vline(x=2047, line_dash="dash", line_color="#FFFFFF", annotation_text="Centenary of Independence")
        fig = apply_dark_theme(fig)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key future initiatives
        st.markdown("""
        <div style="background-color: rgba(49, 51, 63, 0.7); border-radius: 10px; padding: 20px; margin: 20px 0;">
        <h3 style="margin-top: 0; color: #FF9933;">Key National Initiatives Shaping the Future</h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
            <div style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px;">
                <h4 style="margin-top: 0;">Gati Shakti</h4>
                <p>Multi-modal connectivity for integrated infrastructure development</p>
            </div>
            
            <div style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px;">
                <h4 style="margin-top: 0;">National Education Policy</h4>
                <p>Transforming education through flexibility, creativity and digital learning</p>
            </div>
            
            <div style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px;">
                <h4 style="margin-top: 0;">Atmanirbhar Bharat</h4>
                <p>Self-reliance through local manufacturing and supply chain resilience</p>
            </div>
            
            <div style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px;">
                <h4 style="margin-top: 0;">Net Zero by 2070</h4>
                <p>Energy transition through renewables, green hydrogen, and efficiency</p>
            </div>
            
            <div style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px;">
                <h4 style="margin-top: 0;">Digital India 2.0</h4>
                <p>Next generation of digital public infrastructure and smart governance</p>
            </div>
            
            <div style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 8px;">
                <h4 style="margin-top: 0;">Urban Transformation</h4>
                <p>Smart Cities Mission and sustainable urban development models</p>
            </div>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Future outlook insights
        st.markdown("""
        <div class='insight-box'>
        <strong>Future Outlook Insights:</strong>
        <ul>
          <li><strong>Economic Projection:</strong> Potential to become a $17-20 trillion economy by 2047, with per capita income exceeding $15,000.</li>
          <li><strong>Development Model:</strong> India's unique development path may offer alternatives to traditional Western models, combining technology with inclusive growth.</li>
          <li><strong>Aging Transition:</strong> By 2047, demographic dividend will transition as the population ages, requiring preparations for healthcare and social security.</li>
          <li><strong>Global Role:</strong> Likely to be among the top 3 global powers with expanded role in international institutions and regional leadership.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Add a conclusive insights section
    st.header("Synthesizing Modern India")
    
    st.markdown("""
    <div style="background-color: rgba(49, 51, 63, 0.7); border-radius: 10px; padding: 20px; margin: 20px 0;">
    <h3 style="margin-top: 0; color: #FF9933;">The Indian Paradox: Balancing Tradition and Modernity</h3>
    
    <p>Modern India embodies numerous paradoxes that make its development journey unique and complex:</p>
    
    <ol>
        <li><strong>Ancient and Modern:</strong> A civilization with 5000+ years of continuous history embracing cutting-edge technologies and modern governance systems.</li>
        <li><strong>Unity in Diversity:</strong> Extreme diversity in languages, religions, and cultures coexisting within a unified democratic framework.</li>
        <li><strong>Technological Leapfrogging:</strong> Bypassing traditional development stages through digital solutions, even while parts of the country remain in early development phases.</li>
        <li><strong>Global and Local:</strong> Simultaneously participating in global value chains while strengthening local production and cultural identity.</li>
        <li><strong>Traditional and Progressive:</strong> Balancing deep-rooted traditions with progressive social and technological advancements.</li>
    </ol>
    
    <p>These paradoxes are not contradictions but rather complementary aspects that give modern India its distinctive character and resilience as it navigates the complexities of the 21st century.</p>
    </div>
    """, unsafe_allow_html=True) 