import pandas as pd
import plotly.express as px

def create_final_interactive_viz():
    df = pd.read_csv('final_viz_data.csv')
    
    # Sort Efficiency Era for better visualization
    era_order = ['G/F (Pre-Insulation)', 'E (Minimal)', 'D (Standard)', 'C (Modern)', 'B/A (High Efficiency)']
    df['Efficiency_Era'] = pd.Categorical(df['Efficiency_Era'], categories=era_order, ordered=True)
    df = df.sort_values('Efficiency_Era')

    # To make the narrative punchier, let's simplify nature proximity to a binary for the main comparison,
    # or use a Box Plot with points to clearly show the shift in median and distribution
    
    # Create Box plot with points to show distributions clearly
    fig = px.box(df, 
                 x="Efficiency_Era", 
                 y="Price_Deviation_%", 
                 color="Nature_Proximity",
                 points="all", # Shows all points alongside the box
                 hover_data=['city', 'year_build', 'purchase_price', 'distance_to_nature_m'],
                 title="The 'Green Buffer': Quantifying the Nature Premium",
                 color_discrete_map={
                     'Immediate (<1km)': '#1a9850',
                     'Close (1-5km)': '#a6d96a',
                     'Nearby (5-10km)': '#fdae61',
                     'Distant (>10km)': '#d73027'
                 },
                 labels={
                     "Price_Deviation_%": "Price Premium vs Local Median (%)",
                     "Efficiency_Era": "Building Efficiency Era",
                     "Nature_Proximity": "Distance to Nature"
                 })

    fig.update_layout(
        template='plotly_white',
        hovermode='closest',
        boxmode='group', # Group boxes by color
        yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black'),
        font=dict(family="Georgia, serif"),
        legend=dict(
            title="Nature Proximity",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Add a horizontal line at 0 (the local median benchmark)
    fig.add_hline(y=0, line_dash="dash", line_color="black", annotation_text="Local Median Price", annotation_position="bottom right")

    fig.write_html('docs/interactive_analysis.html', include_plotlyjs='cdn')
    print("Interactive Box plot saved to docs/interactive_analysis.html")

if __name__ == "__main__":
    create_final_interactive_viz()
