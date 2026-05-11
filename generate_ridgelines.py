import pandas as pd
import matplotlib.pyplot as plt
from joypy import joyplot
import numpy as np

def create_ridgeline_viz():
    print("Loading data for Ridgeline plot...")
    df = pd.read_parquet('full_housing_data.parquet')
    
    def get_efficiency_era(year):
        if year < 1961: return 'G/F (Pre-1961)'
        if year < 1977: return 'E (1961-77)'
        if year < 1995: return 'D (1977-95)'
        if year < 2010: return 'C (1995-10)'
        return 'B/A (Post-2010)'

    df['Efficiency_Era'] = df['year_build'].apply(get_efficiency_era)
    
    df_pre = df[(df['date'] >= '2018-01-01') & (df['date'] <= '2019-12-31')].copy()
    df_peak = df[(df['date'] >= '2022-01-01') & (df['date'] <= '2023-12-31')].copy()
    
    p99 = df['sqm_price'].quantile(0.99)
    era_order = ['G/F (Pre-1961)', 'E (1961-77)', 'D (1977-95)', 'C (1995-10)', 'B/A (Post-2010)']
    
    # Create 2018-19 plot
    fig1, ax1 = joyplot(df_pre[df_pre['sqm_price'] < p99], by="Efficiency_Era", column="sqm_price", 
                        order=era_order, colormap=plt.cm.RdYlGn, alpha=0.8,
                        figsize=(10, 8), title="Price Distribution 2018-19 (Stable)")
    plt.xlabel("Price per sqm (DKK)")
    plt.savefig('docs/ridges_pre.png', dpi=300, bbox_inches='tight')
    
    # Create 2022-23 plot
    fig2, ax2 = joyplot(df_peak[df_peak['sqm_price'] < p99], by="Efficiency_Era", column="sqm_price", 
                        order=era_order, colormap=plt.cm.RdYlGn, alpha=0.8,
                        figsize=(10, 8), title="Price Distribution 2022-23 (Crisis)")
    plt.xlabel("Price per sqm (DKK)")
    plt.savefig('docs/ridges_peak.png', dpi=300, bbox_inches='tight')
    
    print("Ridgeline plots saved to docs/ridges_pre.png and docs/ridges_peak.png")

if __name__ == "__main__":
    create_ridgeline_viz()
