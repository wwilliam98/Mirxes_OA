import pandas as pd
import json

def risk_category_formula(risk_score):
    if risk_score > 0.8:
        return "High"
    elif 0.4 <= risk_score <= 0.8:
        return "Medium"
    else:
        return "Low"

df = pd.read_excel("patients.xlsx")
df["risk_category"] = df["risk_score"].apply(risk_category_formula)

results = {}
for index, row in df.iterrows():
    patient_id = row["patient_id"]
    results[patient_id] = {
        "risk_score": row["risk_score"],
        "risk_category": row["risk_category"]
    }

with open("output.json", "w") as f:
    json.dump(results, f, indent=4)
