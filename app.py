import glob
import json
import os
import pandas as pd
from DashboardManager import DashboardManager


def load_csv_or_md_data():
    rows = []
    for path in sorted(glob.glob("data/*호선.md")):
        # 현재 제공된 호선 파일은 실제 내용이 CSV 형식이므로 read_csv로 읽습니다.
        try:
            df = pd.read_csv(path, encoding="utf-8-sig")
            rows.extend(df.to_dict(orient="records"))
        except Exception:
            pass
    return rows


def load_json_if_exists(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # prediction JSON이 {"predictions": [...]} 구조여도 처리
    if isinstance(data, dict) and "predictions" in data:
        return data["predictions"]
    return data if isinstance(data, list) else []


congestion_data = load_csv_or_md_data()
prediction_data = load_json_if_exists("data/prediction.json")

DashboardManager(congestion_data, prediction_data).display_dashboard()
