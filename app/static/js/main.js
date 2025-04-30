// Main JavaScript for Sumzap

document.addEventListener('DOMContentLoaded', function() {
    // File input enhancements
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0] ? e.target.files[0].name : 'No file chosen';
            const fileLabel = this.nextElementSibling;
            
            if (fileLabel && fileLabel.classList.contains('custom-file-label')) {
                fileLabel.textContent = fileName;
            }
        });
    });
    
    // Add loading indicator for form submissions
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"]');
            
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            }
        });
    });
}); 
