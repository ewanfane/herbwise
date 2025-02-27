document.addEventListener("DOMContentLoaded", function () {
    console.log("Fetching sensor data for all plants...");

    const containers = document.querySelectorAll(".sensor-data-container");

    containers.forEach(container => {
        const plantId = container.dataset.plantId;

        if (!plantId) {
            console.error("No plant ID found in dataset!");
            return;
        }

        console.log(`Fetching data for plant ${plantId}`);
        fetchLatestRecord(plantId, container);
    });


    
    // Get the garden name from the URL query parameter
    const urlParams = new URLSearchParams(window.location.search);
    const gardenName = urlParams.get('gardenName');

    // If gardenName exists in the URL, update the header with the name
    if (gardenName) {
        document.getElementById('garden-name').textContent = gardenName;
    } else {
        // Default fallback if no garden name is found
        document.getElementById('garden-name').textContent = "Garden Name Not Found";
    }
});


 // Handles click events on the plant container.
 //This function manages the display of plant settings menu, and actions for renaming or deleting plants.
 //It uses event delegation to handle clicks on plant cards and their settings icons.
 //
 // @param {Event} event - The click event object.
 // @returns {void} This function doesn't return a value, it performs DOM manipulations directly.
 
document.getElementById("plant-container").addEventListener("click", function (event) {
    const settingsIcon = event.target.closest(".plant-settings");
    const plantCard = event.target.closest(".plant-card");

    if (settingsIcon) {
        const card = settingsIcon.closest(".plant-card");
        let menu = card.querySelector(".plant-menu");

        if (!menu) {
            menu = document.createElement("ul");
            menu.classList.add("plant-menu");
            card.appendChild(menu);

            const renameOption = document.createElement("li");
            renameOption.textContent = "Rename Plant";
            renameOption.addEventListener("click", (e) => {
                e.stopPropagation();
                renamePlant(card);
            });

            const deleteOption = document.createElement("li");
            deleteOption.textContent = "Delete Plant";
            deleteOption.addEventListener("click", (e) => {
                e.stopPropagation();
                deletePlant(card);
            });

            menu.append(renameOption, deleteOption);
        }

        menu.classList.toggle("show");
    } else if (plantCard && !event.target.closest(".plant-settings")) {
        // Do something when plant card is clicked (e.g., view plant details)
    } else {
        document.querySelectorAll(".plant-menu.show").forEach((menu) => menu.classList.remove("show"));
    }
});

// Add a new plant card when the "Add Plant" card is clicked
document.getElementById("add-plant-card").addEventListener("click", function (event) {
    event.stopPropagation(); // Prevent other click events from triggering

    const plantName = prompt("Enter the name of your new plant:");
    if (plantName) {
        const newPlant = document.createElement("section");
        newPlant.classList.add("plant-card");

        newPlant.innerHTML = `
            <img src="/assets/icon/plant7.png" alt="${plantName}">
            <figcaption>${plantName}</figcaption>
            <img src="/assets/icon/settings-icon.png" class="plant-settings" alt="Settings">
        `;

        document.getElementById("plant-container").insertBefore(newPlant, document.getElementById("add-plant-card"));
    }
});

// Rename Plant function
function renamePlant(card) {
    const newName = prompt("Enter the new name of your plant:");
    if (newName) {
        card.querySelector("figcaption").textContent = newName;
    }
    card.querySelector(".plant-menu").classList.remove("show"); // Hide the menu after renaming
}

// Delete Plant function
function deletePlant(card) {
    card.remove();
}


/*/+
 * Fetches the latest sensor data for a specific plant and updates the corresponding HTML container.//+
 * //+
 * @param {string|number} plantId - The unique identifier of the plant.//+
 * @param {HTMLElement} [container] - The HTML container element to update with the fetched data. If not provided, the function attempts to find it using the plantId.//+
 * @returns {void} This function doesn't return a value, it updates the DOM directly.//+
 *///+
function fetchLatestRecord(plantId, container) {
    fetch(`/latest_record/${plantId}/`)
        .then(response => response.json())
        .then(data => {
            console.log(`Data for plant ID ${plantId}:`, data);
            if (!data.error) {
                // Find the container if it wasn't provided
                if (!container) {
                    container = document.querySelector(`.sensor-data-container[data-plant-id="${plantId}"]`);
                    if (!container) {
                        console.error(`Container for plant ID ${plantId} not found`);
                        return;
                    }
                }

                container.querySelector(".temperature").innerText = `🌡️ ${data.temperature} °C`;
                container.querySelector(".humidity").innerText = `💧 ${data.humidity} %`;
                container.querySelector(".soilMoisture").innerText = `🌱 ${data.soil_moisture}`;
                container.querySelector(".light").innerText = `☀️ ${data.light}`;
            } else {
                if (container) {
                    container.querySelector(".temperature").innerText = "-";
                    container.querySelector(".humidity").innerText = "-";
                    container.querySelector(".soilMoisture").innerText = "-";
                    container.querySelector(".light").innerText = "-";
                }
            }
        })
        .catch(error => console.error("Error fetching data:", error));
}


// Call function every 5 seconds (for real-time updates)
setInterval(() => {
    const containers = document.querySelectorAll(".sensor-data-container");
    containers.forEach(container => {
        const plantId = container.dataset.plantId;
        if (plantId) {
            fetchLatestRecord(plantId, container);
        }
    });
}, 5000);


// Close the menu when clicking outside
document.addEventListener("click", function (event) {
    if (!event.target.closest(".plant-card") && !event.target.closest(".plant-menu")) {
        document.querySelectorAll(".plant-menu.show").forEach((menu) => menu.classList.remove("show"));
    }
});
