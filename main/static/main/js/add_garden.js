document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("add-garden-form");

    form.addEventListener("submit", function (event) {
        const gardenName = document.getElementById("garden-name").value.trim();

        if (!gardenName) {
            alert("Please fill out name field.");
            event.preventDefault();
            return;
        }

    });
});
