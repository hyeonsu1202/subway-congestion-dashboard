import glob
import pandas as pd
from DashboardManager import DashboardManager


def load_congestion_data():
    rows = []

    for path in sorted(glob.glob("data/*호선.md")):
        try:
            df = pd.read_csv(path, encoding="utf-8-sig")
            rows.extend(df.to_dict(orient="records"))

        except Exception as e:
            print(f"파일 읽기 실패: {path}")
            print(e)

    return rows


congestion_data = load_congestion_data()

dashboard = DashboardManager(congestion_data)
dashboard.display_dashboard()
