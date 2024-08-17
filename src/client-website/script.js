document.querySelector('.mail-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Capture form data
    const formData = new FormData(document.getElementById('mailForm'));
    // console.log(formData)

    // Send data to the Flask server
    fetch('http://127.0.0.1:5000/send-email', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Email sent successfully!');
        } else {
            alert('Failed to send email: ' + data.message);
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});
