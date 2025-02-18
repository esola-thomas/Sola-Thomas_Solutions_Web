document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(element => {
        observer.observe(element);
    });
});

// Improved scroll boundary control
document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    let lastScroll = 0;

    // Wheel event handler
    document.addEventListener('wheel', function(e) {
        const maxScroll = body.scrollHeight - window.innerHeight;
        const currentScroll = body.scrollTop;

        if ((currentScroll <= 0 && e.deltaY < 0) || 
            (currentScroll >= maxScroll && e.deltaY > 0)) {
            e.preventDefault();
            return false;
        }
    }, { passive: false });

    // Touch event handlers
    document.addEventListener('touchstart', function(e) {
        lastScroll = body.scrollTop;
    }, { passive: true });

    document.addEventListener('touchmove', function(e) {
        const currentScroll = body.scrollTop;
        const maxScroll = body.scrollHeight - window.innerHeight;

        if ((currentScroll <= 0 && currentScroll < lastScroll) || 
            (currentScroll >= maxScroll && currentScroll > lastScroll)) {
            e.preventDefault();
            return false;
        }
    }, { passive: false });
});
