document.addEventListener('DOMContentLoaded', () => {
    const theme = localStorage.getItem('theme') || 'dark'; // Changed default to dark
    document.documentElement.setAttribute('data-theme', theme);
    
    document.getElementById('theme-toggle').addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Add navbar scroll behavior
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('shrink');
        } else {
            navbar.classList.remove('shrink');
        }
    });
    
    // Initial check for page load
    if (window.scrollY > 50) {
        navbar.classList.add('shrink');
    }

    // Login modal functionality
    const forgotPasswordLink = document.getElementById('forgotPasswordLink');
    const backToLoginBtn = document.getElementById('backToLoginBtn');
    const loginForm = document.getElementById('loginForm');
    const resetPasswordForm = document.getElementById('resetPasswordForm');

    if (forgotPasswordLink && backToLoginBtn && loginForm && resetPasswordForm) {
        // Switch to password reset form
        forgotPasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            loginForm.style.display = 'none';
            resetPasswordForm.style.display = 'block';
        });

        // Switch back to login form
        backToLoginBtn.addEventListener('click', () => {
            resetPasswordForm.style.display = 'none';
            loginForm.style.display = 'block';
        });

        // Form submission handling with validation
        loginForm.addEventListener('submit', (e) => {
            // Client-side validation for login form
            const emailField = document.getElementById('loginEmail');
            const passwordField = document.getElementById('loginPassword');
            let isValid = true;
            
            // Clear previous error messages
            clearValidationErrors();
            
            // Validate email
            if (!emailField.value.trim()) {
                showValidationError(emailField, 'Email is required');
                isValid = false;
            } else if (!isValidEmail(emailField.value)) {
                showValidationError(emailField, 'Please enter a valid email address');
                isValid = false;
            }
            
            // Validate password
            if (!passwordField.value) {
                showValidationError(passwordField, 'Password is required');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault(); // Stop form submission if validation fails
            }
        });

        resetPasswordForm.addEventListener('submit', (e) => {
            // Client-side validation for password reset form
            const resetEmailField = document.getElementById('resetEmail');
            let isValid = true;
            
            // Clear previous error messages
            clearValidationErrors();
            
            // Validate email
            if (!resetEmailField.value.trim()) {
                showValidationError(resetEmailField, 'Email is required');
                isValid = false;
            } else if (!isValidEmail(resetEmailField.value)) {
                showValidationError(resetEmailField, 'Please enter a valid email address');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    }
    
    // Display notification system for messages
    displayNotifications();
    
    // Check if there's any URL parameter indicating an authentication error
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('auth_error')) {
        showNotification('Invalid credentials. Please check your email and password.', 'error');
    } else if (urlParams.has('password_reset_sent')) {
        showNotification('Password reset link has been sent to your email.', 'success');
    } else if (urlParams.has('account_activated')) {
        showNotification('Your account has been successfully activated!', 'success');
    }
    
    // Helper function to validate email format
    function isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
    
    // Helper function to show validation error messages
    function showValidationError(field, message) {
        // Create error element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Add error class to the field
        field.classList.add('is-invalid');
        
        // Insert error message after the field
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    
    // Helper function to clear all validation errors
    function clearValidationErrors() {
        const errorMessages = document.querySelectorAll('.invalid-feedback');
        const invalidFields = document.querySelectorAll('.is-invalid');
        
        errorMessages.forEach(element => {
            element.remove();
        });
        
        invalidFields.forEach(field => {
            field.classList.remove('is-invalid');
        });
    }
    
    // Function to display Django messages passed via context
    function displayNotifications() {
        const messages = document.querySelectorAll('.django-message');
        
        messages.forEach(message => {
            const messageType = message.dataset.type || 'info';
            const messageText = message.textContent;
            
            showNotification(messageText, messageType);
            
            // Remove the element after processing
            message.remove();
        });
    }
    
    // Function to show notifications
    function showNotification(message, type = 'info') {
        // Create notification container if it doesn't exist
        let notificationContainer = document.getElementById('notification-container');
        
        if (!notificationContainer) {
            notificationContainer = document.createElement('div');
            notificationContainer.id = 'notification-container';
            notificationContainer.style.position = 'fixed';
            notificationContainer.style.top = '20px';
            notificationContainer.style.right = '20px';
            notificationContainer.style.zIndex = '1050';
            document.body.appendChild(notificationContainer);
        }
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        notification.role = 'alert';
        
        // Add content
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Add to container
        notificationContainer.appendChild(notification);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 150);
        }, 5000);
    }
    
    // Role-based redirect functionality
    function handleUserRedirect(userData) {
        if (userData && userData.role) {
            switch (userData.role) {
                case 'admin':
                case 'staff':
                    window.location.href = '/portal/admin_dashboard/';
                    break;
                case 'client':
                default:
                    window.location.href = '/portal/dashboard/';
                    break;
            }
        } else {
            // Default redirect if role information is not available
            window.location.href = '/portal/dashboard/';
        }
    }
});
