# Group 4 — Belgian Climate Change and Extreme Temperatures

**Environmental Programming — Project 4**

Research question: **Would these temperatures happen in a world without climate change?**

## Goals
1. **Explore:** Investigate spatial and temporal patterns of extreme temperatures across Belgium.
2. **Detect:** Assess whether the hottest days are getting hotter and identify spatial differences in warming.
3. **Attribute:** Estimate how climate change affected an extreme event's intensity and probability, using the assignment's statistical attribution approach.

## Data
- **Monthly climate grids:** `climategrid_YYYYMM.csv`, supplied separately to group members. The full raw dataset is **not on GitHub**.
- **Administrative boundaries:** Natural Earth Admin-1 shapefile components are in the repository; keep the `.shp`, `.shx`, `.dbf`, `.prj`, and `.cpg` files together.
- **GMST series:** Still to be identified for the attribution model.
- **Pixel coordinates:** The monthly CSVs have a `pixel_id` but not latitude/longitude. A pixel-to-location reference is still required for maps.

The monthly CSVs use **semicolons (`;`)** as separators and contain temperature, precipitation and other meteorological columns. The first script imports only the five fields needed for temperature analysis.

## Task 1 — Combine the monthly files (completed locally)

Script: **[`combineddata.py`](combineddata.py)**

- Selects **January 1960 through December 2024** (inclusive), **780 CSV files**.
- Reads only `pixel_id`, `day`, `temp_max`, `temp_min` and `temp_avg`.
- Uses memory-saving types and parses dates.
- Checks for missing monthly filenames.
- Concatenates the files into a pandas DataFrame named `data`.
- Prints the number of rows, date range, pixel/day counts, memory use, and non-missing temperature counts.

Verified in Spyder on the original course data: **32,289,120 rows × 5 columns**. The script does **not** write the combined DataFrame to disk; `data` lives in the running Python session.

## How each group member runs the script

1. Clone this repository using GitHub Desktop.
2. Obtain the original `climategrid_YYYYMM.csv` files from the approved class/group source, separately from GitHub.
3. Make a folder named `climateGrid` **inside the local repository**, beside `combineddata.py`:
   
   ```text
   Group4-Belgian-Climate-Change/
   ├── combineddata.py
   ├── climateGrid/                  # local only; ignored by Git
   │   ├── climategrid_196001.csv
   │   ├── climategrid_196002.csv
   │   └── ...
   ├── README.md
   ├── .gitignore
   └── ne_10m_admin_1_states_provinces.*
   ```
4. Use a Python environment containing `pandas` (and `pathlib`, which is in the standard library).
5. Open `combineddata.py` in Spyder and run it. It finds data relative to its own file path, so no Windows username or absolute path is needed.
6. Check `Files selected: 780` and `Data shape: (32289120, 5)`. The script requires the 780 monthly files from 1960–2024.

**Important:** `climateGrid/` is excluded by `.gitignore`. Do not force-add the large raw CSV files or commit the complete combined table. The import is memory intensive; avoid rerunning it unnecessarily.

## Recommended next analysis milestone

- Calculate **annual maximum daily temperature (TXx)** per pixel for 1960–2024, giving up to **1,360 × 65 = 88,400** pixel-year values.
- Summarize when the most extreme temperatures occurred and how the distribution evolved.
- Confirm how `pixel_id` maps to spatial coordinates before plotting temperature values against the Natural Earth boundaries.
- For detection, assess time trends and appropriate uncertainty.
- For attribution, apply the supplied GMST regression and event-probability formulas; obtain and document the required GMST data.

These are recommended next steps, not a substitute for the detailed assignment instructions.

## Reproducibility and deliverables
As work progresses, add:
- Python scripts for exploration, detection and attribution
- A Jupyter notebook explaining how to run the analysis
- A Conda `environment.yml`
- Figures and a code flowchart
- Small sample input data, if appropriate and redistribution is permitted
- Dataset provenance, assumptions, results and citations

**Assignment submission:** 21 December 2026 — open-access GitHub repository link, according to the assignment instructions. The repository is currently **private**; it must be made public before submission if required by the course.

## Working together
Each collaborator should clone the repository and get access to the raw dataset separately. Create a **feature branch** for a new component, commit small changes, push the branch, and open a **pull request** for review before merging into `main`. Use GitHub Issues to coordinate tasks and questions.

This repository is a work in progress; the exploration, detection, attribution and final deliverables are not all implemented yet.
