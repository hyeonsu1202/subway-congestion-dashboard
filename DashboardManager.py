import pandas as pd
import streamlit as st


class DashboardManager:
    def __init__(self, congestion_data, prediction_data=None):
        self.congestion_data = congestion_data or []
        self.prediction_data = prediction_data or []
        self.dashboard_data = {}

    def get_lines(self):
        return sorted({row.get("LINE") for row in self.congestion_data if row.get("LINE")})

    def get_stations(self, line):
        return list(dict.fromkeys(
            row.get("DPTRE_STTN") for row in self.congestion_data
            if row.get("LINE") == line and row.get("DPTRE_STTN")
        ))

    def get_day_types(self, line, station):
        return list(dict.fromkeys(
            row.get("DOW_SE") for row in self.congestion_data
            if row.get("LINE") == line
            and row.get("DPTRE_STTN") == station
            and row.get("DOW_SE")
        ))

    def get_directions(self, line, station, day_type):
        return list(dict.fromkeys(
            row.get("UP_DOWN_SE") for row in self.congestion_data
            if row.get("LINE") == line
            and row.get("DPTRE_STTN") == station
            and row.get("DOW_SE") == day_type
            and row.get("UP_DOWN_SE")
        ))

    @staticmethod
    def _time_sort_key(key):
        hh, mm = int(key[4:6]), int(key[6:8])
        minutes = hh * 60 + mm
        if minutes < 5 * 60 + 30:
            minutes += 24 * 60
        return minutes

    @staticmethod
    def _time_label(key):
        return f"{key[4:6]}:{key[6:8]}"

    def _find_row(self, data, line, station, day_type, direction):
        for row in data:
            if (row.get("LINE") == line
                    and row.get("DPTRE_STTN") == station
                    and row.get("UP_DOWN_SE") == direction
                    and (row.get("DOW_SE") == day_type or "DOW_SE" not in row)):
                return row
        return None

    def _row_to_time_data(self, row):
        if not row:
            return []
        keys = sorted(
            [k for k in row if k.startswith("TIME") and len(k) == 8],
            key=self._time_sort_key,
        )
        result = []
        for key in keys:
            try:
                value = float(row[key])
            except (TypeError, ValueError):
                continue
            result.append({"time": self._time_label(key), "value": value})
        return result

    def get_congestion_by_time(self, line, station, day_type, direction):
        row = self._find_row(self.congestion_data, line, station, day_type, direction)
        return self._row_to_time_data(row)

    def get_prediction_by_time(self, line, station, day_type, direction):
        row = self._find_row(self.prediction_data, line, station, day_type, direction)
        return self._row_to_time_data(row)

    def make_dashboard_data(self, line, station, day_type, direction):
        self.dashboard_data = {
            "line": line,
            "station": station,
            "day_type": day_type,
            "direction": direction,
            "congestion": self.get_congestion_by_time(line, station, day_type, direction),
            "prediction": self.get_prediction_by_time(line, station, day_type, direction),
        }
        return self.dashboard_data

    def display_dashboard(self):
        st.set_page_config(page_title="Subway Congestion Dashboard", page_icon="🚇", layout="wide")
        st.title("🚇 Subway Congestion Dashboard")
        st.caption("호선 · 역 · 요일 · 방향을 선택해 시간대별 혼잡도를 확인하세요.")

        lines = self.get_lines()
        if not lines:
            st.error("혼잡도 데이터가 없습니다.")
            return

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            line = st.selectbox("호선", lines)
        with c2:
            station = st.selectbox("역", self.get_stations(line))
        with c3:
            day_type = st.selectbox("요일 유형", self.get_day_types(line, station))
        with c4:
            direction = st.selectbox("방향", self.get_directions(line, station, day_type))

        data = self.make_dashboard_data(line, station, day_type, direction)
        actual = pd.DataFrame(data["congestion"])
        predicted = pd.DataFrame(data["prediction"])

        st.subheader(f"{line} · {station} · {day_type} · {direction}")

        if actual.empty:
            st.warning("선택한 조건의 혼잡도 데이터가 없습니다.")
            return

        peak = actual.loc[actual["value"].idxmax()]
        m1, m2, m3 = st.columns(3)
        m1.metric("최고 혼잡도", f"{peak['value']:.1f}%")
        m2.metric("최고 혼잡 시간", peak["time"])
        m3.metric("평균 혼잡도", f"{actual['value'].mean():.1f}%")

        chart = actual.rename(columns={"value": "기존 혼잡도"}).set_index("time")[["기존 혼잡도"]]
        if not predicted.empty:
            pred = predicted.rename(columns={"value": "예측 혼잡도"}).set_index("time")[["예측 혼잡도"]]
            chart = chart.join(pred, how="outer")

        st.line_chart(chart, x_label="시간", y_label="혼잡도 (%)")

        with st.expander("선택 데이터 보기"):
            st.dataframe(chart, use_container_width=True)
