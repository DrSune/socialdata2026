import pandas as pd
import plotly.graph_objects as go
import numpy as np

def create_heatmap_movie():
    print("Loading data for HeatMapWithTime...")
    df = pd.read_parquet('full_housing_data.parquet')
    
    def get_efficiency_era(year):
        if year < 1961: return 'G/F'
        return 'Other'

    df['Era'] = df['year_build'].apply(get_efficiency_era)
    df_gf = df[df['Era'] == 'G/F'].copy()
    
    df_gf['Quarter'] = pd.to_datetime(df_gf['date']).dt.to_period('Q').astype(str)
    
    # Use 'area' for more granularity
    agg = df_gf.groupby(['Quarter', 'area'], observed=True)['sqm_price'].median().reset_index()
    
    # Cast area to string to avoid Categorical + str error
    agg['area'] = agg['area'].astype(str)
    
    area_coords = {
        'Capital, Copenhagen': [55.67, 12.56],
        'North Zealand': [55.93, 12.3],
        'Other islands': [55.3, 11.6],
        'Fyn & islands': [55.4, 10.4],
        'South jutland': [55.0, 9.4],
        'East & mid jutland': [56.1, 9.8],
        'North jutland': [57.0, 9.9],
        'Bornholm': [55.1, 14.9]
    }
    
    fig = go.Figure()
    quarters = sorted(agg['Quarter'].unique())
    quarters = [q for q in quarters if q >= '2014Q1']
    agg = agg[agg['Quarter'].isin(quarters)]
    
    for q in quarters:
        q_data = agg[agg['Quarter'] == q]
        q_data = q_data[q_data['area'].isin(area_coords.keys())]
        
        fig.add_trace(go.Scattergeo(
            lon=[area_coords[r][1] for r in q_data['area']],
            lat=[area_coords[r][0] for r in q_data['area']],
            text=q_data['area'] + ": " + q_data['sqm_price'].astype(int).astype(str) + " DKK",
            marker=dict(
                size=q_data['sqm_price'] / 400,
                color=q_data['sqm_price'],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Median Price/sqm", thickness=15, len=0.5)
            ),
            name=q,
            visible=False
        ))
        
    fig.data[0].visible = True
    
    steps = []
    for i, q in enumerate(quarters):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": f"The Evolution of the Insulation Penalty: G/F Era Housing Prices ({q})"}],
            label=q
        )
        step["args"][0]["visible"][i] = True
        steps.append(step)
        
    sliders = [dict(active=0, currentvalue={"prefix": "Quarter: "}, pad={"t": 50}, steps=steps)]
    
    fig.update_layout(
        sliders=sliders,
        geo=dict(
            scope='europe',
            resolution=50,
            lonaxis_range=[8, 16],
            lataxis_range=[54.5, 58],
            showland=True,
            landcolor="white",
            subunitcolor="lightgray",
            countrycolor="gray",
            bgcolor="rgba(244,244,244,1)"
        ),
        margin={"r":0,"t":100,"l":0,"b":0},
        title="The Evolution of the Insulation Penalty: G/F Era Housing Prices (2014-2024)",
        font=dict(family="Georgia, serif", size=14)
    )
    
    fig.write_html('docs/vulnerability_movie.html')
    print("Vulnerability Movie saved to docs/vulnerability_movie.html")

if __name__ == "__main__":
    create_heatmap_movie()
