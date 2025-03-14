import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Custom color palette based on requirements
COLORS = {
    'primary': '#2C5282',  # navy blue
    'secondary': '#38A169',  # forest green
    'background': '#F7FAFC',  # off-white
    'text': '#2D3748',  # dark grey
    'accent': '#E53E3E',  # alert red
    'bod5': '#2C5282',  # primary for BOD5
    'nh3n': '#38A169',  # secondary for NH3N
    'ss': '#E53E3E'  # accent for SS
}

def create_yearly_trend_plot(df):
    """
    Create a line chart showing yearly trends for all pollutants.
    """
    yearly_data = df.groupby('year').agg({
        'Proportion bod5': 'mean',
        'Proportion nh3n': 'mean',
        'Proportion SS': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=yearly_data['year'], 
        y=yearly_data['Proportion bod5'],
        mode='lines+markers',
        name='BOD5',
        line=dict(color=COLORS['bod5'], width=2),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_data['year'], 
        y=yearly_data['Proportion nh3n'],
        mode='lines+markers',
        name='NH3N',
        line=dict(color=COLORS['nh3n'], width=2),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_data['year'], 
        y=yearly_data['Proportion SS'],
        mode='lines+markers',
        name='SS',
        line=dict(color=COLORS['ss'], width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Yearly Pollution Proportion Trends (2000-2021)',
        xaxis_title='Year',
        yaxis_title='Proportion (%)',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    return fig

def create_category_trend_plots(df, pollutant):
    """
    Create line charts showing trends for each category (Location A, B, C).
    """
    # Handle case sensitivity issues by standardizing the column name
    if pollutant.lower() == 'ss':
        column_name = 'Proportion SS'
    else:
        column_name = f'Proportion {pollutant.lower()}'
    
    category_data = df.pivot_table(
        index='year', 
        columns='category',
        values=column_name
    ).reset_index()
    
    fig = go.Figure()
    
    for category in ['Location A', 'Location B', 'Location C']:
        fig.add_trace(go.Scatter(
            x=category_data['year'],
            y=category_data[category],
            mode='lines+markers',
            name=category,
            marker=dict(size=8)
        ))
    
    pollutant_name = 'BOD5' if pollutant.lower() == 'bod5' else 'NH3N' if pollutant.lower() == 'nh3n' else 'SS'
    
    fig.update_layout(
        title=f'{pollutant_name} Proportion by Location (2000-2021)',
        xaxis_title='Year',
        yaxis_title=f'{pollutant_name} Proportion (%)',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    return fig

def create_stacked_area_chart(df):
    """
    Create a stacked area chart to show the composition of pollutants over time.
    """
    yearly_data = df.groupby('year').agg({
        'Proportion bod5': 'mean',
        'Proportion nh3n': 'mean',
        'Proportion SS': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=yearly_data['year'],
        y=yearly_data['Proportion bod5'],
        name='BOD5',
        mode='lines',
        line=dict(width=0.5, color=COLORS['bod5']),
        stackgroup='one',
        groupnorm='percent'
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_data['year'],
        y=yearly_data['Proportion nh3n'],
        name='NH3N',
        mode='lines',
        line=dict(width=0.5, color=COLORS['nh3n']),
        stackgroup='one'
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_data['year'],
        y=yearly_data['Proportion SS'],
        name='SS',
        mode='lines',
        line=dict(width=0.5, color=COLORS['ss']),
        stackgroup='one'
    ))
    
    fig.update_layout(
        title='Relative Composition of Pollutants (2000-2021)',
        xaxis_title='Year',
        yaxis_title='Percentage (%)',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500
    )
    
    return fig

def create_heatmap(corr_matrix):
    """
    Create a heatmap to visualize correlations between pollutants.
    """
    # Rename columns for better display
    corr_matrix_display = corr_matrix.copy()
    corr_matrix_display.columns = ['BOD5', 'NH3N', 'SS']
    corr_matrix_display.index = ['BOD5', 'NH3N', 'SS']
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix_display.values,
        x=corr_matrix_display.columns,
        y=corr_matrix_display.index,
        colorscale='RdBu_r',
        zmin=-1, zmax=1,
        colorbar=dict(title='Correlation'),
        text=corr_matrix_display.round(2).values,
        texttemplate="%{text}",
        textfont={"size":14}
    ))
    
    fig.update_layout(
        title='Correlation Between Pollutants',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_box_plots(df):
    """
    Create box plots to visualize the distribution of each pollutant.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=df['Proportion bod5'],
        name='BOD5',
        marker_color=COLORS['bod5'],
        boxmean=True
    ))
    
    fig.add_trace(go.Box(
        y=df['Proportion nh3n'],
        name='NH3N',
        marker_color=COLORS['nh3n'],
        boxmean=True
    ))
    
    fig.add_trace(go.Box(
        y=df['Proportion SS'],
        name='SS',
        marker_color=COLORS['ss'],
        boxmean=True
    ))
    
    fig.update_layout(
        title='Distribution of Pollution Proportions (2000-2021)',
        yaxis_title='Proportion (%)',
        template='plotly_white',
        height=500
    )
    
    return fig

def create_inflection_point_timeline(df, inflection_years):
    """
    Create a timeline visualization highlighting inflection points.
    """
    yearly_data = df.groupby('year').agg({
        'Proportion bod5': 'mean',
        'Proportion nh3n': 'mean',
        'Proportion SS': 'mean'
    }).reset_index()
    
    # Create three subplots, one for each pollutant
    fig = make_subplots(rows=3, cols=1, 
                        shared_xaxes=True,
                        subplot_titles=('BOD5', 'NH3N', 'SS'),
                        vertical_spacing=0.1)
    
    # Add traces for BOD5
    fig.add_trace(
        go.Scatter(
            x=yearly_data['year'], 
            y=yearly_data['Proportion bod5'],
            mode='lines+markers',
            name='BOD5',
            line=dict(color=COLORS['bod5']),
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Add traces for NH3N
    fig.add_trace(
        go.Scatter(
            x=yearly_data['year'], 
            y=yearly_data['Proportion nh3n'],
            mode='lines+markers',
            name='NH3N',
            line=dict(color=COLORS['nh3n']),
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Add traces for SS
    fig.add_trace(
        go.Scatter(
            x=yearly_data['year'], 
            y=yearly_data['Proportion SS'],
            mode='lines+markers',
            name='SS',
            line=dict(color=COLORS['ss']),
            showlegend=False
        ),
        row=3, col=1
    )
    
    # Highlight inflection points
    if not inflection_years.empty:
        for index, row in inflection_years.iterrows():
            year = row['year']
            
            # BOD5 inflection point
            if abs(row['bod5_change']) > 20:
                fig.add_trace(
                    go.Scatter(
                        x=[year],
                        y=[row['Proportion bod5']],
                        mode='markers',
                        marker=dict(
                            symbol='star',
                            size=12,
                            color='black',
                            line=dict(width=2, color=COLORS['bod5'])
                        ),
                        name=f'Inflection {year}',
                        showlegend=False
                    ),
                    row=1, col=1
                )
            
            # NH3N inflection point
            if abs(row['nh3n_change']) > 20:
                fig.add_trace(
                    go.Scatter(
                        x=[year],
                        y=[row['Proportion nh3n']],
                        mode='markers',
                        marker=dict(
                            symbol='star',
                            size=12,
                            color='black',
                            line=dict(width=2, color=COLORS['nh3n'])
                        ),
                        name=f'Inflection {year}',
                        showlegend=False
                    ),
                    row=2, col=1
                )
            
            # SS inflection point
            if abs(row['ss_change']) > 20:
                fig.add_trace(
                    go.Scatter(
                        x=[year],
                        y=[row['Proportion SS']],
                        mode='markers',
                        marker=dict(
                            symbol='star',
                            size=12,
                            color='black',
                            line=dict(width=2, color=COLORS['ss'])
                        ),
                        name=f'Inflection {year}',
                        showlegend=False
                    ),
                    row=3, col=1
                )
    
    fig.update_layout(
        title='Critical Inflection Points in Pollution Trends (2000-2021)',
        height=700,
        template='plotly_white'
    )
    
    fig.update_yaxes(title_text="Proportion (%)", row=1, col=1)
    fig.update_yaxes(title_text="Proportion (%)", row=2, col=1)
    fig.update_yaxes(title_text="Proportion (%)", row=3, col=1)
    fig.update_xaxes(title_text="Year", row=3, col=1)
    
    return fig
