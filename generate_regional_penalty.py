import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def create_regional_facets():
    print("Generating Figure 2: The Regional Penalty (Small Multiples)...")
    df = pd.read_parquet('full_housing_data.parquet')
    
    # 1. Focus on Pre-Crisis (2019) vs Crisis Peak (2023)
    df_compare = df[(df['date'] >= '2019-01-01') & (df['date'] <= '2023-12-31')].copy()
    df_compare['Year'] = pd.to_datetime(df_compare['date']).dt.year
    df_compare = df_compare[df_compare['Year'].isin([2019, 2023])]
    
    def get_group(year):
        if year < 1977: return 'Legacy (G-E)'
        return 'Modern (D-A)'
    df_compare['Group'] = df_compare['year_build'].apply(get_group)
    
    # 2. Calculate Median Price per Area and Year
    agg = df_compare.groupby(['area', 'Year', 'Group'], observed=True)['sqm_price'].median().reset_index()
    
    # 3. Pivot to calculate % Change
    pivot = agg.pivot(index=['area', 'Group'], columns='Year', values='sqm_price').reset_index()
    pivot['Change_%'] = ((pivot[2023] - pivot[2019]) / pivot[2019]) * 100
    
    # 4. Small Multiples Bar Chart
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(14, 10))
    
    # Create the facet plot
    g = sns.catplot(
        data=pivot, kind="bar",
        x="Change_%", y="area", hue="Group",
        palette={"Legacy (G-E)": "#d73027", "Modern (D-A)": "#1a9850"},
        height=6, aspect=1.5,
        legend_out=False
    )
    
    # Add a vertical line at 0
    for ax in g.axes.flat:
        ax.axvline(0, color='black', lw=1.5, linestyle='--')
        # Add labels to bars
        for p in ax.patches:
            width = p.get_width()
            if abs(width) > 0:
                ax.annotate(f'{width:.1f}%', 
                            (width, p.get_y() + p.get_height() / 2),
                            ha = 'left' if width > 0 else 'right', 
                            va = 'center', 
                            xytext = (5 if width > 0 else -5, 0), 
                            textcoords = 'offset points',
                            fontsize=10, fontweight='bold')

    g.set_axis_labels("Price Change 2019 → 2023 (%)", "")
    g.fig.suptitle("The Insulation Tax is Universal: Price Growth by Region", fontsize=20, fontweight='bold', y=1.05)
    
    plt.savefig('docs/regional_penalty.png', dpi=300, bbox_inches='tight')
    print("Figure 2 (Regional Facets) saved.")

if __name__ == "__main__":
    create_regional_facets()
