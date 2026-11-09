# Group 4 — Belgian Climate Change and Extreme Temperatures

**Environmental Programming — Project 4**

Research question: **Would these temperatures happen in a world without climate change?**

## Goals
1. **Explore:** Investigate spatial and temporal patterns of extreme temperatures across Belgium.
2. **Detect:** Assess whether the hottest days are getting hotter and identify spatial differences in warming.
3. **Attribute:** Estimate how climate change affected an extreme event's intensity and probability, using the assignment's statistical attribution approach.

## Data
- **Monthly climate grids:** `climategrid_YYYYMM.csv`, provided separately for analysis. These large raw files are intentionally **not stored in this repository**.
- **Administrative boundaries:** Natural Earth Admin-1 states/provinces shapefile, supplied in the repository. Keep its `.shp`, `.shx`, `.dbf`, `.prj` and `.cpg` files together.
- **GMST series:** To be identified and documented for attribution.

The monthly CSVs are semicolon-delimited. They include `pixel_id`, `day`, `temp_max`, `temp_min`, `temp_avg`, precipitation and other variables. Some months may have missing temperature values; check completeness before analysis.

## First milestone — combine monthly files
Read files for **January 1960 through December 2024** (inclusive), convert `day` to dates, and combine them into one table. This is **780 monthly files** when the record is complete. Initial local testing produced **32,289,120 rows × 11 columns**; validate the imported table and missing values.

## Local setup
Clone this repository with GitHub Desktop. Keep the large `climateGrid` directory outside the repository, for example:

```text
EnvPr/
├── climateGrid/                          # local raw CSVs, not committed
│   ├── climategrid_196001.csv
│   └── ...
└── Group4-Belgian-Climate-Change/       # GitHub clone
    ├── README.md
    └── ...
```

Each contributor should adjust local file paths to their own machine or use paths relative to the repository. Do **not** commit a 32-million-row combined dataset.

## Reproducibility and deliverables
As work progresses, add:
- Python scripts for import, exploration, detection and attribution
- A Jupyter notebook explaining how to run the analysis
- A Conda `environment.yml`
- Figures and a code flowchart
- Small sample input data, if appropriate and redistribution is permitted
- Source details, methodological assumptions and citations

**Assignment submission:** 21 December 2026 — open-access GitHub repository link, according to the assignment instructions. Currently this repository is private; it must be made public before submission if required by the course.

## Working together
Create a **feature branch** for each new component, commit small changes, push your branch, and open a **pull request** for review before merging into `main`. Use GitHub Issues to record tasks and questions.

The repository is a work in progress; not all analyses and project requirements are implemented yet.
