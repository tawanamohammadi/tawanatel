// Initialize AOS
AOS.init({
    duration: 1000,
    offset: 50,
    once: true
});

// Demo Data for Countries
const countries = [
    { id: 172, name: "Iceland", code: "IS", prefix: "+354" },
    { id: 170, name: "Monaco", code: "MC", prefix: "+377" },
    { id: 173, name: "Liechtenstein", code: "LI", prefix: "+423" },
    { id: 169, name: "Faroe Islands", code: "FO", prefix: "+298" },
    { id: 167, name: "Greenland", code: "GL", prefix: "+299" },
    { id: 0, name: "Russia", code: "RU", prefix: "+7" },
    { id: 1, name: "Ukraine", code: "UA", prefix: "+380" },
    { id: 2, name: "Kazakhstan", code: "KZ", prefix: "+77" },
    { id: 6, name: "Indonesia", code: "ID", prefix: "+62" },
    { id: 12, name: "USA", code: "US", prefix: "+1" },
    { id: 15, name: "Vietnam", code: "VN", prefix: "+84" },
    { id: 22, name: "India", code: "IN", prefix: "+91" },
    { id: 3, name: "China", code: "CN", prefix: "+86" },
    { id: 4, name: "Philippines", code: "PH", prefix: "+63" },
    { id: 11, name: "Nigeria", code: "NG", prefix: "+234" },
    { id: 16, name: "Brazil", code: "BR", prefix: "+55" }
];

const coverageList = document.getElementById('coverageList');
const searchInput = document.getElementById('countrySearch');
const mobileToggle = document.getElementById('mobile-toggle');
const mobileMenu = document.getElementById('mobile-menu');

// Mobile Menu logic
mobileToggle.addEventListener('click', () => {
    mobileToggle.classList.toggle('active');
    mobileMenu.classList.toggle('active');
    document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : 'auto';
});

// Close mobile menu on link click
document.querySelectorAll('.mobile-nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        mobileToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        document.body.style.overflow = 'auto';
    });
});

// Render Countries
function renderCountries(filter = '') {
    if (!coverageList) return;
    coverageList.innerHTML = '';
    const filtered = countries.filter(c =>
        c.name.toLowerCase().includes(filter.toLowerCase()) ||
        c.id.toString().includes(filter) ||
        c.prefix.includes(filter)
    );

    filtered.forEach(c => {
        const item = document.createElement('div');
        item.className = 'c-item';
        item.innerHTML = `
            <div class="c-flag">
                <img src="https://flagcdn.com/w80/${c.code.toLowerCase()}.png" alt="${c.name}">
            </div>
            <div class="c-info">
                <span>${c.name}</span>
                <small>${c.prefix}</small>
            </div>
        `;
        item.onclick = () => window.open('https://t.me/TAWANATELBOT', '_blank');
        coverageList.appendChild(item);
    });
}

if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        renderCountries(e.target.value);
    });
}

renderCountries();

// Bottom Nav active state
const bNavItems = document.querySelectorAll('.b-nav-item');
bNavItems.forEach(item => {
    item.addEventListener('click', () => {
        bNavItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');
    });
});

// Sticky Header & Scroll Spy
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.background = 'rgba(5, 6, 8, 0.95)';
        nav.style.padding = '0.7rem 0';
    } else {
        nav.style.background = 'transparent';
        nav.style.padding = '1.2rem 0';
    }
});
