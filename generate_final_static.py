import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_final_static_viz():
    df = pd.read_parquet('full_housing_data.parquet')
    
    def get_efficiency_era(year):
        if year < 1961: return 'G/F (Pre-Insulation)'
        if year < 1977: return 'E (Minimal)'
        if year < 1995: return 'D (Standard)'
        if year < 2010: return 'C (Modern)'
        return 'B/A (High Efficiency)'

    df['Efficiency_Era'] = df['year_build'].apply(get_efficiency_era)
    
    # Filter for two comparable periods: Pre-Crisis (2019) vs Crisis (2023)
    df_2019 = df[(df['date'] >= '2019-01-01') & (df['date'] <= '2019-12-31')].copy()
    df_2023 = df[(df['date'] >= '2023-01-01') & (df['date'] <= '2023-12-31')].copy()
    
    stats_2019 = df_2019.groupby('Efficiency_Era')['sqm_price'].median()
    stats_2023 = df_2023.groupby('Efficiency_Era')['sqm_price'].median()
    
    stats = pd.DataFrame({'2019': stats_2019, '2023': stats_2023})
    stats = stats.reindex(['G/F (Pre-Insulation)', 'E (Minimal)', 'D (Standard)', 'C (Modern)', 'B/A (High Efficiency)'])

    plt.figure(figsize=(10, 8), facecolor='#f4f4f4')
    sns.set_style("white")
    
    colors = ['#d73027', '#f46d43', '#fdae61', '#a6d96a', '#1a9850']
    
    for i, era in enumerate(stats.index):
        y_start = stats.loc[era, '2019']
        y_end = stats.loc[era, '2023']
        
        plt.plot([0, 1], [y_start, y_end], marker='o', color=colors[i], linewidth=4, markersize=10)
        plt.text(-0.05, y_start, f"{era}\n{int(y_start)} DKK", ha='right', va='center', fontsize=11, fontweight='bold', color=colors[i])
        plt.text(1.05, y_end, f"{int(y_end)} DKK", ha='left', va='center', fontsize=11, fontweight='bold', color=colors[i])

    plt.xticks([0, 1], ['2019 (Stable)', '2023 (Crisis)'], fontsize=14, fontweight='bold')
    plt.yticks([])
    plt.title('The Insulation Penalty: Widening Gap in Property Values', fontsize=18, fontweight='bold', pad=40)
    plt.xlim(-0.6, 1.6)
    sns.despine(left=True, bottom=True)
    
    plt.text(0.5, plt.ylim()[1], "Median Price per sqm", ha='center', va='bottom', fontsize=12, style='italic', color='#666')
    
    plt.tight_layout()
    plt.savefig('docs/price_slope_chart.png', dpi=300, bbox_inches='tight')
    print("Static Slope Chart saved to docs/price_slope_chart.png")

if __name__ == "__main__":
    create_final_static_viz()
