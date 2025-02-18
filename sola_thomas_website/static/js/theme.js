document.addEventListener('DOMContentLoaded', () => {
    const theme = localStorage.getItem('theme') || 'dark'; // Changed default to dark
    document.documentElement.setAttribute('data-theme', theme);
    
    document.getElementById('theme-toggle').addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
});
