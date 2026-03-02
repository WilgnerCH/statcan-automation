import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

# =====================================
# CONFIGURAÇÃO
# =====================================

API_URL = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromVectorsAndLatestNPeriods"

VECTOR_START = 87008752
VECTOR_END = 87009012

LATEST_N = 12   # Buscar últimos 12 meses para segurança
DATA_PATH = "data/trade_data.csv"

# =====================================
# DEFINIR MÊS ALVO (4 MESES ATRÁS)
# =====================================

today = datetime.today()
target_date = today - relativedelta(months=4)
target_ref = target_date.strftime("%Y-%m")

print("Target month:", target_ref)

# =====================================
# GERAR LISTA COMPLETA DE VETORES
# =====================================

all_vectors = list(range(VECTOR_START, VECTOR_END + 1))

payload = [
    {
        "vectorId": v,
        "latestN": LATEST_N
    }
    for v in all_vectors
]

# =====================================
# CHAMADA API
# =====================================

response = requests.post(API_URL, json=payload)

if response.status_code != 200:
    raise Exception("API request failed")

data = response.json()

records = []

for item in data:
    obj = item.get("object", {})
    vector_id = obj.get("vectorId")

    for dp in obj.get("vectorDataPoint", []):
        if dp.get("refPer", "")[:7] == target_ref:
            records.append({
                "date": dp["refPer"][:7],
                "vectorId": vector_id,
                "value": dp["value"]
            })

if not records:
    print("No new data available.")
    exit(0)

df_new = pd.DataFrame(records)

# =====================================
# ATUALIZAR DATASET HISTÓRICO
# =====================================

os.makedirs("data", exist_ok=True)

if os.path.exists(DATA_PATH):
    df_existing = pd.read_csv(DATA_PATH)
    df_combined = pd.concat([df_existing, df_new])
    df_combined.drop_duplicates(
        subset=["date", "vectorId"],
        inplace=True
    )
else:
    df_combined = df_new

df_combined.to_csv(DATA_PATH, index=False)

print("Dataset updated successfully.")
