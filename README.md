# Yeast Protein Localization Dashboard 🧬

A fully interactive, premium-grade dashboard built with Streamlit, Pandas, Matplotlib, and Seaborn to analyze localization sites in the Yeast dataset. 

This repository contains the complete source code, exploratory data analysis notebook, and files organized per the project guidelines.

---

## 🛠️ Step-by-Step Project Walkthrough

Here is the exact step-by-step process of how this project was designed, coded, and polished:

### Step 1: Folder Setup & Data Initialization
1. Structured the folder workspace exactly according to the project specifications:
   - `data/` for the dataset.
   - `notebooks/` for exploratory scripts.
   - Root level for the app scripts (`app.py`, `charts.py`, `filters.py`).
2. Placed the `yeast.data` dataset inside `data/`. Since the raw dataset doesn't contain headers and is spaced-separated, we loaded it in Pandas using the space regex separator (`sep=r'\s+'`) and mapped the standard SWISS-PROT column headers:
   - `Sequence_Name`: Accession name
   - `mcg`: McGeoch's signal sequence recognition method
   - `gvh`: von Heijne's signal sequence recognition method
   - `alm`: Score of the ALOM membrane spanning region
   - `mit`: Score of discriminant analysis of the N-terminal region
   - `erl`: HDEL substring presence (binary)
   - `pox`: Peroxisomal targeting signal in C-terminus
   - `vac`: Score of discriminant analysis of vacuolar/extracellular proteins
   - `nuc`: Score of nuclear localization signals
   - `Class`: Localization site (target variable)

### Step 2: Exploratory Data Analysis (`notebooks/analysis.ipynb`)
- Created a notebook to test data loading, data frame cleaning, and graph rendering.
- Set up a clean, single-cell testing workflow. Cell 1 handles the pandas configurations, and subsequent cells generate and render each of the required plots to guarantee there are no exceptions during the visual rendering pipeline.

### Step 3: Isolating Filters (`filters.py`)
- Created custom filtering logic. Rather than cluttering the main app file, all query and slicing operations were isolated here.
- **Handling UI Crashes (Human touch):** During testing, we encountered a Streamlit crash. If the active filters reduced the data rows to a small subset sharing the exact same parameter value (e.g. `mcg = 0.41`), the dynamic slider's minimum and maximum limits collapsed to the same number. Streamlit's slider widget throws an exception in this state. 
- To fix this, the filter boundaries and class options are calculated from the *original* raw dataset (`orig_df`) before slicing, locking the sliders in place. We also added safety check pads (`if mcg_min == mcg_max: mcg_max += 0.01`) as a secondary safeguard.

### Step 4: Modular Visualizations (`charts.py`)
Developed the 10 mandatory plots plus a bonus chart, adding specific adjustments to make them look premium:
1. **Pie Chart (Donut style):** The raw dataset has 10 classes, some of which contain only a tiny fraction of records (e.g. ERL has 5 records). In a normal pie chart, these tiny slices result in overlapping percentage labels. To fix this, we converted it to a donut chart, and grouped any class representing less than 3% of the total dataset under a collective label ("Other").
2. **Histogram:** A clean distribution plot of `mcg` values.
3. **Line Chart:** Sequential line plot showing the trend of `gvh` values.
4. **Bar Chart:** Average `alm` scores sorted across different protein classes.
5. **Scatter Plot:** Bivariate scatter mapping `mcg` against `gvh`.
6. **Box Plot:** Spread and outliers of `nuc` scores.
7. **Heatmap:** Correlation grid of the numerical columns.
8. **Area Chart:** Cumulative area representation of `mit` scores.
9. **Count Plot:** Proportions of the binary `erl` feature.
10. **Violin Plot:** Density representation of the `vac` feature grouped by class.
11. **Bubble Chart (Bonus Plot):** An 11th chart displaying `mcg` vs `gvh` with markers colored by class and sizes dynamically scaled by the `vac` score.

### Step 5: Designing the Streamlit UI (`app.py`)
- **Theme Matching:** Matplotlib figures render with a default white background, which looks jarring in dark mode. We solved this by setting both the figure and axes backgrounds to transparent (`fig.patch.set_alpha(0.0)`) and styling all axes labels, ticks, and grids with slate grey (`#8a95a5`). This makes the plots blend perfectly in both dark and light modes.
- **Title and Header UI:** Added a deep blue gradient banner (`#1e3c72` to `#2a5298`) centered with a protein emoji (`🧬`) to make the top look clean and bold.
- **Custom CSS KPI Cards:** Wrote metric panels using CSS variables (`var(--secondary-background-color)` and `var(--primary-color)`) so they dynamically adapt to dark/light theme shifts.
- **Centered Chart Names:** Positioned the names of the plots centered directly under the charts. The chart name is bolded on line one, and the description sits below in plain text.
- **Zero Comments:** Ensured all source files contain absolutely zero comments or developer docstrings.

---

## 🚀 Installation & Running the Dashboard

### 1. Requirements
Ensure you have Python 3.10+ installed.

### 2. Setup Dependencies
From the repository root, install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Launching the App
Run the Streamlit server:
```bash
streamlit run app.py
```

### 4. Running the Notebook
To explore the step-by-step EDA:
```bash
jupyter notebook notebooks/analysis.ipynb
```
