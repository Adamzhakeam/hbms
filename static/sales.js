document.addEventListener("DOMContentLoaded", () => {
  // Retrieve the token from localStorage
  const token = localStorage.getItem('token');
  if (!token) {
    alert("You are not authenticated. Please log in.");
    window.location.href = "../templates/index.html"; // Redirect to login page if no token is found
    return;
  }

  // Elements
  const productSearch = document.getElementById("productSearch");
  const productDropdown = document.getElementById("productDropdown");
  const quantityInput = document.getElementById("quantity");
  const addProductButton = document.getElementById("addProduct");
  const selectedProductsTable = document.getElementById("selectedProducts").querySelector("tbody");
  const grandTotalElement = document.getElementById("grandTotal");
  const salesForm = document.getElementById("salesForm");

  let products = []; // Store fetched products
  let selectedProducts = []; // Store selected products for the sale

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
        window.location.href = "/login";
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
    const soldTo = document.getElementById("soldTo").value;
    const amountPaid = parseInt(document.getElementById("amountPaid").value, 10);
    const paymentType = document.getElementById("paymentType").value;
    const paymentStatus = document.getElementById("paymentStatus").value;

    const salePayload = {
      grandTotal: selectedProducts.reduce((total, product) => total + product.total, 0),
      numberOfItemsSold: selectedProducts.length,
      soldBy: "brownthighs", // Replace with actual data
      soldTo: soldTo,
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
          window.location.href = "/login";
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
          window.location.href = "/login";
          return;
        }
        return response.json();
      })
      .then(data => {
        if (data.status) {
          alert("Products added successfully!");
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
});