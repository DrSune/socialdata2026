# Assignment B: Refined Visualization & Integrity Strategy

## 1. Addressing AI Style & Course Integrity
To ensure the project remains your own and adheres to the "No Black Box" rule:
- **Originality:** The "Nature vs. Insulation" hypothesis is your unique contribution. AI is used only for **boilerplate code** (geocoding APIs, Folium setup).
- **Transparency:** The Explainer Notebook will document every data cleaning step (e.g., how we filtered out family-gift house sales) and explain the math behind the "Nature Distance" calculation.
- **Critical Reflection:** We will dedicate a section in the notebook to discuss the **limitations of the data** (e.g., energy labels are theoretical, not actual consumption).

---

## 2. Refined Visualizations (High-Signal, No Muddy Plots)

### Viz 1: Static "Price Gap" Analysis (Direct Communication)
**Concept:** *The Penalty is Real.*
- **Type:** **Multi-Panel Slope Chart** (2019 vs. 2023).
- **The Visual:** Each line represents an energy label (A-G). The slope shows the change in median price per sqm.
- **Why it's better than Ridgelines:** It directly shows the *divergence*. You can clearly see the 'G' line dropping steeper than the 'A' line. It's an unambiguous signal of market change.

### Viz 2: Geospatial "Closeness" Map (Direct Spatial Correlation)
**Concept:** *Nature as a Buffer.*
- **Type:** **Binned Choropleth + Point Overlay** (instead of a Heatmap).
- **The Visual:** We bin Denmark into 1km hexes. Color represents the **Nature Proximity Index**. 
- **The Signal:** We overlay individual sales points of "F/G" houses that sold **above** their expected municipal average. 
- **Why it's better than Heatmaps:** Instead of muddy colors, we use categorical regions and high-contrast markers to show *exactly* where the "Nature Buffer" effect is occurring. 

### Viz 3: Interactive "Value Scatters" (Hypothesis Testing)
**Concept:** *The Nature Multiplier.*
- **Type:** **Grouped Dot Plot / Strip Plot** with an interactive **Nature Distance Slider**.
- **The Visual:**
  - **Y-axis:** Deviation from expected price (Residuals).
  - **X-axis:** Energy Label (A through G).
- **The Interaction:** As the user slides the "Distance to Nature" from 2000m down to 0m, they see the "F" and "G" dots (individual sales) physically move up the Y-axis.
- **The Insight:** It directly demonstrates that for the same energy label, houses closer to nature have higher residuals (sell for more than predicted by energy alone).

---

## 3. The Martini Glass Flow
1. **The Stem:** The Slope Chart proves energy labels matter more now.
2. **The Pivot:** The Choropleth shows where nature and poor insulation meet.
3. **The Flare:** The Residual Strip Plot lets the reader "buy" a virtual house and see how nature changes the price tag.
