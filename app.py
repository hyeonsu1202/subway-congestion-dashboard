import glob
import json
import os
import pandas as pd
from DashboardManager import DashboardManager


def load_csv_or_md_data():
    rows = []

    files = sorted(glob.glob("data/*호선.md"))

    print("찾은 파일:", files)

    for path in files:
        try:
            df = pd.read_csv(path, encoding="utf-8-sig")

            print(f"{path} 읽기 성공")
            print("컬럼:", df.columns.tolist())

            rows.extend(df.to_dict(orient="records"))

        except Exception as e:
            print(f"{path} 읽기 실패")
            print("에러:", e)

    print("총 데이터 개수:", len(rows))

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
