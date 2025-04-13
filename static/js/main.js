// main.js - Custom JavaScript for Flask Application

document.addEventListener('DOMContentLoaded', function() {
    console.log('Flask application loaded successfully');

    // Close alert messages automatically after 5 seconds
    const alertMessages = document.querySelectorAll('.alert');
    
    alertMessages.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add active state to current navigation item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });
});
