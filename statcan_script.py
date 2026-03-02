import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

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
    "vectorIds": [41690973],
    "latestN": 12
}

response = requests.post(url, json=payload)
data = response.json()

records = []

for item in data['object']:
    vector_data = item['vectorDataPoint']
    for entry in vector_data:
        if entry['refPer'] == target_ref:
            records.append({
                "ref_date": entry['refPer'],
                "value": entry['value']
            })

if not records:
    print("Data not yet available.")
    exit()

df = pd.DataFrame(records)

# =============================
# 3. SALVAR SEM DUPLICAR
# =============================

filename = f"statcan_trade_{target_ref}.csv"

if not os.path.exists(filename):
    df.to_csv(filename, index=False)
    print("Saved:", filename)
else:
    print("File already exists.")
