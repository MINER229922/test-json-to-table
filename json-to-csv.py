import pandas as pd

# Sample JSON data
json_data = {
    "a": {
        "a": 1,
        "b": 1
    },
    "b": {
        "a": 1,
        "b": 1,
        "c": 1
    },
    "c": [
        1,
        1,
        1
    ]
}

# Normalize the JSON data
df = pd.json_normalize(json_data)

# Handling the list in 'c' and adjusting column names
if 'c' in df.columns:
    c_values = df.at[0, 'c']
    for idx, val in enumerate(c_values):
        df[f'c.{idx}'] = val
    df = df.drop(columns='c')

# Rename columns to match desired headers
df.columns = [col.replace('.', '.') for col in df.columns]

# Save to CSV
df.to_csv('output.csv', index=False)

print("CSV file has been created with headers:")
print(df.columns.tolist())



import json
from flatten_json import flatten
import pandas as pd

# Sample JSON data
json_data = {
    "a": {
        "a": 1,
        "b": 1
    },
    "b": {
        "a": 1,
        "b": 1,
        "c": 1
    },
    "c": [
        1,
        1,
        1
    ]
}

# Flatten the JSON data
flattened_data = flatten(json_data)

# Adjust keys to match desired headers (replace list indices brackets)
flattened_data_adjusted = {k.replace('[', '.').replace(']', ''): v for k, v in flattened_data.items()}

# Convert to DataFrame
df = pd.DataFrame([flattened_data_adjusted])

# Save to CSV
df.to_csv('output.csv', index=False)

print("CSV file has been created with headers:")
print(df.columns.tolist())