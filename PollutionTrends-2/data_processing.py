import pandas as pd
import numpy as np
from datetime import datetime

def load_pollution_data():
    """
    Load and preprocess the pollution proportion data.
    This function creates a structured DataFrame from the raw data.
    """
    # Load data from CSV file (which was generated from Excel file)
    try:
        df = pd.read_csv('data.csv')
        
        # Check column names to debug
        print("Data columns:", df.columns.tolist())
        
        # Rename columns to match the structure expected by the app
        df = df.rename(columns={
            'Date': 'YEAR',
            'BOD5': 'Proportion bod5',
            'NH3N': 'Proportion nh3n',
            'SS': 'Proportion SS'
        })
        
        # Convert year to datetime for proper time series analysis
        df['YEAR'] = pd.to_datetime(df['YEAR'])
        
        # Add a year column for easier grouping
        df['year'] = df['YEAR'].dt.year
        
    except Exception as e:
        print(f"Error loading data: {e}")
        # Return an empty DataFrame with the expected structure
        df = pd.DataFrame(columns=[
            'YEAR', 'Proportion bod5', 'Proportion nh3n', 'Proportion SS', 'year'
        ])
    
    # The new dataset doesn't have multiple entries per year like the old one
    # So we'll create a single location for consistency with the rest of the app
    df['category'] = 'Location A'
    
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
