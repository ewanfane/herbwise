document.addEventListener("DOMContentLoaded", function () {
    // Get plant ID from the page
    const plantId = document.getElementById("plant-data").dataset.plantId;
    
    // Sensor configuration 
    const sensorConfig = {
        temperature: {
            label: "Temperature (°C)",
            color: "rgb(255, 99, 132)"
        },
        humidity: {
            label: "Humidity (%)",
            color: "rgb(54, 162, 235)"
        },
        soil_moisture: {
            label: "Soil Moisture",
            color: "rgb(75, 192, 192)"
        },
        light: {
            label: "Light Level (lux)",
            color: "rgb(255, 205, 86)"
        }
    };
    
    // Fetch data and initialize charts
    fetchSensorData();
    
    /**
     * Fetch all historical sensor data for the plant
     */
    function fetchSensorData() {
        fetch(`/plant_data/${plantId}/`)
            .then(response => response.json())
            .then(data => {
                // Convert string timestamps to Date objects
                const sensorData = data.items.map(item => ({
                    timestamp: new Date(item.timestamp),
                    temperature: item.temperature,
                    humidity: item.humidity,
                    soil_moisture: item.soil_moisture,
                    light: item.light
                }));
                
                // Sort by timestamp (oldest first)
                sensorData.sort((a, b) => a.timestamp - b.timestamp);
                
                // Initialize charts
                createCharts(sensorData);
            })
            .catch(error => {
                console.error("Error fetching sensor data:", error);
                alert("Failed to load sensor data. Please try again later.");
            });
    }
    
    /**
     * Create all charts with sensor data
     */
    function createCharts(sensorData) {
        // Create combined chart
        createCombinedChart(sensorData);
        
        // Create individual sensor charts
        Object.keys(sensorConfig).forEach(sensorType => {
            createSensorChart(sensorType, sensorData);
        });
    }
    
    /**
     * Create the combined chart with all sensor data
     */
    function createCombinedChart(sensorData) {
        const ctx = document.getElementById("combinedChart").getContext("2d");
        
        new Chart(ctx, {
            type: "line",
            data: {
                datasets: Object.keys(sensorConfig).map(sensorType => {
                    const config = sensorConfig[sensorType];
                    return {
                        label: config.label,
                        data: sensorData.map(item => ({
                            x: item.timestamp,
                            y: item[sensorType]
                        })),
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: 2,
                        pointHoverRadius: 5,
                        yAxisID: sensorType === 'light' ? 'y1' : 'y'
                    };
                })
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            boxWidth: 15,
                            usePointStyle: true,
                            pointStyle: 'circle',
                            color: 'white',
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(5, 5, 5, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        borderColor: 'rgba(255, 255, 255, 0.2)',
                        borderWidth: 1,
                        padding: 10,
                    }
                }, 
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'hour',
                            displayFormats: {
                                hour: 'HH:mm',
                                day: 'MMM d'
                            },
                            tooltipFormat: 'MMM d, yyyy HH:mm'
                        },
                        title: {
                            display: true,
                            text: "Time",
                            color: 'white',
                            font: { size: 12 }
                        },
                        ticks: {
                            color: 'white',
                            maxRotation: 45,
                            minRotation: 45
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.92)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Temperature, Humidity, Soil Moisture",
                            color: 'white',
                            font: { size: 12 }
                        },
                        ticks: { 
                            color: 'white',
                            callback: function(value) {
                                return value.toFixed(1);
                            }
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        position: 'left'
                    },
                    y1: {
                        title: {
                            display: true,
                            text: "Light Level (lux)",
                            color: sensorConfig.light.color,
                            font: { size: 12 }
                        },
                        ticks: { 
                            color: 'white',
                            callback: function(value) {
                                return value.toFixed(0);
                            }
                        },
                        grid: {
                            drawOnChartArea: false,
                            color: 'rgba(255, 205, 86, 0.2)'
                        },
                        position: 'right'
                    }
                }
            }
        });
    }
    
    /**
     * Create individual chart for a specific sensor
     */
    function createSensorChart(sensorType, sensorData) {
        const config = sensorConfig[sensorType];
        const ctx = document.getElementById(`${sensorType}Chart`).getContext("2d");
        
        // Create gradient for fill
        const gradient = ctx.createLinearGradient(0, 0, 0, 180);
        gradient.addColorStop(0, config.color.replace('rgb', 'rgba').replace(')', ', 0.5)'));
        gradient.addColorStop(1, config.color.replace('rgb', 'rgba').replace(')', ', 0.0)'));
        
        new Chart(ctx, {
            type: "line",
            data: {
                datasets: [{
                    label: config.label,
                    data: sensorData.map(item => ({
                        x: item.timestamp,
                        y: item[sensorType]
                    })),
                    borderColor: config.color,
                    backgroundColor: gradient,
                    borderWidth: 2,
                    tension: 0.3,
                    pointRadius: 1.5,
                    pointHoverRadius: 4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        borderColor: 'rgba(255, 255, 255, 0.2)',
                        borderWidth: 1,
                        padding: 10,
                        callbacks: {
                            title: function(tooltipItems) {
                                const date = new Date(tooltipItems[0].parsed.x);
                                return date.toLocaleString();
                            },
                            label: function(context) {
                                const unitSymbol = sensorType === 'temperature' ? ' °C' : 
                                                  sensorType === 'humidity' ? ' %' : 
                                                  sensorType === 'light' ? ' lux' : '';
                                                  
                                return `${config.label}: ${context.parsed.y.toFixed(1)}${unitSymbol}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'hour',
                            displayFormats: {
                                hour: 'HH:mm',
                                day: 'MMM d'
                            }
                        },
                        ticks: {
                            color: 'white',
                            maxRotation: 45,
                            minRotation: 45,
                            font: { size: 9 }
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        title: {
                            display: true,
                            text: "Time",
                            color: 'white',
                            font: { size: 10 }
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: config.label,
                            color: config.color,
                            font: { size: 10 }
                        },
                        ticks: { 
                            color: 'white', 
                            font: { size: 9 },
                            callback: function(value) {
                                return sensorType === 'light' ? value.toFixed(0) : value.toFixed(1);
                            }
                        },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        beginAtZero: sensorType !== 'temperature'
                    }
                }
            }
        });
    }
});