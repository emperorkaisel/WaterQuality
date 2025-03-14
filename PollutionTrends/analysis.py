import pandas as pd
import numpy as np
from scipy import stats

def calculate_statistics(df):
    """
    Calculate key statistics for each pollutant.
    """
    stats_dict = {}
    pollutants = ['Proportion bod5', 'Proportion nh3n', 'Proportion SS']
    
    for pollutant in pollutants:
        pollutant_stats = {
            'mean': df[pollutant].mean(),
            'median': df[pollutant].median(),
            'std_dev': df[pollutant].std(),
            'min': df[pollutant].min(),
            'max': df[pollutant].max(),
            'range': df[pollutant].max() - df[pollutant].min()
        }
        stats_dict[pollutant] = pollutant_stats
    
    return stats_dict

def calculate_correlations(df):
    """
    Calculate correlations between different pollutants.
    """
    pollutants = ['Proportion bod5', 'Proportion nh3n', 'Proportion SS']
    corr_matrix = df[pollutants].corr()
    
    return corr_matrix

def analyze_trends(df):
    """
    Analyze trends in pollutant levels over time.
    Returns a dictionary with trend information for each pollutant.
    """
    yearly_data = df.groupby('year').agg({
        'Proportion bod5': 'mean',
        'Proportion nh3n': 'mean',
        'Proportion SS': 'mean'
    }).reset_index()
    
    trends = {}
    pollutants = ['Proportion bod5', 'Proportion nh3n', 'Proportion SS']
    
    for pollutant in pollutants:
        # Calculate trend using linear regression
        x = yearly_data['year']
        y = yearly_data[pollutant]
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Determine trend direction
        if slope > 0.5:
            direction = "strong increase"
        elif slope > 0.1:
            direction = "moderate increase"
        elif slope > 0:
            direction = "slight increase"
        elif slope > -0.1:
            direction = "slight decrease"
        elif slope > -0.5:
            direction = "moderate decrease"
        else:
            direction = "strong decrease"
        
        # Calculate percentage change from start to end
        start_value = yearly_data[pollutant].iloc[0]
        end_value = yearly_data[pollutant].iloc[-1]
        pct_change = ((end_value - start_value) / start_value) * 100 if start_value != 0 else float('inf')
        
        trends[pollutant] = {
            'slope': slope,
            'direction': direction,
            'r_squared': r_value**2,
            'p_value': p_value,
            'pct_change': pct_change
        }
        
        # Add simplified key for ease of access in app.py
        if pollutant == 'Proportion bod5':
            trends['bod5'] = trends[pollutant]
        elif pollutant == 'Proportion nh3n':
            trends['nh3n'] = trends[pollutant]
        elif pollutant == 'Proportion SS':
            trends['SS'] = trends[pollutant] 
    
    return trends

def get_trend_summary(trends):
    """
    Generate a summary of the trends for display.
    """
    summary = {}
    
    for pollutant, data in trends.items():
        # Skip duplicate entries created by our simplified keys
        if pollutant in ['bod5', 'nh3n', 'SS'] and f'Proportion {pollutant.lower()}' in trends:
            continue
            
        name = pollutant.replace('Proportion ', '')
        
        if data['p_value'] < 0.05:
            significance = "statistically significant"
        else:
            significance = "not statistically significant"
            
        trend_strength = f"R² = {data['r_squared']:.2f}"
        
        if data['pct_change'] == float('inf'):
            pct_text = "percentage change could not be calculated (starting value was zero)"
        else:
            pct_text = f"{data['pct_change']:.1f}% change from 2000 to 2021"
        
        summary[name] = {
            'description': f"{name} shows a {data['direction']} over time, which is {significance}.",
            'strength': trend_strength,
            'change': pct_text
        }
    
    # Make sure we have an entry for SS case-insensitive
    if 'ss' in summary and 'SS' not in summary:
        summary['SS'] = summary['ss']
    
    return summary

def identify_potential_causes(trends):
    """
    Based on the observed trends, identify potential underlying causes.
    This is a simplified example based on general environmental knowledge.
    Real analysis would require more context about the specific location and policies.
    """
    causes = {}
    
    # BOD5 (Biochemical Oxygen Demand)
    bod_trend = trends['Proportion bod5']['direction']
    if 'increase' in bod_trend:
        causes['bod5'] = [
            "Increased organic waste discharge from industrial sources",
            "Agricultural runoff containing organic matter",
            "Ineffective wastewater treatment processes",
            "Urban expansion leading to more sewage discharge"
        ]
    else:
        causes['bod5'] = [
            "Improved wastewater treatment technologies",
            "Stricter industrial discharge regulations",
            "Better agricultural practices reducing runoff",
            "Implementation of water quality management programs"
        ]
    
    # NH3N (Ammonia Nitrogen)
    nh3n_trend = trends['Proportion nh3n']['direction']
    if 'increase' in nh3n_trend:
        causes['nh3n'] = [
            "Increased fertilizer use in agriculture",
            "Livestock waste management issues",
            "Industrial processes releasing ammonia compounds",
            "Insufficient nitrogen removal in wastewater treatment"
        ]
    else:
        causes['nh3n'] = [
            "Improved nitrogen removal in wastewater treatment",
            "Better agricultural fertilizer management",
            "Reduced livestock density or improved waste management",
            "Industrial emission controls"
        ]
    
    # SS (Suspended Solids)
    ss_trend = trends['Proportion SS']['direction']
    if 'increase' in ss_trend:
        causes['ss'] = [
            "Increased soil erosion due to deforestation or land use changes",
            "Construction activities increasing sediment runoff",
            "Mining operations affecting water quality",
            "Reduced riparian buffer zones along waterways"
        ]
    else:
        causes['ss'] = [
            "Improved erosion control measures",
            "Reforestation or better land management practices",
            "Enhanced sedimentation control in construction and mining",
            "Establishment of riparian buffer zones"
        ]
    
    return causes
