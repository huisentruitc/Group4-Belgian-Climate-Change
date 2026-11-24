# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:15:56 2026

@author: olivova
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymannkendall as mk

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

#TASK 3: Find the hottest day
# 4. Calculate the mean temperature across all pixels for each day
daily_mean = df.groupby("day")["temp_max"].mean()

# 5. Find the highest daily mean temperature for each year (TXx)
TXx = daily_mean.groupby(daily_mean.index.year).max()

# 6. Find the date of the hottest day in each year
hottest_dates = daily_mean.groupby(daily_mean.index.year).idxmax()

# 7. Create a table with the results
results = pd.DataFrame({
    "Year": TXx.index,
    "Hottest_day": hottest_dates.dt.strftime("%Y-%m-%d").values,
    "TXx": TXx.values
})

# 8. Display the results
print(results.to_string(index=False))

#TASK 4: Make a plot of the hottest days throughout the years
fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(results["Year"], results["TXx"], color = "red", label = "Maximum temperature", marker = "o", markersize=4, linewidth=1.5)
ax.grid(True, linestyle="--", alpha=0.4)
ax.set_xlabel("Year")
ax.set_ylabel("Temperature [°C]")
ax.set_title("Annual Maximum Daily Temperature (TXx) in Belgium (1960–2024)")


#TASK 5: Mann-Kendall test and Sen's slope
trend = mk.original_test(TXx)

print("P-value:", trend.p)
print("Sen's slope:", trend.slope, "°C/year")

if trend.p < 0.05:
    print("The trend is statistically significant.")
else:
    print("The trend is not statistically significant.")

#TASK 6: Adding the trendline into the plot

trendline = trend.slope * (results["Year"] - results["Year"].iloc[0]) + trend.intercept

ax.plot(results["Year"], trendline, linewidth=2, color="black", label="Trend line")

ax.legend()
plt.show()

#TASK 7:
  
# TASK 7: Map of TXx changes in Belgium

# 1. Find the highest temperature for each pixel and year
df["year"] = df["day"].dt.year

annual = df.groupby(["year", "pixel_id"])["temp_max"].max().reset_index()

# 2. Calculate average TXx for two 30-year periods
old = annual[annual["year"].between(1961, 1990)]
new = annual[annual["year"].between(1991, 2020)]

old_mean = old.groupby("pixel_id")["temp_max"].mean()
new_mean = new.groupby("pixel_id")["temp_max"].mean()

# 3. Calculate temperature change
change = new_mean - old_mean

# 4. Read pixel coordinates from metadata
while True:
    metadata_path = Path(input("Enter the full path to your metadata CSV file: ").strip('"\' '))
    if metadata_path.is_file():
        break
    print("File not found. Please enter a valid full path to the metadata CSV file.")

metadata = pd.read_csv(metadata_path, sep=";")

# 5. Add temperature changes to coordinates
metadata["change"] = metadata["PIXEL_ID"].map(change)

# 6. Plot the map
plt.figure(figsize=(9, 7))

plt.scatter(
    metadata["PIXEL_LON_CENTER"],
    metadata["PIXEL_LAT_CENTER"],
    c=metadata["change"],
    cmap="YlOrRd", #cmap = "coolwarm",
    s=35
)

plt.colorbar(label="TXx change [°C]")
plt.xlabel("Longitude [°E]")
plt.ylabel("Latitude [°N]")
plt.title("Change in TXx in Belgium (1961–1990 vs. 1991–2020)")
plt.gca().set_aspect(1 / np.cos(np.deg2rad(50.5)), adjustable="box")
plt.show()
  

    
#PART 2: ATRIBUTTION
#TASK 8: Finding exceptionally hot day (temperature and date)
high_temp = results["TXx"].max()
day_of_high_temp = results[results["TXx"] == high_temp]["Hottest_day"].values[0] 

print("The date is:", day_of_high_temp)
print("The temperature is:", f"{high_temp:.2f}", "°C")

    
#TASK 9: Map of the daily maximum temperature on that day    

# 1. Select temperatures from the hottest day
hot_day_data = df[df["day"] == day_of_high_temp]

# 2. Match temperatures with pixel coordinates
metadata["temperature"] = metadata["PIXEL_ID"].map(
    hot_day_data.set_index("pixel_id")["temp_max"]
)

# 3. Plot the map
plt.figure(figsize=(9, 7))

plt.scatter(
    metadata["PIXEL_LON_CENTER"],
    metadata["PIXEL_LAT_CENTER"],
    c=metadata["temperature"],
    cmap="YlOrRd",
    s=35
)

plt.colorbar(label="Maximum temperature [°C]")
plt.title("Maximum temperature on " + str(day_of_high_temp)[:10])
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.gca().set_aspect(1 / np.cos(np.deg2rad(50.5)), adjustable="box")
plt.show()
    
#TASK 10:     
# 1. Read the GMST file
while True:
    gmst_path = Path(input("Enter the full path to your GMST CSV file: ").strip('"\' '))
    if gmst_path.is_file():
        break
    print("File not found. Please enter a valid full path to the GMST CSV file.")

gmst = pd.read_csv(gmst_path)

# 2. Combine TXx and GMST by year
combined = results.merge(gmst, left_on="Year", right_on="year")

# 3. Remove the event year
event_year = int(str(day_of_high_temp)[:4])
combined = combined[combined["Year"] != event_year]

# 4. Calculate the mean values
mean_gmst = combined["gmst"].mean()
mean_TXx = combined["TXx"].mean()

# 5. Calculate alpha (slope)
alpha = (
    ((combined["gmst"] - mean_gmst) *
     (combined["TXx"] - mean_TXx)).sum()
    /
    ((combined["gmst"] - mean_gmst)**2).sum()
)

# 6. Calculate mu0 (intercept)
mu0 = mean_TXx - alpha * mean_gmst

# 7. Calculate predicted TXx (Formula 1)
predicted = mu0 + alpha * combined["gmst"]

# 8. Calculate residuals
residuals = combined["TXx"] - predicted

# 9. Calculate sigma (Formula 2)
sigma = (sum(residuals**2) / len(residuals))**0.5

# 10. Print the results
print("Alpha:", f"{alpha:.2f}")
print("Mu0:", f"{mu0:.2f}")
print("Sigma:", f"{sigma:.2f}")

 

   
    
    
    
    
    
    
    
    
    
    
    
    
    
    