document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // WhatsApp link generator
    const generateWhatsAppBtn = document.getElementById('generate-whatsapp');
    if (generateWhatsAppBtn) {
        generateWhatsAppBtn.addEventListener('click', function() {
            const phoneInput = document.getElementById('phone');
            const whatsappInput = document.getElementById('whatsapp');
            
            if (phoneInput && phoneInput.value) {
                // Extract only numbers from the phone field
                const phoneNumber = phoneInput.value.replace(/\D/g, '');
                
                // Create WhatsApp link
                if (phoneNumber) {
                    whatsappInput.value = `https://wa.me/${phoneNumber}`;
                } else {
                    alert('Please enter a valid phone number first');
                }
            } else {
                alert('Please enter a phone number first');
            }
        });
    }

    // Initialize datepickers if present
    const datepickers = document.querySelectorAll('.datepicker');
    if (datepickers.length > 0) {
        datepickers.forEach(function(element) {
            element.addEventListener('focus', function() {
                this.type = 'date';
            });
        });
    }

    // Filter function for tables
    const searchInputs = document.querySelectorAll('.table-search');
    if (searchInputs.length > 0) {
        searchInputs.forEach(function(input) {
            input.addEventListener('keyup', function() {
                const tableId = this.getAttribute('data-table');
                const table = document.getElementById(tableId);
                
                if (table) {
                    const term = this.value.toLowerCase();
                    const rows = table.querySelectorAll('tbody tr');
                    
                    rows.forEach(function(row) {
                        const text = row.textContent.toLowerCase();
                        if (text.indexOf(term) > -1) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    });
                }
            });
        });
    }

    // Handle delete confirmations
    const deleteButtons = document.querySelectorAll('.delete-confirm');
    if (deleteButtons.length > 0) {
        deleteButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                    e.preventDefault();
                }
            });
        });
    }

    // Lesson form validation
    const lessonForm = document.getElementById('lessonForm');
    if (lessonForm) {
        lessonForm.addEventListener('submit', function(e) {
            const startTime = document.getElementById('start_time').value;
            const endTime = document.getElementById('end_time').value;
            
            if (startTime >= endTime) {
                e.preventDefault();
                alert('End time must be after start time');
            }
        });
    }

    // Handle guardian selection in student form
    const studentFormGuardian = document.getElementById('guardian_id');
    const newGuardianButton = document.getElementById('new-guardian-button');
    
    if (studentFormGuardian && newGuardianButton) {
        newGuardianButton.addEventListener('click', function() {
            window.open('/guardians/new', '_blank');
        });
    }

    // Date range picker for reports
    const reportStartDate = document.getElementById('report_start_date');
    const reportEndDate = document.getElementById('report_end_date');
    const applyDateRangeButton = document.getElementById('apply_date_range');
    
    if (reportStartDate && reportEndDate && applyDateRangeButton) {
        applyDateRangeButton.addEventListener('click', function() {
            const startDate = reportStartDate.value;
            const endDate = reportEndDate.value;
            
            if (startDate && endDate) {
                window.location.href = `/reports?start_date=${startDate}&end_date=${endDate}`;
            } else {
                alert('Please select both start and end dates');
            }
        });
    }

    // Date range picker for lessons
    const lessonStartDate = document.getElementById('lesson_start_date');
    const lessonEndDate = document.getElementById('lesson_end_date');
    const applyLessonDateRangeButton = document.getElementById('apply_lesson_date_range');
    
    if (lessonStartDate && lessonEndDate && applyLessonDateRangeButton) {
        applyLessonDateRangeButton.addEventListener('click', function() {
            const startDate = lessonStartDate.value;
            const endDate = lessonEndDate.value;
            
            if (startDate && endDate) {
                window.location.href = `/lessons?start_date=${startDate}&end_date=${endDate}`;
            } else {
                alert('Please select both start and end dates');
            }
        });
    }
});
