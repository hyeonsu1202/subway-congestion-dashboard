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

            console.log("선택한 역:", station.name);
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

// 처음 화면에 1호선 표시
drawLine1();
