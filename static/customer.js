document.addEventListener('DOMContentLoaded', () => {
    const registerCustomerForm = document.getElementById('registerCustomerForm');
    const fetchAllCustomersBtn = document.getElementById('fetchAllCustomersBtn');
    const fetchCustomerForm = document.getElementById('fetchCustomerForm');
    const customersTableBody = document.getElementById('customersTableBody');

    // Handle register customer form submission
    registerCustomerForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(registerCustomerForm);
        const payload = {
            others:{'userName':'changhong'}
        };

        formData.forEach((value, key) => {
            payload[key] = value;
        });

        try {
            const response = await fetch('http://127.0.0.1:5000/registerCustomer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (data.status) {
                alert('Customer registered successfully');
                fetchAllCustomers();
            } else {
                alert('Error registering customer: ' + data.log);
            }
        } catch (error) {
            console.error('Error registering customer:', error);
        }
    });

    // Handle fetch all customers button click
    fetchAllCustomersBtn.addEventListener('click', fetchAllCustomers);

    // Handle fetch customer form submission
    fetchCustomerForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(fetchCustomerForm);
        const payload = {};

        formData.forEach((value, key) => {
            payload[key] = value;
        });

        try {
            const response = await fetch('http://127.0.0.1:5000/fetchSpecificCustomer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (data.status) {
                displayCustomers([data.log]); // Display the single fetched customer
            } else {
                alert('Error fetching customer: ' + data.log);
            }
        } catch (error) {
            console.error('Error fetching customer:', error);
        }
    });

    // Fetch all customers and display them
    async function fetchAllCustomers() {
        try {
            const response = await fetch('http://127.0.0.1:5000/fetchAllCustomers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();
            if (data.status) {
                displayCustomers(data.log);
            } else {
                alert('Error fetching customers: ' + data.log);
            }
        } catch (error) {
            console.error('Error fetching customers:', error);
        }
    }

    // Function to display customers in the table
    function displayCustomers(customers) {
        customersTableBody.innerHTML = ''; // Clear previous data
        customers.forEach(customer => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${customer.customerId}</td>
                <td>${customer.customerName}</td>
                <td>${customer.customerPhoneNumber}</td>
                <td>${customer.customerLocation}</td>
                <td>${customer.others}</td>
            `;
            customersTableBody.appendChild(row);
        });
    }

    // Initial fetch to populate the customer table
    fetchAllCustomers();
});
