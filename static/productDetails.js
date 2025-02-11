document.addEventListener('DOMContentLoaded', () => {
    fetchAllProducts(1); // Fetch initial products on page load
    // Setup event listener for search input change
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', debounce(searchProducts, 300)); // Adjust debounce delay as needed
});

// Global variable to keep track of the current page
let currentPage = 1;

// Fetch all products and populate the table with a limit of 4 items per page
async function fetchAllProducts(page) {
    try {
        const response = await fetch('http://127.0.0.1:5000/fetchAllProducts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ page: page, limit: 4 })
        });
        const data = await response.json();

        if (data.status) {
            populateTable(data.log);
            currentPage = page; // Update the current page
        } else {
            alert(data.log);
        }
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

// Populate the product table with data
function populateTable(products) {
    const tableBody = document.getElementById('productTableBody');
    tableBody.innerHTML = '';

    products.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.productName}</td>
            <td>${product.productSerialNumber}</td>
            <td>${product.productCategory}</td>
            <td>${product.productQuantity}</td>
            <td>${product.productSalePrice}</td>
            <td><button onclick="openEditModal('${product.productId}')">Edit</button></td>
        `;
        tableBody.appendChild(row);
    });
}

// Fetch the next set of products
function fetchNextPage() {
    fetchAllProducts(currentPage + 1);
}

// Search products by name, serial number, or category
async function searchProducts() {
    const query = document.getElementById('searchInput').value.toLowerCase(); // Convert to lowercase
    const searchType = document.querySelector('input[name="searchType"]:checked').value;

    let endpoint, payload;
    if (searchType === 'name') {
        endpoint = 'http://127.0.0.1:5000/fetchSpecificProduct';
        payload = { productName: query };
    } else if (searchType === 'serialNumber') {
        endpoint = 'http://127.0.0.1:5000/fetchSpecificProductByPertNumber';
        payload = { productSerialNumber: query };
    } else if (searchType === 'category') {
        endpoint = 'http://127.0.0.1:5000/fetchSpecificProductByCategory';
        payload = { productCategory: query };
    }

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (data.status) {
            populateTable(data.log);
        } else {
            alert(data.log);
        }
    } catch (error) {
        console.error('Error searching products:', error);
    }
}

// Open the edit modal and populate it with product details
async function openEditModal(productId) {
    console.log('Opening edit modal for productId:', productId); // Debugging log
    try {
        const response = await fetch('http://127.0.0.1:5000/fetchSpecificProductById', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ productId: productId })
        });

        const data = await response.json();
        if (data.status) {
            const product = data.log[0];
            document.getElementById('editProductName').value = product.productName;
            document.getElementById('editProductSerialNumber').value = product.productSerialNumber;
            document.getElementById('editProductCategory').value = product.productCategory;
            document.getElementById('editProductCostPrice').value = product.productCostPrice;
            document.getElementById('editProductSalePrice').value = product.productSalePrice;
            document.getElementById('editProductQuantity').value = product.productQuantity;
            document.getElementById('editUnits').value = product.units;
            document.getElementById('editForm').setAttribute('data-product-id', product.productId);

            document.getElementById('editModal').style.display = 'block';
        } else {
            alert(data.log);
        }
    } catch (error) {
        console.error('Error opening edit modal:', error);
    }
}

// Close the edit modal
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
    document.getElementById('editForm').removeAttribute('data-product-id'); // Clear the product ID
}

// Update the product details
async function updateProduct(event) {
    event.preventDefault();
    const productId = document.getElementById('editForm').getAttribute('data-product-id');
    const productDetails = {
        productId: productId,
        productName: document.getElementById('editProductName').value,
        productSerialNumber: document.getElementById('editProductSerialNumber').value,
        productCategory: document.getElementById('editProductCategory').value,
        productCostPrice: parseInt(document.getElementById('editProductCostPrice').value),
        productSalePrice: parseInt(document.getElementById('editProductSalePrice').value),
        productQuantity: parseInt(document.getElementById('editProductQuantity').value),
        units: document.getElementById('editUnits').value
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/editProduct', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productDetails)
        });

        const data = await response.json();
        if (data.status) {
            alert('Product updated successfully');
            closeModal();
            fetchAllProducts(currentPage);
        } else {
            alert(data.log);
        }
    } catch (error) {
        console.error('Error updating product:', error);
    }
}

// Debounce function to delay execution of search function
function debounce(func, delay) {
    let timeout;
    return function () {
        const context = this;
        const args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            timeout = null;
            func.apply(context, args);
        }, delay);
    };
}
