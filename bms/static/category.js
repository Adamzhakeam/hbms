document.addEventListener("DOMContentLoaded", () => {
  const createCategoryBtn = document.getElementById("createCategoryBtn");
  const createCategoryModal = document.getElementById("createCategoryModal");
  const closeModal = document.querySelector(".close");
  const createCategoryForm = document.getElementById("createCategoryForm");
  const categoryTableBody = document.getElementById("categoryTableBody");

  // Show category creation modal on button click
  createCategoryBtn.addEventListener("click", () => {
    createCategoryModal.style.display = "block";
  });

  // Close modal when close button or outside modal is clicked
  closeModal.onclick = function () {
    createCategoryModal.style.display = "none";
  };

  window.onclick = function (event) {
    if (event.target === createCategoryModal) {
      createCategoryModal.style.display = "none";
    }
  };

  // Handle form submission for creating category
  createCategoryForm.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent form's default submission behavior
    const formData = new FormData(createCategoryForm);
    const payload = {};

    formData.forEach((value, key) => {
      payload[key] = value;
    });

    // Add the "others" key with an empty object
    payload["others"] = {"createdBy":"parrot"};

    try {
      const response = await fetch("http://127.0.0.1:5000/createCategory", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      if (data.status) {
        alert("Category created successfully");
        fetchAllCategories(); // Refresh the categories list
        createCategoryModal.style.display = "none"; // Close the modal
        createCategoryForm.reset(); // Clear the form
      } else {
        alert("Error creating category: " + data.log);
      }
    } catch (error) {
      console.error("Error creating category:", error);
      alert("Error creating category. Please check console for details.");
    }
  });

  // Fetch and display all categories
  function fetchAllCategories() {
    fetch("http://127.0.0.1:5000/fetchAllCategories", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status) {
          displayCategories(data.log);
        } else {
          alert("Error fetching categories: " + data.log);
        }
      })
      .catch((error) => console.error("Error fetching categories:", error));
  }

  // Populate categories table
  function displayCategories(categories) {
    categoryTableBody.innerHTML = ""; // Clear table
    categories.forEach((category) => {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${category.category}</td>`;
      categoryTableBody.appendChild(row);
    });
  }

  // Initial fetch to populate table
  fetchAllCategories();
});
