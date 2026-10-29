const stations = [
    { name: "서울역", x: 60, y: 280 },
    { name: "시청", x: 60, y: 220 },
    { name: "종각", x: 120, y: 160 },
    { name: "종로3가", x: 180, y: 100 },
    { name: "종로5가", x: 260, y: 100 },
    { name: "동대문", x: 340, y: 100 },
    { name: "동묘앞", x: 420, y: 100 },
    { name: "신설동", x: 500, y: 100 },
    { name: "제기동", x: 580, y: 100 },
    { name: "청량리", x: 660, y: 100 }
];

function drawLine1() {
    const stationMap = document.querySelector(".station-map");

    stationMap.innerHTML = "";

    // SVG 생성
    const svg = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "svg"
    );

    svg.setAttribute("viewBox", "0 0 730 350");
    svg.classList.add("subway-svg");

    // 노선 연결선 생성
    const path = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "path"
    );

    const pathData = stations.map((station, index) => {
        return `${index === 0 ? "M" : "L"} ${station.x} ${station.y}`;
    }).join(" ");

    path.setAttribute("d", pathData);
    path.classList.add("subway-path");

    svg.appendChild(path);

    // 역 생성
    stations.forEach(station => {

        const circle = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "circle"
        );

        circle.setAttribute("cx", station.x);
        circle.setAttribute("cy", station.y);
        circle.setAttribute("r", 9);
        circle.setAttribute("data-station", station.name);
        circle.classList.add("station-dot");

        // 역 클릭 기능
        circle.addEventListener("click", function() {

            svg.querySelectorAll(".station-dot").forEach(dot => {
                dot.classList.remove("selected");
            });

            this.classList.add("selected");

            // 선택한 역의 모달 열기
            openModal(station.name);
        });

        svg.appendChild(circle);

        // 역 이름 생성
        const label = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "text"
        );

        if (["시청", "종각", "종로3가"].includes(station.name)) {
          label.setAttribute("x", station.x - 18);
          label.setAttribute("y", station.y - 20);
          label.setAttribute("text-anchor", "end");
        } else {
          label.setAttribute("x", station.x);
          label.setAttribute("y", station.y + 28);
        }
        label.classList.add("station-label");
        label.textContent = station.name;

        svg.appendChild(label);
    });

    stationMap.appendChild(svg);
}

// 모달 열기
function openModal(stationName) {

    const modal = document.querySelector(".modal-overlay");

    // 현재 선택된 호선
    const selectedLine = document.querySelector(".line-btn.active");

    // 현재 선택된 방향
    const selectedDirection = document.querySelector(
        "#direction-selector .toggle-btn.active"
    );

    // 현재 선택된 요일
    const selectedDay = document.querySelector(
        "#day-selector .toggle-btn.active"
    );

    // 현재 선택된 시간
    const selectedTime = document.querySelector("#currentTime");

    // 호선 및 역 이름 표시
    document.querySelector(".modal-line").textContent =
        selectedLine.dataset.line;

    document.querySelector(".modal-station").textContent =
        stationName;

    // 방향 · 요일 · 시간 표시
    document.querySelector(".modal-info").textContent =
        `${selectedDirection.dataset.direction} · ${selectedDay.dataset.daytype} · ${selectedTime.textContent.trim() || "4:30"}`;

    // 모달 표시
    modal.classList.add("active");
}


// 모달 닫기 버튼
document.querySelector(".modal-close").addEventListener("click", function() {

    document.querySelector(".modal-overlay").classList.remove("active");

});


// 모달 바깥 영역 클릭 시 닫기
document.querySelector(".modal-overlay").addEventListener("click", function(event) {

    if (event.target === this) {

        this.classList.remove("active");

    }

});


// ESC 키로 모달 닫기
document.addEventListener("keydown", function(event) {

    if (event.key === "Escape") {

        document.querySelector(".modal-overlay").classList.remove("active");

    }

});
// 처음 화면에 1호선 표시
drawLine1();
