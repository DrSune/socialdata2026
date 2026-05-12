import pandas as pd
import plotly.express as px

def create_parallel_categories():
    print("Generating Candidate B: Parallel Resilience Flow...")
    df = pd.read_parquet('full_housing_data.parquet')
    
    # 1. Filter for the crisis era (2023)
    df_2023 = df[(df['date'] >= '2023-01-01') & (df['date'] <= '2023-12-31')].copy()
    
    # 2. Categorize Era
    def get_efficiency_era(year):
        if year < 1961: return 'G/F'
        if year < 1995: return 'E/D'
        return 'C/B/A'
    df_2023['Efficiency'] = df_2023['year_build'].apply(get_efficiency_era)
    
    # 3. Categorize Outcome (Haggling)
    def get_outcome(val):
        val = abs(val)
        if val > 8: return 'Extreme (>8%)'
        if val > 4: return 'Significant (4-8%)'
        return 'Stable (<4%)'
    df_2023['Outcome'] = df_2023['%_change_between_offer_and_purchase'].apply(get_outcome)
    
    # 4. Use Area
    df_2023['Area'] = df_2023['area'].astype(str)
    
    # Filter out small samples or unknowns if any
    plot_df = df_2023[['Efficiency', 'Area', 'Outcome']].dropna().copy()
    
    # Create the flow
    fig = px.parallel_categories(plot_df, 
                                 dimensions=['Efficiency', 'Area', 'Outcome'],
                                 color_continuous_scale=px.colors.sequential.Inferno,
                                 labels={'Efficiency': 'Building Era', 'Area': 'Region', 'Outcome': 'Price Stress'},
                                 title="The Path to Energy Poverty: Flowing through Era, Geography, and Price Stress (2023)")

    fig.update_layout(
        font=dict(family="Georgia, serif", size=14),
        margin=dict(l=150, r=150, t=100, b=100)
    )

    fig.write_html('docs/candidate_parallel.html')
    print("Candidate B (Parallel) saved.")

if __name__ == "__main__":
    create_parallel_categories()
