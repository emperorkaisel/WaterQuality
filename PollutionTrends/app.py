import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import custom modules
from data_processing import (
    load_pollution_data, 
    get_yearly_aggregated_data,
    get_yearly_data_by_category,
    detect_inflection_points
)
from visualization import (
    create_yearly_trend_plot,
    create_category_trend_plots,
    create_stacked_area_chart,
    create_heatmap,
    create_box_plots,
    create_inflection_point_timeline
)
from analysis import (
    calculate_statistics,
    calculate_correlations,
    analyze_trends,
    get_trend_summary,
    identify_potential_causes
)

# Set page config
st.set_page_config(
    page_title="Pollution Proportion Trends (2000-2021)",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for font overrides
st.markdown("""
<style>
    .main {
        font-family: "Source Sans Pro", "IBM Plex Sans", sans-serif;
    }
    h1, h2, h3 {
        font-family: "Source Sans Pro", "IBM Plex Sans", sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.title("Pollution Proportion Trends Analysis (2000-2021)")
st.markdown("""
This interactive dashboard presents trends in pollution proportions over a 21-year period (2000-2021).
The analysis focuses on three key pollutants:

- **BOD5** (Biochemical Oxygen Demand): Indicates the amount of dissolved oxygen needed by aerobic organisms to break down organic material.
- **NH3N** (Ammonia Nitrogen): A measure of ammonia compounds in water, often from agricultural runoff or sewage.
- **SS** (Suspended Solids): Particles suspended in water, affecting water clarity and quality.

Use the navigation menu on the left to explore different aspects of the data.
""")

# Load data
with st.spinner('Loading data...'):
    df = load_pollution_data()
    yearly_data = get_yearly_aggregated_data(df)
    category_data = get_yearly_data_by_category(df)
    inflection_years = detect_inflection_points(df)
    stats = calculate_statistics(df)
    corr_matrix = calculate_correlations(df)
    trends = analyze_trends(df)
    trend_summary = get_trend_summary(trends)
    potential_causes = identify_potential_causes(trends)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a section",
    ["Overview", "Pollutant Analysis", "Statistical Insights", "Critical Inflection Points", "Potential Causes"]
)

# Overview page
if page == "Overview":
    st.header("Overview of Pollution Proportions (2000-2021)")
    
    # Main trend plot
    st.subheader("Key Trends in Pollution Proportions")
    yearly_trend_plot = create_yearly_trend_plot(df)
    st.plotly_chart(yearly_trend_plot, use_container_width=True)
    
    st.markdown("""
    ### Key Observations
    
    The chart above shows the overall trends in the three monitored pollutants from 2000 to 2021.
    
    - **BOD5**: {}
    - **NH3N**: {}
    - **SS**: {}
    
    These trends suggest significant changes in environmental conditions and potentially in pollution control measures over the 21-year period.
    """.format(
        trend_summary['bod5']['description'],
        trend_summary['nh3n']['description'],
        trend_summary['SS']['description'] if 'SS' in trend_summary else "Shows varying patterns over the monitoring period."
    ))
    
    # Stacked area chart
    st.subheader("Relative Composition of Pollutants")
    stacked_area = create_stacked_area_chart(df)
    st.plotly_chart(stacked_area, use_container_width=True)
    
    st.markdown("""
    The stacked area chart above shows how the relative composition of the three pollutants has changed over time.
    This visualization helps to understand which pollutants have become more or less dominant in the overall pollution profile.
    """)

# Pollutant Analysis page
elif page == "Pollutant Analysis":
    st.header("Detailed Pollutant Analysis")
    
    # Pollutant selector
    pollutant = st.selectbox(
        "Select a pollutant to analyze:",
        ["BOD5", "NH3N", "SS"]
    )
    
    # Convert display name to column name
    if pollutant.lower() == 'ss':
        column_name = 'Proportion SS'
    else:
        column_name = f"Proportion {pollutant.lower()}"
    
    # Display trend by category
    st.subheader(f"{pollutant} Trends by Location")
    category_plot = create_category_trend_plots(df, pollutant)
    st.plotly_chart(category_plot, use_container_width=True)
    
    # Determine which key to use in trend_summary
    trend_key = pollutant.lower() if pollutant.lower() in trend_summary else 'SS' if pollutant == 'SS' else pollutant.lower()
    
    st.markdown(f"""
    ### {pollutant} Analysis
    
    The chart above shows how {pollutant} levels have varied across different locations from 2000 to 2021.
    This can help identify whether pollution trends are consistent across all monitoring sites or if certain locations
    experience unique patterns.
    
    **Key Statistics for {pollutant}**:
    - Average: {stats[column_name]['mean']:.2f}%
    - Median: {stats[column_name]['median']:.2f}%
    - Standard Deviation: {stats[column_name]['std_dev']:.2f}%
    - Range: {stats[column_name]['min']:.2f}% to {stats[column_name]['max']:.2f}%
    
    **Trend Analysis**:
    {trend_summary[trend_key]['description'] if trend_key in trend_summary else "Shows varying patterns across the monitoring period."}
    {trend_summary[trend_key]['strength'] if trend_key in trend_summary else ""}
    {trend_summary[trend_key]['change'] if trend_key in trend_summary else ""}
    """)
    
    # Box plot for selected pollutant
    st.subheader(f"{pollutant} Distribution")
    
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df[column_name],
        name=pollutant,
        boxmean=True
    ))
    
    fig.update_layout(
        title=f'Distribution of {pollutant} Proportions (2000-2021)',
        yaxis_title='Proportion (%)',
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    The box plot above shows the distribution of {pollutant} values across the entire dataset.
    This helps visualize the central tendency, variability, and potential outliers in the data.
    """)

# Statistical Insights page
elif page == "Statistical Insights":
    st.header("Statistical Insights")
    
    # Display correlation heatmap
    st.subheader("Correlation Between Pollutants")
    heatmap = create_heatmap(corr_matrix)
    st.plotly_chart(heatmap, use_container_width=True)
    
    st.markdown("""
    The correlation heatmap shows the strength of relationships between different pollutants.
    
    - A value close to 1 indicates a strong positive correlation (both pollutants increase together).
    - A value close to -1 indicates a strong negative correlation (one increases as the other decreases).
    - A value close to 0 indicates little to no correlation.
    
    These relationships can provide insights into potential common sources or environmental factors affecting multiple pollutants.
    """)
    
    # Display box plots for distribution
    st.subheader("Distribution of Pollution Proportions")
    box_plots = create_box_plots(df)
    st.plotly_chart(box_plots, use_container_width=True)
    
    st.markdown("""
    The box plots show the distribution of each pollutant across the entire dataset period (2000-2021).
    
    Key elements of each box plot:
    - The box represents the interquartile range (25th to 75th percentile).
    - The line inside the box is the median.
    - The whiskers extend to the minimum and maximum values within 1.5 times the interquartile range.
    - Points outside the whiskers are potential outliers.
    
    This visualization helps understand the central tendency and variability of each pollutant.
    """)
    
    # Show summary statistics in a table
    st.subheader("Summary Statistics")
    
    # Create a DataFrame for display
    stats_df = pd.DataFrame({
        'Statistic': ['Mean', 'Median', 'Standard Deviation', 'Minimum', 'Maximum', 'Range'],
        'BOD5 (%)': [
            f"{stats['Proportion bod5']['mean']:.2f}",
            f"{stats['Proportion bod5']['median']:.2f}",
            f"{stats['Proportion bod5']['std_dev']:.2f}",
            f"{stats['Proportion bod5']['min']:.2f}",
            f"{stats['Proportion bod5']['max']:.2f}",
            f"{stats['Proportion bod5']['range']:.2f}"
        ],
        'NH3N (%)': [
            f"{stats['Proportion nh3n']['mean']:.2f}",
            f"{stats['Proportion nh3n']['median']:.2f}",
            f"{stats['Proportion nh3n']['std_dev']:.2f}",
            f"{stats['Proportion nh3n']['min']:.2f}",
            f"{stats['Proportion nh3n']['max']:.2f}",
            f"{stats['Proportion nh3n']['range']:.2f}"
        ],
        'SS (%)': [
            f"{stats['Proportion SS']['mean']:.2f}",
            f"{stats['Proportion SS']['median']:.2f}",
            f"{stats['Proportion SS']['std_dev']:.2f}",
            f"{stats['Proportion SS']['min']:.2f}",
            f"{stats['Proportion SS']['max']:.2f}",
            f"{stats['Proportion SS']['range']:.2f}"
        ]
    })
    
    st.table(stats_df)

# Critical Inflection Points page
elif page == "Critical Inflection Points":
    st.header("Critical Inflection Points")
    
    st.markdown("""
    Inflection points represent years with significant changes in pollution trends.
    These points often correspond to important environmental events, policy changes, or technological advancements
    that affected pollution levels.
    
    The chart below highlights years where pollutant proportions changed by more than 20% compared to the previous year.
    """)
    
    # Display inflection points timeline
    timeline_plot = create_inflection_point_timeline(df, inflection_years)
    st.plotly_chart(timeline_plot, use_container_width=True)
    
    # Display table of inflection years
    if not inflection_years.empty:
        st.subheader("Significant Change Years")
        
        # Create a more readable table
        inflection_table = pd.DataFrame({
            'Year': inflection_years['year'],
            'BOD5 Change (%)': inflection_years['bod5_change'].round(2),
            'NH3N Change (%)': inflection_years['nh3n_change'].round(2),
            'SS Change (%)': inflection_years['ss_change'].round(2)
        })
        
        st.table(inflection_table)
        
        st.markdown("""
        The table above lists the years with significant changes in at least one pollutant.
        The percentage values represent the year-over-year change in each pollutant's proportion.
        """)
    else:
        st.info("No major inflection points were detected in the data.")

# Potential Causes page
elif page == "Potential Causes":
    st.header("Potential Underlying Causes")
    
    st.markdown("""
    Based on the observed trends in pollution proportions, we can identify potential underlying causes
    that may have contributed to the changes over time. 
    
    These potential causes are based on general environmental knowledge and typical factors that affect
    water pollution. A more precise analysis would require additional contextual information about the
    specific location, relevant policies, and local industrial and agricultural activities.
    """)
    
    # Create tabs for each pollutant
    tab1, tab2, tab3 = st.tabs(["BOD5", "NH3N", "SS"])
    
    with tab1:
        st.subheader("Biochemical Oxygen Demand (BOD5)")
        st.markdown(f"""
        **Trend Summary**: {trend_summary['bod5']['description']}
        
        **Potential Causes**:
        """)
        
        for cause in potential_causes['bod5']:
            st.markdown(f"- {cause}")
        
        st.markdown("""
        **About BOD5**:
        
        Biochemical Oxygen Demand (BOD5) is a measure of the amount of dissolved oxygen needed by aerobic organisms
        to break down organic material in water over a 5-day period. High BOD5 levels indicate higher amounts of
        biodegradable organic matter, which can deplete oxygen levels in water bodies, potentially harming aquatic life.
        
        Common sources include:
        - Municipal and industrial wastewater
        - Agricultural runoff
        - Food processing waste
        - Decaying plant and animal matter
        """)
    
    with tab2:
        st.subheader("Ammonia Nitrogen (NH3N)")
        st.markdown(f"""
        **Trend Summary**: {trend_summary['nh3n']['description']}
        
        **Potential Causes**:
        """)
        
        for cause in potential_causes['nh3n']:
            st.markdown(f"- {cause}")
        
        st.markdown("""
        **About NH3N**:
        
        Ammonia Nitrogen (NH3N) refers to nitrogen in the form of ammonia compounds in water.
        High levels can be toxic to aquatic organisms, especially fish. NH3N can also contribute
        to eutrophication when it converts to nitrates, causing excessive algae growth.
        
        Common sources include:
        - Agricultural fertilizers
        - Animal waste from livestock operations
        - Municipal wastewater and sewage
        - Industrial processes, particularly food processing
        - Natural decomposition of organic nitrogen compounds
        """)
    
    with tab3:
        st.subheader("Suspended Solids (SS)")
        st.markdown(f"""
        **Trend Summary**: {trend_summary['SS']['description'] if 'SS' in trend_summary else "Shows varying patterns over the monitoring period, with significant fluctuations between locations."}
        
        **Potential Causes**:
        """)
        
        if 'ss' in potential_causes:
            for cause in potential_causes['ss']:
                st.markdown(f"- {cause}")
        else:
            st.markdown("""
            - Improved erosion control measures in some areas
            - Reforestation or better land management practices
            - Enhanced sedimentation control in construction and mining
            - Establishment of riparian buffer zones
            - Changes in precipitation patterns affecting sediment transport
            """)
        
        st.markdown("""
        **About SS**:
        
        Suspended Solids (SS) are particles that remain suspended in water and do not dissolve.
        High levels of suspended solids can reduce water clarity, increase water temperature by absorbing
        more sunlight, and decrease oxygen levels. They can also clog fish gills and smother aquatic habitats.
        
        Common sources include:
        - Soil erosion from construction, agriculture, and deforestation
        - Urban runoff carrying sediment from roads and developed areas
        - Industrial discharges
        - Mining operations
        - Natural processes like stream bank erosion
        """)

# Footer 
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>Pollution Proportion Trends Analysis Dashboard (2000-2021)</p>
    <p>Data visualization and analysis platform</p>
</div>
""", unsafe_allow_html=True)

# Allow users to download data
with st.sidebar.expander("Download Data"):
    st.download_button(
        label="Download Raw Data (CSV)",
        data=df.to_csv(index=False),
        file_name="pollution_data_2000_2021.csv",
        mime="text/csv"
    )
    
    st.download_button(
        label="Download Yearly Aggregated Data (CSV)",
        data=yearly_data.to_csv(index=False),
        file_name="yearly_pollution_data_2000_2021.csv",
        mime="text/csv"
    )
