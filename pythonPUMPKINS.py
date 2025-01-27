import pandas as pd
file_path = "pumpkins_12.csv" 
pumpkins = pd.read_csv(file_path)
print(pumpkins.info())
print(pumpkins.head())

#Find information of heaviest pumpkin
heaviest_pumpkin = pumpkins.loc[pumpkins['weight_lbs'].idxmax()]
print("Heaviest pumpkin information:")
print(heaviest_pumpkin[['weight_lbs', 'variety', 'city', 'state_prov', 'country', 'id']])

# Convert weight from pounds to kilograms
pumpkins['weight_kg'] = pumpkins['weight_lbs'] * 0.453592

def classify_weight(weight_kg):
    if weight_kg < 500:
        return "Light"  
    elif 500 <= weight_kg < 1000:
        return "Medium"  
    else:
        return "Heavy" 

pumpkins['weight_class'] = pumpkins['weight_kg'].apply(classify_weight)
print(pumpkins[['id', 'weight_kg', 'weight_class']].head())


# Plot the weight relationship photo
!pip install matplotlib
!pip install seaborn
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pumpkins, x='weight_kg', y='est_weight', hue='weight_class', palette='viridis', alpha=0.9)
plt.title('Relationship Between Estimated and Actual Weight', fontsize=15)
plt.xlabel('Actual Weight (kg) ', fontsize=12)
plt.ylabel('Estimated Weight (lbs) ', fontsize=12)
plt.legend(title='Weight Class ')
plt.grid(True)
plt.tight_layout()
plt.savefig("actual_vs_estimated_weight.png") 
plt.show()


# filter data
filtered_countries = ['USA', 'Mexico', 'France']  
filtered_pumpkins = pumpkins[pumpkins['country'].isin(filtered_countries)]
filtered_pumpkins.to_csv("pumpkins_filtered.csv", index=False)

# Calculate average weight by country
avg_weight_by_country = filtered_pumpkins.groupby('country')['weight_kg'].mean().sort_values(ascending=False)
print("Average weight by country:")
print(avg_weight_by_country)

# Calculate average weight by country and variety
avg_weight_by_variety = (
    filtered_pumpkins.groupby(['country', 'variety'])['weight_kg']
    .mean()
    .reset_index()
    .sort_values(by=['country', 'weight_kg'])
)
lowest_avg_variety_by_country = avg_weight_by_variety.groupby('country').first()
print("Lowest average weight variety by country:")
print(lowest_avg_variety_by_country)


#Plot the boxplot for weight distribution by country
plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_pumpkins, x='country', y='weight_kg', palette='viridis')
plt.title('Weight Distribution by Country ', fontsize=15)
plt.xlabel('Country ', fontsize=12)
plt.ylabel('Weight (kg) ', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.9)
plt.tight_layout()
plt.savefig("weight_distribution_by_country.png") 
plt.show()

#Plot the facet grid boxplot by variety and country)
g = sns.catplot(
    data=filtered_pumpkins,
    x='country',
    y='weight_kg',
    col='variety',
    kind='box',
    palette='viridis',
    col_wrap=3,
    height=4
)
g.fig.subplots_adjust(top=0.7)
g.fig.suptitle('Weight Distribution by Variety and Country', fontsize=15)
g.savefig("weight_distribution_by_variety.png") 
