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
            // TODO: Implement client-side validation for login form
            // - Check if email/username field is not empty and valid format
            // - Ensure password field is not empty
            // - Display inline validation errors if needed
            
            // TODO: Handle form submission via AJAX (optional)
            // Form will be handled by Django's authentication system by default
        });

        resetPasswordForm.addEventListener('submit', (e) => {
            // TODO: Implement client-side validation for password reset form
            // - Validate email format before submission
            // - Display inline validation errors if needed
            
            // TODO: Consider adding AJAX submission for better UX
            // By default will be handled by Django's password reset system
        });
    }

    // TODO: Implement notification system for login/auth messages
    // - Create a function to display error/success messages
    // - Parse any Django messages from the session
    // - Style messages according to type (error, success, warning)
    
    // TODO: Add role-based redirect functionality after login
    // - Check user permissions from response data
    // - Redirect to appropriate dashboard based on user role
});
