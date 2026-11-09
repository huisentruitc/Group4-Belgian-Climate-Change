# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:10:12 2026

@author: calvi
"""

import pandas as pd
from pathlib import Path

# TASK 1: Combine monthly climate data (1960–2024)

# 1. Locate the data folder
folder = Path(__file__).resolve().parent / "climateGrid"

if not folder.is_dir():
    raise FileNotFoundError(f"Data folder not found: {folder}")

# 2. Find the monthly CSV files
files = sorted(folder.glob("climategrid_*.csv"))

# 3. Select files from January 1960 to December 2024
files = [
    f for f in files
    if "196001" <= f.stem[-6:] <= "202412"
]

print("Files selected:", len(files), flush=True)

# Check that all expected months are present
expected = {
    f"{year}{month:02d}"
    for year in range(1960, 2025)
    for month in range(1, 13)
}

found = {f.stem[-6:] for f in files}
missing = expected - found

if missing:
    raise ValueError(f"Missing months: {sorted(missing)}")

# 4. Select only the required columns
columns = [
    "pixel_id",
    "day",
    "temp_max",
    "temp_min",
    "temp_avg"
]

# 5. Set efficient data types
dtypes = {
    "pixel_id": "int16",
    "temp_max": "float32",
    "temp_min": "float32",
    "temp_avg": "float32"
}

# 6. Read all monthly files
frames = []

for i, file in enumerate(files, start=1):

    df = pd.read_csv(
        file,
        sep=";",
        usecols=columns,
        dtype=dtypes,
        parse_dates=["day"]
    )

    frames.append(df)

    if i % 50 == 0 or i == len(files):
        print(f"Loaded {i}/{len(files)} files", flush=True)

# 7. Combine all months into one table
data = pd.concat(frames, ignore_index=True)
del frames

# 8. Verify the combined dataset
print("\nDATA SUMMARY")
print("Shape:", data.shape)
print("First date:", data["day"].min())
print("Last date:", data["day"].max())
print("Unique pixels:", data["pixel_id"].nunique())
print("Unique days:", data["day"].nunique())

print("Memory usage:",
      round(data.memory_usage(deep=True).sum() / 1e9, 2),
      "GB")

# 9. Check available temperature observations
print("\nNON-MISSING TEMPERATURE VALUES")
print(data[["temp_max", "temp_min", "temp_avg"]].count())

# 10. Preview the table
print("\nFIRST FIVE ROWS")
print(data.head())
