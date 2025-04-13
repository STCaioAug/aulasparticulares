/**
 * Main JavaScript file for the Flask application
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('Application loaded successfully');
  
  // Initialize any components that need JavaScript
  initializeTooltips();
  setupAlertDismissal();
});

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

/**
 * Setup automatic alert dismissal after 5 seconds
 */
function setupAlertDismissal() {
  const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
  
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
}

// Add more JavaScript functionality as needed
