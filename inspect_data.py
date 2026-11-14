from pathlib import Path
import pandas as pd

# Path to the data folder
DATA_PATH = Path("data")

# Find the CSV file inside data/
csv_files = list(DATA_PATH.glob("*.csv"))
if not csv_files:
    raise FileNotFoundError("No CSV file found in the 'data' folder! Check the folder name.")

csv_file = csv_files[0]
print(f"Reading file: {csv_file.name}")
print("=" * 50)

# Load the dataset
df = pd.read_csv(csv_file)

# 1. Total rows and columns
print(f"Total Rows: {df.shape[0]}")
print(f"Total Columns: {df.shape[1]}")
print("-" * 50)

# 2. Column names and data types
print("Columns and their types:")
print(df.dtypes)
print("-" * 50)

# 3. Check for missing values (empty cells)
print("Missing values per column:")
null_counts = df.isnull().sum()
print(null_counts[null_counts > 0] if null_counts.sum() > 0 else "None! Data is clean.")
print("-" * 50)

# 4. Preview first 3 rows
print("First 3 rows:")
print(df.head(3))