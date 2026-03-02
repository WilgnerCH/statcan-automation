import requests
import pandas as pd
import os
import sys

# =============================
# 1. CONSULTAR API
# =============================

url = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods"

payload = [
    {
        "vectorId": 41690973,
        "latestN": 1
    }
]

response = requests.post(url, json=payload)

if response.status_code != 200:
    print("API request failed.")
    sys.exit(1)

data = response.json()

if not isinstance(data, list) or "object" not in data[0]:
    print("Unexpected API response:", data)
    sys.exit(1)

data_object = data[0]["object"]

if not data_object["vectorDataPoint"]:
    print("No data returned from API.")
    sys.exit(0)

entry = data_object["vectorDataPoint"][0]

ref_date = entry["refPer"]
value = entry["value"]

print("Latest available month:", ref_date)

# =============================
# 2. SALVAR CSV
# =============================

os.makedirs("data", exist_ok=True)

filename = f"data/statcan_{ref_date}.csv"

if not os.path.exists(filename):
    df = pd.DataFrame([{
        "ref_date": ref_date,
        "value": value
    }])

    df.to_csv(filename, index=False)
    print("Saved:", filename)
else:
    print("File already exists.")
