async function populateUnits() {
    try {
        const response = await fetch('http://127.0.0.1:5000/fetchAllUnits', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        console.log('Units data:', data); // Log the response to check the structure

        const unitsSelect = document.getElementById('units');
        unitsSelect.innerHTML = ''; // Clear previous options

        if (data.status) {
            data.log.forEach(unit => {
                const option = document.createElement('option');
                option.value = unit.unit; // Adjust according to your data structure
                option.innerText = unit.unit;
                unitsSelect.appendChild(option);
            });
        } else {
            console.error('Failed to fetch units:', data.log);
        }
    } catch (error) {
        console.error('Error fetching units:', error.message);
    }
}

async function populateCategories() {
    try {
        const response = await fetch('http://127.0.0.1:5000/fetchAllCategories', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();
        console.log('Categories data:', data); // Log the response to check the structure

        const categoriesSelect = document.getElementById('productCategory');
        categoriesSelect.innerHTML = ''; // Clear previous options

        if (data.status) {
            data.log.forEach(category => {
                const option = document.createElement('option');
                option.value = category.category; // Adjust according to your data structure
                option.innerText = category.category;
                categoriesSelect.appendChild(option);
            });
        } else {
            console.error('Failed to fetch categories:', data.log);
        }
    } catch (error) {
        console.error('Error fetching categories:', error.message);
    }
}
