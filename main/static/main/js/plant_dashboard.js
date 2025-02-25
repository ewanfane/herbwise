document.addEventListener("DOMContentLoaded", function () {
    const sensorChart = document.getElementById("sensorChart").getContext("2d");

    // Extract data from Django template
    const timestamps = [];
    const temperatures = [];
    const humidities = [];
    const soilMoistures = [];
    const lightLevels = [];

    document.querySelectorAll("tbody tr").forEach(row => {
        timestamps.push(row.cells[0].innerText);
        temperatures.push(parseFloat(row.cells[1].innerText));
        humidities.push(parseFloat(row.cells[2].innerText));
        soilMoistures.push(parseFloat(row.cells[3].innerText));
        lightLevels.push(parseFloat(row.cells[4].innerText));
    });

    new Chart(sensorChart, {
        type: "line",
        data: {
            labels: timestamps.reverse(),
            datasets: [
                { label: "Temperature (°C)", data: temperatures.reverse(), borderColor: "red", fill: false },
                { label: "Humidity (%)", data: humidities.reverse(), borderColor: "blue", fill: false },
                { label: "Soil Moisture", data: soilMoistures.reverse(), borderColor: "green", fill: false },
                { label: "Light Level", data: lightLevels.reverse(), borderColor: "orange", fill: false }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { x: { title: { display: true, text: "Time" } }, y: { title: { display: true, text: "Value" } } }
        }
    });
});
