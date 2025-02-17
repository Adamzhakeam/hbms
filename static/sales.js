document.addEventListener("DOMContentLoaded", () => {
  // Retrieve the token from localStorage
  const token = localStorage.getItem('token');
  if (!token) {
    alert("You are not authenticated. Please log in.");
    window.location.href = "../templates/index.html"; // Redirect to login page if no token is found
    return;
  }

  // Header Buttons
  const homeButton = document.getElementById("homeButton");
  const logoutButton = document.getElementById("logoutButton");

  // Home Button: Redirect to usersDashboard.html
  homeButton.addEventListener("click", () => {
    window.location.href = "../templates/usersDashboard.html";
  });

  // Logout Button: Clear token and redirect to index.html
  logoutButton.addEventListener("click", () => {
    localStorage.removeItem('token'); // Clear the token
    window.location.href = "../templates/index.html"; // Redirect to login page
  });

  // Elements
  const productSearch = document.getElementById("productSearch");
  const productDropdown = document.getElementById("productDropdown");
  const quantityInput = document.getElementById("quantity");
  const addProductButton = document.getElementById("addProduct");
  const selectedProductsTable = document.getElementById("selectedProducts").querySelector("tbody");
  const grandTotalElement = document.getElementById("grandTotal");
  const salesForm = document.getElementById("salesForm");
  const soldToDropdown = document.getElementById("soldTo");

  let products = []; // Store fetched products
  let selectedProducts = []; // Store selected products for the sale

  // Fetch customers from backend
  fetch("http://127.0.0.1:5000/fetchAllCustomers", {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}` // Include the token in the headers
    },
    body: JSON.stringify({}),
  })
    .then(response => {
      if (response.status === 401) {
        // Token is invalid or expired, redirect to login
        alert("Your session has expired. Please log in again.");
        window.location.href = "../templates/index.html";
        return;
      }
      return response.json();
    })
    .then(data => {
      if (data.status) {
        const customers = data.log;
        populateCustomerDropdown(customers);
      } else {
        alert("Error fetching customers: " + data.log);
      }
    })
    .catch(error => console.error("Error:", error));

  // Populate customer dropdown
  function populateCustomerDropdown(customers) {
    soldToDropdown.innerHTML = '<option value="" disabled selected>Select a customer</option>';
    customers.forEach(customer => {
      const option = document.createElement("option");
      option.value = customer.customerId; // Use customerId as the value
      option.textContent = `${customer.customerName} - ${customer.customerPhoneNumber}`; // Display name and phone number
      soldToDropdown.appendChild(option);
    });
  }

  // Fetch products from backend
  fetch("http://127.0.0.1:5000/fetchAllProducts", {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}` // Include the token in the headers
    },
    body: JSON.stringify({}),
  })
    .then(response => {
      if (response.status === 401) {
        // Token is invalid or expired, redirect to login
        alert("Your session has expired. Please log in again.");
        window.location.href = "../templates/index.html";
        return;
      }
      return response.json();
    })
    .then(data => {
      if (data.status) {
        products = data.log;
        populateProductDropdown(products);
      } else {
        alert("Error fetching products: " + data.log);
      }
    })
    .catch(error => console.error("Error:", error));

  // Populate product dropdown
  function populateProductDropdown(products) {
    productDropdown.innerHTML = '<option value="">Select a product</option>';
    products.forEach(product => {
      const option = document.createElement("option");
      option.value = product.productId;
      option.textContent = `${product.productName} - ${product.productSalePrice} - ${product.productCategory}`;
      productDropdown.appendChild(option);
    });
  }

  // Filter products based on search input
  productSearch.addEventListener("input", () => {
    const searchTerm = productSearch.value.toLowerCase();
    const filteredProducts = products.filter(product =>
      product.productName.toLowerCase().includes(searchTerm)
    );
    populateProductDropdown(filteredProducts);
  });

  // Populate quantity field based on selected product
  productDropdown.addEventListener("change", () => {
    const selectedProductId = productDropdown.value;
    const selectedProduct = products.find(product => product.productId === selectedProductId);

    quantityInput.value = selectedProduct ? selectedProduct.productQuantity : "";
  });

  // Add product to the selected products table
  addProductButton.addEventListener("click", () => {
    const selectedProductId = productDropdown.value;
    const selectedProduct = products.find(product => product.productId === selectedProductId);
    const quantity = parseInt(quantityInput.value, 10);

    if (!selectedProduct || isNaN(quantity) || quantity <= 0) {
      alert("Please select a valid product and quantity.");
      return;
    }

    if (quantity > selectedProduct.productQuantity) {
      alert("You cannot select more than the available quantity.");
      return;
    }

    const total = selectedProduct.productSalePrice * quantity;
    selectedProducts.push({ ...selectedProduct, quantity, total });

    updateSelectedProductsTable();
    updateGrandTotal();
    quantityInput.value = "";
  });

  // Update the selected products table
  function updateSelectedProductsTable() {
    selectedProductsTable.innerHTML = "";
    selectedProducts.forEach((product, index) => {
      const row = document.createElement("tr");
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
    document.querySelectorAll(".remove").forEach(button => {
      button.addEventListener("click", removeProduct);
    });
  }

  // Remove product from selected products table
  function removeProduct(event) {
    const index = event.target.getAttribute("data-index");
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
  salesForm.addEventListener("submit", event => {
    event.preventDefault();
    const soldTo = soldToDropdown.value; // Get the selected customerId
    const amountPaid = parseFloat(document.getElementById("amountPaid").value);
    const paymentType = document.getElementById("paymentType").value;
    const paymentStatus = document.getElementById("paymentStatus").value;
    const grandTotal = parseFloat(grandTotalElement.textContent);

    if (isNaN(amountPaid) || amountPaid < 0) {
      alert("Please enter a valid amount paid.");
      return;
    }

    if (amountPaid < grandTotal && paymentStatus === "cleared") {
      alert("Amount paid is less than the grand total. Please adjust the payment status or amount.");
      return;
    }

    // Calculate change if amount paid is more than grand total
    const change = amountPaid > grandTotal ? (amountPaid - grandTotal).toFixed(2) : 0;

    const salePayload = {
      grandTotal: grandTotal,
      numberOfItemsSold: selectedProducts.length,
      soldBy: "brownthighs", // Replace with actual data
      soldTo: soldTo, // Use customerId here
      paymentType: paymentType,
      paymentStatus: paymentStatus,
      amountPaid: amountPaid,
      others: { userName: "nakanjako" }, // Replace with actual data
    };

    fetch("http://127.0.0.1:5000/addSale", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}` // Include the token in the headers
      },
      body: JSON.stringify(salePayload),
    })
      .then(response => {
        if (response.status === 401) {
          // Token is invalid or expired, redirect to login
          alert("Your session has expired. Please log in again.");
          window.location.href = "../templates/index.html";
          return;
        }
        return response.json();
      })
      .then(data => {
        if (data.status) {
          alert("Sale added successfully!");
          const saleId = data.saleId;

          // Add individual product sales
          const productSalesPayload = selectedProducts.map(product => ({
            saleId: saleId,
            productId: product.productId,
            unitPrice: product.productSalePrice,
            units: product.units,
            productQuantity: product.quantity,
            total: product.total,
            others: { name: "thickthighs" }, // Replace with actual data
          }));

          return fetch("http://127.0.0.1:5000/addSingleProductSale", {
            method: "POST",
            headers: { 
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}` // Include the token in the headers
            },
            body: JSON.stringify(productSalesPayload),
          });
        } else {
          throw new Error("Error adding sale: " + data.log);
        }
      })
      .then(response => {
        if (response.status === 401) {
          // Token is invalid or expired, redirect to login
          alert("Your session has expired. Please log in again.");
          window.location.href = "../templates/index.html";
          return;
        }
        return response.json();
      })
      .then(data => {
        if (data.status) {
          alert("Products added successfully!");
          // Generate and display receipt
          generateReceipt(grandTotal, amountPaid, change);
          // Clear the form and selected products after successful submission
          selectedProducts = [];
          updateSelectedProductsTable();
          updateGrandTotal();
          salesForm.reset();
        } else {
          alert("Error adding products: " + data.log);
        }
      })
      .catch(error => alert(error.message));
  });

  // Generate and display receipt
  function generateReceipt(grandTotal, amountPaid, change) {
    const receiptContent = `
      <h2>Receipt</h2>
      <p><strong>Grand Total:</strong> ${grandTotal.toFixed(2)}</p>
      <p><strong>Amount Paid:</strong> ${amountPaid.toFixed(2)}</p>
      ${change > 0 ? `<p><strong>Change:</strong> ${change}</p>` : ''}
      <h3>Products Sold:</h3>
      <ul>
        ${selectedProducts.map(product => `
          <li>${product.productName} - ${product.quantity} x ${product.productSalePrice.toFixed(2)} = ${product.total.toFixed(2)}</li>
        `).join('')}
      </ul>
    `;

    // Display receipt in a modal or new window
    const receiptWindow = window.open("", "Receipt", "width=600,height=400");
    receiptWindow.document.write(`
      <html>
        <head>
          <title>Receipt</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h2 { color: #4CAF50; }
            ul { list-style-type: none; padding: 0; }
            li { margin-bottom: 10px; }
          </style>
        </head>
        <body>
          ${receiptContent}
          <button onclick="window.print()">Print Receipt</button>
        </body>
      </html>
    `);
    receiptWindow.document.close();
  }
});