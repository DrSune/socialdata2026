# Assignment B: The Viz Strategy (Martini Glass Structure)

Our Data Story follows the **Magazine Genre** using a **Martini Glass Structure**:
1. **The Stem (Author-Driven):** Lead the reader through a specific discovery (Energy Crisis impact).
2. **The Flare (Reader-Driven):** Open up to an interactive tool for personal exploration.

---

## 1. Static Visualization (The Stem - Narrative Foundation)
**Concept:** *The Cost of a Letter.*
- **Type:** Ridgeline Plot (Joyplot) or Boxplot.
- **X-axis:** Price per Square Meter (DKK/sqm).
- **Y-axis:** Energy Labels (A, B, C, D, E, F, G).
- **The Story:** We show two "Snapshots": 2019 (Pre-crisis) vs. 2023 (Post-crisis). 
- **What it reveals:** In 2019, the price distributions for 'C' and 'F' overlap significantly. In 2023, the 'F' and 'G' distributions shift left and flatten, showing a clear "market decoupling" where buyers started penalizing poor insulation.
- **Role:** This establishes the "Insulation Penalty" as a fact before we introduce Nature.

## 2. Geospatial Map (The Pivot - Adding Nature)
**Concept:** *The Nature Buffer.*
- **Type:** Dual-Layer Folium Heatmap.
- **Layer 1 (Heatmap):** Concentration of "G-labeled" houses (The 'Energy Poverty' zones).
- **Layer 2 (Overlays):** Green polygons representing §3 Protected Nature.
- **The Story:** This map highlights rural areas (like parts of Zealand or Jutland) where houses are old (poor labels) but surrounded by nature.
- **Insight:** It asks the question: "Are these high-nature/low-energy areas actually selling for more than low-nature/low-energy areas?"

## 3. Interactive Visualization (The Flare - Reader Exploration)
**Concept:** *The Trade-off Calculator.*
- **Type:** Plotly Scatter Plot with Sliders.
- **X-axis:** Distance to nearest Protected Nature (meters).
- **Y-axis:** Sales Price (Adjusted for sqm).
- **Color/Filter:** Interactive toggle for Energy Label (A-G).
- **Slider:** Year of Sale (2010 -> 2024).
- **The Story:** The reader can select "Energy Label F" and move the "Year" slider to 2022. They will see the points (houses) drop in price. Then, as they filter for "Distance to Nature < 500m", they can see if those specific houses maintained their value better than those at 2km+ distance.
- **Role:** This is the "Flare" where the reader tests the hypothesis themselves.

---

## Technical Feasibility Note
- **Coordinates:** Using the DAWA `/adresser` endpoint (which we verified) to get [lon, lat] for each house.
- **Nature Distance:** We will use the `shapely` library to calculate the minimum distance between each house point and the nearest Nature polygon from our GeoJSON.
- **Non-Aggregated:** Every point in our final interactive viz will be an **actual house sale**, fulfilling the "no aggregated statistics" mandate.
