document.addEventListener("DOMContentLoaded", function() {
    console.log("Fetching sensor data for all plants...");

    const containers = document.querySelectorAll(".sensor-data-container");

    containers.forEach(container => {
        const plantId = container.dataset.plantId;
        if (plantId) {  // Simpler check
            console.log(`Fetching data for plant ${plantId}`);
            fetchLatestRecord(plantId, container);
        }
    });

    // Get the garden name (Consider setting this directly in the template from the view)
    const urlParams = new URLSearchParams(window.location.search);
    const gardenName = urlParams.get('gardenName');
    document.getElementById('garden-name').textContent = gardenName || "Garden Name Not Found";

    // Event listener for plant settings and actions
    document.getElementById("plant-container").addEventListener("click", function(event) {
        const settingsIcon = event.target.closest(".plant-settings");
        if (settingsIcon) {
            const plantCard = settingsIcon.closest(".plant-card");
            const plantId = plantCard.dataset.plantId;  // Get the plant ID!
            const menu = plantCard.querySelector(".plant-menu");

            menu.classList.toggle("show");

            // Add click listeners to menu items *only once* when the menu is shown
            if (menu.classList.contains("show")) {
                const renameOption = menu.querySelector(".rename-option");
                const deleteOption = menu.querySelector(".delete-option");

                // Use named functions so we can remove them later
                function renameHandler() { renamePlant(plantId, plantCard); }
                function deleteHandler() { deletePlant(plantId, plantCard); }

                // Remove any existing listeners to prevent duplicates
                renameOption.removeEventListener("click", renameHandler);
                deleteOption.removeEventListener("click", deleteHandler);

                // Add the listeners
                renameOption.addEventListener("click", renameHandler);
                deleteOption.addEventListener("click", deleteHandler);
            }
        } else {
             // Close any open menus if the click is outside a settings icon
             document.querySelectorAll(".plant-menu.show").forEach(menu => menu.classList.remove("show"));
         }
    });


    // Close menu when clicking outside the plant-card
    document.addEventListener("click", function(event) {
        if (!event.target.closest(".plant-card")) {
            document.querySelectorAll(".plant-menu.show").forEach(menu => menu.classList.remove("show"));
        }
    });



    function renamePlant(plantId, plantCard) {
        const newName = prompt("Enter the new name of your plant:");
        if (newName) {
            // Sends a POST request to /rename_plant/<plant_id>/
            fetch(`/rename_plant/${plantId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Gets the CSRF token
                },
                body: JSON.stringify({ new_name: newName }) // Sends the new name
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    plantCard.querySelector("figcaption").textContent = newName;
                    plantCard.querySelector(".plant-menu").classList.remove("show");
                } else {
                    alert("Error renaming plant: " + (data.error || "Unknown error"));
                }
            })
            .catch(error => console.error("Error:", error));
        } else {
             plantCard.querySelector(".plant-menu").classList.remove("show"); // Hide menu if canceled
        }
    }
    
    
    function deletePlant(plantId, plantCard) {
        if (confirm("Are you sure you want to delete this plant?")) {
            // Sends a POST request to /delete_plant/<plant_id>/
            fetch(`/delete_plant/${plantId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    plantCard.remove(); // Removes the plant card from the page
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