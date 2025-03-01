/**
 * Contact page JavaScript functionality
 * Handles form submission feedback and modal interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the message modal if present
    const messageModal = document.getElementById('messageModal');
    if (messageModal) {
        // Check if we should display the modal (determined by server-side template)
        if (messageModal.dataset.showModal === 'true') {
            const bootstrapModal = new bootstrap.Modal(messageModal);
            bootstrapModal.show();
            
            // If this is a success message, reset the form when the modal is closed
            if (messageModal.dataset.messageType === 'success') {
                messageModal.addEventListener('hidden.bs.modal', function() {
                    const contactForm = document.getElementById('contact-form');
                    if (contactForm) {
                        contactForm.reset();
                    }
                });
            }
        }
    }
});
