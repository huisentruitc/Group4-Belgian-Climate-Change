# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 09:17:28 2026

@author: calvi
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:15:56 2026

@author: olivova
"""

from pathlib import Path
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Ask for folder path until all 780 files (196001 to 202412) are found
while True:
    folder = Path(input("Enter your floder path: "))
    files = [
        f for f in sorted(folder.glob("climategrid_*.csv"))
        if "climategrid_196001.csv" <= f.name <= "climategrid_202412.csv"
    ]
    if len(files) == 780:
        break
    print(f"Found {len(files)}/780 files. Please enter another folder.")

# 2. Read and combine only the 3 needed columns from every file
df = pd.concat(
    pd.read_csv(f, sep=";", usecols=["pixel_id", "day", "temp_max"], parse_dates=["day"])
    for f in files
)

# 3. Reshape into a 2D NumPy array with dimensions (day, pixel)
temp_max_array = df.pivot(index="day", columns="pixel_id", values="temp_max").to_numpy()

#TASK 4: Find the hottest day
# 4. Calculate the mean temperature across all pixels for each day
daily_mean = df.groupby("day")["temp_max"].mean()

# 5. Find the highest daily mean temperature for each year (TXx)
TXx = daily_mean.groupby(daily_mean.index.year).max()

# 6. Find the date of the hottest day in each year
hottest_dates = daily_mean.groupby(daily_mean.index.year).idxmax()

# 7. Create a table with the results
results = pd.DataFrame({
    "Year": TXx.index,
    "Hottest_day": hottest_dates.values,
    "TXx": TXx.values
})

# 8. Display the results
print(results.to_string(index=False))

#TASK 5: Make a plot of the hottest days throughout the years
fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(results["Year"], results["TXx"], color = "red", label = "Hottest days through out the years", marker = "o", markersize=4, linewidth=1.5)
ax.grid(True, linestyle="--", alpha=0.4)
ax.set_xlabel("Year")
ax.set_ylabel("Temperature [°C]")
ax.set_title("Annual Maximum Daily Temperature (TXx) in Belgium (1960–2024)")
plt.show()