#!/usr/bin/env python3
"""
Water Quality Analysis Script
This script processes water quality data from Malaysia, performing cleaning,
statistical analysis, and visualization of BOD5, NH3N, and SS pollution parameters.
The processed data is saved for use in an interactive dashboard.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from datetime import datetime

# Set style for plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('viridis')

def load_and_clean_data(file_path='excelnew.xlsx'):
    """
    Load and clean the water quality data from Excel file.
    Args:
        file_path (str): Path to the Excel file
    Returns:
        pd.DataFrame: Cleaned dataframe with proper column names
    """
    print(f"Loading data from {file_path}...")
    # Read the Excel file
    try:
        df = pd.read_excel(file_path)
        print(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns.")
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

    # Rename columns appropriately
    if len(df.columns) >= 4:
        df.columns = ['date', 'bod5_proportion', 'nh3n_proportion', 'ss_proportion']
    else:
        print(f"Warning: Expected at least 4 columns but found {len(df.columns)}")
        # Handle variable column numbers
        cols = ['date']
        if len(df.columns) > 1:
            cols.extend(['bod5_proportion', 'nh3n_proportion', 'ss_proportion'][:len(df.columns)-1])
        df.columns = cols

    # Convert date column to datetime
    try:
        df['date'] = pd.to_datetime(df['date'])
        print("Date column converted to datetime format.")
    except:
        print("Warning: Could not convert date column to datetime format.")

    # Drop rows with all NaN values
    df = df.dropna(how='all')

    # Handle any remaining missing values
    for col in df.columns[1:]:  # Skip date column
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill NaN values with column means
    df = df.fillna(df.mean())

    # Remove any potential outliers (values beyond 3 std deviations)
    for col in df.columns[1:]:
        mean, std = df[col].mean(), df[col].std()
        df = df[np.abs(df[col] - mean) <= 3 * std]

    # Add year and month columns for easier analysis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    print(f"Data cleaning complete. Final dataset has {df.shape[0]} rows.")
    return df

def perform_statistical_analysis(df):
    """
    Perform statistical analysis on water quality parameters.
    Args:
        df (pd.DataFrame): Cleaned dataframe
    Returns:
        dict: Dictionary containing statistical results
    """
    print("Performing statistical analysis...")
    stats_results = {}

    # Basic descriptive statistics
    stats_results['descriptive'] = df[['bod5_proportion', 'nh3n_proportion', 'ss_proportion']].describe()

    # Correlation analysis
    stats_results['correlation'] = df[['bod5_proportion', 'nh3n_proportion', 'ss_proportion']].corr()

    # Analyze trends over time (annual)
    annual_stats = df.groupby('year')[['bod5_proportion', 'nh3n_proportion', 'ss_proportion']].agg(
        ['mean', 'median', 'std', 'min', 'max']
    )
    stats_results['annual'] = annual_stats

    # Check for seasonality (monthly patterns)
    monthly_stats = df.groupby('month')[['bod5_proportion', 'nh3n_proportion', 'ss_proportion']].mean()
    stats_results['monthly'] = monthly_stats

    # Perform basic trend analysis
    # Simple linear regression for each parameter over time
    trend_results = {}
    for param in ['bod5_proportion', 'nh3n_proportion', 'ss_proportion']:
        # Convert dates to numeric (days since first date)
        date_numeric = (df['date'] - df['date'].min()).dt.days
        slope, intercept, r_value, p_value, std_err = stats.linregress(date_numeric, df[param])
        trend_results[param] = {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value**2,
            'p_value': p_value,
            'trend_direction': 'increasing' if slope > 0 else 'decreasing',
            'significant': p_value < 0.05
        }
    stats_results['trends'] = trend_results

    print("Statistical analysis complete.")
    return stats_results

def create_visualizations(df, stats_results, output_dir='visualizations'):
    """
    Create visualizations of water quality data.
    Args:
        df (pd.DataFrame): Cleaned dataframe
        stats_results (dict): Statistical analysis results
        output_dir (str): Directory to save visualizations
    """
    print("Creating visualizations...")
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Time series plots for each parameter
    plt.figure(figsize=(14, 8), constrained_layout=True)
    for i, param in enumerate(['bod5_proportion', 'nh3n_proportion', 'ss_proportion']):
        plt.subplot(3, 1, i+1)
        plt.plot(df['date'], df[param], label=param, linewidth=1.5)
        
        # Add trend line
        date_min = df['date'].min()
        date_numeric = (df['date'] - date_min).dt.days
        slope = stats_results['trends'][param]['slope']
        intercept = stats_results['trends'][param]['intercept']
        trend_x = np.linspace(date_numeric.min(), date_numeric.max(), 100)
        trend_dates = date_min + pd.to_timedelta(trend_x, unit='D')
        plt.plot(trend_dates, intercept + slope * trend_x, 'r--', 
                 label=f"Trend: {'Increasing' if slope > 0 else 'Decreasing'}")
        
        plt.title(f"{param.replace('_', ' ').title()} Over Time")
        plt.ylabel('Proportion')
        plt.legend()
    plt.savefig(f"{output_dir}/time_series_trends.png", dpi=300)

    # Correlation heatmap
    corr_df = stats_results['correlation'].rename(columns={
        'bod5_proportion': 'BOD5', 
        'nh3n_proportion': 'NH3N', 
        'ss_proportion': 'SS'
    }).set_index(pd.Index(['BOD5', 'NH3N', 'SS']))

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1, 
                annot_kws={"size": 12})
    plt.title('Correlation Between Water Quality Parameters', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(f"{output_dir}/correlation_heatmap.png", dpi=300)

    # Annual trends
    annual_means = df.groupby('year')[['bod5_proportion', 'nh3n_proportion', 'ss_proportion']].mean()
    plt.figure(figsize=(12, 6), constrained_layout=True)
    annual_means.plot(kind='bar', figsize=(12, 6))
    plt.title('Annual Average of Water Quality Parameters', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Proportion', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/annual_trends.png", dpi=300)

    # Monthly patterns (seasonality)
    monthly_means = df.groupby('month')[['bod5_proportion', 'nh3n_proportion', 'ss_proportion']].mean()
    plt.figure(figsize=(12, 6), constrained_layout=True)
    monthly_means.plot(kind='line', marker='o', figsize=(12, 6))
    plt.title('Monthly Patterns of Water Quality Parameters', fontsize=14)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Proportion', fontsize=12)
    plt.xticks(ticks=range(1,13), 
               labels=['Jan','Feb','Mar','Apr','May','Jun',
                       'Jul','Aug','Sep','Oct','Nov','Dec'],
               fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/monthly_patterns.png", dpi=300)

    # Box plots for distribution
    plt.figure(figsize=(14, 8))
    plt.subplot(1, 3, 1)
    sns.boxplot(y=df['bod5_proportion'])
    plt.title('BOD5 Distribution', fontsize=12)
    plt.subplot(1, 3, 2)
    sns.boxplot(y=df['nh3n_proportion'])
    plt.title('NH3N Distribution', fontsize=12)
    plt.subplot(1, 3, 3)
    sns.boxplot(y=df['ss_proportion'])
    plt.title('SS Distribution', fontsize=12)
    plt.subplots_adjust(wspace=0.3)  # Add space between subplots
    plt.tight_layout()
    plt.savefig(f"{output_dir}/parameter_distributions.png", dpi=300)

    print(f"Visualizations saved to {output_dir}/ directory.")

def save_processed_data(df, stats_results, output_dir='processed_data'):
    """
    Save processed data and analysis results for dashboard use.
    Args:
        df (pd.DataFrame): Cleaned dataframe
        stats_results (dict): Statistical analysis results
        output_dir (str): Directory to save processed data
    """
    print("Saving processed data...")
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save cleaned data
    df.to_csv(f"{output_dir}/cleaned_water_quality_data.csv", index=False)

    # Save statistics as CSV
    stats_results['descriptive'].to_csv(f"{output_dir}/descriptive_statistics.csv")
    stats_results['correlation'].to_csv(f"{output_dir}/correlation_matrix.csv")
    stats_results['annual'].to_csv(f"{output_dir}/annual_statistics.csv")
    stats_results['monthly'].to_csv(f"{output_dir}/monthly_patterns.csv")

    # Save trend analysis as JSON
    import json
    with open(f"{output_dir}/trend_analysis.json", 'w') as f:
        # Convert numpy types to Python native types for JSON serialization
        serializable_trends = {}
        for param, values in stats_results['trends'].items():
            serializable_trends[param] = {
                k: (
                    float(v) if isinstance(v, (np.float64, np.float32)) else
                    bool(v) if isinstance(v, np.bool_) else
                    int(v) if isinstance(v, (np.int64, np.int32)) else
                    v
                ) for k, v in values.items()
            }
        json.dump(serializable_trends, f, indent=4)

    # Create a summary file
    with open(f"{output_dir}/analysis_summary.txt", 'w') as f:
        f.write("WATER QUALITY DATA ANALYSIS SUMMARY\n")
        f.write("===================================\n")
        f.write(f"Analysis performed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("DATASET OVERVIEW\n")
        f.write(f"Total records: {df.shape[0]}\n")
        f.write(f"Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}\n")
        f.write("TREND ANALYSIS\n")
        for param, values in stats_results['trends'].items():
            param_name = param.replace('_', ' ').upper()
            f.write(f"{param_name}:\n")
            f.write(f"  - Trend: {values['trend_direction'].title()}\n")
            f.write(f"  - Statistical significance: {'Yes' if values['significant'] else 'No'}\n")
            f.write(f"  - R-squared: {values['r_squared']:.4f}\n")
            f.write(f"  - p-value: {values['p_value']:.4f}\n")

    print(f"Processed data saved to {output_dir}/ directory.")

def main():
    """
    Main function to execute the water quality analysis workflow.
    """
    print("=== WATER QUALITY ANALYSIS ===")
    # Load and clean data
    df = load_and_clean_data()
    if df is None:
        print("Error: Could not proceed with analysis due to data loading issues.")
        return

    # Perform statistical analysis
    stats_results = perform_statistical_analysis(df)

    # Create visualizations
    create_visualizations(df, stats_results)

    # Save processed data
    save_processed_data(df, stats_results)

    print("=== ANALYSIS COMPLETE ===")
    print("The processed data and visualizations are ready for dashboard creation.")

if __name__ == "__main__":
    main()
