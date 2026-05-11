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
    
    df_gf['date_dt'] = pd.to_datetime(df_gf['date'])
    df_gf['Quarter'] = df_gf['date_dt'].dt.to_period('Q').astype(str)
    
    agg = df_gf.groupby(['Quarter', 'area'], observed=True)['sqm_price'].median().reset_index()
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
    quarters = [q for q in quarters if q >= '2016Q1']
    agg = agg[agg['Quarter'].isin(quarters)]
    
    for q in quarters:
        q_data = agg[agg['Quarter'] == q]
        q_data = q_data[q_data['area'].isin(area_coords.keys())]
        
        fig.add_trace(go.Scattergeo(
            lon=[area_coords[r][1] for r in q_data['area']],
            lat=[area_coords[r][0] for r in q_data['area']],
            # Remove text from markers to prevent overlap, rely on hover
            hoverinfo="text",
            hovertext=q_data['area'] + ": " + q_data['sqm_price'].astype(int).astype(str) + " DKK",
            mode='markers',
            marker=dict(
                size=q_data['sqm_price'] / 400,
                color=q_data['sqm_price'],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Median Price/sqm", thickness=15, len=0.7, y=0.5)
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
                  {"title": f"The Evolution of the Insulation Penalty: G/F Era ({q})"}],
            label=q
        )
        step["args"][0]["visible"][i] = True
        steps.append(step)
        
    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Selected: ", "font": {"size": 16}, "visible": True},
        pad={"t": 80, "b": 10},
        steps=steps,
        minorticklen=0,
        ticklen=10,
        len=0.9,
        x=0.05
    )]
    
    fig.update_layout(
        sliders=sliders,
        geo=dict(
            scope='europe',
            resolution=50,
            lonaxis_range=[8, 16],
            lataxis_range=[54.5, 58],
            showland=True,
            landcolor="#f5f5f5",
            subunitcolor="white",
            countrycolor="#dcdcdc",
            bgcolor="rgba(0,0,0,0)"
        ),
        margin={"r":20,"t":100,"l":20,"b":50},
        height=700,
        title=dict(
            text="The Evolution of the Insulation Penalty: G/F Era (2016-2024)",
            x=0.5,
            y=0.95,
            font=dict(size=22, family="Helvetica Neue")
        ),
        font=dict(family="Georgia, serif")
    )
    
    fig.write_html('docs/vulnerability_movie.html')
    print("Fixed Vulnerability Movie saved.")

if __name__ == "__main__":
    create_heatmap_movie()
