async function registerProduct() {
    const payload = {
        productName: document.getElementById('productName').value,
        productCostPrice: document.getElementById('productCostPrice').value,
        productSalePrice: document.getElementById('productSalePrice').value,
        productSerialNumber: document.getElementById('productSerialNumber').value,
        productCategory: document.getElementById('productCategory').value,
        productQuantity: document.getElementById('productQuantity').value,
        units: document.getElementById('units').value,
        productImage: document.getElementById('productImage').value
    };

    const response = await fetch('http://127.0.0.1:5000/registerProduct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const data = await response.json();
    alert(data.log);
}

async function fetchAllProducts() {
    const response = await fetch('http://127.0.0.1:5000/fetchAllProducts', { method: 'POST' });
    const data = await response.json();

    const productsList = document.getElementById('products-list');
    productsList.innerHTML = ''; // Clear existing list

    if (data.status) {
        data.log.forEach(product => {
            const productDiv = document.createElement('div');
            productDiv.innerText = `${product.productName} - ${product.productSerialNumber}`;
            productsList.appendChild(productDiv);
        });
    } else {
        productsList.innerText = data.log;
    }
}

async function fetchSpecificProduct() {
    const productName = document.getElementById('searchProductName').value;
    const productSerialNumber = document.getElementById('searchProductSerialNumber').value;

    const payload = { productName, productSerialNumber };

    const response = await fetch('http://127.0.0.1:5000/fetchSpecificProduct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (data.status) {
        document.getElementById('edit-product-fields').style.display = 'block';
        const product = data.log[0];
        document.getElementById('editProductName').value = product.productName;
        document.getElementById('editProductCostPrice').value = product.productCostPrice;
        document.getElementById('editProductSalePrice').value = product.productSalePrice;
        document.getElementById('editProductCategory').value = product.productCategory;
        document.getElementById('editProductQuantity').value = product.productQuantity;
        document.getElementById('editUnits').value = product.units;
        document.getElementById('editProductId').value = product.productId;
    } else {
        alert(data.log);
    }
}

async function editProduct() {
    const payload = {
        productId: document.getElementById('editProductId').value,
        productName: document.getElementById('editProductName').value,
        productCostPrice: parseInt(document.getElementById('editProductCostPrice').value),
        productSalePrice: parseInt(document.getElementById('editProductSalePrice').value),
        productCategory: document.getElementById('editProductCategory').value,
        productQuantity: parseInt(document.getElementById('editProductQuantity').value),
        units: document.getElementById('editUnits').value
    };

    const response = await fetch('http://127.0.0.1:5000/editProduct', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const data = await response.json();
    alert(data.log);
}
// the section below is responsible for sales route handling
// Fetch products and populate dropdown on page load
document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const productSearch = document.getElementById('productSearch');
    const productDropdown = document.getElementById('productDropdown');
    const quantityInput = document.getElementById('quantity');
    const addProductButton = document.getElementById('addProduct');
    const selectedProductsTable = document.getElementById('selectedProducts').querySelector('tbody');
    const grandTotalElement = document.getElementById('grandTotal');
    const salesForm = document.getElementById('salesForm');
    
    let products = []; // This will store the fetched products
    let selectedProducts = []; // This will store the selected products for the sale

    // Fetch products from the backend
    fetch('http://127.0.0.1:5000/fetchAllProducts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            products = data.log;
            populateProductDropdown(products);
        } else {
            alert('Error fetching products: ' + data.log);
        }
    })
    .catch(error => console.error('Error:', error));

    // Populate product dropdown
    function populateProductDropdown(products) {
        productDropdown.innerHTML = '';
        products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.productId;
            option.textContent = `${product.productName} - ${product.productSalePrice} - ${product.productCategory}`;
            productDropdown.appendChild(option);
        });
    }

    // Filter products based on search input
    productSearch.addEventListener('input', () => {
        const searchTerm = productSearch.value.toLowerCase();
        const filteredProducts = products.filter(product => 
            product.productName.toLowerCase().includes(searchTerm)
        );
        populateProductDropdown(filteredProducts);
    });

    // Populate quantity field based on selected product
    productDropdown.addEventListener('change', () => {
        const selectedProductId = productDropdown.value;
        const selectedProduct = products.find(product => product.productId === selectedProductId);

        if (selectedProduct) {
            quantityInput.value = selectedProduct.productQuantity;
        } else {
            quantityInput.value = '';
        }
    });

    // Add product to the selected products table
    addProductButton.addEventListener('click', () => {
        const selectedProductId = productDropdown.value;
        const selectedProduct = products.find(product => product.productId === selectedProductId);
        const quantity = parseInt(quantityInput.value, 10);

        if (!selectedProduct || isNaN(quantity) || quantity <= 0) {
            alert('Please select a valid product and quantity.');
            return;
        }

        if (quantity > selectedProduct.productQuantity) {
            alert('You cannot select more than the available quantity.');
            return;
        }

        const total = selectedProduct.productSalePrice * quantity;
        selectedProducts.push({ ...selectedProduct, quantity, total });

        updateSelectedProductsTable();
        updateGrandTotal();
        quantityInput.value = '';
    });

    // Update the selected products table
    function updateSelectedProductsTable() {
        selectedProductsTable.innerHTML = '';
        selectedProducts.forEach((product, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${product.productName}</td>
                <td>${product.productSalePrice}</td>
                <td>${product.quantity}</td>
                <td>${product.total}</td>
                <td><button type="button" class="remove" data-index="${index}">Remove</button></td>
            `;
            selectedProductsTable.appendChild(row);
        });

        // Add event listeners for remove buttons
        document.querySelectorAll('.remove').forEach(button => {
            button.addEventListener('click', removeProduct);
        });
    }

    // Remove product from the selected products table
    function removeProduct(event) {
        const index = event.target.getAttribute('data-index');
        selectedProducts.splice(index, 1);
        updateSelectedProductsTable();
        updateGrandTotal();
    }

    // Update the grand total
    function updateGrandTotal() {
        const grandTotal = selectedProducts.reduce((total, product) => total + product.total, 0);
        grandTotalElement.textContent = grandTotal;
    }

    // Handle form submission
    salesForm.addEventListener('submit', event => {
        event.preventDefault();
        const soldTo = document.getElementById('soldTo').value;
        const amountPaid = parseInt(document.getElementById('amountPaid').value, 10);
        const paymentType = document.getElementById('paymentType').value;
        const paymentStatus = document.getElementById('paymentStatus').value;

        const salePayload = {
            grandTotal: selectedProducts.reduce((total, product) => total + product.total, 0),
            numberOfItemsSold: selectedProducts.length,
            soldBy: 'brownthighs', // Replace with actual data
            soldTo: soldTo,
            paymentType: paymentType,
            paymentStatus: paymentStatus,
            amountPaid: amountPaid,
            others: {'userName':'nakanjako'} // Replace with actual data
        };

        fetch('http://127.0.0.1:5000/addSale', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(salePayload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                alert('Sale added successfully!');
                const saleId = data.saleId; // Capture the saleId from the response

                // Now add individual product sales
                const productSalesPayload = selectedProducts.map(product => ({
                    saleId: saleId, // Use the captured saleId
                    productId: product.productId,
                    unitPrice: product.productSalePrice,
                    units: product.units,
                    productQuantity: product.quantity,
                    total: product.total,
                    others: {'name':'thickthighs'} // Replace with actual data
                }));

                fetch('http://127.0.0.1:5000/addSingleProductSale', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(productSalesPayload)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status) {
                        alert('Products added successfully!');
                    } else {
                        alert('Error adding products: ' + data.log);
                    }
                })
                .catch(error => console.error('Error:', error));
            } else {
                alert('Error adding sale: ' + data.log);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});


// ---log in aka index.hmtl page java script
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    var phone = document.getElementById('phone').value;
    var password = document.getElementById('password').value;

    // Create payload object
    var payload = {
        'phoneNumber': phone,
        'password': password
    };

    // Send POST request to /login endpoint
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            // Redirect to dashboard or handle success as needed
            window.location.href = '../../bms/templates/adminDashboard.html';  // Replace with your actual dashboard URL
        } else {
            // Handle login failure (e.g., show error message)
            console.log(data.log);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
