import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_final_static_viz():
    df = pd.read_parquet('full_housing_data.parquet')
    
    # Proxy for Energy Efficiency based on Danish Building Regulations (BR)
    # BR77, BR95, BR06, BR10, BR15 are key shifts
    def get_efficiency_era(year):
        if year < 1961: return 'G/F (Pre-Insulation)'
        if year < 1977: return 'E (Minimal)'
        if year < 1995: return 'D (Standard)'
        if year < 2010: return 'C (Modern)'
        return 'B/A (High Efficiency)'

    df['Efficiency_Era'] = df['year_build'].apply(get_efficiency_era)
    
    # Filter for two comparable periods: Stable (2018-2019) vs Crisis (2022-2023)
    df_2019 = df[(df['date'] >= '2018-01-01') & (df['date'] <= '2019-12-31')].copy()
    df_2023 = df[(df['date'] >= '2022-01-01') & (df['date'] <= '2023-12-31')].copy()
    
    df_2019['Period'] = '2018-19 (Stable)'
    df_2023['Period'] = '2022-23 (Crisis)'
    
    df_plot = pd.concat([df_2019, df_2023])
    
    # Calculate median sqm_price per Era per Period
    stats = df_plot.groupby(['Period', 'Efficiency_Era'])['sqm_price'].median().unstack('Period')
    stats = stats.sort_values(by='2018-19 (Stable)')

    # Create Slope Chart
    plt.figure(figsize=(10, 8))
    sns.set_style("white")
    
    eras = stats.index.tolist()
    colors = sns.color_palette("RdYlGn", len(eras))

    for i, era in enumerate(eras):
        y_start = stats.loc[era, '2018-19 (Stable)']
        y_end = stats.loc[era, '2022-23 (Crisis)']
        
        plt.plot([0, 1], [y_start, y_end], marker='o', color=colors[i], linewidth=3, label=era)
        plt.text(-0.05, y_start, f"{era}: {int(y_start)}", horizontalalignment='right', fontsize=10, weight='bold')
        plt.text(1.05, y_end, f"{int(y_end)}", horizontalalignment='left', fontsize=10, weight='bold')

    plt.xticks([0, 1], ['2018-19 (Stable)', '2022-23 (Crisis)'], fontsize=12, weight='bold')
    plt.yticks([])
    plt.title('The Widening Gap: Median Price/sqm by Efficiency Era', fontsize=16, pad=30)
    plt.xlim(-0.5, 1.5)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    
    plt.legend(title="Building Era", loc='upper left', bbox_to_anchor=(1.1, 1))
    plt.tight_layout()
    plt.savefig('docs/price_slope_chart.png', dpi=300)
    print("Static Slope Chart saved to docs/price_slope_chart.png")

if __name__ == "__main__":
    create_final_static_viz()
