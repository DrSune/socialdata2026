import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Load data
df_hist = pd.read_csv('solutions/hist.csv')
df_recent = pd.read_csv('solutions/recent.csv')

# Standardize categories
df_hist['Category'] = df_hist['Category'].str.upper().str.replace('/', ' ')
df_recent['Category'] = df_recent['Incident Category'].str.upper().str.replace('/', ' ')

crime_map = {
    'DRUG NARCOTIC': 'DRUG OFFENSE', 
    'MOTOR VEHICLE THEFT': 'VEHICLE THEFT', 
    'LARCENY/THEFT': 'LARCENY THEFT'
}
df_hist['Category'] = df_hist['Category'].replace(crime_map)
df_recent['Category'] = df_recent['Category'].replace(crime_map)

h = df_hist[['Category', 'PdDistrict', 'Date', 'Time', 'X', 'Y']].copy()
r = df_recent[['Category', 'Police District', 'Incident Date', 'Incident Time', 'Longitude', 'Latitude']].copy()
r.columns = h.columns
df = pd.concat([h, r], ignore_index=True)
df = df.dropna(subset=['X', 'Y', 'Date', 'Time'])
df = df[(df['X'] < -122.3) & (df['X'] > -122.6) & (df['Y'] < 37.9) & (df['Y'] > 37.6)]
df['Date'] = pd.to_datetime(df['Date'], format='mixed')
df['Time_dt'] = pd.to_datetime(df['Time'], format='mixed')
df['Hour'] = df['Time_dt'].dt.hour
df['Minute'] = df['Time_dt'].dt.minute
df['Year'] = df['Date'].dt.year

focus_crimes = ['LARCENY THEFT', 'BURGLARY', 'DRUG OFFENSE', 'VEHICLE THEFT', 'ROBBERY', 'VANDALISM', 'ASSAULT', 'PROSTITUTION']
df_focus = df[df['Category'].isin(focus_crimes)].copy()

# 1. Yearly
yearly = df_focus.groupby(['Year', 'Category']).size().unstack()
print("### 1. Yearly Trend Analysis ###")
print(yearly.to_string())
print("\n")

# 2. District Ratios
p_crime = df_focus['Category'].value_counts(normalize=True)
p_crime_district = df_focus.groupby('PdDistrict')['Category'].value_counts(normalize=True).unstack()
ratios = p_crime_district.div(p_crime, axis=1)
print("### 2. District Ratios ###")
print(ratios.to_string())
print("\n")

# 3. Jitter
jitter_data = df[(df['Category'] == 'LARCENY THEFT') & (df['Year'] == 2024) & (df['Hour'] == 13)]
print("### 3. Jitter Precision ###")
print(f"Sample X values: {jitter_data['X'].head(10).tolist()}")
print(f"Number of unique coordinates: {len(jitter_data.groupby(['X', 'Y']))} / {len(jitter_data)}")
print("\n")

# 4. QQ
lat1 = df[df['Category'] == 'LARCENY THEFT']['Y']
lat2 = df[df['Category'] == 'DRUG OFFENSE']['Y']
print("### 4. Latitude Distribution (QQ-like) ###")
print(f"LARCENY THEFT Latitude stats:\n{lat1.describe()}")
print(f"DRUG OFFENSE Latitude stats:\n{lat2.describe()}")
print("\n")

# 5. Time of day
hourly_dist = df_focus.groupby(['Hour', 'Category']).size().unstack()
print("### 5. Hourly Distribution ###")
print(hourly_dist.to_string())
print("\n")

# 6. Power Law
most_common = df_focus['Category'].value_counts().idxmax()
crime_data = df_focus[df_focus['Category'] == most_common]
x_bins = np.arange(-122.52, -122.35, 0.001)
y_bins = np.arange(37.70, 37.82, 0.001)
H, _, _ = np.histogram2d(crime_data['X'], crime_data['Y'], bins=(x_bins, y_bins))
counts = H.flatten()
k_vals, N_k = np.unique(counts, return_counts=True)
print("### 6. Power Law Spatial ###")
print(f"Most common crime: {most_common}")
print(f"k_vals (unique counts per cell): {k_vals[:10]}...")
print(f"N_k (frequency of these counts): {N_k[:10]}...")
print("\n")

# 7. Correlation
df_focus['DayOfWeek'] = df_focus['Date'].dt.dayofweek
df_focus['HourOfWeek'] = df_focus['DayOfWeek'] * 24 + df_focus['Hour']
selected_crimes = ['LARCENY THEFT', 'BURGLARY', 'DRUG OFFENSE', 'ASSAULT']
vectors = {c: df_focus[df_focus['Category'] == c].groupby('HourOfWeek').size().reindex(range(168), fill_value=0).values for c in selected_crimes}
corrs = pd.DataFrame({c: vectors[c] for c in selected_crimes}).corr()
print("### 7. Correlation Matrix ###")
print(corrs)
