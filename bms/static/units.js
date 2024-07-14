document.addEventListener('DOMContentLoaded', () => {
    const createUnitForm = document.getElementById('createUnitForm');
    const fetchAllUnitsBtn = document.getElementById('fetchAllUnitsBtn');
    const fetchUnitForm = document.getElementById('fetchUnitForm');
    const unitsTableBody = document.getElementById('unitsTableBody');

    // Handle create unit form submission
    createUnitForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(createUnitForm);
        const payload = {
            'others':{'username':'iamGonaBeRich'}
        };

        formData.forEach((value, key) => {
            payload[key] = value;
        });

        try {
            const response = await fetch('http://127.0.0.1:5000/createUnit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (data.status) {
                alert('Unit created successfully');
                fetchAllUnits();
            } else {
                alert('Error creating unit: ' + data.log);
            }
        } catch (error) {
            console.error('Error creating unit:', error);
        }
    });

    // Handle fetch all units button click
    fetchAllUnitsBtn.addEventListener('click', fetchAllUnits);

    // Handle fetch unit form submission
    fetchUnitForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(fetchUnitForm);
        const payload = {};

        formData.forEach((value, key) => {
            payload[key] = value;
        });

        try {
            const response = await fetch('http://127.0.0.1:5000/fetchUnit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (data.status) {
                displayUnits([data.log]); // Display the single fetched unit
            } else {
                alert('Error fetching unit: ' + data.log);
            }
        } catch (error) {
            console.error('Error fetching unit:', error);
        }
    });

    // Fetch all units and display them
    async function fetchAllUnits() {
        try {
            const response = await fetch('http://127.0.0.1:5000/fetchAllUnits', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();
            if (data.status) {
                displayUnits(data.log);
            } else {
                alert('Error fetching units: ' + data.log);
            }
        } catch (error) {
            console.error('Error fetching units:', error);
        }
    }

    // Function to display units in the table
    function displayUnits(units) {
        unitsTableBody.innerHTML = ''; // Clear previous data
        units.forEach(unit => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${unit.unitId}</td>
                <td>${unit.unit}</td>
                <td>${unit.others}</td>
            `;
            unitsTableBody.appendChild(row);
        });
    }

    // Initial fetch to populate the unit table
    fetchAllUnits();
});
