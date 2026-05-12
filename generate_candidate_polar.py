import pandas as pd
import plotly.express as px
import numpy as np

def create_polar_compass():
    print("Generating Candidate A: Polar Market Compass...")
    df = pd.read_parquet('full_housing_data.parquet')
    
    # Focus on the crisis period
    df_crisis = df[(df['date'] >= '2022-01-01') & (df['date'] <= '2023-12-31')].copy()
    
    df_crisis['Month'] = pd.to_datetime(df_crisis['date']).dt.month
    df_crisis['MonthName'] = pd.to_datetime(df_crisis['date']).dt.month_name()
    
    def get_efficiency_era(year):
        if year < 1977: return 'Legacy (G-E)'
        return 'Modern (D-A)'
    df_crisis['Group'] = df_crisis['year_build'].apply(get_efficiency_era)
    
    # Calculate median haggling (%) per month
    df_crisis['Haggling'] = df_crisis['%_change_between_offer_and_purchase'].abs()
    
    agg = df_crisis.groupby(['Month', 'MonthName', 'Group'])['Haggling'].median().reset_index()
    
    # Polar bar chart
    fig = px.bar_polar(agg, r="Haggling", theta="MonthName", color="Group",
                       template="plotly_white",
                       barmode="group",
                       title="The Seasonal Squeeze: Negotiation Pressure by Month (2022-23)",
                       color_discrete_map={'Legacy (G-E)': '#d73027', 'Modern (D-A)': '#4575b4'},
                       labels={"Haggling": "Median Discount (%)"})
    
    fig.update_layout(
        font=dict(family="Georgia, serif", size=14),
        polar=dict(
            radialaxis=dict(showticklabels=True, ticks='', ticksuffix='%'),
            angularaxis=dict(rotation=90, direction="clockwise")
        )
    )
    
    fig.write_html('docs/candidate_polar.html')
    print("Candidate A (Polar) saved.")

if __name__ == "__main__":
    create_polar_compass()
