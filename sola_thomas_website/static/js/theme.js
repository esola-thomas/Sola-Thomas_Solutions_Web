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
            // TODO: Add client-side validation if needed
            
            // TODO: Implement proper form submission
            // This will be handled by Django's authentication system
        });

        resetPasswordForm.addEventListener('submit', (e) => {
            // TODO: Add client-side validation if needed
            
            // TODO: Implement password reset functionality
            // This will be handled by Django's password reset system
        });
    }

    // TODO: Handle login errors and display them to the user
    // TODO: Handle password reset success/error messages
    // TODO: Implement user role checking after successful login
});
