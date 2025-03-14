import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from PIL import Image
import plotly.express as px
import json

# Set page configuration
st.set_page_config(
    page_title="Water Quality Dashboard",
    page_icon="💧",
    layout="wide"
)

# Dashboard title and introduction
st.title("💧 Water Quality Analysis Dashboard")
st.markdown("""
This dashboard presents insights from water quality data analysis. 
Explore visualizations, statistics, and trends related to water quality parameters.
""")

# Function to load processed data
@st.cache_data
def load_processed_data():
    data_files = {}
    
    # Try loading the main processed dataset
    try:
        data_files['main_data'] = pd.read_csv('processed_data/cleaned_water_quality_data.csv')
    except FileNotFoundError:
        try:
            data_files['main_data'] = pd.read_excel('processed_data/cleaned_water_quality_data.xlsx')
        except FileNotFoundError:
            st.warning("Main cleaned dataset not found. Some dashboard features may be unavailable.")
            data_files['main_data'] = None
    
    # Try loading statistical summary
    try:
        data_files['stats'] = pd.read_csv('processed_data/water_quality_statistics.csv')
    except FileNotFoundError:
        try:
            data_files['stats'] = pd.read_excel('processed_data/water_quality_statistics.xlsx')
        except FileNotFoundError:
            data_files['stats'] = None
    
    # Try loading any other processed data files that might exist
    try:
        # Look for trend data
        trend_files = glob.glob('processed_data/*trend*.csv') + glob.glob('processed_data/*trend*.xlsx')
        if trend_files:
            if trend_files[0].endswith('.csv'):
                data_files['trends'] = pd.read_csv(trend_files[0])
            else:
                data_files['trends'] = pd.read_excel(trend_files[0])
    except Exception:
        data_files['trends'] = None
    
    return data_files

# Function to load visualizations
def load_visualizations():
    visualizations = {}
    
    # Look for image files in visualizations directory
    image_files = glob.glob('visualizations/*.png') + glob.glob('visualizations/*.jpg')
    for img_file in image_files:
        file_name = os.path.basename(img_file)
        visualizations[file_name] = img_file
    
    # Look for HTML files (interactive plotly plots)
    html_files = glob.glob('visualizations/*.html')
    for html_file in html_files:
        file_name = os.path.basename(html_file)
        visualizations[file_name] = html_file
    
    return visualizations

# Load data and visualizations
data = load_processed_data()
visualizations = load_visualizations()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page",
    ["Overview", "Data Explorer", "Visualizations", "Insights", "About"]
)

# Overview page
if page == "Overview":
    st.header("Water Quality Analysis Overview")
    
    # Display summary statistics if available
    if data['stats'] is not None:
        st.subheader("Summary Statistics")
        st.dataframe(data['stats'])
    
    # Display a key visualization if available
    key_viz_candidates = [f for f in visualizations.keys() if 'overview' in f.lower() or 'summary' in f.lower()]
    if key_viz_candidates:
        st.subheader("Key Visualization")
        viz_path = visualizations[key_viz_candidates[0]]
        if viz_path.endswith(('.png', '.jpg')):
            st.image(viz_path, caption=key_viz_candidates[0], use_column_width=True)
        elif viz_path.endswith('.html'):
            st.components.v1.html(open(viz_path, 'r').read(), height=600)
    
    # Display key findings
    st.subheader("Key Findings")
    st.markdown("""
    - Analysis based on 65 rows of water quality data
    - Data was cleaned and processed for accurate insights
    - Multiple visualizations created to explore different aspects of water quality
    - Statistical analysis performed to identify patterns and anomalies
    
    Use the navigation panel on the left to explore different sections of this dashboard.
    """)

# Data Explorer page
elif page == "Data Explorer":
    st.header("Water Quality Data Explorer")
    
    if data['main_data'] is not None:
        # Allow users to select columns to view
        all_columns = data['main_data'].columns.tolist()
        selected_columns = st.multiselect("Select columns to display", all_columns, default=all_columns[:5])
        
        if selected_columns:
            st.dataframe(data['main_data'][selected_columns])
            
            # Add a download button
            st.download_button(
                label="Download selected data as CSV",
                data=data['main_data'][selected_columns].to_csv(index=False).encode('utf-8'),
                file_name="water_quality_data.csv",
                mime="text/csv"
            )
            
            # Add filtering capabilities
            st.subheader("Filter Data")
            numeric_columns = data['main_data'].select_dtypes(include=['number']).columns.tolist()
            
            if numeric_columns:
                filter_column = st.selectbox("Select column to filter", numeric_columns)
                min_value = float(data['main_data'][filter_column].min())
                max_value = float(data['main_data'][filter_column].max())
                
                filter_range = st.slider(
                    f"Filter range for {filter_column}",
                    min_value, max_value,
                    (min_value, max_value)
                )
                
                filtered_data = data['main_data'][
                    (data['main_data'][filter_column] >= filter_range[0]) & 
                    (data['main_data'][filter_column] <= filter_range[1])
                ]
                
                st.subheader("Filtered Data")
                st.dataframe(filtered_data[selected_columns])
    else:
        st.warning("No processed data available to explore.")

