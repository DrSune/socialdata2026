import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df_hist = pd.read_csv('solutions/hist.csv')
df_recent = pd.read_csv('solutions/recent.csv')

# Standardize
df_hist['Category'] = df_hist['Category'].str.upper().str.replace('/', ' ')
df_recent['Category'] = df_recent['Incident Category'].str.upper().str.replace('/', ' ')
crime_map = {'DRUG NARCOTIC': 'DRUG OFFENSE', 'LARCENY/THEFT': 'LARCENY THEFT'}
df_hist['Category'] = df_hist['Category'].replace(crime_map)
df_recent['Category'] = df_recent['Category'].replace(crime_map)

# Extract Year
df_hist['Year'] = pd.to_datetime(df_hist['Date'], format='mixed').dt.year
df_recent['Year'] = pd.to_datetime(df_recent['Incident Date'], format='mixed').dt.year

# Combine
h = df_hist[['Category', 'Year']]
r = df_recent[['Category', 'Year']]
df = pd.concat([h, r], ignore_index=True)

# Filter and Group
focus = ['LARCENY THEFT', 'DRUG OFFENSE']
df_f = df[df['Category'].isin(focus)]
yearly = df_f.groupby(['Year', 'Category']).size().reset_index(name='Counts')

# Create Plotly figure
fig = px.line(yearly, x='Year', y='Counts', color='Category',
              title='Decoupling Trends: Larceny (Opportunity) vs. Drugs (Enforcement)',
              labels={'Counts': 'Number of Incidents'},
              markers=True)

# Add annotations for key shifts (e.g., 2018 schema change or specific policy shifts)
fig.add_annotation(x=2020, y=yearly[yearly['Year']==2020]['Counts'].max(),
            text="COVID-19 Impact", showarrow=True, arrowhead=1)

fig.update_layout(
    template='plotly_white',
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Save as HTML (Option B: CDN for smaller file)
fig.write_html('docs/interactive_trends.html', include_plotlyjs='cdn')
print("Interactive plot saved to docs/interactive_trends.html")
