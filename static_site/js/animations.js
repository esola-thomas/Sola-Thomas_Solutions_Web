document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('visible')) {
                // Add a small delay before adding the visible class
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, 100);
            }
        });
    }, {
        threshold: 0.25,  // Trigger when 25% of element is visible
        rootMargin: '-100px 0px'  // Slightly delayed trigger point
    });

    elements.forEach(element => {
        observer.observe(element);
    });
});

// Remove the restrictive scroll boundary control code that was here before
