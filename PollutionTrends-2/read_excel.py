import pandas as pd

try:
    # Try to read the Excel file
    data = pd.read_excel('attached_assets/data2.xlsx')
    print("Excel file read successfully!")
    print("Columns:", data.columns.tolist())
    print("First few rows:")
    print(data.head())
    
    # Save as CSV for easier handling
    data.to_csv('data.csv', index=False)
    print("Data saved to data.csv")
    
except Exception as e:
    print(f"Error reading Excel file: {e}")