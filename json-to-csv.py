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