// Water Quality Dashboard JavaScript
// Handles data loading, visualization, and interactive functionality

// Global variables for data and charts
let waterQualityData = [];
let timeSeriesChart, correlationChart, predictionChart;
let currentTimeRange = 'all'; // Default time range

// Load actual data for the dashboard from processed CSV files
function loadData() {
    // Load the actual water quality data from CSV
    return new Promise((resolve, reject) => {
        fetch('processed_data/cleaned_water_quality_data.csv')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to load data: ${response.status} ${response.statusText}`);
                }
                return response.text();
            })
            .then(csvText => {
                // Parse CSV data
                const lines = csvText.split('\n');
                const headers = lines[0].split(',');
                
                const dateIndex = headers.indexOf('Date');
                const bod5Index = headers.indexOf('BOD5');
                const nh3nIndex = headers.indexOf('NH3N');
                const ssIndex = headers.indexOf('SS');
                
                if (dateIndex === -1 || bod5Index === -1 || nh3nIndex === -1 || ssIndex === -1) {
                    throw new Error('CSV is missing required columns');
                }
                
                const data = [];
                
                for (let i = 1; i < lines.length; i++) {
                    if (lines[i].trim() === '') continue;
                    
                    const values = lines[i].split(',');
                    
                    const dateValue = values[dateIndex];
                    const bod5Value = parseFloat(values[bod5Index]);
                    const nh3nValue = parseFloat(values[nh3nIndex]);
                    const ssValue = parseFloat(values[ssIndex]);
                    
                    if (isNaN(bod5Value) || isNaN(nh3nValue) || isNaN(ssValue)) continue;
                    
                    data.push({
                    if (isNaN(bod5Value) || isNaN(nh3nValue) || isNaN(ssValue)) continue;
                    
                    try {
                        const dateObj = new Date(dateValue);
                        if (isNaN(dateObj.getTime())) {
                            console.warn(`Invalid date: ${dateValue}`);
                            continue;
                        }
                        
                        data.push({
                            date: dateObj,
                            bod5: bod5Value.toFixed(2),
                            nh3n: nh3nValue.toFixed(2),
                            ss: ssValue.toFixed(2),
                            complies: bod5Value < 2.5 && nh3nValue < 0.9 && ssValue < 40
                        });
                    } catch (e) {
                        console.warn(`Error parsing date: ${dateValue}`, e);
                    }
                fetch('processed_data/descriptive_statistics.csv')
                    .then(response => response.text())
                    .then(statsText => {
                        // Parse statistics for later use
                        window.descriptiveStats = parseDescriptiveStats(statsText);
                        resolve(data);
                    })
                    .catch(error => {
                        console.warn('Failed to load statistics, continuing with data only:', error);
                        resolve(data);
                    });
            })
            .catch(error => {
                console.error('Error loading data:', error);
                reject(error);
            });
    });
}

// Function to parse descriptive statistics CSV
function parseDescriptiveStats(csvText) {
    const lines = csvText.split('\n');
    const stats = {};
    
    // Skip header and process each line
    for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim() === '') continue;
        
        const values = lines[i].split(',');
        if (values.length >= 2) {
            const parameter = values[0].trim();
            stats[parameter] = {};
            
            // Find header positions (assumes first row has headers)
            const headers = lines[0].split(',');
            
            // Map each statistic value to its header
            for (let j = 1; j < values.length; j++) {
                if (j < headers.length) {
                    const statName = headers[j].trim();
                    const statValue = parseFloat(values[j]);
                    if (!isNaN(statValue)) {
                        stats[parameter][statName] = statValue;
                    }
                }
            }
        }
    }
    
    return stats;
}

// Filter data based on selected time range
function filterDataByTimeRange(data, range) {
    const now = new Date();
    let startDate;
    
    switch (range) {
        case '1y':
            startDate = new Date(now.getFullYear() - 1, now.getMonth(), 1);
            break;
        case '2y':
            startDate = new Date(now.getFullYear() - 2, now.getMonth(), 1);
            break;
        case '3y':
            startDate = new Date(now.getFullYear() - 3, now.getMonth(), 1);
            break;
        default: // 'all'
            return data;
    }
    
    return data.filter(item => item.date >= startDate);
}

// Create and render the time series chart
function createTimeSeriesChart(data) {
    // Option 1: Use actual visualization image if available
    const timeSeriesImageContainer = document.getElementById('timeSeriesImageContainer');
    if (timeSeriesImageContainer) {
        timeSeriesImageContainer.innerHTML = `
            <img src="visualizations/time_series_plot.png" alt="Water Quality Time Series" class="img-fluid chart-image">
        `;
    }
    
    // Option 2: Create dynamic chart with Chart.js
    const ctx = document.getElementById('timeSeriesChart');
    if (!ctx) return; // Skip if canvas not found
    
    // Extract data for charts
    const dates = data.map(item => item.date);
    const bod5Values = data.map(item => item.bod5);
    const nh3nValues = data.map(item => item.nh3n);
    const ssValues = data.map(item => item.ss);
    
    // If chart already exists, destroy it to prevent duplicates
    if (timeSeriesChart) {
        timeSeriesChart.destroy();
    }
    
    timeSeriesChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'BOD5 (mg/L)',
                    data: bod5Values.map(val => parseFloat(val)),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.3,
                    borderWidth: 2
                },
                {
                    label: 'NH3N (mg/L)',
                    data: nh3nValues.map(val => parseFloat(val)),
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.3,
                    borderWidth: 2
                },
                {
                    label: 'SS (mg/L)',
                    data: ssValues.map(val => parseFloat(val)),
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.3,
                    borderWidth: 2,
                    hidden: true // Hidden by default to reduce initial clutter
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Water Quality Parameters Over Time',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true
                    }
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'month',
                        displayFormats: {
                            month: 'MMM yyyy'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Concentration (mg/L)'
                    }
                }
            }
        }
    });
}

// Create and render the correlation chart
function createCorrelationChart(data) {
    // Option 1: Use actual visualization image if available
    const correlationImageContainer = document.getElementById('correlationImageContainer');
    if (correlationImageContainer) {
        correlationImageContainer.innerHTML = `
            <img src="visualizations/correlation_plot.png" alt="Parameter Correlation" class="img-fluid chart-image">
        `;
    }
    
    // Option 2: Create dynamic chart with Chart.js
    const ctx = document.getElementById('correlationChart');
    if (!ctx) return; // Skip if canvas not found
    
    // Prepare data for correlation chart
    const bod5Values = data.map(item => parseFloat(item.bod5));
    const nh3nValues = data.map(item => parseFloat(item.nh3n));
    
    // Calculate regression line
    const n = bod5Values.length;
    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
    
    for (let i = 0; i < n; i++) {
        sumX += bod5Values[i];
        sumY += nh3nValues[i];
        sumXY += bod5Values[i] * nh3nValues[i];
        sumX2 += bod5Values[i] * bod5Values[i];
    }
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    
    // If chart already exists, destroy it to prevent duplicates
    if (correlationChart) {
        correlationChart.destroy();
    }
    
    // Calculate correlation coefficient
    const meanX = sumX / n;
    const meanY = sumY / n;
    let numerator = 0, denominator1 = 0, denominator2 = 0;
    
    for (let i = 0; i < n; i++) {
        numerator += (bod5Values[i] - meanX) * (nh3nValues[i] - meanY);
        denominator1 += Math.pow(bod5Values[i] - meanX, 2);
        denominator2 += Math.pow(nh3nValues[i] - meanY, 2);
    }
    
    const correlationCoefficient = numerator / Math.sqrt(denominator1 * denominator2);
    
    // Create scatter chart with regression line
    correlationChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'BOD5 vs NH3N',
                    data: data.map(item => ({
                        x: parseFloat(item.bod5),
                        y: parseFloat(item.nh3n)
                    })),
                    pointBackgroundColor: 'rgba(255, 99, 132, 0.7)',
                    pointBorderColor: 'rgba(255, 99, 132, 1)',
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'Regression Line',
                    data: (() => {
                        const minX = Math.min(...bod5Values);
                        const maxX = Math.max(...bod5Values);
                        return [
                            { x: minX, y: minX * slope + intercept },
                            { x: maxX, y: maxX * slope + intercept }
                        ];
                    })(),
                    type: 'line',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    pointRadius: 0,
                    borderWidth: 2,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `BOD5 vs NH3N Correlation (r = ${correlationCoefficient.toFixed(3)})`,
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `BOD5: ${context.parsed.x.toFixed(2)}, NH3N: ${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'BOD5 (mg/L)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'NH3N (mg/L)'
                    }
                }
            }
        }
    });
}

