function registerUser(event) {
    event.preventDefault(); // Prevent the form submission
    console.log("Hello")
    const reg_username = document.getElementById('reg_username').value;
    const reg_password = document.getElementById('reg_password').value;

    const formData = new FormData();
    formData.append('reg_username', reg_username);
    formData.append('reg_password', reg_password);

    fetch('/register', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const modal = document.getElementById('myModal');
            const registrationMessage = document.getElementById('registration-message');
            modal.style.display = 'block';
            registrationMessage.textContent = 'Registration completed!';
        } else {
            alert('Registration failed.');
        }
    });
}

function validateForm() {
    // Get the values entered by the user
    const username = document.getElementById('reg_username').value;
    const password = document.getElementById('reg_password').value;

    // Check if username and password are not empty
    if (username.trim() === '' || password.trim() === '') {
        alert('Please enter both username and password.');
        return false; // Prevent form submission
    }

    // If username and password are provided, make a POST request to the '/login' route
    fetch('/login', {
        method: 'POST',
        body: new URLSearchParams({ reg_username: username, reg_password: password }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Login successful'); // You can display a success message
            // You can also redirect the user or perform other actions here
            window.location.href = '/hello';
        } else {
            alert('Invalid login'); // You can display an error message
        }
    });

    return false; // Prevent the default form submission
}

// Close the modal dialog
const closeModal = document.getElementById('closeModal');
closeModal.addEventListener('click', function() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
});

document.addEventListener('DOMContentLoaded', function () {
    const userDropdown = document.getElementById('userDropdown');
    const selectedUserDiv = document.getElementById('selectedUser');
    const searchContainer = document.getElementById('searchContainer');
    let selectedUser = null;

    // Fetch all users when the page loads
    fetch('/search_users')
        .then(response => response.json())
        .then(users => {
            displayAllUsers(users.results);
        })
        .catch(error => console.error('Error:', error));

    function displayAllUsers(users) {
        // Clear previous options
        userDropdown.innerHTML = '';

        // Add a default option
        const defaultOption = document.createElement('option');
        defaultOption.textContent = 'Select a user to get a combined recomendation:';
        userDropdown.appendChild(defaultOption);

        // Add users to the dropdown
        users.forEach(username => {
            const option = document.createElement('option');
            option.textContent = username;
            userDropdown.appendChild(option);
        });

        // Event listener for dropdown change
        userDropdown.addEventListener('change', () => {
            const selectedUsername = userDropdown.value;
            const selectedUser = { username: selectedUsername };
            displaySelectedUser(selectedUser);
        });
    }

    function displaySelectedUser(user) {
        searchContainer.style.display = 'block'; // Show search bar
        selectedUserDiv.style.display = 'block'; // Show selected user info
        selectedUserDiv.innerHTML = `<p>Select a user to get a combined recomendation: ${user.username}</p>`;
        // Add more details here if needed
    }
});

function submitForm() {
    const myDropdown = document.getElementById('myDropdown');
    const selectedUser = myDropdown.value;

    // Create a form dynamically
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/hello2'; // Replace with the actual URL of the new page

    // Create an input field to hold the selected user value
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'selectedUser';
    input.value = selectedUser;

    // Append the input field to the form
    form.appendChild(input);

    // Append the form to the document and submit it
    document.body.appendChild(form);
    form.submit();
}
function backForm() {
    // Create a form dynamically
    window.location.href = '/hello';
}