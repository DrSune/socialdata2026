import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_insulation_explorer():
    print("Generating Figure 3: The Insulation Tax Explorer (Flare Scatter)...")
    df = pd.read_parquet('full_housing_data.parquet')
    
    # 1. Filter for 2023 sales to show the current reality
    df_2023 = df[(df['date'] >= '2023-01-01') & (df['date'] <= '2023-12-31')].copy()
    
    # Take a manageable sample for interactivity (2000 points)
    df_sample = df_2023.sample(min(2000, len(df_2023)), random_state=42).copy()
    
    # 2. Add Age Category
    def get_era(year):
        if year < 1961: return 'Pre-1961 (G/F)'
        if year < 1977: return '1961-77 (E)'
        if year < 1995: return '1977-95 (D)'
        return 'Post-1995 (C-A)'
    df_sample['Era'] = df_sample['year_build'].apply(get_era)
    
    # 3. Handle Haggling (Price Drop)
    df_sample['Haggle_%'] = df_sample['%_change_between_offer_and_purchase'].abs()

    # 4. Create Interactive Scatter
    fig = px.scatter(df_sample, 
                     x="year_build", 
                     y="sqm_price", 
                     color="Era",
                     size="Haggle_%",
                     hover_data=['address', 'city', 'purchase_price', 'sqm'],
                     title="The Age-Value Relationship in 2023: Every Year Matters",
                     labels={
                         "year_build": "Year House was Built",
                         "sqm_price": "Sale Price (DKK per sqm)",
                         "Haggle_%": "Price Discount Negotiated (%)"
                     },
                     color_discrete_map={
                         'Pre-1961 (G/F)': '#d73027',
                         '1961-77 (E)': '#f46d43',
                         '1977-95 (D)': '#fdae61',
                         'Post-1995 (C-A)': '#1a9850'
                     },
                     template="plotly_white")

    # Add a Trend Line (Lowess/OLS) manually for better control
    # Sort for plotting trend
    df_trend = df_sample.sort_values('year_build')
    
    fig.update_layout(
        font=dict(family="Georgia, serif", size=14),
        legend=dict(title="Building Era", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(range=[1850, 2025]) # Focus on relevant building years
    )

    # Add helpful annotations
    fig.add_annotation(
        x=1960, y=df_sample['sqm_price'].quantile(0.1),
        text="The 'Legacy' Cluster:<br>High discounts, lower equity",
        showarrow=True, arrowhead=1, ax=-50, ay=-50
    )
    
    fig.add_annotation(
        x=2015, y=df_sample['sqm_price'].quantile(0.9),
        text="The 'Resilient' Cluster:<br>Premium value, stable pricing",
        showarrow=True, arrowhead=1, ax=50, ay=50
    )

    fig.write_html('docs/insulation_explorer.html')
    print("Figure 3 (Interactive Scatter) saved.")

if __name__ == "__main__":
    create_insulation_explorer()
