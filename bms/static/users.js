document.addEventListener('DOMContentLoaded', () => {
    const createUserBtn = document.getElementById('createUserBtn');
    const createUserModal = document.getElementById('createUserModal');
    const closeModal = document.querySelector('.close');
    const createUserForm = document.getElementById('createUserForm');
    const roleSelect = document.getElementById('roles');
    const userTableBody = document.getElementById('userTableBody');

    // Fetch all roles and populate dropdown
    fetch('http://127.0.0.1:5000/fetchAllRoles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}` // Include token here
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            data.log.forEach(role => {
                const option = document.createElement('option');
                option.value = role.roleId;
                option.textContent = role.role;
                roleSelect.appendChild(option);
            });
        } else {
            alert('Error fetching roles: ' + data.log);
        }
    })
    .catch(error => console.error('Error fetching roles:', error));

    // Show user creation modal on button click
    createUserBtn.addEventListener('click', () => {
        createUserModal.style.display = 'block';
        document.body.classList.add('blur');
    });

    // Close modal when close button or outside modal is clicked
    closeModal.onclick = function() {
        createUserModal.style.display = 'none';
        document.body.classList.remove('blur');
    };

    window.onclick = function(event) {
        if (event.target === createUserModal) {
            createUserModal.style.display = 'none';
            document.body.classList.remove('blur');
        }
    };

    // Handle form submission for creating user
    createUserForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(createUserForm);
        const payload = {};

        // Manually add form data to payload
        formData.forEach((value, key) => {
            payload[key] = value;
        });

        // Add the selected roleId to the payload
        payload['roleId'] = roleSelect.value;

        fetch('http://127.0.0.1:5000/addUser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Include token here
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                alert('User created successfully');
                fetchAllUsers();
                createUserModal.style.display = 'none';
                document.body.classList.remove('blur');
            } else {
                alert('Error creating user: ' + data.log);
            }
        })
        .catch(error => console.error('Error creating user:', error));
    });

    // Function to fetch all users and populate the table
    function fetchAllUsers() {
        fetch('http://127.0.0.1:5000/fetchAllUsers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Include token here
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                displayUsers(data.log); // Updated to data.log
            } else {
                alert('Error fetching users: ' + data.log);
            }
        })
        .catch(error => console.error('Error fetching users:', error));
    }

    // Function to display users in the table
    function displayUsers(users) {
        userTableBody.innerHTML = ''; // Clear previous data
        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.userName}</td>
                <td>${user.email}</td>
                <td>${user.phoneNumber}</td>
                <td id="role_${user.userId}">Loading...</td> <!-- Placeholder for role name -->
            `;
            userTableBody.appendChild(row);

            // Fetch and display role for each user
            fetchRoleById(user.roleId)
            .then(role => {
                const roleCell = document.getElementById(`role_${user.userId}`);
                if (role) {
                    roleCell.textContent = role.role; // Display role name
                } else {
                    roleCell.textContent = 'Role Not Found';
                }
            })
            .catch(error => {
                console.error('Error fetching role details:', error);
                const roleCell = document.getElementById(`role_${user.userId}`);
                roleCell.textContent = 'Error fetching role';
            });
        });
    }

    // Function to fetch role details by roleId
    function fetchRoleById(roleId) {
        return fetch('http://127.0.0.1:5000/fetchRole', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Include token here
            },
            body: JSON.stringify({ roleId: roleId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                return data.log[0]; // Assuming role details are returned as the first element in the list
            } else {
                throw new Error('Role fetch error: ' + data.log);
            }
        })
        .catch(error => {
            console.error('Error fetching role:', error);
            return null;
        });
    }

    // Initial fetch of all users when the page loads
    fetchAllUsers();
});
