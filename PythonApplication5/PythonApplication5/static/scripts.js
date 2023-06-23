document.addEventListener('DOMContentLoaded', function () {
    // Add event listener to the registration form
    var form = document.querySelector('form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        // Collect form data
        var name = document.querySelector('#name').value;
        var email = document.querySelector('#email').value;
        var interests = [];
        var checkboxes = document.querySelectorAll('input[name="interests"]:checked');
        checkboxes.forEach(function (checkbox) {
            interests.push(checkbox.value);
        });

        // Send form data to the server using AJAX
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
            if (xhr.status === 200) {
                // Registration successful
                var response = JSON.parse(xhr.responseText);
                alert(response.message);
                form.reset();
            } else {
                // Registration failed
                alert('Registration failed. Please try again.');
            }
        };
        xhr.send(JSON.stringify({ name: name, email: email, interests: interests }));
    });
});
