// Show/Hide Register and Login Forms
document.getElementById('show-register-form').addEventListener('click', function () {
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('register-container').style.display = 'block';
});

document.getElementById('show-login-form').addEventListener('click', function () {
    document.getElementById('register-container').style.display = 'none';
    document.getElementById('login-container').style.display = 'block';
});

// Handle Login form submission
document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    fetch('/api/user/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.msg === 'Login success') {
                window.location.href = '/dashboard';
            } else {
                alert(data.error || 'Login failed');
            }
        })
        .catch((error) => {
            console.error('Error during login:', error);
            alert('An error occurred during login.');
        });
});

// Handle Register form submission
document.getElementById('register-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    fetch('/api/user/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.msg === 'Registered and logged in successfully') {
                window.location.href = '/dashboard';
            } else {
                alert(data.error || 'Registration failed');
            }
        })
        .catch((error) => {
            console.error('Error during registration:', error);
            alert('An error occurred during registration.');
        });
});
