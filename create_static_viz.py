import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup styling
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# Load and prep data (simplified from analysis.py)
df_hist = pd.read_csv('solutions/hist.csv')
df_recent = pd.read_csv('solutions/recent.csv')

df_hist['Category'] = df_hist['Category'].str.upper().str.replace('/', ' ')
df_recent['Category'] = df_recent['Incident Category'].str.upper().str.replace('/', ' ')

crime_map = {'DRUG NARCOTIC': 'DRUG OFFENSE', 'MOTOR VEHICLE THEFT': 'VEHICLE THEFT', 'LARCENY/THEFT': 'LARCENY THEFT'}
df_hist['Category'] = df_hist['Category'].replace(crime_map)
df_recent['Category'] = df_recent['Category'].replace(crime_map)

h = df_hist[['Category', 'Time']].copy()
r = df_recent[['Category', 'Incident Time']].copy()
r.columns = h.columns
df = pd.concat([h, r], ignore_index=True)
df = df.dropna()

df['Time_dt'] = pd.to_datetime(df['Time'], format='mixed')
df['Hour'] = df['Time_dt'].dt.hour

# Focus on contrasting rhythms
focus = ['LARCENY THEFT', 'BURGLARY', 'DRUG OFFENSE']
df_f = df[df['Category'].isin(focus)]
hourly = df_f.groupby(['Hour', 'Category']).size().unstack()

# Normalize to see relative "peakiness"
hourly_norm = hourly / hourly.sum()

# Plot
plt.figure(figsize=(12, 6))
for cat in focus:
    plt.plot(hourly_norm.index, hourly_norm[cat], label=cat, linewidth=3, marker='o', markersize=4)

plt.title('The Daily Rhythm of SF Crime: Opportunity vs. Enforcement', fontsize=16, pad=20)
plt.xlabel('Hour of Day (24h)', fontsize=12)
plt.ylabel('Proportion of Daily Total', fontsize=12)
plt.xticks(range(24))
plt.legend(title='Crime Type')
plt.grid(True, linestyle='--', alpha=0.7)

# Add annotations to guide the reader
plt.annotate('Larceny peaks with\ndaytime foot traffic', xy=(14, 0.07), xytext=(17, 0.08),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
plt.annotate('Burglary peaks\nunder cover of darkness', xy=(3, 0.06), xytext=(5, 0.07),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

plt.tight_layout()
plt.savefig('docs/hourly_rhythm.svg', bbox_inches='tight')
print("Static chart saved to docs/hourly_rhythm.svg")
