document.addEventListener('DOMContentLoaded', () => {
    const creditsTableBody = document.getElementById('creditsTableBody');
    const editModal = document.getElementById('editModal');
    const closeModal = document.querySelector('.close');
    const editCreditForm = document.getElementById('editCreditForm');
    const amountPaidInput = document.getElementById('amountPaid');
    let currentCreditId, currentSaleId, currentAmountInDebt, currentPaymentStatus;

    function fetchCredits() {
        fetch('http://127.0.0.1:5000/fetchAllCredits', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                displayCredits(data.log);
            } else {
                alert('Error fetching credits: ' + data.log);
            }
        })
        .catch(error => console.error('Error fetching credits:', error));
    }

    function displayCredits(credits) {
        creditsTableBody.innerHTML = ''; // Clear previous data
        credits.forEach(credit => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${credit.saleId}</td>
                <td>${credit.soldTo}</td>
                <td>${credit.amountInDebts}</td> <!-- Corrected here -->
                <td>${credit.paymentStatus}</td>
                <td><button class="edit-btn" data-credit-id="${credit.creditId}" data-sale-id="${credit.saleId}" data-amount-in-debt="${credit.amountInDebts}" data-payment-status="${credit.paymentStatus}">Edit</button></td>
            `;
            creditsTableBody.appendChild(row);
        });
        // Attach edit button event listeners
        document.querySelectorAll('.edit-btn').forEach(button => {
            button.addEventListener('click', openEditModal);
        });
    }

    function openEditModal(event) {
        currentCreditId = event.target.dataset.creditId;
        currentSaleId = event.target.dataset.saleId;
        currentAmountInDebt = event.target.dataset.amountInDebts; // Corrected here
        currentPaymentStatus = event.target.dataset.paymentStatus;
        editModal.style.display = 'block';
        document.body.classList.add('blur');
    }

    closeModal.onclick = function() {
        editModal.style.display = 'none';
        document.body.classList.remove('blur');
    };

    window.onclick = function(event) {
        if (event.target === editModal) {
            editModal.style.display = 'none';
            document.body.classList.remove('blur');
        }
    };

    editCreditForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const amountPaid = amountPaidInput.value;
        const payload = {
            creditId: currentCreditId,
            saleId: currentSaleId,
            amountInDebt: currentAmountInDebt, // Ensure this value is correct
            paymentStatus: currentPaymentStatus,
            amountPaid: parseInt(amountPaid)
        };
        editCredit(payload);
    });

    function editCredit(payload) {
        fetch('http://127.0.0.1:5000/editCredit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                alert('Credit updated successfully');
                fetchCredits();
                editModal.style.display = 'none';
                document.body.classList.remove('blur');
            } else {
                alert('Error updating credit: ' + data.log);
            }
        })
        .catch(error => console.error('Error updating credit:', error));
    }

    // Initial fetch
    fetchCredits();
});
