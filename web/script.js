// Initialize AOS
AOS.init({
    duration: 1000,
    offset: 100,
    once: true
});

// Demo Data for Countries (Can be expanded)
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
    { id: 5, name: "Myanmar", code: "MM", prefix: "+95" },
    { id: 10, name: "Egypt", code: "EG", prefix: "+20" },
    { id: 11, name: "Nigeria", code: "NG", prefix: "+234" },
    { id: 16, name: "Brazil", code: "BR", prefix: "+55" },
    { id: 18, name: "Mauritius", code: "MU", prefix: "+230" },
    { id: 20, name: "Colombia", code: "CO", prefix: "+57" }
];

const coverageList = document.getElementById('coverageList');
const searchInput = document.getElementById('countrySearch');

function renderCountries(filter = '') {
    coverageList.innerHTML = '';
    const filtered = countries.filter(c =>
        c.name.toLowerCase().includes(filter.toLowerCase()) ||
        c.id.toString().includes(filter) ||
        c.prefix.includes(filter)
    );

    filtered.forEach(c => {
        const item = document.createElement('div');
        item.className = 'c-item';
        item.setAttribute('data-aos', 'fade-up');
        item.innerHTML = `
            <div class="c-flag">
                <img src="https://flagcdn.com/w80/${c.code.toLowerCase()}.png" alt="${c.name}">
            </div>
            <div class="c-info">
                <span>${c.name}</span>
                <small>${c.prefix} (ID: ${c.id})</small>
            </div>
        `;
        item.onclick = () => window.open('https://t.me/TAWANATELBOT', '_blank');
        coverageList.appendChild(item);
    });
}

searchInput.addEventListener('input', (e) => {
    renderCountries(e.target.value);
});

// Initial Render
renderCountries();

// Sticky Header
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.background = 'rgba(5, 6, 8, 0.9)';
        nav.style.padding = '1rem 0';
    } else {
        nav.style.background = 'transparent';
        nav.style.padding = '1.5rem 0';
    }
});
