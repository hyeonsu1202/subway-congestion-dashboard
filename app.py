import glob
import json
import os
import pandas as pd
from DashboardManager import DashboardManager


def load_csv_or_md_data():
    rows = []

    for path in sorted(glob.glob("data/*호선.md")):
        try:
            df = pd.read_csv(path, encoding="utf-8-sig")
            rows.extend(df.to_dict(orient="records"))
        except Exception as e:
            print(f"파일 읽기 실패: {path}, {e}")

    return rows


def load_json_if_exists(path):
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "predictions" in data:
        return data["predictions"]

    return data if isinstance(data, list) else []


congestion_data = load_csv_or_md_data()
prediction_data = load_json_if_exists("data/prediction.json")

dashboard = DashboardManager(
    congestion_data,
    prediction_data
)

dashboard.display_dashboard()
