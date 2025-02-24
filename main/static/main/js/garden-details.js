document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".plant-card").forEach(card => {
        const plantId = card.querySelector(".sensor-data-container").dataset.plantId;
        if (plantId) {
            fetchLatestRecord(plantId);
        }
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

// Event delegation: Apply listener to the parent container of plant cards
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
/*document.getElementById("add-plant-card").addEventListener("click", function (event) {
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
});*/

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

function fetchLatestRecord(plantId) {
    fetch(`/latest_record/${plantId}/`)  // ✅ Correct syntax

        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                document.getElementById("temperature").innerText = data.temperature + "°C";
                document.getElementById("humidity").innerText = data.humidity + "%";
                document.getElementById("soilMoisture").innerText = data.soil_moisture + "%";
                document.getElementById("light").innerText = data.light + " lux";
            } else {
                document.getElementById("temperature").innerText = "-";
                document.getElementById("humidity").innerText = "-";
                document.getElementById("soilMoisture").innerText = "-";
                document.getElementById("light").innerText = "-";
            }
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Call function every 5 seconds (for real-time updates)
setInterval(() => {
    document.querySelectorAll(".plant-card").forEach(card => {
        const plantId = card.querySelector(".sensor-data-container").dataset.plantId;
        if (plantId) {
            fetchLatestRecord(plantId);
        }
    });
}, 5000);


// Close the menu when clicking outside
document.addEventListener("click", function (event) {
    if (!event.target.closest(".plant-card") && !event.target.closest(".plant-menu")) {
        document.querySelectorAll(".plant-menu.show").forEach((menu) => menu.classList.remove("show"));
    }
});
