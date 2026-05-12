import pandas as pd
import plotly.express as px
import numpy as np

def create_insulation_explorer():
    print("Generating Figure 3: The Insulation Tax Explorer (Refined)...")
    df = pd.read_parquet('full_housing_data.parquet')
    
    # 1. Filter for 2023 sales
    df_2023 = df[(df['date'] >= '2023-01-01') & (df['date'] <= '2023-12-31')].copy()
    
    # Sample for performance
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

    # 4. Refine the scatter to highlight the 'Renovation Gap'
    # We'll use marker symbol to distinguish between 'Typical' and 'Premium Outliers'
    # or just use color more effectively.
    
    fig = px.scatter(df_sample, 
                     x="year_build", 
                     y="sqm_price", 
                     color="Era",
                     size="Haggle_%",
                     hover_data=['address', 'city', 'sqm'],
                     title="The Insulation Tax vs. The 'Newness' Premium",
                     labels={
                         "year_build": "Year Built",
                         "sqm_price": "Price (DKK/sqm)",
                         "Haggle_%": "Price Haggle (%)"
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
        legend=dict(title="Building Era", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Add annotation for the 'Renovated Exception'
    fig.add_annotation(
        x=1920, y=df_sample[df_sample['year_build'] < 1940]['sqm_price'].max(),
        text="Renovated Outliers:<br>Old soul, modern efficiency",
        showarrow=True, arrowhead=1, ax=-60, ay=-30
    )

    fig.write_html('docs/insulation_explorer.html')
    print("Figure 3 (Refined) saved.")

if __name__ == "__main__":
    create_insulation_explorer()
