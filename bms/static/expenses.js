document.addEventListener("DOMContentLoaded", function () {
    const openBackdropBtn = document.getElementById("open-backdrop");
    const closeBackdropBtn = document.getElementById("close-backdrop");
    const backdrop = document.getElementById("expense-backdrop");
    const expenseForm = document.getElementById("expenseForm");
    const expensesTableBody = document.getElementById("expensesTableBody");
    const totalAmount = parseInt(document.getElementById("totalAmount"));
    const filter = document.getElementById("filter");
    const fetchFilteredBtn = document.getElementById("fetch-filtered");
    const fetchByDateBtn = document.getElementById("fetchByDateBtn");
    const fetchByRangeBtn = document.getElementById("fetchByRangeBtn");

    // Open the form backdrop
    openBackdropBtn.addEventListener("click", () => {
        backdrop.style.display = "flex";
    });

    // Close the form backdrop
    closeBackdropBtn.addEventListener("click", () => {
        backdrop.style.display = "none";
    });

    // Handle form submission
    expenseForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(expenseForm);
        const data = Object.fromEntries(formData.entries());

        fetch('http://127.0.0.1:5000 /createAnExpense', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                alert('Expense added successfully');
                fetchExpenses(); // Refresh expenses after adding a new one
                backdrop.style.display = "none"; // Close the form
                expenseForm.reset(); // Reset form fields
            } else {
                alert(data.log);
            }
        });
    });

    // Fetch expenses (initial and after adding new expenses)
    function fetchExpenses() {
        fetch('http://127.0.0.1:5000 /fetchAllExpense', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                renderExpenses(data.log);
            } else {
                alert(data.log);
            }
        });
    }

    // Render expenses in the table
    function renderExpenses(expenses) {
        expensesTableBody.innerHTML = ''; // Clear existing rows
        let total = 0;
        expenses.forEach(expense => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${expense.dateOfExpense}</td>
                <td>${expense.description}</td>
                <td>${expense.amountSpent}</td>
                <td>${expense.others}</td>
            `;
            expensesTableBody.appendChild(row);
            total += parseFloat(expense.amountSpent); // Accumulate total amount
        });
        totalAmount.textContent = total.toFixed(2); // Update the total amount
    }

    // Fetch filtered expenses based on dropdown selection
    fetchFilteredBtn.addEventListener("click", function () {
        const selectedFilter = filter.value;
        fetch('http://127.0.0.1:5000 /fetchSpecificExpense', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filter: selectedFilter })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                renderExpenses(data.log);
            } else {
                alert(data.log);
            }
        });
    });

    // Fetch expenses by specific date
    fetchByDateBtn.addEventListener("click", function () {
        const specificDate = document.getElementById("specificDate").value;
        if (!specificDate) {
            alert("Please select a specific date");
            return;
        }
        fetch('http://127.0.0.1:5000 /fetchSpecificDateExpenses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ specificDate })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                renderExpenses(data.log);
            } else {
                alert(data.log);
            }
        });
    });

    // Fetch expenses by date range
    fetchByRangeBtn.addEventListener("click", function () {
        const dateFrom = document.getElementById("dateFrom").value;
        const dateTo = document.getElementById("dateTo").value;
        
        if (!dateFrom || !dateTo) {
            alert("Please select both start and end dates");
            return;
        }

        fetch('http://127.0.0.1:5000 /fetchExpensesFromTo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ dateFrom, dateTo })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                renderExpenses(data.log);
            } else {
                alert(data.log);
            }
        });
    });

    // Initial fetch of expenses when the page loads
    fetchExpenses();
});
