import pandas as pd
import os

# path to raw dataset
data_path = "../data/smart_grid_stability_augmented.csv"

df = pd.read_csv(data_path)

print("Loaded dataset:", df.shape)

# keep only numeric columns
df = df.select_dtypes(include=["number"])

print("Numeric columns:", df.columns)

# remove missing values
df = df.dropna()

# save processed dataset
output_path = "../data/stability_processed.csv"

df.to_csv(output_path, index=False)

print("Saved processed dataset to:", output_path)