import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_market_rhythms():
    print("Loading data for Market Rhythms...")
    df = pd.read_parquet('full_housing_data.parquet')
    
    # Define groups
    def get_efficiency_era(year):
        if year < 1977: return 'Legacy (G-E)'
        return 'Modern (D-A)'
    df['Group'] = df['year_build'].apply(get_efficiency_era)
    
    # Use '%_change_between_offer_and_purchase' (Price Haggling)
    # This is a high-signal metric for 'Market Anxiety' or 'Pressure'
    df['date_dt'] = pd.to_datetime(df['date'])
    df_recent = df[df['date_dt'] >= '2019-01-01'].copy()
    
    df_recent['Month'] = df_recent['date_dt'].dt.month
    df_recent['Year'] = df_recent['date_dt'].dt.year
    
    # Calculate median haggling per year/month
    # Note: typically haggling is negative (reduction). We'll use absolute to show 'Gap'
    df_recent['Haggling_%'] = df_recent['%_change_between_offer_and_purchase'].abs()

    fig, axes = plt.subplots(1, 2, figsize=(20, 8), sharey=True)
    groups = ['Modern (D-A)', 'Legacy (G-E)']
    
    for i, group in enumerate(groups):
        subset = df_recent[df_recent['Group'] == group]
        pivot = subset.groupby(['Year', 'Month'])['Haggling_%'].median().unstack(fill_value=0)
        
        sns.heatmap(pivot, ax=axes[i], cmap="YlOrRd", annot=True, fmt=".1f", cbar_kws={'label': 'Median Price Haggle (%)'})
        axes[i].set_title(f"Haggling Intensity: {group}", fontsize=16, fontweight='bold')
        axes[i].set_xlabel("Month of Year")
        axes[i].set_ylabel("Year")

    plt.suptitle("The Anxiety Index: Negotiating the Insulation Penalty (2019-2024)", fontsize=22, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.savefig('docs/market_rhythms.png', dpi=300, bbox_inches='tight')
    print("Haggling Rhythms Heatmap saved.")

if __name__ == "__main__":
    create_market_rhythms()
