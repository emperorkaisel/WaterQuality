# Water Quality Dynamics in Malaysia: Statistical Trends and Policy Implications

## Project Overview

This project analyzes the statistical trends and policy implications of water quality parameters in Malaysia, focusing on Biochemical Oxygen Demand (BOD5), Ammoniacal Nitrogen (NH3N), and Suspended Solids (SS) pollution. Through comprehensive data analysis and interactive visualization, this project aims to provide insights for sustainable urban development and water resource management in Malaysia.

The interactive dashboard presents historical trends, statistical analyses, and predictive modeling using the deepseek-r1 model to forecast future water quality dynamics. These insights can help policymakers, environmental scientists, and urban planners make informed decisions about water quality management strategies.

## Technologies Used

- **Python**: For data cleaning, processing, statistical analysis, and visualization preparation
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib/Seaborn**: Statistical visualizations
- **HTML/CSS**: Dashboard structure and styling
- **JavaScript**: Interactive features implementation
- **Chart.js**: Interactive data visualizations on the dashboard
- **Bootstrap**: Responsive design framework
- **deepseek-r1**: AI model for water quality prediction

## Project Structure

```
water-quality-dynamics/
│
├── excelnew.xlsx                   # Raw water quality dataset
├── water_quality_analysis.py       # Python script for data cleaning and analysis
├── water_quality_dashboard.html    # Interactive HTML dashboard
├── dashboard.js                    # JavaScript functionality for the dashboard
├── processed_data/                 # Directory containing processed datasets
│   ├── clean_data.csv              # Cleaned water quality data
│   ├── trend_analysis.csv          # Results of trend analysis
│   └── prediction_results.csv      # Model predictions
├── assets/                         # Static assets for the dashboard
│   ├── css/                        # CSS styling files
│   └── images/                     # Images used in the dashboard
└── README.md                       # Project documentation
```

## Installation Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd water-quality-dynamics
   ```

2. **Set up Python environment**:
   ```bash
   # Create and activate a virtual environment (optional but recommended)
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   
   # Install required packages
   pip install pandas numpy matplotlib seaborn scikit-learn
   ```

3. **Install deepseek-r1 model** (if not already installed):
   ```bash
   # Follow the installation instructions for deepseek-r1 from official documentation
   pip install deepseek-r1
   ```

## Usage Instructions

### Data Analysis

1. Run the water quality analysis script:
   ```bash
   python water_quality_analysis.py
   ```
   This script will:
   - Clean and preprocess the raw data from `excelnew.xlsx`
   - Perform statistical analysis on water quality parameters
   - Generate visualizations for trends over time
   - Save processed data for the dashboard

### Interactive Dashboard

1. Open the dashboard in a web browser:
   ```bash
   # Either open directly from file explorer
   # Or use a local server
   python -m http.server
   # Then navigate to http://localhost:8000/water_quality_dashboard.html
   ```

2. Use the dashboard controls to:
   - Select different time periods for analysis
   - View trends for specific water quality parameters
   - Explore correlations between parameters
   - Review prediction results

## Dashboard Features

The interactive dashboard offers the following features:

1. **Overview Panel**: Summary statistics and key insights about water quality parameters.

2. **Time Series Analysis**: Interactive charts showing trends of BOD5, NH3N, and SS over time with the ability to zoom and filter by time range.

3. **Statistical Insights**: Displays statistical metrics including:
   - Mean, median, and standard deviation
   - Seasonal patterns
   - Correlation analysis between parameters

4. **Policy Implications**: Contextualizes the data within Malaysian environmental policies and highlights areas of concern.

5. **Prediction Module**: Shows predictions from the deepseek-r1 model for future water quality trends.

6. **Geographical Distribution**: Visual representation of water quality parameters across different regions in Malaysia.

7. **Interactive Filters**: Allow users to customize the view based on:
   - Time range
   - Specific parameters
   - Region selection

## Data Analysis Methodology

Our analytical approach includes:

1. **Data Cleaning**: Handling missing values, outlier detection, and normalization of water quality parameters.

2. **Exploratory Data Analysis**: Investigating distributions, identifying patterns, and analyzing seasonal variations in water quality.

3. **Trend Analysis**: Employing statistical methods to identify long-term trends and significant changes in water quality parameters.

4. **Correlation Analysis**: Examining relationships between different water quality parameters and external factors.

5. **Statistical Testing**: Applying hypothesis tests to validate findings and ensure statistical significance.

6. **Time Series Analysis**: Using techniques such as moving averages and decomposition to understand temporal patterns.

## Gemma3 Model for Predictions

The project leverages the deepseek-r1 model, a state-of-the-art AI model for time series prediction, to forecast future water quality trends:

1. **Model Application**: The model is run locally to process historical water quality data and generate predictions.

2. **Training Process**: The model is fine-tuned on Malaysia-specific water quality data to improve prediction accuracy.

3. **Prediction Methodology**: The model considers historical patterns, seasonal variations, and correlations between parameters to generate forecasts.

4. **Validation**: Predictions are validated using historical data to ensure accuracy and reliability.

5. **Interpretation**: The dashboard presents prediction results with confidence intervals and explanations of key factors influencing the predictions.

## Future Improvements

Planned enhancements for this project include:

1. **Real-time Data Integration**: Connect to live water quality monitoring stations for real-time updates.

2. **Enhanced Prediction Models**: Incorporate additional environmental and climate factors to improve prediction accuracy.

3. **Mobile Application**: Develop a companion mobile app for on-the-go access to water quality insights.

4. **Policy Recommendation Engine**: Implement an AI-based system that can suggest specific policy interventions based on water quality trends.

5. **Community Engagement Features**: Add functionality for public reporting of water quality issues and citizen science initiatives.

6. **Expanded Geographic Coverage**: Include more regions and water bodies across Malaysia.

7. **Integration with Other Environmental Data**: Combine water quality data with other environmental metrics for a more comprehensive analysis.

## Contributing

Contributions to improve the project are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Malaysian Department of Environment for providing access to water quality data
- Contributors to the open-source libraries used in this project
- Academic advisors who provided guidance on water quality analysis methodologies

