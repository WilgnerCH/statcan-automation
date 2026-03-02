import requests
import pandas as pd
from datetime import datetime

url = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods"

payload = {
    "vectorIds": [41690973],  # você pode mudar depois
    "latestN": 1
}

response = requests.post(url, json=payload)
data = response.json()

records = []

for item in data['object']:
    vector_data = item['vectorDataPoint']
    for entry in vector_data:
        records.append({
            "ref_date": entry['refPer'],
            "value": entry['value']
        })

df = pd.DataFrame(records)

month_tag = datetime.today().strftime("%Y_%m")
filename = f"statcan_{month_tag}.csv"

df.to_csv(filename, index=False)

print("Arquivo criado:", filename)
