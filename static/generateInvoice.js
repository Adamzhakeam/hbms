// Check for token in local storage
const token = localStorage.getItem('token');
if (!token) {
    // Redirect to login page if token is missing
    window.location.href = '../templates/index.html';
}

// Function to verify token and fetch user data
function fetchUserProfile() {
    $.ajax({
        url: 'http://127.0.0.1:5000/profile',
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        success: function(response) {
            if (response.status) {
                // Display user info in the header
                $('#userName').text(`Welcome, ${response.userName}`);
                $('#userRole').text(`Role: ${response.role}`);
            } else {
                // Redirect to login page if token is invalid
                window.location.href = '../static/index.html';
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.error("Error fetching user profile:", textStatus, errorThrown);
            // Redirect to login page if there's an error
            window.location.href = '../static/index.html';
        }
    });
}

// Fetch user profile on page load
$(document).ready(function() {
    fetchUserProfile();

    // Initialize Select2
    $('.searchable-dropdown').select2({
        placeholder: "Search or Add",
        allowClear: true
    });

    // Fetch customers and products
    fetchCustomers();
    fetchProducts();

    // Handle customer dropdown change
    $('#customer').on('change', function() {
        if ($(this).val()) {
            $('#manualCustomer').hide();
            $('#customerName, #customerPhone').val('');
        } else {
            $('#manualCustomer').show();
        }
    });
});

let invoiceItems = [];

function fetchCustomers() {
    $.post('http://127.0.0.1:5000/fetchAllCustomers', function(response) {
        if (response.status && Array.isArray(response.log)) {
            let customerDropdown = $('#customer');
            customerDropdown.empty().append('<option value="">Select Customer or Add New</option>');
            response.log.forEach(customer => {
                customerDropdown.append(`<option value="${customer.customerId}">${customer.customerName} - ${customer.customerPhoneNumber}</option>`);
            });
        } else {
            console.error("Invalid response format from fetchAllCustomers:", response);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.error("Error fetching customers:", textStatus, errorThrown);
    });
}

function fetchProducts() {
    $.post('http://127.0.0.1:5000/fetchAllProducts', function(response) {
        if (response.status && Array.isArray(response.log)) {
            let productDropdown = $('#product');
            productDropdown.empty().append('<option value="">Select Product</option>');
            response.log.forEach(product => {
                productDropdown.append(`<option value="${product.productId}" data-price="${product.productSalePrice}">${product.productName}</option>`);
            });
        } else {
            console.error("Invalid response format from fetchAllProducts:", response);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.error("Error fetching products:", textStatus, errorThrown);
    });
}

function addProduct() {
    let productId = $('#product').val();
    let productName = $('#product option:selected').text();
    let price = parseFloat($('#product option:selected').attr('data-price')) || 0;
    let quantity = parseInt($('#quantity').val()) || 1;

    if (!productId) {
        alert("Please select a product.");
        return;
    }

    let total = price * quantity;

    invoiceItems.push({ productId, productName, quantity, price, total });
    updateInvoiceTable();
}

function updateInvoiceTable() {
    let tbody = $('#invoiceTable tbody');
    tbody.empty();
    let totalAmount = 0;

    invoiceItems.forEach((item, index) => {
        totalAmount += item.total;
        tbody.append(`
            <tr>
                <td>${item.productName}</td>
                <td>${item.quantity}</td>
                <td>${item.price}</td>
                <td>${item.total}</td>
                <td><button onclick="removeItem(${index})">Remove</button></td>
            </tr>
        `);
    });

    $('#totalAmount').text(totalAmount.toFixed(2));
}

function removeItem(index) {
    invoiceItems.splice(index, 1);
    updateInvoiceTable();
}

function generateInvoice() {
    let customer = $('#customer').val();
    let customerName = $('#customerName').val();
    let customerPhone = $('#customerPhone').val();

    // Validate customer input
    if (!customer && (!customerName || !customerPhone)) {
        alert("Please select or enter a customer.");
        return;
    }

    // Validate products
    if (invoiceItems.length === 0) {
        alert("Please add at least one product.");
        return;
    }

    // Prepare invoice data
    let invoiceData = {
        customer: {
            name: customer ? $('#customer option:selected').text().split(' - ')[0] : customerName,
            phone: customer ? $('#customer option:selected').text().split(' - ')[1] : customerPhone
        },
        items: invoiceItems,
        totalAmount: parseFloat($('#totalAmount').text())
    };

    console.log("Invoice Data:", invoiceData); // Debugging

    try {
        // Create a new workbook
        let wb = XLSX.utils.book_new();

        // Combine all data into one sheet
        let data = [
            ["Invoice for:", invoiceData.customer.name || "N/A"], // Title row
            ["Customer Phone:", invoiceData.customer.phone || "N/A"],
            [], // Empty row for spacing
            ["Product", "Quantity", "Price", "Total"]
        ];

        // Add product rows
        invoiceData.items.forEach(item => {
            data.push([item.productName, item.quantity, item.price, item.total]);
        });

        // Add total amount
        data.push([], ["Total Amount", invoiceData.totalAmount]);

        // Convert data to a worksheet
        let ws = XLSX.utils.aoa_to_sheet(data);

        // Add the worksheet to the workbook
        XLSX.utils.book_append_sheet(wb, ws, "Invoice");

        // Generate the invoice file name
        let fileName = `Invoice_${invoiceData.customer.name || "Customer"}_${invoiceData.customer.phone || "NoPhone"}.xlsx`;

        // Generate the Excel file and trigger download
        XLSX.writeFile(wb, fileName);
    } catch (error) {
        console.error("Error generating invoice:", error);
        alert("Error generating invoice. Check console for details.");
    }
}