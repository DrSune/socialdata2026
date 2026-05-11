# Assignment A: The 1-Minute Pitch Outline
**Title:** The Green Trade-off: Does Nature Offset the Insulation Penalty?

## 1. The Hook (0-15s)
*   **Visual:** Opening with a contrasting split-screen mockup. On one side, a modern "A-labeled" apartment in a dense city; on the other, a drafty "G-labeled" villa surrounded by forest.
*   **Audio/Script:** "When the 2022 energy crisis hit Denmark, the 'Energimærke' became a financial death sentence for some houses. But is it always? We're exploring a hidden trade-off: Can proximity to Denmark's protected nature areas rescue the value of a poorly insulated home? Or is the 'Green Premium' strictly about energy bills?"

## 2. The Data (15-30s)
*   **Visual:** Quick scrolling text/graphic showing the datasets:
    *   1.5 Million Danish Housing Sales (1992-2024).
    *   Official Energy Label Database (A-G grades).
    *   §3 Protected Nature Areas (GeoJSON).
*   **Audio/Script:** "We’re leveraging a massive dataset of 1.5 million sales, geocoded and enriched with official energy labels. By spatial-joining this with Denmark’s protected nature registry, we can calculate exactly how many meters of 'forest view' it takes to offset an 'F' rating."

## 3. The Genre & Strategy (30-45s)
*   **Visual:** A "Magazine Style" layout mockup showing scrollytelling elements.
*   **Audio/Script:** "We’ve chosen the **Magazine Genre**. This allows us to lead the reader from the macro-economic shock of the energy crisis into a personal, reader-driven exploration of their own neighborhood. We’re using a 'Martini Glass' structure: starting with a strong narrative stem and ending with an interactive map where you can explore the Nature-vs-Insulation balance yourself."

## 4. The Viz Mockups (45-60s)
*   **Visual:** Rapidly showing three mockup sketches:
    *   **Static:** A ridgeline plot showing price distributions shifted by energy labels vs. nature proximity.
    *   **Map:** A dual-layer Folium map (Energy efficiency vs. Nature zones).
    *   **Interactive:** A Plotly scatter plot with a 'Nature Distance' slider.
*   **Audio/Script:** "Our viz will include a static deep-dive into price rhythms, a geographic heatmap of 'Energy Poverty' in nature-rich areas, and an interactive tool to find the 'sweet spot' for your next home purchase. This isn't just data; it's a guide to the new Danish reality."

---

## Technical Appendix (For your Video Prep)
*   **Central Idea:** Investigating if "closeness to nature" acts as a buffer for the price drop expected in low-energy-efficiency houses.
*   **Genre:** Magazine (Segel & Heer Section 4.3).
*   **Preliminary Analysis:** 
    *   ~800,000 relevant sales records.
    *   Focusing on 2022-2024 (The Energy Crisis era).
    *   Spatial data: MultiPolygon GeoJSON for nature areas.
