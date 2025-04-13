/**
 * Main JavaScript file for Aulas Particulares Caio
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    initializeTooltips();
    
    // Setup automatic alert dismissal after 5 seconds
    setupAlertDismissal();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            boundary: document.body
        });
    });
}

/**
 * Setup automatic alert dismissal after 5 seconds
 */
function setupAlertDismissal() {
    var alertList = document.querySelectorAll('.alert:not(.alert-permanent)');
    alertList.forEach(function(alert) {
        setTimeout(function() {
            // Create a bootstrap alert object and close it
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}