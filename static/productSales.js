document.addEventListener('DOMContentLoaded', () => {
    const fetchAllSalesBtn = document.getElementById('fetchAllProductSalesBtn');
    const fetchSpecificSalesBtn = document.getElementById('fetchSpecificProductSalesBtn');
    const fetchSalesFromToBtn = document.getElementById('fetchProductSalesFromToBtn');
    const salesTableBody = document.getElementById('salesTableBody');

    fetchAllSalesBtn.addEventListener('click', () => {
        fetchSales('http://127.0.0.1:5000/fetchAllProductSales');
    });

    fetchSpecificSalesBtn.addEventListener('click', () => {
        const saleDate = prompt('Enter specific sale date (YYYY-MM-DD):');
        if (saleDate) {
            fetchSales('http://127.0.0.1:5000/fetchSpecificProductSales', { saleDate: saleDate });
        }
    });

    fetchSalesFromToBtn.addEventListener('click', () => {
        const dateFrom = prompt('Enter start date (YYYY-MM-DD):');
        const dateTo = prompt('Enter end date (YYYY-MM-DD):');
        if (dateFrom && dateTo) {
            fetchSales('http://127.0.0.1:5000/fetchSpecificProductSalesFromTo', { dateFrom: dateFrom, dateTo: dateTo });
        }
    });

    function fetchSales(endpoint, payload) {
        console.log('Fetching sales from endpoint:', endpoint, 'with payload:', payload);
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
            if (data.status) {
                fetchProductNames(data.log);
            } else {
                alert('Error fetching sales: ' + data.log);
            }
        })
        .catch(error => console.error('Error fetching sales:', error));
    }

    function fetchProductNames(sales) {
        const productIds = [...new Set(sales.map(sale => sale.productId))];
        console.log('Product IDs:', productIds); // Debugging log
        Promise.all(productIds.map(productId => 
            fetch('http://127.0.0.1:5000/fetchSpecificProductById', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ productId: productId })
            }).then(response => response.json())
        ))
        .then(productDetails => {
            const productNamesMap = {};
            productDetails.forEach(product => {
                console.log('Product detail response:', product); // Log each product detail response
                if (product.status) {
                    const prod = product.log[0];
                    productNamesMap[prod.productId] = prod.productName; // Map productId to productName
                } else {
                    console.error('Product not found:', product);
                }
            });
            console.log('Product Names Map:', productNamesMap); // Debugging log
            displaySales(sales, productNamesMap);
        })
        .catch(error => console.error('Error fetching product names:', error));
    }

    function displaySales(sales, productNamesMap) {
        salesTableBody.innerHTML = ''; // Clear previous data
        sales.forEach(sale => {
            const productName = productNamesMap[sale.productId] || 'Unknown Product';
            console.log(`Mapping sale product ID ${sale.productId} to product name: ${productName}`); // Log the mapping
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${sale.saleId}</td>
                <td>${productName}</td>
                <td>${sale.unitPrice}</td>
                <td>${sale.quantity}</td>
                <td>${sale.units}</td>
                <td>${sale.total}</td>
                
            `;
            salesTableBody.appendChild(row);
        });
    }
});
