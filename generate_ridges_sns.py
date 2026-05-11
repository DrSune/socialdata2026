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
    
    df_pre['Period'] = '2018-19 (Stable)'
    df_peak['Period'] = '2022-23 (Crisis)'
    
    df_plot = pd.concat([df_pre, df_peak])
    p99 = df['sqm_price'].quantile(0.99)
    df_plot = df_plot[df_plot['sqm_price'] < p99]
    
    era_order = ['G/F (Pre-1961)', 'E (1961-77)', 'D (1977-95)', 'C (1995-10)', 'B/A (Post-2010)']
    
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
    
    def plot_period(data, title, filename):
        g = sns.FacetGrid(data, row="Efficiency_Era", hue="Efficiency_Era", aspect=15, height=.5, palette=pal, row_order=era_order)
        g.map(sns.kdeplot, "sqm_price", bw_adjust=.5, clip_on=False, fill=True, alpha=1, linewidth=1.5)
        g.map(sns.kdeplot, "sqm_price", clip_on=False, color="w", lw=2, bw_adjust=.5)
        g.map(plt.axhline, y=0, lw=2, clip_on=False)

        def label(x, color, label):
            ax = plt.gca()
            ax.text(0, .2, label, fontweight="bold", color=color, ha="left", va="center", transform=ax.transAxes)

        g.map(label, "sqm_price")
        g.fig.subplots_adjust(hspace=-.25)
        g.set_titles("")
        g.set(yticks=[], ylabel="")
        g.despine(bottom=True, left=True)
        plt.xlabel("Price per sqm (DKK)")
        g.fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
        plt.savefig(filename, dpi=300, bbox_inches='tight')

    plot_period(df_pre, "Price Distribution 2018-19 (Stable)", "docs/ridges_pre.png")
    plot_period(df_peak, "Price Distribution 2022-23 (Crisis)", "docs/ridges_peak.png")
    print("Seaborn Ridgelines saved.")

if __name__ == "__main__":
    create_ridges_seaborn()
