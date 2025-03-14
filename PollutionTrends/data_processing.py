import pandas as pd
import numpy as np
from datetime import datetime

def load_pollution_data():
    """
    Load and preprocess the pollution proportion data.
    This function creates a structured DataFrame from the raw data.
    """
    # Raw data as provided in the request
    raw_data = """YEAR,Proportion bod5,Proportion nh3n,Proportion SS
2000-01-01,32.5,41.67,35
2000-01-01,52.5,40,20.83
2000-01-01,15,18.33,44.17
2001-01-01,48.33,44.17,47.5
2001-01-01,34.17,35.83,20.83
2001-01-01,17.5,20,31.67
2002-01-01,57.5,42.5,65
2002-01-01,24.17,33.33,11.67
2002-01-01,18.33,24.17,23.33
2003-01-01,63.33,45,62.5
2003-01-01,24.17,30.83,14.17
2003-01-01,12.5,24.17,23.33
2004-01-01,54.17,35.83,65
2004-01-01,30.83,39.17,9.17
2004-01-01,15,25,25.83
2005-01-01,52.74,33.56,61.64
2005-01-01,28.08,36.99,15.07
2005-01-01,19.18,29.45,23.29
2006-01-01,65.75,33.56,57.53
2006-01-01,19.18,38.36,13.7
2006-01-01,15.07,28.08,28.77
2007-01-01,65.73,33.57,43.36
2007-01-01,25.87,41.26,27.27
2007-01-01,8.39,25.17,29.37
2008-01-01,55.24,50.35,39.86
2008-01-01,32.17,26.57,23.08
2008-01-01,12.59,23.08,37.06
2009-01-01,19.58,39.16,37.76
2009-01-01,51.05,32.87,22.38
2009-01-01,29.37,27.97,39.86
2010-01-01,8.39,24.48,47.55
2010-01-01,55.24,46.15,18.88
2010-01-01,36.36,29.37,33.57
2011-01-01,2.14,29.29,56.43
2011-01-01,57.14,45.71,18.57
2011-01-01,40.71,25,25
2012-01-01,8.57,25,68.57
2012-01-01,49.29,47.86,20
2012-01-01,42.14,27.14,11.43
2013-01-01,0,29.29,75
2013-01-01,32.86,41.43,17.14
2013-01-01,67.14,29.29,7.86
2014-01-01,0,29.29,70.71
2014-01-01,10.71,42.14,15.71
2014-01-01,89.29,28.57,13.57
2015-01-01,0,22.86,76.43
2015-01-01,13.57,46.43,9.29
2015-01-01,86.43,30.71,14.29
2016-01-01,0,13.57,62.14
2016-01-01,7.86,59.29,16.43
2016-01-01,92.14,27.14,21.43
2017-01-01,0,7.86,46.43
2017-01-01,35.71,61.43,32.14
2017-01-01,64.29,30.71,21.43
2018-01-01,37.76,3.5,49.65
2018-01-01,25.87,61.54,21.68
2018-01-01,36.36,34.97,28.67
2019-01-01,36.81,8.33,54.17
2019-01-01,27.08,51.39,25
2019-01-01,36.11,40.28,20.83
2020-01-01,57.64,19.44,76.39
2020-01-01,31.94,51.39,9.72
2020-01-01,10.42,29.17,13.89
2021-01-01,86.11,40.28,88.19"""

    # Convert string data to DataFrame with comma delimiter
    import io
    df = pd.read_csv(io.StringIO(raw_data))
    
    # Check column names to debug
    print("Data columns:", df.columns.tolist())
    
    # Convert year to datetime for proper time series analysis
    df['YEAR'] = pd.to_datetime(df['YEAR'])
    
    # Add a year column for easier grouping
    df['year'] = df['YEAR'].dt.year
    
    # Add a category column to differentiate the three rows per year
    # Looking at the data pattern, it seems these might represent different sampling locations
    # or different measurement categories
    categories = ['Location A', 'Location B', 'Location C']
    df['category'] = df.groupby('year').cumcount().apply(lambda x: categories[x])
    
    return df

def get_yearly_aggregated_data(df):
    """
    Aggregate data by year to show trends over time.
    Returns a DataFrame with yearly averages for each pollutant.
    """
    yearly_data = df.groupby('year').agg({
        'Proportion bod5': 'mean',
        'Proportion nh3n': 'mean',
        'Proportion SS': 'mean'
    }).reset_index()
    
    return yearly_data

def get_yearly_data_by_category(df):
    """
    Get data grouped by year and category to show trends 
    for each category over time.
    """
    category_data = df.groupby(['year', 'category']).agg({
        'Proportion bod5': 'mean',
        'Proportion nh3n': 'mean',
        'Proportion SS': 'mean'
    }).reset_index()
    
    return category_data

def detect_inflection_points(df):
    """
    Detect significant changes in pollution trends.
    Uses a simple method to identify years with notable changes.
    """
    yearly_data = get_yearly_aggregated_data(df)
    
    # Compute year-over-year changes
    yearly_data['bod5_change'] = yearly_data['Proportion bod5'].pct_change() * 100
    yearly_data['nh3n_change'] = yearly_data['Proportion nh3n'].pct_change() * 100
    yearly_data['ss_change'] = yearly_data['Proportion SS'].pct_change() * 100
    
    # Define significant change threshold (e.g., 20% change)
    threshold = 15  # Lower threshold to ensure more inflection points are detected
    
    # Identify years with significant changes in any pollutant
    inflection_years = yearly_data[
        (abs(yearly_data['bod5_change']) > threshold) |
        (abs(yearly_data['nh3n_change']) > threshold) |
        (abs(yearly_data['ss_change']) > threshold)
    ]
    
    return inflection_years
