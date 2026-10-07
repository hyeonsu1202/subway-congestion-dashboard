import pandas as pd
import streamlit as st


class DashboardManager:
    def __init__(self, congestion_data):
        self.congestion_data = congestion_data or []
        self.dashboard_data = {}

    # 존재하는 호선 가져오기
    def get_lines(self):
        return sorted({
            row.get("LINE")
            for row in self.congestion_data
            if row.get("LINE")
        })

    # 선택한 호선에 존재하는 역 가져오기
    def get_stations(self, line):
        return list(dict.fromkeys(
            row.get("DPTRE_STTN")
            for row in self.congestion_data
            if row.get("LINE") == line
            and row.get("DPTRE_STTN")
        ))

    # 선택한 역에서 사용할 수 있는 요일 종류 가져오기
    def get_day_types(self, line, station):
        return list(dict.fromkeys(
            row.get("DOW_SE")
            for row in self.congestion_data
            if row.get("LINE") == line
            and row.get("DPTRE_STTN") == station
            and row.get("DOW_SE")
        ))

    # 선택한 역의 방향 가져오기
    def get_directions(self, line, station, day_type):
        return list(dict.fromkeys(
            row.get("UP_DOWN_SE")
            for row in self.congestion_data
            if row.get("LINE") == line
            and row.get("DPTRE_STTN") == station
            and row.get("DOW_SE") == day_type
            and row.get("UP_DOWN_SE")
        ))

    # TIME0530 같은 값을 시간순으로 정렬하기 위한 함수
    @staticmethod
    def _time_sort_key(key):
        hh = int(key[4:6])
        mm = int(key[6:8])

        minutes = hh * 60 + mm

        # 00:00, 00:30은 하루의 마지막으로 보내기
        if minutes < 5 * 60 + 30:
            minutes += 24 * 60

        return minutes

    # TIME0530 -> 05:30
    @staticmethod
    def _time_label(key):
        return f"{key[4:6]}:{key[6:8]}"

    # 선택 조건과 일치하는 행 찾기
    def _find_row(self, line, station, day_type, direction):
        for row in self.congestion_data:

            if (
                row.get("LINE") == line
                and row.get("DPTRE_STTN") == station
                and row.get("DOW_SE") == day_type
                and row.get("UP_DOWN_SE") == direction
            ):
                return row

        return None

    # 한 행의 TIME 데이터를 그래프용 형태로 변환
    def _row_to_time_data(self, row):

        if not row:
            return []

        time_keys = [
            key
            for key in row
            if key.startswith("TIME") and len(key) == 8
        ]

        time_keys = sorted(
            time_keys,
            key=self._time_sort_key
        )

        result = []

        for key in time_keys:

            try:
                value = float(row[key])

            except (TypeError, ValueError):
                continue

            result.append({
                "time": self._time_label(key),
                "value": value
            })

        return result

    # 선택된 조건의 혼잡도 가져오기
    def get_congestion_by_time(
        self,
        line,
        station,
        day_type,
        direction
    ):

        row = self._find_row(
            line,
            station,
            day_type,
            direction
        )

        return self._row_to_time_data(row)

    # 대시보드에서 사용할 데이터 생성
    def make_dashboard_data(
        self,
        line,
        station,
        day_type,
        direction
    ):

        self.dashboard_data = {

            "line": line,
            "station": station,
            "day_type": day_type,
            "direction": direction,

            "congestion":
                self.get_congestion_by_time(
                    line,
                    station,
                    day_type,
                    direction
                )
        }

        return self.dashboard_data

    # 실제 웹 대시보드
    def display_dashboard(self):

        st.set_page_config(
            page_title="Subway Congestion Dashboard",
            page_icon="🚇",
            layout="wide"
        )

        st.title("🚇 Subway Congestion Dashboard")

        st.caption(
            "호선 · 역 · 요일 · 방향을 선택해 "
            "시간대별 혼잡도를 확인하세요."
        )

        # 호선 선택
        lines = self.get_lines()

        if not lines:
            st.error("혼잡도 데이터가 없습니다.")
            return

        # 선택 메뉴
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            line = st.selectbox(
                "호선",
                lines
            )

        with c2:
            stations = self.get_stations(line)

            station = st.selectbox(
                "역",
                stations
            )

        with c3:
            day_types = self.get_day_types(
                line,
                station
            )

            day_type = st.selectbox(
                "요일 유형",
                day_types
            )

        with c4:
            directions = self.get_directions(
                line,
                station,
                day_type
            )

            direction = st.selectbox(
                "방향",
                directions
            )

        # 선택 데이터 가져오기
        data = self.make_dashboard_data(
            line,
            station,
            day_type,
            direction
        )

        congestion = pd.DataFrame(
            data["congestion"]
        )

        st.subheader(
            f"{line} · {station} · "
            f"{day_type} · {direction}"
        )

        if congestion.empty:
            st.warning(
                "선택한 조건의 혼잡도 데이터가 없습니다."
            )
            return

        # 최고 혼잡도
        peak = congestion.loc[
            congestion["value"].idxmax()
        ]

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "최고 혼잡도",
            f"{peak['value']:.1f}%"
        )

        m2.metric(
            "최고 혼잡 시간",
            peak["time"]
        )

        m3.metric(
            "평균 혼잡도",
            f"{congestion['value'].mean():.1f}%"
        )

        # 그래프
        chart = (
            congestion
            .rename(
                columns={"value": "혼잡도"}
            )
            .set_index("time")
        )

        st.line_chart(
            chart,
            x_label="시간",
            y_label="혼잡도 (%)"
        )

        # 실제 데이터 표
        with st.expander(
            "선택 데이터 보기"
        ):
            st.dataframe(
                chart,
                use_container_width=True
            )