// Create and render the prediction chart
function createPredictionChart(data) {
    // Option 1: Use actual visualization image if available
    const predictionImageContainer = document.getElementById('predictionImageContainer');
    if (predictionImageContainer) {
        predictionImageContainer.innerHTML = `
            <img src="visualizations/prediction_plot.png" alt="Trend Prediction" class="img-fluid chart-image">
        `;
    }
    
    // Option 2: Create dynamic chart with Chart.js
    const ctx = document.getElementById('predictionChart');
    if (!ctx) return; // Skip if canvas not found
    
    // Get the last 24 months of data
    const recentData = data.slice(-24);
    
    // Extract dates and BOD5 values
    const dates = recentData.map(item => item.date);
    const bod5Values = recentData.map(item => parseFloat(item.bod5));
    
    // Simple linear regression for prediction
    const xValues = Array.from(Array(24).keys()); // 0-23 representing months
    const n = xValues.length;
    
    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
    for (let i = 0; i < n; i++) {
        sumX += xValues[i];
        sumY += bod5Values[i];
        sumXY += xValues[i] * bod5Values[i];
        sumX2 += xValues[i] * xValues[i];
    }
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;
    
    // Generate prediction for next 12 months
    const lastDate = new Date(dates[dates.length - 1]);
    const predictedDates = [];
    const predictedValues = [];
    
    for (let i = 1; i <= 12; i++) {
        const nextMonth = new Date(lastDate);
        nextMonth.setMonth(lastDate.getMonth() + i);
        predictedDates.push(nextMonth);
        
        const predictedValue = intercept + slope * (n + i - 1);
        predictedValues.push(predictedValue);
    }
    
    // If chart already exists, destroy it to prevent duplicates
    if (predictionChart) {
        predictionChart.destroy();
    }
    
    // Combine actual dates and predicted dates
    const allDates = [...dates, ...predictedDates];
    
    // Create prediction chart
    predictionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: allDates,
            datasets: [
                {
                    label: 'Historical BOD5',
                    data: bod5Values.concat(Array(12).fill(null)),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.3,
                    borderWidth: 2
                },
                {
                    label: 'Predicted BOD5',
                    data: Array(24).fill(null).concat(predictedValues),
                    borderColor: 'rgba(255, 159, 64, 1)',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    borderDash: [5, 5],
                    tension: 0.3,
                    borderWidth: 2,
                    pointRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'BOD5 Trend Prediction for Next 12 Months',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        title: function(context) {
                        title: function(context) {
                            const date = context[0].label;
                            // Check if the date is a Date object before calling toLocaleString
                            if (date instanceof Date) {
                                return date.toLocaleString('en-US', { year: 'numeric', month: 'short' });
                            } else {
                                return date; // Return as is if not a Date object
                            }
                        }
                    }
                }
            },
                x: {
                    type: 'time',
                    time: {
                        unit: 'month',
                        displayFormats: {
                            month: 'MMM yyyy'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'BOD5 (mg/L)'
                    }
                }
            }
        }
    });
}

