# Assignment 1 Solutions

This folder contains the implementation of Assignment 1 for the Social Data Analysis 2026 course.

## Contents

- `assignment1_solutions.ipynb`: A Jupyter notebook with the complete analytical workflow.
  - **Data Acquisition**: Logic to download the 2003-2018 and 2018-Present SF Crime datasets.
  - **Preprocessing**: Merging datasets and mapping incident categories.
  - **Exercise 1.1 - 1.5**: Full solutions for temporal trends, district profiles, distribution visualizations, spatial power law, and regression analysis.

## How to Run

1.  **Open the Notebook**: Launch `assignment1_solutions.ipynb` in VS Code or Jupyter.
2.  **Download Data**: The second code cell contains logic to download the raw CSV files from DataSF. Un-comment the download lines if you don't have the files locally yet.
3.  **Run All Cells**: The notebook is structured to run sequentially.

## Important Notes

- **Data Size**: The raw datasets are large (totaling ~1GB). Ensure you have sufficient disk space.
- **Focus Crimes**: You can adjust the `focus_crimes` list in the setup cell to match your specific selection.
- **Visualizations**: The notebook uses `matplotlib`, `seaborn`, and `scipy.stats` for plotting.
