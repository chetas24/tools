document.addEventListener('DOMContentLoaded', function() {
    // --- Theme Toggle functionality ---
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;
    
    // Apply saved theme preference on load
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
    }
    
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        localStorage.setItem('theme', body.classList.contains('dark-mode') ? 'dark' : 'light');
    });

    // --- Button Loading State (Safe Implementation) ---
    // This will provide visual feedback, then submit the form.
    document.querySelectorAll('.btn-primary').forEach(button => {
        button.addEventListener('click', function(event) {
            // Get the parent form of the clicked button
            const form = this.closest('form');
            if (!form) {
                console.warn("Button not inside a form. Skipping loading state for:", this);
                return;
            }

            // Prevent the default form submission immediately
            event.preventDefault(); 
            
            const originalText = button.innerHTML; // Store original button content
            
            // Set button to loading state
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            button.disabled = true; // Disable to prevent multiple clicks

            // After a short delay, submit the form programmatically
            setTimeout(() => {
                form.submit(); // This line triggers the actual form submission
                // The page will reload after submission, so no need to revert button state here.
            }, 800); // Simulate 0.8 seconds of processing before submitting
        });
    });

    // --- Copy to Clipboard Functionality (for result.html) ---
    const copyButton = document.getElementById('copyOutputBtn');
    if (copyButton) { // Check if the button exists on the current page (i.e., result.html)
        copyButton.addEventListener('click', function() {
            const outputElement = document.querySelector('.output');
            if (outputElement) {
                // Use the Clipboard API for modern browsers
                navigator.clipboard.writeText(outputElement.textContent)
                    .then(() => {
                        // Change button text temporarily to indicate success
                        const originalBtnText = this.innerHTML;
                        this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                        this.classList.add('btn-success'); // Add a success class for visual feedback
                        
                        setTimeout(() => {
                            this.innerHTML = originalBtnText;
                            this.classList.remove('btn-success');
                        }, 1500); // Revert after 1.5 seconds
                    })
                    .catch(err => {
                        console.error('Failed to copy text: ', err);
                        alert('Failed to copy text. Please copy manually.');
                    });
            }
        });
    }
});