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
            if (gardenCard.id !== "add-garden-card") {
                const gardenId = gardenCard.getAttribute("data-garden-id");
                if (gardenId) {
                    // Navigate to the garden details page
                    window.location.href = `/gardens/${gardenId}/`;
                }
            }
        } else {
            document.querySelectorAll(".garden-menu.show").forEach((menu) => menu.classList.remove("show"));
        }
    });

   document.getElementById("add-garden-card").addEventListener("click", function (event) {
        event.stopPropagation();
        const gardenName = prompt("Enter the name of your new garden:");
        if (gardenName) {

            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/create_garden/';

            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value;


            const nameInput = document.createElement('input');
            nameInput.type = 'hidden';
            nameInput.name = 'garden_name';
            nameInput.value = gardenName;

            form.appendChild(csrfInput);
            form.appendChild(nameInput);
            document.body.appendChild(form);
            form.submit();
        }
    });

  async function renameGarden(card) {
      const gardenId = card.dataset.gardenId;
      const newName = prompt("Enter the new name of your garden:");
      if (newName && gardenId) {
          try {
              const response = await fetch(`/gardens/${gardenId}/rename/`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/x-www-form-urlencoded', // Important for form data
                      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                  },
                  body: `garden_name=${encodeURIComponent(newName)}`, // URL-encode the data
              });

              if (response.ok) {
                  // Update the garden name in the DOM *only* if the server confirms success
                  card.querySelector("figcaption").textContent = newName;
              } else {
                  // Handle errors (e.g., display an error message)
                  console.error('Failed to rename garden:', response.status, response.statusText);
                  alert('Failed to rename garden. Please try again.');
              }
          } catch (error) {
              console.error('Error renaming garden:', error);
              alert('An error occurred. Please try again.');
          }
      }
      card.querySelector(".garden-menu").classList.remove("show");
  }

  async function deleteGarden(card) {
      const gardenId = card.dataset.gardenId;
      if (gardenId && confirm("Are you sure you want to delete this garden?")) {
          try {
              const response = await fetch(`/gardens/${gardenId}/delete/`, {
                  method: 'POST', // Or 'DELETE' if your view uses that method
                  headers: {
                      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                  },
              });

              if (response.ok) {
                  // Remove the card from the DOM *only* if the server confirms deletion
                  card.remove();
              } else {
                  console.error('Failed to delete garden:', response.status, response.statusText);
                  alert('Failed to delete garden. Please try again.');
              }
          } catch (error) {
              console.error('Error deleting garden:', error);
              alert('An error occurred. Please try again.');
          }
      }
  }

    document.addEventListener("click", function (event) {
        if (!event.target.closest(".garden-card") && !event.target.closest(".garden-menu")) {
            document.querySelectorAll(".garden-menu.show").forEach((menu) => menu.classList.remove("show"));
        }
    });
});