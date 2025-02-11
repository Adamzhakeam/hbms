document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const productSearch = document.getElementById("productSearch");
  const productDropdown = document.getElementById("productDropdown");
  const quantityInput = document.getElementById("quantity");
  const addProductButton = document.getElementById("addProduct");
  const selectedProductsTable = document
    .getElementById("selectedProducts")
    .querySelector("tbody");
  const grandTotalElement = document.getElementById("grandTotal");
  const salesForm = document.getElementById("salesForm");

  let products = []; // Stores fetched products
  let selectedProducts = []; // Stores selected products for the sale

  // Retrieve token from local storage
  const token = localStorage.getItem("authToken");
  if (!token) {
    alert("You are not authenticated. Please log in.");
    window.location.href = "/login"; // Redirect to login if token is missing
    return;
  }

  // Decode token to get username
  const decodedToken = JSON.parse(atob(token.split(".")[1]));
  const username = decodedToken.user_name;

  // Fetch products from the backend
  fetch("http://127.0.0.1:5000 /fetchAllProducts", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`, // Include token in the headers
    },
    body: JSON.stringify({}),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status) {
        products = data.log;
        populateProductDropdown(products);
      } else {
        alert("Error fetching products: " + data.log);
      }
    })
    .catch((error) => console.error("Error:", error));

  // Populate product dropdown
  function populateProductDropdown(products) {
    productDropdown.innerHTML = "";
    products.forEach((product) => {
      const option = document.createElement("option");
      option.value = product.productId;
      option.textContent = `${product.productName} - ${product.productSalePrice} - ${product.productCategory}`;
      productDropdown.appendChild(option);
    });
  }

  // Handle adding product to the selected products table
  addProductButton.addEventListener("click", () => {
    const selectedProductId = productDropdown.value;
    const selectedProduct = products.find(
      (product) => product.productId === selectedProductId
    );
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

  // Update selected products table
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

    document.querySelectorAll(".remove").forEach((button) => {
      button.addEventListener("click", (event) => {
        const index = event.target.getAttribute("data-index");
        selectedProducts.splice(index, 1);
        updateSelectedProductsTable();
        updateGrandTotal();
      });
    });
  }

  // Update grand total
  function updateGrandTotal() {
    const grandTotal = selectedProducts.reduce(
      (total, product) => total + product.total,
      0
    );
    grandTotalElement.textContent = grandTotal;
  }

  // Handle form submission
  salesForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const soldTo = document.getElementById("soldTo").value;
    const amountPaid = parseInt(document.getElementById("amountPaid").value, 10);
    const paymentType = document.getElementById("paymentType").value;
    const paymentStatus = document.getElementById("paymentStatus").value;

    const salePayload = {
      grandTotal: selectedProducts.reduce(
        (total, product) => total + product.total,
        0
      ),
      numberOfItemsSold: selectedProducts.length,
      soldBy: username, // Use username from token
      soldTo,
      paymentType,
      paymentStatus,
      amountPaid,
    };

    // Add sale to backend
    fetch("http://127.0.0.1:5000 /addSale", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`, // Include token in the headers
      },
      body: JSON.stringify(salePayload),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status) {
          alert("Sale added successfully!");
          const saleId = data.saleId;

          // Add individual product sales
          const productSalesPayload = selectedProducts.map((product) => ({
            saleId,
            productId: product.productId,
            unitPrice: product.productSalePrice,
            quantity: product.quantity,
            total: product.total,
          }));

          fetch("http://127.0.0.1:5000 /addSingleProductSale", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`, // Include token in the headers
            },
            body: JSON.stringify(productSalesPayload),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.status) {
                alert("Products added successfully!");
              } else {
                alert("Error adding products: " + data.log);
              }
            });
        } else {
          alert("Error adding sale: " + data.log);
        }
      })
      .catch((error) => console.error("Error:", error));
  });
});
