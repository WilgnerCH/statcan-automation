import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import sys

# =============================
# 1. CALCULAR MÊS DISPONÍVEL
# =============================

today = datetime.today()
target_date = today - relativedelta(months=4)
target_ref = target_date.strftime("%Y-%m")

print("Target month:", target_ref)

# =============================
# 2. CONSULTAR API
# =============================

url = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods"

payload = {
    "vectorIds": [41690973],  # teste temporário
    "latestN": 12
}

response = requests.post(url, json=payload)

if response.status_code != 200:
    print("API request failed.")
    sys.exit(1)

data = response.json()

# Verificação de segurança
if "object" not in data:
    print("Unexpected API response:", data)
    sys.exit(1)

records = []

for item in data["object"]:
    if "vectorDataPoint" not in item:
        continue
        
    for entry in item["vectorDataPoint"]:
        if entry.get("refPer") == target_ref:
            records.append({
                "ref_date": entry["refPer"],
                "value": entry["value"]
            })

if not records:
    print("Data not yet available for:", target_ref)
    sys.exit(0)

df = pd.DataFrame(records)

filename = f"statcan_{target_ref}.csv"

if not os.path.exists(filename):
    df.to_csv(filename, index=False)
    print("Saved:", filename)
else:
    print("File already exists.")
