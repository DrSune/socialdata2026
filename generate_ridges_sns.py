import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_ridges_seaborn():
    print("Loading data for Seaborn Ridgelines...")
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
    
    # Increase spacing and fix text clipping
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    pal = sns.color_palette("RdYlGn", 5) # Use clear semantic colors
    
    def plot_period(data, title, filename):
        data_clean = data[data['sqm_price'] < p99].copy()
        
        # Increased height and adjusted aspect for better vertical separation
        g = sns.FacetGrid(data_clean, row="Efficiency_Era", hue="Efficiency_Era", aspect=8, height=1.2, palette=pal, row_order=era_order)
        
        g.map(sns.kdeplot, "sqm_price", bw_adjust=.5, clip_on=False, fill=True, alpha=0.7, linewidth=2)
        g.map(sns.kdeplot, "sqm_price", clip_on=False, color="black", lw=1, bw_adjust=.5)
        g.map(plt.axhline, y=0, lw=2, clip_on=False, color='black')

        def label(x, color, label):
            ax = plt.gca()
            # Move labels further left and ensure they don't overlap the plot
            ax.text(-0.15, .2, label, fontweight="bold", color='black', ha="right", va="center", transform=ax.transAxes, fontsize=12)

        g.map(label, "sqm_price")
        
        # Fix overlap and clipping
        g.fig.subplots_adjust(hspace=0.1, left=0.2) 
        g.set_titles("")
        g.set(yticks=[], ylabel="")
        g.despine(bottom=True, left=True)
        
        plt.xlabel("Price per sqm (DKK)", fontsize=12, fontweight='bold')
        g.fig.suptitle(title, fontsize=18, fontweight='bold', y=1.02)
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

    plot_period(df_pre, "2018-19: Stable Market Overlap", "docs/ridges_pre.png")
    plot_period(df_peak, "2022-23: The Great Decoupling", "docs/ridges_peak.png")
    print("Fixed Ridgeline plots saved.")

if __name__ == "__main__":
    create_ridges_seaborn()
