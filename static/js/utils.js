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