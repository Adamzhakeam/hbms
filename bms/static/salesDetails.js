document.addEventListener('DOMContentLoaded', () => {
    const fetchAllSalesBtn = document.getElementById('fetchAllSalesBtn');
    const fetchSpecificSalesBtn = document.getElementById('fetchSpecificSalesBtn');
    const fetchSalesFromToBtn = document.getElementById('fetchSalesFromToBtn');
    const salesTableBody = document.getElementById('salesTableBody');
    const salesFilterDropdown = document.getElementById('salesFilterDropdown');
    const totalExpectedAmountElem = document.getElementById('totalExpectedAmount');
    const totalAmountPaidElem = document.getElementById('totalAmountPaid');

    // Fetch all sales on page load
    fetchSales('http://127.0.0.1:5000/fetchAllSales');

    // Add event listeners for the buttons
    fetchAllSalesBtn.addEventListener('click', () => {
        fetchSales('http://127.0.0.1:5000/fetchAllSales');
    });

    fetchSpecificSalesBtn.addEventListener('click', () => {
        const saleDate = prompt('Enter specific sale date (YYYY-MM-DD):');
        if (saleDate) {
            fetchSales('http://127.0.0.1:5000/fetchSpecificSales', { saleDate: saleDate });
        }
    });

    fetchSalesFromToBtn.addEventListener('click', () => {
        const dateFrom = prompt('Enter start date (YYYY-MM-DD):');
        const dateTo = prompt('Enter end date (YYYY-MM-DD):');
        if (dateFrom && dateTo) {
            fetchSales('http://127.0.0.1:5000/fetchSpecificSalesFromTo', { dateFrom: dateFrom, dateTo: dateTo });
        }
    });

    // Add event listener for the filter dropdown
    salesFilterDropdown.addEventListener('change', (event) => {
        const filterOption = event.target.value;
        if (filterOption === 'today') {
            const today = new Date().toISOString().split('T')[0];
            fetchSales('http://127.0.0.1:5000/fetchSpecificSales', { saleDate: today });
        } else if (filterOption === 'thisMonth') {
            const date = new Date();
            const year = date.getFullYear();
            const month = ('0' + (date.getMonth() + 1)).slice(-2); // Get month in format MM
            const dateFrom = `${year}-${month}-01`;
            const dateTo = new Date(year, date.getMonth() + 1, 0).toISOString().split('T')[0];
            fetchSales('http://127.0.0.1:5000/fetchSpecificSalesFromTo', { dateFrom: dateFrom, dateTo: dateTo });
        } else {
            fetchSales('http://127.0.0.1:5000/fetchAllSales');
        }
    });

    function fetchSales(endpoint, payload) {
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Fetched sales data:', data);
            if (data.status && data.log) { // Ensure data.log exists and holds the array of sales
                displaySales(data.log);
                calculateTotals(data.log);
            } else {
                alert('Error fetching sales: ' + (data.log || 'Unknown error'));
            }
        })
        .catch(error => console.error('Error fetching sales:', error));
    }

    function displaySales(sales) {
        salesTableBody.innerHTML = ''; // Clear previous data
        sales.forEach(sale => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${sale.soldBy}</td>
                <td>${sale.numberOfItemsSold}</td>
                <td>${sale.grandTotal}</td>
                <td>${sale.amountPaid}</td>
                <td>${sale.paymentType}</td>
                <td>${sale.paymentStatus}</td>
            `;
            salesTableBody.appendChild(row);
        });
    }

    function calculateTotals(sales) {
        let totalExpected = 0;
        let totalPaid = 0;
        sales.forEach(sale => {
            totalExpected += parseFloat(sale.grandTotal);
            totalPaid += parseFloat(sale.amountPaid);
        });
        totalExpectedAmountElem.textContent = `Total Expected Amount: ${totalExpected.toFixed(2)}`;
        totalAmountPaidElem.textContent = `Total Amount Paid: ${totalPaid.toFixed(2)}`;
    }
});
