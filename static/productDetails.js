document.addEventListener('DOMContentLoaded', () => {
    fetchAllProducts(1); // Fetch initial products on page load
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', debounce(searchProducts, 300));
});

let currentPage = 1;
let selectedProducts = []; // Array to store selected products

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
            currentPage = page;
        } else {
            alert(data.log);
        }
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

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
            <td>
                <button onclick="openEditModal('${product.productId}')">Edit</button>
                <button onclick="selectProduct('${product.productId}', '${product.productName}', '${product.productCategory}', '${product.units}')">Select</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

function fetchNextPage() {
    fetchAllProducts(currentPage + 1);
}

async function searchProducts() {
    const query = document.getElementById('searchInput').value.trim().toLowerCase();
    const searchType = document.querySelector('input[name="searchType"]:checked').value;

    if (!query) {
        alert("Please enter a search term.");
        return;
    }

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

function selectProduct(productId, productName, productCategory, units) {
    const product = { productId, productName, productCategory, units };
    if (!selectedProducts.some(p => p.productId === productId)) {
        selectedProducts.push(product);
        alert(`${productName} added to selection.`);
    } else {
        alert(`${productName} is already selected.`);
    }
}

function generatePurchaseOrder() {
    if (selectedProducts.length === 0) {
        alert("No products selected.");
        return;
    }

    // Prepare purchase order data
    const purchaseOrder = {
        products: selectedProducts,
        timestamp: new Date().toISOString()
    };

    // Log the purchase order (for debugging)
    console.log("Purchase Order:", purchaseOrder);

    // Create a worksheet from the selected products
    const worksheetData = [
        ["Product ID", "Product Name", "Category", "Units"] // Header row
    ];

    selectedProducts.forEach(product => {
        worksheetData.push([product.productId, product.productName, product.productCategory, product.units]);
    });

    const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);

    // Create a workbook and add the worksheet
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Purchase Order");

    // Generate the Excel file and trigger download
    const fileName = `Purchase_Order_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(workbook, fileName);

    alert("Purchase order generated and downloaded successfully.");
}

// Function to open the edit modal and populate it with product details
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

// Function to close the edit modal
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
    document.getElementById('editForm').removeAttribute('data-product-id'); // Clear the product ID
}

// Function to update the product details
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