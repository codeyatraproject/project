import streamlit as st
import pandas as pd
import plotly.express as px
from modules.utils import apply_dark_theme, load_education_data, get_color_palette

def render():
    """Render the Education Landscape chapter content"""
    st.title("📚 Education Landscape of India")
    
    st.markdown("""
    <div class='story-text'>
    India's education system is one of the largest in the world, serving over 250 million students. 
    From ancient gurukuls to modern digital learning platforms, education in India has evolved significantly 
    while maintaining its core focus on knowledge and skill development. This data story explores the current 
    landscape of Indian education through key metrics and regional variations.
    </div>
    """, unsafe_allow_html=True)
    
    # Load and prepare data
    with st.spinner("Analyzing education data..."):
        try:
            df = load_education_data()
            
            if df is None or df.empty:
                st.error("Failed to load education data. Please check your data files.")
                return
                
        except Exception as e:
            st.error(f"Error loading education data: {e}")
            return
    
    # Overview section
    st.header("Educational Landscape Overview")
    
    # Key metrics with error handling
    try:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            literacy_rate = df['National Literacy Rate (%)'].iloc[0]
            if isinstance(literacy_rate, str):
                literacy_rate = float(literacy_rate)
            st.metric("Literacy Rate", f"{literacy_rate:.1f}%")
        with col2:
            enrollment_rate = df['Primary Enrollment Rate (%)'].iloc[0]
            if isinstance(enrollment_rate, str):
                enrollment_rate = float(enrollment_rate)
            st.metric("Primary Enrollment", f"{enrollment_rate:.1f}%")
        with col3:
            universities = df['Number of Universities'].iloc[0]
            if isinstance(universities, str):
                universities = universities.replace(',', '')
            st.metric("Universities", f"{universities}")
        with col4:
            higher_ed = df['Higher Education Enrollment (millions)'].iloc[0]
            if isinstance(higher_ed, str):
                higher_ed = float(higher_ed)
            st.metric("Students in Higher Ed", f"{higher_ed:.1f}M")
    except Exception as e:
        st.warning(f"Could not display all education metrics: {e}")
    
    # Educational metrics tabs
    tabs = st.tabs(["Literacy & Enrollment", "Educational Infrastructure", "Quality Metrics", "Gender Parity"])
    
    # Tab 1: Literacy and Enrollment
    with tabs[0]:
        try:
            # Extract state-level data safely
            state_names = df['State Names'].iloc[0].split(', ') if isinstance(df['State Names'].iloc[0], str) else []
            literacy_rates = [float(x) for x in df['State Literacy Rates (%)'].iloc[0].split(', ')] if isinstance(df['State Literacy Rates (%)'].iloc[0], str) else []
            primary_enrollment = [float(x) for x in df['State Primary Enrollment (%)'].iloc[0].split(', ')] if isinstance(df['State Primary Enrollment (%)'].iloc[0], str) else []
            secondary_enrollment = [float(x) for x in df['State Secondary Enrollment (%)'].iloc[0].split(', ')] if isinstance(df['State Secondary Enrollment (%)'].iloc[0], str) else []
            higher_ed_enrollment = [float(x) for x in df['State Higher Ed Enrollment (%)'].iloc[0].split(', ')] if isinstance(df['State Higher Ed Enrollment (%)'].iloc[0], str) else []
            
            # Ensure all lists have the same length
            min_length = min(len(state_names), len(literacy_rates), len(primary_enrollment), 
                            len(secondary_enrollment), len(higher_ed_enrollment))
            
            if min_length > 0:
                states_df = pd.DataFrame({
                    'State': state_names[:min_length],
                    'Literacy Rate': literacy_rates[:min_length],
                    'Primary Enrollment': primary_enrollment[:min_length],
                    'Secondary Enrollment': secondary_enrollment[:min_length],
                    'Higher Ed Enrollment': higher_ed_enrollment[:min_length]
                })
                
                # Sort by literacy rate
                states_df = states_df.sort_values('Literacy Rate', ascending=False)
                
                # Create visualization
                fig = px.bar(
                    states_df,
                    x='State',
                    y='Literacy Rate',
                    color='Literacy Rate',
                    title='Literacy Rates by State (%)',
                    color_continuous_scale='Viridis',
                    text='Literacy Rate'
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
                
                # Enrollment rates comparison
                enrollment_df = states_df.sort_values('Primary Enrollment', ascending=False).head(10)
                
                fig = px.bar(
                    enrollment_df,
                    x='State',
                    y=['Primary Enrollment', 'Secondary Enrollment', 'Higher Ed Enrollment'],
                    title='Education Enrollment by Level (%) - Top 10 States',
                    barmode='group',
                    labels={'value': 'Enrollment Rate (%)', 'variable': 'Education Level'}
                )
                fig = apply_dark_theme(fig)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient state data available for visualization.")
                
            # Educational progress metrics
            st.subheader("Education Progress Over Time")
            
            # Create years data safely
            years_str = df['Literacy Rate Years'].iloc[0] if 'Literacy Rate Years' in df.columns else ""
            rates_str = df['Literacy Rate History'].iloc[0] if 'Literacy Rate History' in df.columns else ""
            
            if isinstance(years_str, str) and isinstance(rates_str, str) and years_str and rates_str:
                years = [int(x) for x in years_str.split(', ')]
                rates = [float(x) for x in rates_str.split(', ')]
                
                # Ensure both lists have the same length
                min_length = min(len(years), len(rates))
                
                if min_length > 0:
                    # Create time series data
                    history_df = pd.DataFrame({
                        'Year': years[:min_length],
                        'Literacy Rate (%)': rates[:min_length]
                    })
                    
                    fig = px.line(
                        history_df,
                        x='Year',
                        y='Literacy Rate (%)',
                        title='National Literacy Rate Trend (%)',
                        markers=True
                    )
                    fig = apply_dark_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Insufficient historical data for time series visualization.")
            else:
                st.warning("Historical literacy rate data not available.")
        except Exception as e:
            st.error(f"Error in literacy and enrollment visualization: {e}")
    
    # Tab 2: Educational Infrastructure
    with tabs[1]:
        try:
            # Extract infrastructure data safely
            primary_schools = df['Number of Primary Schools'].iloc[0] if 'Number of Primary Schools' in df.columns else "0"
            secondary_schools = df['Number of Secondary Schools'].iloc[0] if 'Number of Secondary Schools' in df.columns else "0"
            colleges = df['Number of Colleges'].iloc[0] if 'Number of Colleges' in df.columns else "0"
            universities = df['Number of Universities'].iloc[0] if 'Number of Universities' in df.columns else "0"
            technical_institutions = df['Number of Technical Institutions'].iloc[0] if 'Number of Technical Institutions' in df.columns else "0"
            
            # Clean the data
            primary_schools = int(str(primary_schools).replace(',', ''))
            secondary_schools = int(str(secondary_schools).replace(',', ''))
            colleges = int(str(colleges).replace(',', ''))
            universities = int(str(universities).replace(',', ''))
            technical_institutions = int(str(technical_institutions).replace(',', ''))
            
            infra_data = {
                'Category': ['Primary Schools', 'Secondary Schools', 'Colleges', 'Universities', 'Technical Institutions'],
                'Count': [primary_schools, secondary_schools, colleges, universities, technical_institutions]
            }
            
            infra_df = pd.DataFrame(infra_data)
            
            fig = px.bar(
                infra_df,
                x='Category',
                y='Count',
                color='Category',
                title='Educational Institutions in India',
                color_discrete_sequence=get_color_palette(len(infra_df)),
                text='Count',
                log_y=True
            )
            fig = apply_dark_theme(fig)
            fig.update_traces(texttemplate='%{text:,}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            # Infrastructure distribution by region - with error handling
            try:
                regions_str = df['Regional Names'].iloc[0] if 'Regional Names' in df.columns else ""
                primary_schools_str = df['Regional Primary Schools'].iloc[0] if 'Regional Primary Schools' in df.columns else ""
                secondary_schools_str = df['Regional Secondary Schools'].iloc[0] if 'Regional Secondary Schools' in df.columns else ""
                colleges_str = df['Regional Colleges'].iloc[0] if 'Regional Colleges' in df.columns else ""
                population_str = df['Regional Population (millions)'].iloc[0] if 'Regional Population (millions)' in df.columns else ""
                
                if all(isinstance(x, str) and x for x in [regions_str, primary_schools_str, secondary_schools_str, colleges_str, population_str]):
                    regions = regions_str.split(', ')
                    primary_schools_list = [int(x.replace(',', '')) for x in primary_schools_str.split(', ')]
                    secondary_schools_list = [int(x.replace(',', '')) for x in secondary_schools_str.split(', ')]
                    colleges_list = [int(x.replace(',', '')) for x in colleges_str.split(', ')]
                    population_list = [float(x) for x in population_str.split(', ')]
                    
                    # Ensure all lists have the same length
                    min_length = min(len(regions), len(primary_schools_list), len(secondary_schools_list), 
                                    len(colleges_list), len(population_list))
                    
                    if min_length > 0:
                        region_df = pd.DataFrame({
                            'Region': regions[:min_length],
                            'Primary Schools': primary_schools_list[:min_length],
                            'Secondary Schools': secondary_schools_list[:min_length],
                            'Colleges': colleges_list[:min_length],
                            'Population (millions)': population_list[:min_length]
                        })
                        
                        # Normalize data for better comparison
                        region_df['Primary per Million'] = region_df['Primary Schools'] / region_df['Population (millions)']
                        region_df['Secondary per Million'] = region_df['Secondary Schools'] / region_df['Population (millions)']
                        region_df['Colleges per Million'] = region_df['Colleges'] / region_df['Population (millions)']
                        
                        fig = px.bar(
                            region_df,
                            x='Region',
                            y=['Primary per Million', 'Secondary per Million', 'Colleges per Million'],
                            title='Educational Institutions per Million Population by Region',
                            barmode='group',
                            labels={'value': 'Institutions per Million', 'variable': 'Institution Type'}
                        )
                        fig = apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Insufficient regional data for visualization.")
                else:
                    st.warning("Regional data not available for visualization.")
            except Exception as e:
                st.warning(f"Could not display regional infrastructure distribution: {e}")
            
            # Teacher-student ratios - with error handling
            try:
                primary_ratio = df['Teacher-Student Ratio Primary'].iloc[0] if 'Teacher-Student Ratio Primary' in df.columns else "1:0"
                secondary_ratio = df['Teacher-Student Ratio Secondary'].iloc[0] if 'Teacher-Student Ratio Secondary' in df.columns else "1:0"
                higher_ed_ratio = df['Teacher-Student Ratio Higher Ed'].iloc[0] if 'Teacher-Student Ratio Higher Ed' in df.columns else "1:0"
                
                # Extract ratio values
                primary_ratio_val = float(primary_ratio.replace('1:', '')) if isinstance(primary_ratio, str) else 0
                secondary_ratio_val = float(secondary_ratio.replace('1:', '')) if isinstance(secondary_ratio, str) else 0
                higher_ed_ratio_val = float(higher_ed_ratio.replace('1:', '')) if isinstance(higher_ed_ratio, str) else 0
                
                st.subheader("Teacher-Student Ratios")
                
                ratio_data = {
                    'Level': ['Primary', 'Secondary', 'Higher Education'],
                    'Teacher-Student Ratio': [primary_ratio_val, secondary_ratio_val, higher_ed_ratio_val]
                }
                
                ratio_df = pd.DataFrame(ratio_data)
                
                fig = px.bar(
                    ratio_df,
                    x='Level',
                    y='Teacher-Student Ratio',
                    color='Level',
                    title='Teacher-Student Ratio by Education Level',
                    color_discrete_sequence=get_color_palette(len(ratio_df)),
                    text='Teacher-Student Ratio'
                )
                fig = apply_dark_theme(fig)
                fig.update_traces(texttemplate='1:%{text:.1f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display teacher-student ratios: {e}")
        except Exception as e:
            st.error(f"Error in educational infrastructure visualization: {e}")
    
    # Tab 3: Quality Metrics
    with tabs[2]:
        try:
            # Extract quality metrics safely
            pisa_reading = df['PISA Reading Score'].iloc[0] if 'PISA Reading Score' in df.columns else "0"
            pisa_math = df['PISA Math Score'].iloc[0] if 'PISA Math Score' in df.columns else "0"
            pisa_science = df['PISA Science Score'].iloc[0] if 'PISA Science Score' in df.columns else "0"
            innovation_index = df['Global Innovation Index'].iloc[0] if 'Global Innovation Index' in df.columns else "0/100"
            higher_ed_rank = df['Higher Education Quality Rank'].iloc[0] if 'Higher Education Quality Rank' in df.columns else "0/0"
            
            # Convert to numeric values
            pisa_reading_val = float(pisa_reading) if isinstance(pisa_reading, str) else 0
            pisa_math_val = float(pisa_math) if isinstance(pisa_math, str) else 0
            pisa_science_val = float(pisa_science) if isinstance(pisa_science, str) else 0
            innovation_index_val = float(innovation_index.split('/')[0]) if isinstance(innovation_index, str) else 0
            higher_ed_rank_val = float(higher_ed_rank.split('/')[0]) if isinstance(higher_ed_rank, str) else 0
            
            quality_data = {  # Unused variable
                'Metric': [
                    'PISA Reading Score', 'PISA Math Score', 'PISA Science Score', 
                    'Global Innovation Index', 'Higher Ed Quality Rank'
                ],
                'Score': [
                    pisa_reading_val, pisa_math_val, pisa_science_val,
                    innovation_index_val, higher_ed_rank_val
                ],
                'Category': [
                    'International Assessment', 'International Assessment', 'International Assessment',
                    'Innovation', 'Higher Education'
                ]
            }
            
#             quality_df = pd.DataFrame(quality_data)  # Unused variable
            
            # PISA scores comparison - with error handling
            try:
                countries_str = df['PISA Comparison Countries'].iloc[0] if 'PISA Comparison Countries' in df.columns else ""
                reading_str = df['PISA Comparison Reading'].iloc[0] if 'PISA Comparison Reading' in df.columns else ""
                math_str = df['PISA Comparison Math'].iloc[0] if 'PISA Comparison Math' in df.columns else ""
                science_str = df['PISA Comparison Science'].iloc[0] if 'PISA Comparison Science' in df.columns else ""
                
                if all(isinstance(x, str) and x for x in [countries_str, reading_str, math_str, science_str]):
                    countries = countries_str.split(', ')
                    reading_scores = [float(x) for x in reading_str.split(', ')]
                    math_scores = [float(x) for x in math_str.split(', ')]
                    science_scores = [float(x) for x in science_str.split(', ')]
                    
                    # Ensure all lists have the same length
                    min_length = min(len(countries), len(reading_scores), len(math_scores), len(science_scores))
                    
                    if min_length > 0:
                        pisa_df = pd.DataFrame({
                            'Country': countries[:min_length],
                            'Reading Score': reading_scores[:min_length],
                            'Math Score': math_scores[:min_length],
                            'Science Score': science_scores[:min_length]
                        })
                        
                        fig = px.bar(
                            pisa_df,
                            x='Country',
                            y=['Reading Score', 'Math Score', 'Science Score'],
                            title='PISA Scores Comparison with Selected Countries',
                            barmode='group',
                            labels={'value': 'PISA Score', 'variable': 'Assessment Area'}
                        )
                        fig = apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Insufficient PISA comparison data for visualization.")
                else:
                    st.warning("PISA comparison data not available.")
            except Exception as e:
                st.warning(f"Could not display PISA comparison: {e}")
            
            # Top universities - with error handling
            try:
                universities_str = df['Top Universities'].iloc[0] if 'Top Universities' in df.columns else ""
                ranks_str = df['University World Ranks'].iloc[0] if 'University World Ranks' in df.columns else ""
                
                if isinstance(universities_str, str) and isinstance(ranks_str, str) and universities_str and ranks_str:
                    universities = universities_str.split(', ')
                    ranks = [int(x) for x in ranks_str.split(', ')]
                    
                    # Ensure both lists have the same length
                    min_length = min(len(universities), len(ranks))
                    
                    if min_length > 0:
                        st.subheader("Top Universities by Ranking")
                        
                        uni_df = pd.DataFrame({
                            'University': universities[:min_length],
                            'World Rank': ranks[:min_length]
                        })
                        
                        fig = px.bar(
                            uni_df,
                            x='University',
                            y='World Rank',
                            color='University',
                            title='Top Indian Universities by World Ranking',
                            color_discrete_sequence=get_color_palette(len(uni_df)),
                            text='World Rank'
                        )
                        fig = apply_dark_theme(fig)
                        fig.update_traces(texttemplate='%{text}', textposition='outside')
                        fig.update_yaxes(autorange="reversed")  # Lower rank is better
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Insufficient university ranking data for visualization.")
                else:
                    st.warning("University ranking data not available.")
            except Exception as e:
                st.warning(f"Could not display university rankings: {e}")
        except Exception as e:
            st.error(f"Error in quality metrics visualization: {e}")
    
    # Tab 4: Gender Parity
    with tabs[3]:
        try:
            # Extract gender parity data safely
            primary_parity = df['Gender Parity Primary'].iloc[0] if 'Gender Parity Primary' in df.columns else "0"
            secondary_parity = df['Gender Parity Secondary'].iloc[0] if 'Gender Parity Secondary' in df.columns else "0"
            higher_ed_parity = df['Gender Parity Higher Ed'].iloc[0] if 'Gender Parity Higher Ed' in df.columns else "0"
            
            # Convert to numeric values
            primary_parity_val = float(primary_parity) if isinstance(primary_parity, str) else 0
            secondary_parity_val = float(secondary_parity) if isinstance(secondary_parity, str) else 0
            higher_ed_parity_val = float(higher_ed_parity) if isinstance(higher_ed_parity, str) else 0
            
            gender_data = {
                'Level': ['Primary', 'Secondary', 'Higher Education'],
                'Gender Parity Index': [primary_parity_val, secondary_parity_val, higher_ed_parity_val]
            }
            
            gender_df = pd.DataFrame(gender_data)
            
            fig = px.bar(
                gender_df,
                x='Level',
                y='Gender Parity Index',
                color='Level',
                title='Gender Parity Index by Education Level (1.0 = Perfect Parity)',
                color_discrete_sequence=get_color_palette(len(gender_df)),
                text='Gender Parity Index'
            )
            fig = apply_dark_theme(fig)
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            
            # Add a horizontal line at 1.0 (perfect parity)
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=1,
                x1=2.5,
                y1=1,
                line=dict(color="red", width=2, dash="dash")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Gender disparity by state - with error handling
            try:
                state_names = df['State Names'].iloc[0].split(', ') if isinstance(df['State Names'].iloc[0], str) else []
                female_literacy = [float(x) for x in df['State Female Literacy (%)'].iloc[0].split(', ')] if isinstance(df['State Female Literacy (%)'].iloc[0], str) else []
                male_literacy = [float(x) for x in df['State Male Literacy (%)'].iloc[0].split(', ')] if isinstance(df['State Male Literacy (%)'].iloc[0], str) else []
                
                # Ensure all lists have the same length
                min_length = min(len(state_names), len(female_literacy), len(male_literacy))
                
                if min_length > 0:
                    state_gender_df = pd.DataFrame({
                        'State': state_names[:min_length],
                        'Female Literacy': female_literacy[:min_length],
                        'Male Literacy': male_literacy[:min_length]
                    })
                    
                    state_gender_df['Literacy Gap'] = state_gender_df['Male Literacy'] - state_gender_df['Female Literacy']
                    state_gender_df = state_gender_df.sort_values('Literacy Gap', ascending=False)
                    
                    fig = px.bar(
                        state_gender_df.head(10),
                        x='State',
                        y=['Male Literacy', 'Female Literacy'],
                        title='States with Highest Gender Literacy Gap',
                        barmode='group',
                        labels={'value': 'Literacy Rate (%)', 'variable': 'Gender'}
                    )
                    fig = apply_dark_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Insufficient gender literacy data for visualization.")
            except Exception as e:
                st.warning(f"Could not display gender literacy gap by state: {e}")
        except Exception as e:
            st.error(f"Error in gender parity visualization: {e}")
    
    # Educational challenges and opportunities
    st.header("Challenges & Future Directions")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚧 Key Challenges")
        st.markdown("""
        - **Accessibility gaps** between urban and rural areas
        - **Quality disparities** across states and socioeconomic groups
        - **High dropout rates** especially in secondary education
        - **Infrastructure deficits** in many government schools
        - **Gender gaps** persistent in certain states and communities
        - **Digital divide** limiting online education reach
        """)
    
    with col2:
        st.subheader("🌟 Future Opportunities")
        st.markdown("""
        - **National Education Policy 2020** reform implementation
        - **EdTech revolution** expanding digital learning access
        - **Skill development initiatives** aligning education with employment
        - **Public-private partnerships** improving infrastructure
        - **International collaborations** raising quality standards
        - **Inclusive education approaches** reducing inequality
        """)
    
    # Final summary
    st.markdown("""
    <div class='story-text'>
    India's education landscape shows remarkable progress alongside persistent challenges. The literacy rate has 
    improved significantly over decades, yet educational quality and access remain uneven across regions. 
    
    The data reveals both the scale of India's educational system and the ongoing work needed to fulfill the 
    promise of quality education for all. With policy reforms, technology integration, and focus on inclusive 
    growth, India's education sector is positioned for transformative change in the coming decades.
    </div>
    """, unsafe_allow_html=True) 