document.addEventListener('DOMContentLoaded', function() {
    const getMessageButton = document.getElementById('getMessage');
    const apiMessageDiv = document.getElementById('apiMessage');
    
    getMessageButton.addEventListener('click', function() {
        // Show loading state
        apiMessageDiv.style.display = 'block';
        apiMessageDiv.textContent = 'Loading...';
        
        // Fetch message from API
        fetch('/api/hello')
            .then(response => response.json())
            .then(data => {
                apiMessageDiv.textContent = data.message;
            })
            .catch(error => {
                apiMessageDiv.textContent = 'Error: ' + error.message;
            });
    });
});
