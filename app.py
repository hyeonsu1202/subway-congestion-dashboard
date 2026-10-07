import glob
import pandas as pd
from DashboardManager import DashboardManager


def load_markdown_table(path):
    """
    .md 파일 안의 Markdown 표를 읽어서
    list[dict] 형태로 변환합니다.
    """

    with open(path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    table_lines = []

    # DOW_SE로 시작하는 표 찾기
    table_started = False

    for line in lines:
        line = line.strip()

        # 표의 헤더 시작
        if "DOW_SE" in line and "LINE" in line and "DPTRE_STTN" in line:
            table_started = True

        if table_started:
            # Markdown 표의 | 가 있는 줄만 저장
            if "|" in line:
                table_lines.append(line)
            elif table_lines:
                break

    if len(table_lines) < 3:
        return []

    # 첫 번째 줄 = 컬럼 이름
    headers = [
        value.strip()
        for value in table_lines[0].strip("|").split("|")
    ]

    rows = []

    # table_lines[1]은
    # | --- | --- | --- |
    # 같은 구분선이므로 건너뜀
    for line in table_lines[2:]:

        values = [
            value.strip()
            for value in line.strip("|").split("|")
        ]

        if len(values) != len(headers):
            continue

        row = dict(zip(headers, values))

        # TIME 데이터 숫자로 변환
        for key in row:

            if key.startswith("TIME"):
                try:
                    row[key] = float(row[key])
                except ValueError:
                    pass

        rows.append(row)

    return rows


def load_congestion_data():

    all_rows = []

    files = sorted(glob.glob("data/*호선.md"))

    for path in files:

        try:
            rows = load_markdown_table(path)

            all_rows.extend(rows)

        except Exception as e:
            print(f"{path} 읽기 실패:", e)

    return all_rows


# 기존 혼잡도 데이터 불러오기
congestion_data = load_congestion_data()


# Dashboard 실행
dashboard = DashboardManager(congestion_data)

dashboard.display_dashboard()
