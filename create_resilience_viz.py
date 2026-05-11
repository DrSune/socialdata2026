import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Mocking the data logic for the "Two Denmarks" visualization
# We will use the 800k housing data to categorize by region/city and estimate costs

def generate_resilience_mockup():
    # 1. Load a subset of our actual housing data
    try:
        df = pd.read_parquet('test_raw.parquet')
        df = df[df['date'] >= '2022-01-01'] # Focus on the crisis era
    except:
        print("Data not found, using simulation for mockup")
        return

    # 2. Categorize Urban vs Rural (Simplified)
    cities = ['København', 'Aarhus', 'Odense', 'Aalborg']
    df['Setting'] = df['city'].apply(lambda x: 'Urban (Collective)' if any(c in str(x) for c in cities) else 'Rural (Individual)')
    
    # 3. Estimate "Crisis Energy Cost" 
    # Logic: Rural houses are larger and have worse energy labels (BBR reality)
    # We'll use purchase_price and sqm as proxies for "House Quality"
    # and randomize the 'Heating Source' based on Setting
    
    # Simulation of "Crisis Cost" for the mockup
    # In the real script, we would use BBR heating_type codes.
    def estimate_cost(row):
        base = 15000 # Base district heating cost
        if row['Setting'] == 'Rural (Individual)':
            # Rural has higher variance due to Gas/Oil exposure
            return base + np.random.normal(15000, 8000) 
        else:
            # Urban is shielded by collective district heating
            return base + np.random.normal(2000, 1000)

    df['Estimated_Annual_Energy_Cost'] = df.apply(estimate_cost, axis=1)

    # 4. Plotting the "Hard" Visualization
    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")
    
    # Using a KDE plot (Density) with high transparency to show the distribution
    sns.kdeplot(data=df, x='Estimated_Annual_Energy_Cost', hue='Setting', 
                fill=True, common_norm=False, palette='viridis', alpha=.5, linewidth=2)

    plt.title('The Inequality of the Energy Crisis (2022-2023)', fontsize=16, pad=20)
    plt.xlabel('Estimated Annual Heating Cost (DKK)', fontsize=12)
    plt.ylabel('Density of Households', fontsize=12)
    plt.xlim(0, 60000)
    
    # Adding Annotations to tell the story
    plt.annotate('Urban Resilience:\nShielded by District Heating', xy=(17000, 0.00025), xytext=(5000, 0.0003),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1))
    
    plt.annotate('Rural Vulnerability:\nExposed to Gas/Oil Spikes', xy=(30000, 0.00005), xytext=(40000, 0.00015),
                 arrowprops=dict(facecolor='red', shrink=0.05, width=1))

    plt.tight_layout()
    plt.savefig('docs/urban_rural_resilience.png', dpi=300)
    print("Mockup saved to docs/urban_rural_resilience.png")

if __name__ == "__main__":
    generate_resilience_mockup()
