document.addEventListener("DOMContentLoaded", function () {
    const gardenContainer = document.getElementById("garden-container");

    gardenContainer.addEventListener("click", function (event) {
        const settingsIcon = event.target.closest(".garden-settings");
        const gardenCard = event.target.closest(".garden-card");

        if (settingsIcon) {
            const card = settingsIcon.closest(".garden-card");
            let menu = card.querySelector(".garden-menu");

            if (!menu) {
                menu = document.createElement("ul");
                menu.classList.add("garden-menu");
                card.appendChild(menu);

                const renameOption = document.createElement("li");
                renameOption.textContent = "Rename Garden";
                renameOption.addEventListener("click", (e) => {
                    e.stopPropagation();
                    renameGarden(card);
                });

                const deleteOption = document.createElement("li");
                deleteOption.textContent = "Delete Garden";
                deleteOption.addEventListener("click", (e) => {
                    e.stopPropagation();
                    deleteGarden(card);
                });

                menu.append(renameOption, deleteOption);
            }

            menu.classList.toggle("show");
        } else if (gardenCard && !event.target.closest(".garden-settings")) {
            const gardenName = gardenCard.querySelector("figcaption").textContent;
            window.location.href = window.GARDEN_DETAILS_URL;
        } else {
            document.querySelectorAll(".garden-menu.show").forEach((menu) => menu.classList.remove("show"));
        }
    });

    document.getElementById("add-garden-card").addEventListener("click", function (event) {
        event.stopPropagation();
        const gardenName = prompt("Enter the name of your new garden:");
        if (gardenName) {
            const newGarden = document.createElement("section");
            newGarden.classList.add("garden-card");

            newGarden.innerHTML = `
                <img src="/static/main/assets/icon/pot.webp" alt="${gardenName}">
                <figcaption>${gardenName}</figcaption>
                <img src="/static/main/assets/icon/settings-icon.png" class="garden-settings" alt="Settings">
            `;

            document.getElementById("garden-container").insertBefore(newGarden, document.getElementById("add-garden-card"));
        }
    });

    function renameGarden(card) {
        const newName = prompt("Enter the new name of your garden:");
        if (newName) {
            card.querySelector("figcaption").textContent = newName;
        }
        card.querySelector(".garden-menu").classList.remove("show");
    }

    function deleteGarden(card) {
        card.remove();
    }

    document.addEventListener("click", function (event) {
        if (!event.target.closest(".garden-card") && !event.target.closest(".garden-menu")) {
            document.querySelectorAll(".garden-menu.show").forEach((menu) => menu.classList.remove("show"));
        }
    });
});
