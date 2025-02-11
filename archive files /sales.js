// ----------the section below is responsible for sales route handling---------
// Fetch products and populate dropdown on page load
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

  let products = []; // This will store the fetched products
  let selectedProducts = [];

  // This will store the selected products for the sale

  const discountModal = document.getElementById("discountModal");
  const setDiscountButton = document.getElementById("setDiscount");
  const applyDiscountButton = document.getElementById("applyDiscount");
  const closeModalButton = document.querySelector(".close");
  const discountType = document.getElementById("discountType");
  const discountValue = document.getElementById("discountValue");
  const discountHint = document.getElementById("discountHint");

  // Open the modal
  setDiscountButton.addEventListener("click", () => {
    discountModal.style.display = "block";
  });

  // Close the modal
  closeModalButton.addEventListener("click", () => {
    discountModal.style.display = "none";
  });

  // Close modal if clicking outside the content
  window.addEventListener("click", (event) => {
    if (event.target === discountModal) {
      discountModal.style.display = "none";
    }
  });

  // Handle discount value input
  discountValue.addEventListener("input", () => {
    if (discountType.value === "percentage") {
      const value = parseInt(discountValue.value, 10);
      if (value > 99) {
        discountHint.textContent = "Percentage cannot exceed 99%";
        discountValue.value = "99"; // Cap the input to 99
      } else {
        discountHint.textContent = `% applied: ${value}%`;
      }
    } else {
      discountHint.textContent = "Flat amount will be applied.";
    }
  });

  // Handle applying the discount
  applyDiscountButton.addEventListener("click", () => {
    const discount = discountValue.value;
    const type = discountType.value;
    // Add your logic to apply the discount here
    console.log("Discount:", discount, "Type:", type);

    discountModal.style.display = "none"; // Close the modal after applying the discount
  });

  let selectedProductIds = [];

  // Fetch products by category
  function fetchProductsByCategory(category) {
    fetch("http://127.0.0.1:5000 /fetchSpecificProductByCategory", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ productCategory: category }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status) {
          populateProductList(data.log); // populate UI with the fetched products
        } else {
          alert("No products found in this category");
        }
      })
      .catch((error) =>
        console.error("Error fetching products by category:", error)
      );
  }

  // Fetch products by name
  function fetchProductsByName(productName) {
    fetch("http://127.0.0.1:5000 /fetchSpecificProduct", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ productName: productName }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status) {
          populateProductList(data.log); // populate UI with the fetched products
        } else {
          alert("No product found with this name");
        }
      })
      .catch((error) =>
        console.error("Error fetching products by name:", error)
      );
  }

  // Populate the list of products fetched in the UI
  function populateProductList(productList) {
    let productContainer = document.getElementById("product-container"); // Ensure you have a div or section with this ID
    productContainer.innerHTML = ""; // Clear the previous products

    productList.forEach((product) => {
      let productItem = document.createElement("div");
      productItem.className = "product-item";
      productItem.innerHTML = `
            <h3>${product.productName}</h3>
            <p>Category: ${product.productCategory}</p>
            <p>Sale Price: ${product.productSalePrice}</p>
            <button onclick="selectProduct(${product.productId})">Select Product</button>
        `;
      productContainer.appendChild(productItem);
    });
  }

  // Add selected product to an array for further actions (e.g., applying discount)
  function selectProduct(productId) {
    if (!selectedProductIds.includes(productId)) {
      selectedProductIds.push(productId);
      alert("Product selected");
    } else {
      alert("Product already selected");
    }
  }

  // Apply discount to selected products
  function applyDiscountToSelectedProducts(discountPercentage) {
    if (selectedProductIds.length === 0) {
      alert("No products selected");
      return;
    }

    // Logic to apply discount (you might need to send this information to the backend)
    selectedProductIds.forEach((productId) => {
      console.log(
        `Applying ${discountPercentage}% discount to product ID: ${productId}`
      );
      // Example: Send the discount to the backend for each product
    });

    alert(`Discount applied to ${selectedProductIds.length} products.`);
  }

  // Example call to search by category
  document
    .getElementById("category-search-btn")
    .addEventListener("click", function () {
      let category = document.getElementById("category-input").value;
      fetchProductsByCategory(category);
    });

  // Example call to search by name
  document
    .getElementById("name-search-btn")
    .addEventListener("click", function () {
      let productName = document.getElementById("name-input").value;
      fetchProductsByName(productName);
    });

  // Apply discount button
  document
    .getElementById("apply-discount-btn")
    .addEventListener("click", function () {
      let discount = parseFloat(
        document.getElementById("discount-input").value
      );
      applyDiscountToSelectedProducts(discount);
    });

  fetch("http://127.0.0.1:5000 /fetchAllProducts", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
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

  // Filter products based on search input
  productSearch.addEventListener("input", () => {
    const searchTerm = productSearch.value.toLowerCase();
    const filteredProducts = products.filter((product) =>
      product.productName.toLowerCase().includes(searchTerm)
    );
    populateProductDropdown(filteredProducts);
  });

  // Populate quantity field based on selected product
  productDropdown.addEventListener("change", () => {
    const selectedProductId = productDropdown.value;
    const selectedProduct = products.find(
      (product) => product.productId === selectedProductId
    );

    if (selectedProduct) {
      quantityInput.value = selectedProduct.productQuantity;
    } else {
      quantityInput.value = "";
    }
  });

  // Add product to the selected products table
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
    document.querySelectorAll(".remove").forEach((button) => {
      button.addEventListener("click", removeProduct);
    });
  }

  // Remove product from the selected products table
  function removeProduct(event) {
    const index = event.target.getAttribute("data-index");
    selectedProducts.splice(index, 1);
    updateSelectedProductsTable();
    updateGrandTotal();
  }

  // Update the grand total
  function updateGrandTotal() {
    let sr = fetchuserData().then((data) => {
      const userName = data.user_name;
    });
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
    const amountPaid = parseInt(
      document.getElementById("amountPaid").value,
      10
    );
    const paymentType = document.getElementById("paymentType").value;
    const paymentStatus = document.getElementById("paymentStatus").value;

    const salePayload = {
      grandTotal: selectedProducts.reduce(
        (total, product) => total + product.total,
        0
      ),
      numberOfItemsSold: selectedProducts.length,
      // soldBy: sr, // Replace with actual data
      soldTo: soldTo,
      paymentType: paymentType,
      paymentStatus: paymentStatus,
      amountPaid: amountPaid,
      // others: { userName: sr }, // Replace with actual data
    };

    fetch("http://127.0.0.1:5000 /addSale", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`, // Include token here
      },
      body: JSON.stringify(salePayload),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status) {
          alert("Sale added successfully!");
          const saleId = data.saleId; // Capture the saleId from the response

          // Now add individual product sales
          const productSalesPayload = selectedProducts.map((product) => ({
            saleId: saleId, // Use the captured saleId
            productId: product.productId,
            unitPrice: product.productSalePrice,
            units: product.units,
            productQuantity: product.quantity,
            total: product.total,
            // others: { name: sr }, // Replace with actual data
          }));

          fetch("http://127.0.0.1:5000 /addSingleProductSale", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("token")}`, // Include token here
            },
            body: JSON.stringify(productSalesPayload),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.status) {
                alert("Products added successfully!");
              } else {
                alert("Error adding products: " + data.log);
                // ----------the section below is responsible for sales route handling---------
                // Fetch products and populate dropdown on page load
                document.addEventListener("DOMContentLoaded", () => {
                  // Elements
                  const productSearch =
                    document.getElementById("productSearch");
                  const productDropdown =
                    document.getElementById("productDropdown");
                  const quantityInput = document.getElementById("quantity");
                  const addProductButton =
                    document.getElementById("addProduct");
                  const selectedProductsTable = document
                    .getElementById("selectedProducts")
                    .querySelector("tbody");
                  const grandTotalElement =
                    document.getElementById("grandTotal");
                  const salesForm = document.getElementById("salesForm");

                  let products = []; // This will store the fetched products
                  let selectedProducts = []; // This will store the selected products for the sale

                  // Fetch products from the backend
                  fetch("http://127.0.0.1:5000 /fetchAllProducts", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
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

                  // Filter products based on search input
                  productSearch.addEventListener("input", () => {
                    const searchTerm = productSearch.value.toLowerCase();
                    const filteredProducts = products.filter((product) =>
                      product.productName.toLowerCase().includes(searchTerm)
                    );
                    populateProductDropdown(filteredProducts);
                  });

                  // Populate quantity field based on selected product
                  productDropdown.addEventListener("change", () => {
                    const selectedProductId = productDropdown.value;
                    const selectedProduct = products.find(
                      (product) => product.productId === selectedProductId
                    );

                    if (selectedProduct) {
                      quantityInput.value = selectedProduct.productQuantity;
                    } else {
                      quantityInput.value = "";
                    }
                  });

                  // Add product to the selected products table
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
                      alert(
                        "You cannot select more than the available quantity."
                      );
                      return;
                    }

                    const total = selectedProduct.productSalePrice * quantity;
                    selectedProducts.push({
                      ...selectedProduct,
                      quantity,
                      total,
                    });

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
                    document.querySelectorAll(".remove").forEach((button) => {
                      button.addEventListener("click", removeProduct);
                    });
                  }

                  // Remove product from the selected products table
                  function removeProduct(event) {
                    const index = event.target.getAttribute("data-index");
                    selectedProducts.splice(index, 1);
                    updateSelectedProductsTable();
                    updateGrandTotal();
                  }

                  // Update the grand total
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
                    const amountPaid = parseInt(
                      document.getElementById("amountPaid").value,
                      10
                    );
                    const paymentType =
                      document.getElementById("paymentType").value;
                    const paymentStatus =
                      document.getElementById("paymentStatus").value;

                    const salePayload = {
                      grandTotal: selectedProducts.reduce(
                        (total, product) => total + product.total,
                        0
                      ),
                      numberOfItemsSold: selectedProducts.length,
                      soldBy: user_name, // Replace with actual data
                      soldTo: soldTo,
                      paymentType: paymentType,
                      paymentStatus: paymentStatus,
                      amountPaid: amountPaid,
                      // others: { userName: user_name }, // Replace with actual data
                    };

                    fetch("http://127.0.0.1:5000 /addSale", {
                      method: "POST",
                      headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem(
                          "token"
                        )}`, // Include token here
                      },
                      body: JSON.stringify(salePayload),
                    })
                      .then((response) => response.json())
                      .then((data) => {
                        if (data.status) {
                          alert("Sale added successfully!");
                          const saleId = data.saleId; // Capture the saleId from the response

                          // Now add individual product sales
                          const productSalesPayload = selectedProducts.map(
                            (product) => ({
                              saleId: saleId, // Use the captured saleId
                              productId: product.productId,
                              unitPrice: product.productSalePrice,
                              units: product.units,
                              productQuantity: product.quantity,
                              total: product.total,
                              // others: { name: user_name }, // Replace with actual data
                            })
                          );

                          fetch("http://127.0.0.1:5000 /addSingleProductSale", {
                            method: "POST",
                            headers: {
                              "Content-Type": "application/json",
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
                            })
                            .catch((error) => console.error("Error:", error));
                        } else {
                          alert("Error adding sale: " + data.log);
                        }
                      })
                      .catch((error) => console.error("Error:", error));
                  });
                });
              }
            })
            .catch((error) => console.error("Error:", error));
        } else {
          alert("Error adding sale: " + data.log);
        }
      })
      .catch((error) => console.error("Error:", error));
  });
});
