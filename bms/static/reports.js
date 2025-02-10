// Function to convert array of objects to CSV string
function arrayToCsv(array) {
    const headers = Object.keys(array[0]);
    let csvContent = headers.join(',') + '\n';
    
    array.forEach(row => {
        const rowValues = headers.map(header => 
            typeof row[header] === 'string' ? `"${row[header].replace(/"/g, '""')}"` : String(row[header])
        );
        csvContent += rowValues.join(',') + '\n';
    });

    return csvContent;
}

// Function to generate and display CSV
function generateAndDisplayCsv(data) {
    if (!Array.isArray(data) || data.length === 0) {
        alert('No data available to generate CSV.');
        return;
    }

    const csvContent = arrayToCsv(data);

    // Display CSV content in the page
    document.getElementById('reportResult').textContent = csvContent;

    // Add download button
    const downloadBtn = document.createElement('button');
    downloadBtn.textContent = 'Download CSV';
    downloadBtn.onclick = () => downloadCsv(csvContent);
    document.body.appendChild(downloadBtn);
}

// Function to download CSV
function downloadCsv(csvContent) {
    const blob = new Blob([csvContent], {type: 'text/csv;charset=utf-8;'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'sales_report.csv';
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Main function to fetch sales data and generate CSV
async function fetchSales(endpoint, params = {}) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('Fetched data:', data);

        if (data.status) {
            console.log('Data to be processed for CSV:', data.log);
            generateAndDisplayCsv(data.log);
        } else {
            alert('Error fetching data: ' + data.message);
        }
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        alert('An error occurred while fetching data: ' + error.message);
    }
}

// Event listeners
document.getElementById('fetchAllSalesBtn').addEventListener('click', () => {
    fetchSales('http://127.0.0.1:5000 /fetchAllSalesReports');
});

document.getElementById('fetchSpecificDateBtn').addEventListener('click', () => {
    const date = prompt('Enter the date (YYYY-MM-DD):');
    if (date) {
        fetchSales('http://127.0.0.1:5000 /fetchSpecificSalesReports', { saleDate: date });
    }
});

document.getElementById('fetchSalesFromToBtn').addEventListener('click', () => {
    const startDate = prompt('Enter the start date (YYYY-MM-DD):');
    const endDate = prompt('Enter the end date (YYYY-MM-DD):');
    
    if (startDate && endDate) {
        fetchSales('http://127.0.0.1:5000 /fetchSpecificSalesFromToReports', { dateFrom: startDate, dateTo: endDate });
    }
});

document.getElementById('generateCSVBtn').addEventListener('click', () => {
    const dateRange = document.getElementById('dateRangeDropdown').value;
    let endpoint = '';
    let params = {};

    switch (dateRange) {
        case 'today':
            const today = new Date().toISOString().split('T')[0];
            endpoint = 'http://127.0.0.1:5000 /fetchSpecificSalesReports';
            params = { saleDate: today };
            break;
        case 'thisWeek':
            const startOfWeek = getStartOfWeek().toISOString().split('T')[0];
            const endOfWeek = getEndOfWeek().toISOString().split('T')[0];
            endpoint = 'http://127.0.0.1:5000 /fetchSpecificSalesFromToReports';
            params = { dateFrom: startOfWeek, dateTo: endOfWeek };
            break;
        case 'thisMonth':
            const startOfMonth = new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0];
            const endOfMonth = new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).toISOString().split('T')[0];
            endpoint = 'http://127.0.0.1:5000 /fetchSpecificSalesFromToReports';
            params = { dateFrom: startOfMonth, dateTo: endOfMonth };
            break;
    }

    if (endpoint) {
        fetchSales(endpoint, params);
    }
});

// Helper functions
function getStartOfWeek() {
    const today = new Date();
    const firstDay = today.getDate() - today.getDay();
    return new Date(today.setDate(firstDay));
}

function getEndOfWeek() {
    const today = new Date();
    const lastDay = today.getDate() + (6 - today.getDay());
    return new Date(today.setDate(lastDay));
}