// Load analysis summary from the text file
function loadAnalysisSummary() {
    return fetch('processed_data/analysis_summary.txt')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to load analysis summary: ${response.status}`);
            }
            return response.text();
        })
        .then(text => {
            // Parse the summary text
            window.analysisSummary = text;
            
            // Update the analysis summary section in the UI
            const summaryElement = document.getElementById('analysisSummary');
            if (summaryElement) {
                // Format the text for HTML display
                const formattedText = text.replace(/\n/g, '<br>');
                summaryElement.innerHTML = formattedText;
            }
            
            // Update key findings section with brief highlights
            const findingsElement = document.getElementById('keyFindings');
            if (findingsElement) {
                // Extract key phrases for findings
                const findings = [];
                if (text.includes('trend')) {
                    const trendMatch = text.match(/trend[^.]+\./i);
                    if (trendMatch) findings.push(trendMatch[0]);
                }
                if (text.includes('correlation')) {
                    const corrMatch = text.match(/correlation[^.]+\./i);
                    if (corrMatch) findings.push(corrMatch[0]);
                }
                if (text.includes('significant')) {
                    const sigMatch = text.match(/significant[^.]+\./i);
                    if (sigMatch) findings.push(sigMatch[0]);
                }
                
                // Add findings to the page
                if (findings.length > 0) {
                    findingsElement.innerHTML = findings.map(f => `<li>${f}</li>`).join('');
                } else {
                    findingsElement.innerHTML = '<li>See full analysis summary for details.</li>';
                }
            }
            
            return text;
        })
        .catch(error => {
            console.warn('Failed to load analysis summary:', error);
            return null;
        });
}

// Update dashboard statistics
function updateStatistics(data) {
    // Use pre-calculated statistics if available, otherwise calculate from data
    let avgBOD5, avgNH3N, avgSS, trendDirection, trendPercentage;
    
    if (window.descriptiveStats && window.descriptiveStats['BOD5'] && window.descriptiveStats['NH3N'] && window.descriptiveStats['SS']) {
        // Use descriptive statistics from analysis
        avgBOD5 = window.descriptiveStats['BOD5']['Mean'];
        avgNH3N = window.descriptiveStats['NH3N']['Mean'];
        avgSS = window.descriptiveStats['SS']['Mean'];
        
        // Load other stats
        document.getElementById('minBOD5').textContent = window.descriptiveStats['BOD5']['Min'].toFixed(2) + ' mg/L';
        document.getElementById('maxBOD5').textContent = window.descriptiveStats['BOD5']['Max'].toFixed(2) + ' mg/L';
        document.getElementById('stdBOD5').textContent = window.descriptiveStats['BOD5']['Std'].toFixed(2) + ' mg/L';
    } else {
        // Calculate average values from data
        avgBOD5 = data.reduce((sum, item) => sum + parseFloat(item.bod5), 0) / data.length;
        avgNH3N = data.reduce((sum, item) => sum + parseFloat(item.nh3n), 0) / data.length;
        avgSS = data.reduce((sum, item) => sum + parseFloat(item.ss), 0) / data.length;
    }
    
    // Calculate compliance percentage
    const compliantCount = data.filter(item => item.complies).length;
    const complianceRate = (compliantCount / data.length * 100).toFixed(1);
    
    // Calculate trend direction (comparing first and last quarters)
    const quarterLength = Math.floor(data.length / 4);
    const quarterLength = Math.max(1, Math.floor(data.length / 4));
    const firstQuarter = data.slice(0, quarterLength);
    const lastQuarter = data.slice(-quarterLength);
    const avgBOD5First = firstQuarter.reduce((sum, item) => sum + parseFloat(item.bod5), 0) / firstQuarter.length;
    const avgBOD5Last = lastQuarter.reduce((sum, item) => sum + parseFloat(item.bod5), 0) / lastQuarter.length;
    
    // Calculate percentage change and trend direction
    const percentChange = avgBOD5First !== 0 ? ((avgBOD5Last - avgBOD5First) / avgBOD5First * 100) : 0;
    trendDirection = percentChange > 0 ? 'increasing' : (percentChange < 0 ? 'decreasing' : 'stable');
    trendPercentage = Math.abs(percentChange).toFixed(1);
    
    // Update DOM elements with calculated statistics
    document.getElementById('avgBOD5').textContent = avgBOD5.toFixed(2) + ' mg/L';
    document.getElementById('avgNH3N').textContent = avgNH3N.toFixed(2) + ' mg/L';
    document.getElementById('avgSS').textContent = avgSS.toFixed(2) + ' mg/L';
    document.getElementById('complianceRate').textContent = complianceRate + '%';
    
    // Update trend information
    const trendElement = document.getElementById('trendInfo');
    if (trendElement) {
        trendElement.textContent = `BOD5 is ${trendDirection} by ${trendPercentage}% (comparing first and last quarters)`;
        if (trendDirection === 'increasing') {
            trendElement.className = 'trend-up';
        } else if (trendDirection === 'decreasing') {
            trendElement.className = 'trend-down';
        } else {
            trendElement.className = 'trend-stable';
        }
    }
    
    // Update policy implications based on statistics
    updatePolicyImplications(avgBOD5, avgNH3N, avgSS, complianceRate, trendDirection);
}

// Update policy implications section based on water quality statistics
function updatePolicyImplications(avgBOD5, avgNH3N, avgSS, complianceRate, trendDirection) {
    const policyElement = document.getElementById('policyImplications');
    let policyText = '';
    
    // Generate policy implications based on water quality parameters
    if (complianceRate < 70) {
        policyText += '<p><strong>Urgent Action Required:</strong> Low compliance rate indicates systemic issues in water management infrastructure.</p>';
    } else if (complianceRate < 90) {
        policyText += '<p><strong>Improvement Needed:</strong> Moderate compliance rate suggests the need for targeted interventions.</p>';
    } else {
        policyText += '<p><strong>Sustainable Management:</strong> High compliance rate indicates effective water quality control measures.</p>';
    }
    
    // Add parameter-specific recommendations
    if (avgBOD5 > 3) {
        policyText += '<p><strong>BOD5 Management:</strong> Implement stricter controls on organic waste discharge from industrial and agricultural sources.</p>';
    }
    
    if (avgNH3N > 0.8) {
        policyText += '<p><strong>NH3N Reduction:</strong> Enhance wastewater treatment facilities and regulate fertilizer use in agricultural activities.</p>';
    }
    
    if (avgSS > 35) {
        policyText += '<p><strong>Suspended Solids Control:</strong> Improve erosion control measures and enhance sediment management in waterways.</p>';
    }
    
    // Add trend-based recommendations
    if (trendDirection === 'increasing') {
        policyText += '<p><strong>Trend Alert:</strong> Increasing pollution levels indicate the need for preemptive regulatory measures and enforcement.</p>';
    } else {
        policyText += '<p><strong>Positive Trend:</strong> Decreasing pollution levels suggest current policies are effective and should be maintained.</p>';
    }
    
    // Include any insights from analysis summary if available
    if (window.analysisSummary) {
        // Extract key insights from the analysis summary
        let insights = '';
        if (window.analysisSummary.includes('recommendation') || 
            window.analysisSummary.includes('Recommendation')) {
            // Extract recommendations from the summary text
            const recommendationMatch = window.analysisSummary.match(/recommendation[s]?:([^.]+)/i);
            if (recommendationMatch && recommendationMatch[1]) {
                insights += `<p><strong>Analysis Recommendation:</strong>${recommendationMatch[1]}</p>`;
            }
        }
        
        // Add insights to policy text if found
        if (insights) {
            policyText += '<hr><p><strong>Based on Analysis:</strong></p>' + insights;
        }
    }
    
    policyElement.innerHTML = policyText;
}

// Create and render the parameter distribution chart
function createDistributionChart(data) {
    // Use actual visualization image if available
    const distributionImageContainer = document.getElementById('distributionImageContainer');
    if (distributionImageContainer) {
        distributionImageContainer.innerHTML = `
            <img src="visualizations/distribution_plot.png" alt="Parameter Distribution" class="img-fluid chart-image">
        `;
    }
}

// Handle time range selection events
function handleTimeRangeSelection() {
    const timeRangeButtons = document.querySelectorAll('.time-range-btn');
    
    timeRangeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            timeRangeButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to the clicked button
            this.classList.add('active');
            
            // Update current time range
            currentTimeRange = this.dataset.range;
            
            // Update dashboard with filtered data
            updateDashboard();
        });
    });
}

// Function to apply smoothing to data for trend visualization
function applySmoothing(data, windowSize = 3) {
    if (data.length < windowSize) return data;
    
    const smoothedData = [];
    for (let i = 0; i < data.length; i++) {
        let sum = 0;
        let count = 0;
        
        for (let j = Math.max(0, i - Math.floor(windowSize/2)); 
             j <= Math.min(data.length - 1, i + Math.floor(windowSize/2)); 
             j++) {
            sum += parseFloat(data[j]);
            count++;
        }
        
        smoothedData.push((sum / count).toFixed(2));
    }
    
    return smoothedData;
}

// Update the entire dashboard with current data and settings
function updateDashboard() {
    // Show loading spinner
    document.getElementById('loadingIndicator').style.display = 'block';
    
    // Filter data based on current time range
    const filteredData = filterDataByTimeRange(waterQualityData, currentTimeRange);
    
    // Update charts and statistics with a slight delay to show loading effect
    setTimeout(() => {
        createTimeSeriesChart(filteredData);
        createCorrelationChart(filteredData);
        createPredictionChart(filteredData);
        createDistributionChart(filteredData);
        updateStatistics(filteredData);
        
        // Update water quality standards compliance status
        updateComplianceStatus(filteredData);
        
        // Hide loading spinner
        document.getElementById('loadingIndicator').style.display = 'none';
    }, 300);
}

// Function to export dashboard data as CSV
function exportData() {
    const filteredData = filterDataByTimeRange(waterQualityData, currentTimeRange);
    
    // Create CSV content
    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Date,BOD5 (mg/L),NH3N (mg/L),SS (mg/L),Complies\n";
    
    filteredData.forEach(item => {
        const dateStr = item.date.toISOString().split('T')[0];
        csvContent += `${dateStr},${item.bod5},${item.nh3n},${item.ss},${item.complies}\n`;
    });
    
    // Create download link
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "water_quality_data.csv");
    document.body.appendChild(link);
    
    // Trigger download and remove link
    link.click();
    document.body.removeChild(link);
}

// Set up export button event handler
function setupExportButton() {
    const exportButton = document.getElementById('exportButton');
    if (exportButton) {
        exportButton.addEventListener('click', exportData);
    }
}

// Update water quality standards compliance status
function updateComplianceStatus(data) {
    const complianceStatusElement = document.getElementById('complianceStatus');
    if (!complianceStatusElement) return;
    
    // Calculate compliance percentages
    const totalSamples = data.length;
    const bod5Compliant = data.filter(item => parseFloat(item.bod5) < 2.5).length;
    const nh3nCompliant = data.filter(item => parseFloat(item.nh3n) < 0.9).length;
    const ssCompliant = data.filter(item => parseFloat(item.ss) < 40).length;
    const overallCompliant = data.filter(item => item.complies).length;
    
    // Calculate compliance rates
    const bod5Rate = (bod5Compliant / totalSamples * 100).toFixed(1);
    const nh3nRate = (nh3nCompliant / totalSamples * 100).toFixed(1);
    const ssRate = (ssCompliant / totalSamples * 100).toFixed(1);
    const overallRate = (overallCompliant / totalSamples * 100).toFixed(1);
    
    // Update compliance status display
    complianceStatusElement.innerHTML = `
        <div class="row">
            <div class="col-md-3">
                <div class="compliance-item ${bod5Rate > 90 ? 'compliant' : bod5Rate > 70 ? 'moderate' : 'non-compliant'}">
                    <h5>BOD5</h5>
                    <div class="compliance-rate">${bod5Rate}%</div>
                    <div class="compliance-label">of samples < 2.5 mg/L</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="compliance-item ${nh3nRate > 90 ? 'compliant' : nh3nRate > 70 ? 'moderate' : 'non-compliant'}">
                    <h5>NH3N</h5>
                    <div class="compliance-rate">${nh3nRate}%</div>
                    <div class="compliance-label">of samples < 0.9 mg/L</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="compliance-item ${ssRate > 90 ? 'compliant' : ssRate > 70 ? 'moderate' : 'non-compliant'}">
                    <h5>SS</h5>
                    <div class="compliance-rate">${ssRate}%</div>
                    <div class="compliance-label">of samples < 40 mg/L</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="compliance-item ${overallRate > 90 ? 'compliant' : overallRate > 70 ? 'moderate' : 'non-compliant'}">
                    <h5>Overall</h5>
                    <div class="compliance-rate">${overallRate}%</div>
                    <div class="compliance-label">compliance</div>
                </div>
            </div>
        </div>
    `;
}

// Initialize dashboard with data and visualizations
function initializeDashboard() {
    console.log('Initializing water quality dashboard...');
    
    // Show loading indicator
    document.getElementById('loadingIndicator').style.display = 'block';
    
    // Load the water quality data
    loadData()
        .then(data => {
            console.log(`Loaded ${data.length} water quality records`);
            
            // Load analysis summary
            return loadAnalysisSummary().then(() => data);
        })
        .then(data => {
            // Store data globally
            waterQualityData = data;
            
            // Initialize charts and statistics
            updateDashboard();
            
            // Set up event handlers
            handleTimeRangeSelection();
            setupExportButton();
            
            // Hide loading message/spinner
            document.getElementById('loadingIndicator').style.display = 'none';
        })
        .catch(error => {
            console.error('Error loading data:', error);
            document.getElementById('loadingIndicator').textContent = 'Error loading data. Please refresh the page.';
        });
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', initializeDashboard);
