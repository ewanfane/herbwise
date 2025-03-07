document.addEventListener("DOMContentLoaded", function () {
    console.log("Fetching sensor data for all plants...");

    const plantContainer = document.getElementById("plant-container");

    plantContainer.addEventListener("click", function (event) {
        const settingsIcon = event.target.closest(".plant-settings");
        if (settingsIcon) {
            const plantCard = settingsIcon.closest(".plant-card");
            const plantId = plantCard.dataset.plantId;
            const menu = plantCard.querySelector(".plant-menu");

            // Hide all other open menus before showing the new one
            document.querySelectorAll(".plant-menu.show").forEach(m => {
                if (m !== menu) m.classList.remove("show");
            });

            // Toggle menu visibility
            menu.classList.toggle("show");

            if (menu.classList.contains("show")) {
                const renameOption = menu.querySelector(".rename-option");
                const deleteOption = menu.querySelector(".delete-option");

                renameOption.onclick = () => renamePlant(plantId, plantCard);
                deleteOption.onclick = () => deletePlant(plantId, plantCard);
            }
        } else {
            // Clicked outside a settings icon -> close open menus
            document.querySelectorAll(".plant-menu.show").forEach(menu => menu.classList.remove("show"));
        }
    });

    



        document.querySelectorAll(".sensor-data-container").forEach(container => {

        const plantId = container.dataset.plantId;

        if (plantId) {  // Simpler check

            console.log(`Fetching data for plant ${plantId}`);

            fetchLatestRecord(plantId, container);

        }

    });

    // Close menu if clicking anywhere outside a menu or plant-card
    document.addEventListener("click", function (event) {
        if (!event.target.closest(".plant-card") && !event.target.closest(".plant-menu")) {
            document.querySelectorAll(".plant-menu.show").forEach(menu => menu.classList.remove("show"));
        }
    });

    function renamePlant(plantId, plantCard) {
        const newName = prompt("Enter the new name of your plant:");
        if (newName) {
            fetch(`/rename_plant/${plantId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({ new_name: newName }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Ensure we update the correct text element
                        const nameElement = plantCard.querySelector(".plant-name");
                        if (nameElement) {
                            nameElement.textContent = newName;
                        } else {
                            console.error("Plant name element not found inside the card.");
                        }
                    } else {
                        alert("Error renaming plant: " + (data.error || "Unknown error"));
                    }
                })
                .catch(error => console.error("Error:", error))
                .finally(() => {
                    plantCard.querySelector(".plant-menu").classList.remove("show"); // Hide menu after action
                });
        }
    }

    function deletePlant(plantId, plantCard) {
        if (confirm("Are you sure you want to delete this plant?")) {
            fetch(`/delete_plant/${plantId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        plantCard.remove();
                    } else {
                        alert("Error deleting plant: " + (data.error || "Unknown error"));
                    }
                })
                .catch(error => console.error("Error:", error));
        }
    }

    function fetchLatestRecord(plantId, container) {

                fetch(`/latest_record/${plantId}/`)
        
                    .then(response => response.json())
        
                    .then(data => {
        
                        console.log(`Data for plant ID ${plantId}:`, data);
        
                        if (!data.error) {
        
                            // No need to check for container; it's always passed now
        
                            container.querySelector(".temperature").innerText = `🌡️ ${data.temperature} °C`;
        
                            container.querySelector(".humidity").innerText = `💧 ${data.humidity} %`;
        
                            container.querySelector(".soilMoisture").innerText = `🌱 ${data.soil_moisture}`;
        
                            container.querySelector(".light").innerText = `☀️ ${data.light}`;
        
                        } else {
        
                            container.querySelector(".temperature").innerText = "-";
        
                            container.querySelector(".humidity").innerText = "-";
        
                            container.querySelector(".soilMoisture").innerText = "-";
        
                            container.querySelector(".light").innerText = "-";
        
                        }
        
                    })
        
                    .catch(error => console.error("Error fetching data:", error));
        
            }
        
        
        
            // Call function every 5 seconds (for real-time updates)
        
            setInterval(() => {
        
                document.querySelectorAll(".sensor-data-container").forEach(container => {
        
                    const plantId = container.dataset.plantId;
        
                    if (plantId) {
        
                        fetchLatestRecord(plantId, container);
        
                    }
        
                });
        
            }, 5000);
        
        
        
            // Helper function to get CSRF token (Django's built-in protection)
        
            function getCookie(name) {
        
                let cookieValue = null;
        
                if (document.cookie && document.cookie !== '') {
        
                    const cookies = document.cookie.split(';');
        
                    for (let i = 0; i < cookies.length; i++) {
        
                        const cookie = cookies[i].trim();
        
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
        
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        
                            break;
        
                        }
        
                    }
        
                }
        
                return cookieValue;
        
            }
});
