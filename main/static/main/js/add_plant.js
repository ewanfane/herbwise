document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("add-plant-form");

    form.addEventListener("submit", function (event) {
        const plantName = document.getElementById("plant-name").value.trim();
        const plantType = document.getElementById("plant-type").value;
        const hardwareId = document.getElementById("hardware-id").value.trim();

        if (!plantName || !plantType || !hardwareId) {
            alert("Please fill out all fields.");
            event.preventDefault();
            return;
        }

    });
});
