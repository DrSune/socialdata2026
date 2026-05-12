import pandas as pd
import plotly.express as px
import numpy as np

def create_insulation_explorer():
    print("Generating Figure 3: The Insulation Tax Explorer (Academic Grade)...")
    df = pd.read_parquet('full_housing_data.parquet')
    
    # 1. Filter for 2023 sales
    df_2023 = df[(df['date'] >= '2023-01-01') & (df['date'] <= '2023-12-31')].copy()
    
    # Sample for performance and noise reduction
    df_sample = df_2023.sample(min(2000, len(df_2023)), random_state=42).copy()
    
    # 2. Add Age Category
    def get_era(year):
        if year < 1961: return 'Pre-1961 (G/F)'
        if year < 1977: return '1961-77 (E)'
        if year < 1995: return '1977-95 (D)'
        return 'Post-1995 (C-A)'
    df_sample['Era'] = df_sample['year_build'].apply(get_era)
    
    # 3. Haggle metric
    df_sample['Haggle_%'] = df_sample['%_change_between_offer_and_purchase'].abs()

    # 4. Create Scatter with OLS Regression (Learning Objective: Estimating functional relationships)
    fig = px.scatter(df_sample, 
                     x="year_build", 
                     y="sqm_price", 
                     color="Era",
                     size="Haggle_%",
                     trendline="ols", # Demonstrates regression and smoothing noise
                     hover_data=['address', 'city', 'sqm'],
                     title="The Insulation Tax: Functional Relationship between Age and Value (2023)",
                     labels={
                         "year_build": "Construction Year",
                         "sqm_price": "Price (DKK/sqm)",
                         "Haggle_%": "Negotiated Discount (%)"
                     },
                     color_discrete_map={
                         'Pre-1961 (G/F)': '#d73027',
                         '1961-77 (E)': '#f46d43',
                         '1977-95 (D)': '#fdae61',
                         'Post-1995 (C-A)': '#1a9850'
                     },
                     template="plotly_white")

    fig.update_layout(
        font=dict(family="Georgia, serif", size=14),
        legend=dict(title="Efficiency Era", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(range=[1880, 2025])
    )

    # Note on Regression
    fig.add_annotation(
        x=2000, y=df_sample['sqm_price'].quantile(0.95),
        text="OLS Regression Line:<br>Quantifying the average price increase per building year",
        showarrow=False, bgcolor="white", opacity=0.8
    )

    fig.write_html('docs/insulation_explorer.html')
    print("Figure 3 (Academic Grade) saved.")

if __name__ == "__main__":
    create_insulation_explorer()
