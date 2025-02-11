document.addEventListener('DOMContentLoaded', () => {
    const createRoleForm = document.getElementById('createRoleForm');
    const rolesTableBody = document.getElementById('rolesTableBody');

    // Fetch all roles on page load
    fetchAllRoles();

    createRoleForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const role = document.getElementById('role').value;

        const payload = {
            'role':role,
            others: { 'userName': 'camero' }
        };

        fetch('http://127.0.0.1:5000/createRole', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                alert('Role created successfully');
                createRoleForm.reset();
                fetchAllRoles(); // Fetch roles again to update the list
            } else {
                alert('Error creating role: ' + data.log);
            }
        })
        .catch(error => console.error('Error creating role:', error));
    });

    function fetchAllRoles() {
        fetch('http://127.0.0.1:5000/fetchAllRoles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Fetched roles data:', data); // Log fetched data
            if (data.status) {
                displayRoles(data.log); // Use data.log instead of data.roles
            } else {
                alert('Error fetching roles: ' + data.log);
            }
        })
        .catch(error => console.error('Error fetching roles:', error));
    }

    function displayRoles(roles) {
        rolesTableBody.innerHTML = ''; // Clear previous data
        if (roles && roles.length) {
            roles.forEach(role => {
                const row = document.createElement('tr');
                row.innerHTML = `●●●●●
                    <td>${role.roleId}</td>
                    <td>${role.role}</td>
                    <td>${JSON.stringify(role.others)}</td>
                `;
                rolesTableBody.appendChild(row);
            });
        } else {
            console.warn('No roles available to display');
        }
    }
});