# Visualizations page
elif page == "Visualizations":
    st.header("Water Quality Visualizations")
    
    if visualizations:
        # Group visualizations by type
        image_viz = [f for f in visualizations.keys() if f.endswith(('.png', '.jpg'))]
        html_viz = [f for f in visualizations.keys() if f.endswith('.html')]
        
        # Create tabs for different visualization types
        viz_type = st.radio("Visualization type", ["Images", "Interactive Plots"], horizontal=True)
        
        if viz_type == "Images":
            if image_viz:
                selected_viz = st.selectbox("Select visualization", image_viz)
                st.image(visualizations[selected_viz], caption=selected_viz, use_column_width=True)
                
                # Optional: Add description based on filename
                viz_name = selected_viz.replace('.png', '').replace('.jpg', '').replace('_', ' ').title()
                st.markdown(f"**{viz_name}**")
                st.markdown("This visualization shows the relationship between water quality parameters.")
            else:
                st.info("No image visualizations found.")
                
        else:  # Interactive Plots
            if html_viz:
                selected_viz = st.selectbox("Select interactive visualization", html_viz)
                st.components.v1.html(open(visualizations[selected_viz], 'r').read(), height=600)
                
                # Optional: Add description based on filename
                viz_name = selected_viz.replace('.html', '').replace('_', ' ').title()
                st.markdown(f"**{viz_name}**")
                st.markdown("This interactive plot allows you to explore water quality data in detail.")
            else:
                st.info("No interactive visualizations found.")
    else:
        st.warning("No visualizations found in the visualizations directory.")
        
        # Create a sample visualization using the main data if available
        if data['main_data'] is not None:
            st.subheader("Sample Visualization")
            numeric_columns = data['main_data'].select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_columns) >= 2:
                x_col = st.selectbox("Select X-axis", numeric_columns, index=0)
                y_col = st.selectbox("Select Y-axis", numeric_columns, index=min(1, len(numeric_columns)-1))
                
                fig = px.scatter(data['main_data'], x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig, use_container_width=True)

# Insights page
elif page == "Insights":
    st.header("Water Quality Insights")
    
    st.subheader("Key Observations")
    st.markdown("""
    - The water quality data shows variations across different sampling periods
    - Correlation between key parameters indicates potential environmental factors affecting water quality
    - Statistical analysis reveals patterns that can help in monitoring water quality effectively
    """)
    
    # Create tabs for different types of insights
    insight_type = st.tabs(["Statistical Insights", "Trend Analysis", "Recommendations"])
    
    with insight_type[0]:
        st.markdown("### Statistical Analysis")
        if data['stats'] is not None:
            st.dataframe(data['stats'])
        else:
            # Create simple statistics if data is available
            if data['main_data'] is not None:
                numeric_cols = data['main_data'].select_dtypes(include=['number'])
                if not numeric_cols.empty:
                    st.dataframe(numeric_cols.describe())
                else:
                    st.info("No numeric data available for statistical analysis.")
            else:
                st.info("No data available for statistical analysis.")
    
    with insight_type[1]:
        st.markdown("### Trend Analysis")
        if data['trends'] is not None:
            st.dataframe(data['trends'])
        else:
            trend_viz = [f for f in visualizations.keys() if 'trend' in f.lower()]
            if trend_viz:
                viz_path = visualizations[trend_viz[0]]
                if viz_path.endswith(('.png', '.jpg')):
                    st.image(viz_path, caption=trend_viz[0], use_column_width=True)
                elif viz_path.endswith('.html'):
                    st.components.v1.html(open(viz_path, 'r').read(), height=600)
            else:
                st.info("No trend analysis available.")
    
    with insight_type[2]:
        st.markdown("### Recommendations")
        st.markdown("""
        Based on the water quality analysis, here are some key recommendations:
        
        1. **Continuous Monitoring**: Establish a regular monitoring program for key water quality parameters
        2. **Parameter Focus**: Pay special attention to parameters that showed significant variations
        3. **Seasonal Analysis**: Consider seasonal factors when interpreting water quality data
        4. **Data Collection**: Improve data collection methods to ensure consistency and reliability
        5. **Intervention Points**: Identify critical thresholds for intervention based on statistical analysis
        """)

# About page
elif page == "About":
    st.header("About This Dashboard")
    
    st.markdown("""
    ### Water Quality Analysis Dashboard
    
    This dashboard presents the results of water quality analysis performed on data from various sources.
    
    #### Data Sources:
    - Original data from `excelnew.xlsx`
    - 65 rows of water quality measurements
    - 4 columns of parameters
    
    #### Analysis Process:
    1. Data loading and cleaning
    2. Statistical analysis of water quality parameters
    3. Visualization creation to identify patterns and trends
    4. Processing and storing of results for dashboard presentation
    
    #### Dashboard Features:
    - Interactive data exploration
    - Visualization gallery
    - Statistical insights and recommendations
    - Downloadable processed data
    
    #### Tools Used:
    - Python for data processing
    - Pandas for data manipulation
    - Matplotlib and Plotly for visualizations
    - Streamlit for dashboard creation
    
    For more information, contact the data analysis team.
    """)

# Footer
st.markdown("---")
st.markdown("Water Quality Analysis Dashboard | Created with Streamlit")

