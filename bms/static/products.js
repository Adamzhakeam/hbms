document.addEventListener('DOMContentLoaded', function() {
    fetchUnits();
    fetchCategories();
});

function fetchUnits() {
    fetch('http://127.0.0.1:5000/fetchAllUnits', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Units response data:', data); // Log the response data
        if (data.status) {
            populateDropdown('units', data.log, 'unit'); // Assuming 'unitName' is the correct key
        } else {
            console.error('Failed to fetch units:', data.log);
        }
    })
    .catch(error => console.error('Error fetching units:', error));
}

function fetchCategories() {
    fetch('http://127.0.0.1:5000/fetchAllCategories', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Categories response data:', data); // Log the response data
        if (data.status) {
            populateDropdown('productCategory', data.log, 'category'); // Assuming 'categoryName' is the correct key
        } else {
            console.error('Failed to fetch categories:', data.log);
        }
    })
    .catch(error => console.error('Error fetching categories:', error));
}

function populateDropdown(elementId, options, key) {
    const select = document.getElementById(elementId);
    select.innerHTML = '';

    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option[key]; // Use dynamic key
        optionElement.textContent = option[key]; // Use dynamic key
        select.appendChild(optionElement);
    });
}

function registerProduct() {
    const productName = document.getElementById('productName').value;
    const productCostPrice = document.getElementById('productCostPrice').value;
    const productSalePrice = document.getElementById('productSalePrice').value;
    const productSerialNumber = document.getElementById('productSerialNumber').value;
    const productCategory = document.getElementById('productCategory').value;
    const productQuantity = document.getElementById('productQuantity').value;
    const units = document.getElementById('units').value;
    const productImage = document.getElementById('productImage').value;

    const payload = {
        productName: productName,
        productCostPrice: parseInt(productCostPrice), // Ensure float or integer as needed
        productSalePrice: parseInt(productSalePrice), // Ensure float or integer as needed
        productSerialNumber: productSerialNumber,
        productCategory: productCategory,
        productQuantity: parseInt(productQuantity), // Ensure integer
        units: units,
        productImage: productImage
        // Add other fields as needed
    };

    fetch('http://127.0.0.1:5000/registerProduct', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Register product response data:', data); // Log the response data
        if (data.status) {
            alert('Product registered successfully!');
            // Optionally reset the form or perform other actions
        } else {
            alert('Failed to register product. Error: ' + data.log);
        }
    })
    .catch(error => {
        console.error('Error registering product:', error);
        alert('Error registering product. Please try again.');
    });
}
