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
// script.js
document.addEventListener("DOMContentLoaded", () => {
    const productSelect = document.getElementById("product-select");
    const selectedProductsList = document.getElementById("selected-products");
    const grandTotalInput = document.getElementById("grand-total");
    const addProductButton = document.getElementById("add-product");
    const salesForm = document.getElementById("sales-form");

    let selectedProducts = [];

    // Fetch all products and populate the dropdown
    fetch('http://127.0.0.1:5000/fetchAllProducts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            const products = data.log;
            if (Array.isArray(products)) {
                productSelect.innerHTML = "<option value=''>Select a product</option>";
                products.forEach(product => {
                    const option = document.createElement("option");
                    option.value = JSON.stringify(product);
                    option.text = `${product.productName} - ${product.productSalePrice}`;
                    productSelect.appendChild(option);
                });
            }
        }
    })
    .catch(error => {
        console.error('Error fetching products:', error);
    });

    // Add selected product to the list
    addProductButton.addEventListener("click", () => {
        const selectedOption = productSelect.options[productSelect.selectedIndex];
        if (selectedOption.value === '') return;
        const product = JSON.parse(selectedOption.value);

        const listItem = document.createElement("li");
        listItem.innerHTML = `
            ${product.productName} - ${product.productSalePrice} 
            <input type="number" value="1" min="1" class="quantity" data-product='${selectedOption.value}'>
            <button type="button" class="btn-remove">Remove</button>
        `;
        
        selectedProductsList.appendChild(listItem);
        selectedProducts.push(product);

        updateGrandTotal();

        // Remove product from list
        listItem.querySelector(".btn-remove").addEventListener("click", () => {
            listItem.remove();
            selectedProducts = selectedProducts.filter(p => p.productId !== product.productId);
            updateGrandTotal();
        });

        // Update total amount on quantity change
        listItem.querySelector(".quantity").addEventListener("change", updateGrandTotal);
    });

    // Update the grand total
    function updateGrandTotal() {
        let grandTotal = 0;
        selectedProductsList.querySelectorAll("li").forEach(listItem => {
            const quantity = parseInt(listItem.querySelector(".quantity").value);
            const product = JSON.parse(listItem.querySelector(".quantity").dataset.product);
            grandTotal += quantity * product.productSalePrice;
        });
        grandTotalInput.value = grandTotal;
    }

    // Handle form submission
    salesForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const soldTo = document.getElementById("sold-to").value;
        const paymentType = document.getElementById("payment-type").value;
        const paymentStatus = document.getElementById("payment-status").value;
        const amountPaid = document.getElementById("amount-paid").value;
        const others = document.getElementById("others").value;

        const grandTotal = parseFloat(grandTotalInput.value);
        const numberOfItemsSold = selectedProducts.length;

        const salePayload = {
            // entryId: kutils.codes.new(),
            // saleId: ,
            // timestamp: '',
            grandTotal,
            numberOfItemsSold,
            soldBy: 'thauk', // Set this value as per your requirement
            soldTo,
            paymentType,
            paymentStatus,
            amountPaid,
            others
        };

        fetch('/addSale', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(salePayload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                const saleId = salePayload.saleId;

                // Add individual product sales
                const productSalesPayload = [];
                selectedProductsList.querySelectorAll("li").forEach(listItem => {
                    const quantity = parseInt(listItem.querySelector(".quantity").value);
                    const product = JSON.parse(listItem.querySelector(".quantity").dataset.product);
                    const total = quantity * product.productSalePrice;

                    const productSalePayload = {
                        // entryId: kutils.codes.new(),
                        // timestamp: kutils.dates.currentTimestamp(),
                        saleId,
                        productId: product.productId,
                        unitPrice: product.productSalePrice,
                        units: quantity,
                        productQuantity: quantity,
                        total,
                        others: ''  // Adjust if there are specific other details
                    };

                    productSalesPayload.push(productSalePayload);
                });

                fetch('/addSingleToDb', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(productSalesPayload)
                })
                .then(response => response.json())
                .then(productData => {
                    if (productData.status) {
                        console.log('Product sale added successfully!');
                    }
                })
                .catch(error => {
                    console.error('Error adding product sale:', error);
                });

                alert('Sale added successfully!');
                salesForm.reset();
                selectedProductsList.innerHTML = '';
                selectedProducts = [];
                updateGrandTotal();
            }
        })
        .catch(error => {
            console.error('Error adding sale:', error);
        });
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
