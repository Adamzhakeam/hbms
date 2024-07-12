document.addEventListener('DOMContentLoaded', () => {
    const createCategoryBtn = document.getElementById('createCategoryBtn');
    const createCategoryModal = document.getElementById('createCategoryModal');
    const closeModal = document.querySelector('.close');
    const createCategoryForm = document.getElementById('createCategoryForm');
    const categoryTableBody = document.getElementById('categoryTableBody');

    // Show category creation modal on button click
    createCategoryBtn.addEventListener('click', () => {
        createCategoryModal.style.display = 'block';
    });

    // Close modal when close button or outside modal is clicked
    closeModal.onclick = function() {
        createCategoryModal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target === createCategoryModal) {
            createCategoryModal.style.display = 'none';
        }
    };

    // Handle form submission for creating category
    createCategoryForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(createCategoryForm);
        const payload = {};
        formData.forEach((value, key) => {
            payload[key] = value;
        });

        fetch('http://127.0.0.1:5000/addCategory', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                alert('Category created successfully');
                fetchAllCategories(); // Update category list
                createCategoryModal.style.display = 'none';
            } else {
                alert('Error creating category: ' + data.log);
            }
        })
        .catch(error => console.error('Error creating category:', error));
    });

    // Function to fetch all categories and populate the table
    function fetchAllCategories() {
        fetch('http://127.0.0.1:5000/fetchAllCategories', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                displayCategories(data.categories);
            } else {
                alert('Error fetching categories: ' + data.log);
            }
        })
        .catch(error => console.error('Error fetching categories:', error));
    }

    // Function to display categories in the table
    function displayCategories(categories) {
        categoryTableBody.innerHTML = ''; // Clear previous data
        categories.forEach(category => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${category.category}</td>
            `;
            categoryTableBody.appendChild(row);
        });
    }

    // Initial fetch to populate the category table
    fetchAllCategories();
});
