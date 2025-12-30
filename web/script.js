// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Simple animation for numbers in stats
const stats = document.querySelectorAll('.stat-item h3');
stats.forEach(stat => {
    const target = stat.innerText;
    if (target.includes('+') || target === 'Inst') return;

    let count = 0;
    const speed = 2000 / parseInt(target);

    const updateCount = () => {
        if (count < parseInt(target)) {
            count++;
            stat.innerText = count;
            setTimeout(updateCount, speed);
        } else {
            stat.innerText = target;
        }
    }
});

// Sticky header background
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.background = 'rgba(5, 5, 5, 0.95)';
        nav.style.boxShadow = '0 10px 30px rgba(0,0,0,0.5)';
    } else {
        nav.style.background = 'rgba(5, 5, 5, 0.8)';
        nav.style.boxShadow = 'none';
    }
});
