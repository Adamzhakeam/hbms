const  sideMenu = document.querySelector('aside');
const menuBtn = document.querySelector('#menu_bar');
const closeBtn = document.querySelector('#close_btn');


const themeToggler = document.querySelector('.theme-toggler');



menuBtn.addEventListener('click',()=>{
       sideMenu.style.display = "block"
})
closeBtn.addEventListener('click',()=>{
    sideMenu.style.display = "none"
})

themeToggler.addEventListener('click',()=>{
     document.body.classList.toggle('dark-theme-variables')
     themeToggler.querySelector('span:nth-child(1').classList.toggle('active')
     themeToggler.querySelector('span:nth-child(2').classList.toggle('active')
})
document.addEventListener('DOMContentLoaded', () => {
    fetchTotalSales();
});

// =======this module below responsible for to earnings 

document.addEventListener('DOMContentLoaded', () => {
    fetchTotalAmountPaid();
  });
  
  function fetchTotalAmountPaid() {
    fetch('http://127.0.0.1:5000/fetchAllSales', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            const totalAmountPaid = calculateTotalAmountPaid(data.log);
            updateTotalAmountPaid(totalAmountPaid);
        } else {
            console.error('Failed to fetch sales:', data.log);
            updateTotalAmountPaid(0); // Set to 0 if there's an error or no sales
        }
    })
    .catch(error => {
        console.error('Error fetching sales:', error);
        updateTotalAmountPaid(0); // Set to 0 if there's an error
    });
  }
  
  function calculateTotalAmountPaid(sales) {
    let total = 0;
    sales.forEach(sale => {
        total += parseFloat(sale.amountPaid);
    });
    return total;
  }
  
  function updateTotalAmountPaid(total) {
    const totalAmountPaidElement = document.getElementById('totalAmountPaid');
    totalAmountPaidElement.textContent = `ugx${total.toFixed(2)}`;
  }
//   ----- the number of sales made 
document.addEventListener('DOMContentLoaded', () => {
    fetchTotalSales();
  });
  
  function fetchTotalSales() {
    fetch('http://127.0.0.1:5000/fetchAllSales', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            updateTotalSales(data.log.length);
        } else {
            console.error('Failed to fetch sales:', data.log);
            updateTotalSales(0); // Set to 0 if there's an error or no sales
        }
    })
    .catch(error => {
        console.error('Error fetching sales:', error);
        updateTotalSales(0); // Set to 0 if there's an error
    });
  }
  
  function updateTotalSales(total) {
    const totalSalesElement = document.getElementById('totalNumberOfSale');
    totalSalesElement.textContent = total;
  }
// ------the module is for fetching the total  products sold
document.addEventListener('DOMContentLoaded', () => {
    fetchTotalAmountSold();
  });
  
  function fetchTotalAmountSold() {
    fetch('http://127.0.0.1:5000/fetchAllProductSales', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            const totalAmountSold = calculateTotalAmountSold(data.log);
            updateTotalAmountSold(totalAmountSold);
        } else {
            console.error('Failed to fetch sales:', data.log);
            updateTotalAmountSold(0); // Set to 0 if there's an error or no sales
        }
    })
    .catch(error => {
        console.error('Error fetching sales:', error);
        updateTotalAmountSold(0); // Set to 0 if there's an error
    });
  }
  
  function calculateTotalAmountSold(products) {
    let total = 0;
    products.forEach(product => {
        total += parseInt(product.quantity);
    });
    return total;
  }
  
  function updateTotalAmountSold(total) {
    const totalAmountPaidElement = document.getElementById('totalAmountOfProductsSold');
    totalAmountPaidElement.textContent = `${total.toFixed(2)}`;
  }
//   ==== this module is responsible for fetching total number of products in stock===
document.addEventListener('DOMContentLoaded', () => {
    fetchProductsInStock();
});

function fetchProductsInStock() {
    fetch('http://127.0.0.1:5000/fetchAllProducts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            const totalProductsInStock = calculateTotalProductsInStock(data.log);
            updateTotalProductsInStock(totalProductsInStock);
        } else {
            console.error('Failed to fetch products:', data.log);
            updateTotalProductsInStock(0); // Set to 0 if there's an error or no products
        }
    })
    .catch(error => {
        console.error('Error fetching products:', error);
        updateTotalProductsInStock(0); // Set to 0 if there's an error
    });
}

function calculateTotalProductsInStock(products) {
    let total = 0;
    products.forEach(product => {
        total += parseInt(product.productQuantity, 10); // Ensure productQuantity is parsed as an integer
    });
    return total;
}

function updateTotalProductsInStock(total) {
    const totalAmountPaidElement = document.getElementById('stock');
    totalAmountPaidElement.textContent = `${total.toFixed(2)}`;
}

// --- the code below is for extracting ------products wiith warning stock
document.addEventListener('DOMContentLoaded', () => {
    fetchProductsWithWarningStock();
  });
  
  function fetchProductsWithWarningStock() {
    fetch('http://127.0.0.1:5000/fetchAllProductsWithWarningStock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            updateTotalProductsWithWarningStock(data.log.length);
        } else {
            console.error('Failed to fetch products:', data.log);
            updateTotalProductsWithWarningStock(0); // Set to 0 if there's an error or no sales
        }
    })
    .catch(error => {
        console.error('Error fetching sales:', error);
        updateTotalProductsWithWarningStock(0); // Set to 0 if there's an error
    });
  }
  
  function updateTotalProductsWithWarningStock(total) {
    const totalProductsWithWarningStock = document.getElementById('warningStock');
    totalProductsWithWarningStock.textContent = total;
  }

//   ----the code below is responsible for the dshboard table ----
document.addEventListener('DOMContentLoaded', () => {
    fetchDebtorsData();
});

function fetchDebtorsData() {
    fetch('http://127.0.0.1:5000/fetchAllUnclearedCredits', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            populateDebtorsTable(data.log);
        } else {
            console.error('Failed to fetch debtors:', data.log);
            populateDebtorsTable([]); // Populate with empty data if there's an error
        }
    })
    .catch(error => {
        console.error('Error fetching debtors:', error);
        populateDebtorsTable([]); // Populate with empty data if there's an error
    });
}

function populateDebtorsTable(debtors) {
    const tableBody = document.querySelector('table tbody');
    tableBody.innerHTML = ''; // Clear existing table rows

    debtors.forEach(debtor => {
        const row = document.createElement('tr');

        const soldToCell = document.createElement('td');
        soldToCell.textContent = debtor.soldTo;
        row.appendChild(soldToCell);

        const soldByCell = document.createElement('td');
        soldByCell.textContent = debtor.soldBy;
        row.appendChild(soldByCell);

        const amountInDebtCell = document.createElement('td');
        amountInDebtCell.textContent = `UGX${debtor.amountInDebts}`;
        row.appendChild(amountInDebtCell);

        const paymentStatusCell = document.createElement('td');
        paymentStatusCell.textContent = debtor.paymentStatus;
        paymentStatusCell.className = getStatusClass(debtor.paymentStatus);
        row.appendChild(paymentStatusCell);

        tableBody.appendChild(row);
    });
}

function getStatusClass(paymentStatus) {
    switch(paymentStatus.toLowerCase()) {
        case 'paid':
            return 'delivered';
        case 'due':
            return 'pending';
        case 'return':
            return 'return';
        case 'in progress':
            return 'inProgress';
        default:
            return '';
    }
}


