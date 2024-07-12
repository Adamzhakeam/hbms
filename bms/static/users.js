document.addEventListener('DOMContentLoaded', () => {
    const createUserBtn = document.getElementById('createUserBtn');
    const createUserModal = document.getElementById('createUserModal');
    const closeModal = document.querySelector('.close');
    const createUserForm = document.getElementById('createUserForm');
    const roleSelect = document.getElementById('role');
    const userTableBody = document.getElementById('userTableBody');

    // Fetch all roles and populate dropdown
    fetch('http://127.0.0.1:5000/fetchAllRoles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            data.roles.forEach(role => {
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
        formData.forEach((value, key) => {
            payload[key] = value;
        });

        fetch('http://127.0.0.1:5000/addUser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                alert('User created successfully');
                fetchAllUsers(); // Optional: Implement fetchAllUsers() to update user list
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
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                displayUsers(data.users);
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
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${user.phone}</td>
                <td>${user.role}</td>
            `;
            userTableBody.appendChild(row);
        });
    }

    // Initial fetch to populate the user table
    fetchAllUsers();
});
