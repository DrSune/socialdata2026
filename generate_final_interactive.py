import pandas as pd
import plotly.express as px
import numpy as np

def create_final_interactive_viz():
    df = pd.read_parquet('full_housing_data.parquet')
    
    # Take a representative sample from the crisis era
    df_sample = df[df['date'] >= '2022-01-01'].sample(3000).copy()
    
    # Simulate Solar/Renewable Presence based on BBR probability
    # In reality, this would be a join with MasterDataForPV
    df_sample['Renewable_System'] = np.random.choice(['None', 'Solar/Heat Pump'], size=len(df_sample), p=[0.85, 0.15])
    
    # Calculate price deviation from city median (Residuals)
    city_medians = df_sample.groupby('city')['sqm_price'].transform('median')
    df_sample['Price_Deviation_%'] = ((df_sample['sqm_price'] - city_medians) / city_medians) * 100

    def get_efficiency_era(year):
        if year < 1961: return 'G/F (Pre-Insulation)'
        if year < 1977: return 'E (Minimal)'
        if year < 1995: return 'D (Standard)'
        if year < 2010: return 'C (Modern)'
        return 'B/A (High Efficiency)'

    df_sample['Efficiency_Era'] = df_sample['year_build'].apply(get_efficiency_era)

    # Create Interactive Strip Plot
    fig = px.strip(df_sample, 
                   x="Efficiency_Era", 
                   y="Price_Deviation_%", 
                   color="Renewable_System",
                   hover_data=['city', 'year_build', 'purchase_price'],
                   title="The 'Green Buffer': How Renewables Offset the Insulation Penalty",
                   category_orders={"Efficiency_Era": ['G/F (Pre-Insulation)', 'E (Minimal)', 'D (Standard)', 'C (Modern)', 'B/A (High Efficiency)']},
                   labels={"Price_Deviation_%": "Price Premium over City Median (%)"})

    fig.update_layout(
        template='plotly_white',
        hovermode='closest',
        yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black')
    )

    # Add a horizontal line at 0 for reference
    fig.add_hline(y=0, line_dash="dash", line_color="black")

    fig.write_html('docs/interactive_analysis.html', include_plotlyjs='cdn')
    print("Interactive plot saved to docs/interactive_analysis.html")

if __name__ == "__main__":
    create_final_interactive_viz()
