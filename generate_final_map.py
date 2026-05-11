import pandas as pd
import folium

def create_final_map():
    df = pd.read_csv('final_viz_data.csv')
    
    # Center map on Denmark
    m = folium.Map(location=[56.0, 10.5], zoom_start=7, tiles='CartoDB positron')
    
    # Define Resilient Outliers
    legacy_eras = ['G/F (Pre-Insulation)', 'E (Minimal)', 'D (Standard)']
    close_nature = ['Immediate (<1km)', 'Close (1-5km)']
    
    df['is_outlier'] = (
        (df['Efficiency_Era'].isin(legacy_eras)) & 
        (df['Price_Deviation_%'] > 0) & 
        (df['Nature_Proximity'].isin(close_nature))
    )

    # Plot Background Houses (Normal/Expected)
    for _, row in df[~df['is_outlier']].iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=3,
            color='gray',
            fill=True,
            fill_opacity=0.4,
            stroke=False,
            popup=(f"<b>Standard Sale</b><br>"
                   f"<b>Era:</b> {row['Efficiency_Era']}<br>"
                   f"<b>Nature Distance:</b> {int(row['distance_to_nature_m'])}m<br>"
                   f"<b>Price Deviation:</b> {row['Price_Deviation_%']:.1f}%")
        ).add_to(m)

    # Plot Resilient Outliers
    for _, row in df[df['is_outlier']].iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=8,
            color='#1a9850', # Vibrant Green
            fill=True,
            fill_opacity=0.9,
            weight=2,
            popup=(f"<b>RESILIENT OUTLIER</b><br>"
                   f"<b>Address:</b> {row['input']}<br>"
                   f"<b>Era:</b> {row['Efficiency_Era']} (High Penalty Risk)<br>"
                   f"<b>Nature Distance:</b> {int(row['distance_to_nature_m'])}m<br>"
                   f"<b>Price Premium:</b> <span style='color:green'>+{row['Price_Deviation_%']:.1f}%</span> vs local median")
        ).add_to(m)

    # Add a more narrative legend
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 300px; height: auto; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white; opacity: 0.9; padding: 15px; border-radius: 5px;">
     <h4 style="margin-top:0; margin-bottom:10px; font-size:16px;">The Geography of Resilience</h4>
     <p style="margin-bottom:10px; font-size:12px; line-height:1.2;">Mapping how nature offsets poor insulation.</p>
     <i class="fa fa-circle" style="color:#1a9850; font-size:16px;"></i> <b>Resilient Outliers</b><br>
     <span style="font-size:11px; color:#555; margin-left:15px; display:block; margin-bottom:8px;">Older homes (G-D labels) near nature selling <i>above</i> local medians.</span>
     <i class="fa fa-circle" style="color:gray; font-size:10px;"></i> <b>Standard Sales</b><br>
     <span style="font-size:11px; color:#555; margin-left:15px; display:block;">Modern homes or expected price penalties.</span>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    m.save('docs/geographic_distribution.html')
    print("Narrative Map saved to docs/geographic_distribution.html")

if __name__ == "__main__":
    create_final_map()
