// scripts.js - All JavaScript för RightHome Dashboard

// Bostadsdata (exempeldata - ersätt med din riktiga data från CSV)
const properties = [
    { 
        price: 499000, 
        priceKr: 499000, 
        rooms: 3, 
        area: 2267, 
        type: 'house', 
        address: '3410 Siena Way, Vineland, NJ 08361', 
        meta: '3 bedrooms | 3 bathrooms | 2267 sqft · House for sale' 
    },
    { 
        price: 495000, 
        priceKr: 495000, 
        rooms: 3, 
        area: 2286, 
        type: 'house', 
        address: '105 Lucky Fint Dr, Harrington, DE 19952', 
        meta: '3 bedrooms | 3 bathrooms | 2286 sqft · House for sale' 
    },
    { 
        price: 495000, 
        priceKr: 495000, 
        rooms: 3, 
        area: 2286, 
        type: 'house', 
        address: '105 Lucky Fint Dr, Harrington, DE 19952', 
        meta: '3 bedrooms | 3 bathrooms | 2286 sqft · House for sale' 
    },
    { 
        price: 499000, 
        priceKr: 499000, 
        rooms: 3, 
        area: 2267, 
        type: 'house', 
        address: '3410 Siena Way, Vineland, NJ 08361', 
        meta: '3 bedrooms | 3 bathrooms | 2267 sqft · House for sale' 
    },
    { 
        price: 499000, 
        priceKr: 499000, 
        rooms: 3, 
        area: 2267, 
        type: 'house', 
        address: '3410 Siena Way, Vineland, NJ 08361', 
        meta: '3 bedrooms | 3 bathrooms | 2267 sqft · House for sale' 
    },
    { 
        price: 495000, 
        priceKr: 495000, 
        rooms: 3, 
        area: 2286, 
        type: 'house', 
        address: '105 Lucky Fint Dr, Harrington, DE 19952', 
        meta: '3 bedrooms | 3 bathrooms | 2286 sqft · House for sale' 
    }
];

// Globala variabler för filter
let currentBudget = 9500;
let currentSearch = '';
let currentRooms = '0';
let filters = { 
    hyra: false, 
    kopa: false, 
    hus: false, 
    lagenhet: false 
};

// API-konfiguration (för framtida koppling till din CSV-data)
const API_URL = 'http://localhost:5000';

// ========== 1. BUDGET FUNKTIONER ==========
function updateBudget(val) {
    currentBudget = parseInt(val);
    const formatted = currentBudget.toLocaleString('sv-SE') + ' kr';
    const budgetSpan = document.querySelector('.budget-value');
    if (budgetSpan) budgetSpan.textContent = formatted;
    
    // Uppdatera sliderns gradient
    const pct = ((currentBudget - 2000) / (30000 - 2000)) * 100;
    const slider = document.getElementById('budgetSlider');
    if (slider) {
        slider.style.background = `linear-gradient(to right, var(--coral) ${pct}%, var(--border) ${pct}%)`;
    }
    
    filterAndDisplayProperties();
}

// ========== 2. FILTER & DISPLAY FUNKTIONER ==========
function filterAndDisplayProperties() {
    let filtered = [...properties];
    
    // Filtrera på söktext
    if (currentSearch) {
        filtered = filtered.filter(p => 
            p.address.toLowerCase().includes(currentSearch.toLowerCase())
        );
    }
    
    // Filtrera på antal rum
    if (currentRooms !== '0') {
        const minRooms = parseInt(currentRooms);
        filtered = filtered.filter(p => p.rooms >= minRooms);
    }
    
    // Filtrera på hustyp
    if (filters.hus && !filters.lagenhet) {
        filtered = filtered.filter(p => p.type === 'house');
    } else if (filters.lagenhet && !filters.hus) {
        filtered = filtered.filter(p => p.type === 'apartment');
    }
    
    // Filtrera på budget (om priset finns i kr)
    filtered = filtered.filter(p => p.priceKr <= currentBudget);
    
    updateListingsGrid(filtered);
    updateBostaderCount(filtered.length);
    updateStatistics(filtered);
}

function updateListingsGrid(propertiesToShow) {
    const grid = document.getElementById('listingsGrid');
    if (!grid) return;
    
    if (propertiesToShow.length === 0) {
        grid.innerHTML = '<div style="grid-column: span 2; text-align: center; padding: 40px;">Inga bostäder matchar dina kriterier</div>';
        return;
    }
    
    grid.innerHTML = propertiesToShow.map((prop, index) => `
        <div class="property-card" data-id="${index}">
            <div class="property-img">
                <svg viewBox="0 0 200 110" class="house-svg">
                    <rect x="0" y="0" width="200" height="110" fill="#C8D8A8"/>
                    <rect x="0" y="0" width="200" height="60" fill="#B8D0E8"/>
                    <rect x="0" y="75" width="200" height="35" fill="#88A868"/>
                    <rect x="40" y="45" width="120" height="50" fill="#F0EAD8"/>
                    <polygon points="30,48 100,15 170,48" fill="#8A6040"/>
                    <rect x="110" y="60" width="45" height="35" fill="#D8D0C0"/>
                    <rect x="72" y="68" width="20" height="27" fill="#8A6040"/>
                    <rect x="48" y="53" width="16" height="14" fill="#A8C8E8"/>
                    <rect x="136" y="53" width="16" height="14" fill="#A8C8E8"/>
                </svg>
            </div>
            <div class="property-info">
                <div class="property-price">${prop.priceKr.toLocaleString('sv-SE')} kr 
                    <span class="heart-icon" data-saved="false">⊕</span>
                </div>
                <div class="property-meta">${prop.meta}</div>
                <div class="property-addr">${prop.address}</div>
            </div>
        </div>
    `).join('');
    
    attachPropertyCardListeners();
    attachHeartListeners();
}

function updateBostaderCount(count) {
    const countElement = document.getElementById('bostaderCount');
    if (countElement) {
        countElement.innerHTML = `<div class="legend-dot" style="background:#4A7EC7"></div> ${count} bostäder`;
    }
}

function updateStatistics(filteredProperties) {
    // Uppdatera genomsnittspris
    if (filteredProperties.length > 0) {
        const avgPrice = filteredProperties.reduce((sum, p) => sum + p.priceKr, 0) / filteredProperties.length;
        const legendPill = document.querySelector('.legend-pill');
        if (legendPill) {
            legendPill.textContent = `${Math.round(avgPrice).toLocaleString('sv-SE')} kr`;
        }
    }
}

// ========== 3. EVENT LISTENERS ==========
function attachPropertyCardListeners() {
    document.querySelectorAll('.property-card').forEach(card => {
        card.removeEventListener('click', card.cardClickHandler);
        card.cardClickHandler = () => {
            const addr = card.querySelector('.property-addr')?.textContent || 'Okänd adress';
            const price = card.querySelector('.property-price')?.textContent || '';
            alert(`Mer information om:\n${addr}\n${price}`);
        };
        card.addEventListener('click', card.cardClickHandler);
    });
}

function attachHeartListeners() {
    document.querySelectorAll('.heart-icon').forEach(heart => {
        heart.removeEventListener('click', heart.clickHandler);
        heart.clickHandler = (e) => {
            e.stopPropagation();
            const isSaved = heart.getAttribute('data-saved') === 'true';
            if (!isSaved) {
                heart.textContent = '❤️';
                heart.setAttribute('data-saved', 'true');
                heart.style.color = '#E8735A';
                saveToLocalStorage(heart);
            } else {
                heart.textContent = '⊕';
                heart.setAttribute('data-saved', 'false');
                heart.style.color = '';
                removeFromLocalStorage(heart);
            }
        };
        heart.addEventListener('click', heart.clickHandler);
    });
}

// ========== 4. LOCAL STORAGE (Spara favoriter) ==========
function saveToLocalStorage(heart) {
    const card = heart.closest('.property-card');
    const address = card?.querySelector('.property-addr')?.textContent || '';
    let saved = JSON.parse(localStorage.getItem('savedProperties') || '[]');
    if (!saved.includes(address)) {
        saved.push(address);
        localStorage.setItem('savedProperties', JSON.stringify(saved));
    }
}

function removeFromLocalStorage(heart) {
    const card = heart.closest('.property-card');
    const address = card?.querySelector('.property-addr')?.textContent || '';
    let saved = JSON.parse(localStorage.getItem('savedProperties') || '[]');
    saved = saved.filter(a => a !== address);
    localStorage.setItem('savedProperties', JSON.stringify(saved));
}

function loadSavedFavorites() {
    const saved = JSON.parse(localStorage.getItem('savedProperties') || '[]');
    document.querySelectorAll('.property-card').forEach(card => {
        const address = card.querySelector('.property-addr')?.textContent || '';
        const heart = card.querySelector('.heart-icon');
        if (heart && saved.includes(address)) {
            heart.textContent = '❤️';
            heart.setAttribute('data-saved', 'true');
            heart.style.color = '#E8735A';
        }
    });
}

// ========== 5. API-FUNKTIONER (För koppling till din CSV-data) ==========
async function fetchPropertiesFromAPI() {
    try {
        const response = await fetch(`${API_URL}/api/bostader`);
        if (response.ok) {
            const data = await response.json();
            console.log('Hämtade bostäder från API:', data.length);
            return data;
        }
    } catch (error) {
        console.log('API ej tillgänglig, använder lokal data');
        return null;
    }
    return null;
}

async function fetchStatisticsFromAPI() {
    try {
        const response = await fetch(`${API_URL}/api/statistik`);
        if (response.ok) {
            const stats = await response.json();
            console.log('Statistik från API:', stats);
            return stats;
        }
    } catch (error) {
        console.log('Kunde inte hämta statistik från API');
        return null;
    }
    return null;
}

async function syncFiltersWithAPI() {
    const filterData = {
        max_pris: currentBudget,
        omrade: currentSearch,
        typ: filters.hyra ? 'hyresrätt' : (filters.kopa ? 'bostadsrätt' : null),
        min_boyta: 0,
        rum: currentRooms !== '0' ? parseInt(currentRooms) : null
    };
    
    try {
        const response = await fetch(`${API_URL}/api/filtrera`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filterData)
        });
        if (response.ok) {
            const filtered = await response.json();
            console.log('Filtrerade bostäder från API:', filtered.length);
            return filtered;
        }
    } catch (error) {
        console.log('API-filter ej tillgänglig');
        return null;
    }
    return null;
}

// ========== 6. ALLA UI-EVENT LISTENERS ==========
function setupEventListeners() {
    // Budget slider
    const budgetSlider = document.getElementById('budgetSlider');
    if (budgetSlider) {
        budgetSlider.addEventListener('input', (e) => updateBudget(e.target.value));
    }
    
    // Sökfält - vänster sidebar
    const searchInput = document.getElementById('searchAreaInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            currentSearch = e.target.value;
            filterAndDisplayProperties();
        });
    }
    
    // Sökfält - höger panel (synkar med vänster)
    const rightSearchInput = document.getElementById('rightSearchInput');
    if (rightSearchInput) {
        rightSearchInput.addEventListener('input', (e) => {
            currentSearch = e.target.value;
            const mainSearch = document.getElementById('searchAreaInput');
            if (mainSearch) mainSearch.value = currentSearch;
            filterAndDisplayProperties();
        });
    }
    
    // Checkboxes för hyra/köpa och hus/lägenhet
    const hyraCheck = document.getElementById('hyraCheckbox');
    const kopaCheck = document.getElementById('kopaCheckbox');
    const husCheck = document.getElementById('husCheckbox');
    const lagenhetCheck = document.getElementById('lagenhetCheckbox');
    
    if (hyraCheck) hyraCheck.addEventListener('change', (e) => { 
        filters.hyra = e.target.checked; 
        filterAndDisplayProperties(); 
    });
    if (kopaCheck) kopaCheck.addEventListener('change', (e) => { 
        filters.kopa = e.target.checked; 
        filterAndDisplayProperties(); 
    });
    if (husCheck) husCheck.addEventListener('change', (e) => { 
        filters.hus = e.target.checked; 
        filterAndDisplayProperties(); 
    });
    if (lagenhetCheck) lagenhetCheck.addEventListener('change', (e) => { 
        filters.lagenhet = e.target.checked; 
        filterAndDisplayProperties(); 
    });
    
    // Rum select
    const roomsSelect = document.getElementById('roomsSelect');
    if (roomsSelect) {
        roomsSelect.addEventListener('change', (e) => {
            currentRooms = e.target.value;
            filterAndDisplayProperties();
        });
    }
    
    // Profil - klicka på avatar för att ändra namn
    const avatar = document.getElementById('avatar');
    const userNameSpan = document.getElementById('userName');
    if (avatar && userNameSpan) {
        avatar.addEventListener('click', () => {
            const newName = prompt('Ange ditt fullständiga namn:', userNameSpan.textContent);
            if (newName && newName.trim()) {
                userNameSpan.textContent = newName.trim();
                const initial = newName.trim().charAt(0).toUpperCase();
                avatar.textContent = initial;
                // Spara till localStorage
                localStorage.setItem('userName', userNameSpan.textContent);
                localStorage.setItem('userInitial', avatar.textContent);
            }
        });
        
        // Ladda sparat namn från localStorage
        const savedName = localStorage.getItem('userName');
        const savedInitial = localStorage.getItem('userInitial');
        if (savedName) userNameSpan.textContent = savedName;
        if (savedInitial) avatar.textContent = savedInitial;
    }
    
    // Logga ut knapp
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (confirm('Är du säker på att du vill logga ut?')) {
                alert('Du har loggats ut!');
                if (userNameSpan) userNameSpan.textContent = 'Anna N.';
                if (avatar) avatar.textContent = 'A';
                localStorage.removeItem('userName');
                localStorage.removeItem('userInitial');
            }
        });
    }
    
    // Läs mer-länkar
    document.querySelectorAll('.las-mer-link').forEach(link => {
        link.addEventListener('click', () => {
            const text = link.textContent;
            alert(`Information om: ${text}\n\nDetta avsnitt är under uppbyggnad.`);
        });
    });
    
    // Prispunkter på kartan
    document.querySelectorAll('.map-price-dot').forEach(dot => {
        dot.addEventListener('click', (e) => {
            e.stopPropagation();
            const price = dot.textContent;
            alert(`Bostäder i detta område\nPrisnivå: ${price}\n3 lediga objekt i närheten`);
        });
    });
    
    // Avstånd till - items
    document.querySelectorAll('.avstand-item').forEach(item => {
        item.addEventListener('click', () => {
            const place = item.getAttribute('data-place') || item.querySelector('.avstand-name')?.textContent || '';
            alert(`Avstånd till ${place}:\n5 min promenad\n2 min med cykel\n8 min med buss`);
        });
    });
    
    // Chart badge - random uppdatering var 30e sekund
    const chartBadge = document.getElementById('chartBadge');
    if (chartBadge) {
        setInterval(() => {
            const randomChange = Math.floor(Math.random() * 30) - 5;
            const sign = randomChange >= 0 ? '+' : '';
            chartBadge.textContent = `${sign}${randomChange}%`;
        }, 30000);
    }
}

// ========== 7. INITIERING ==========
async function init() {
    console.log('RightHome Dashboard - Startar...');
    
    // Försök hämta data från API (om tillgängligt)
    const apiData = await fetchPropertiesFromAPI();
    if (apiData && apiData.length > 0) {
        // Uppdatera properties med API-data
        // properties.length = 0;
        // properties.push(...apiData);
        console.log('Data från API laddad');
    }
    
    // Hämta statistik från API
    await fetchStatisticsFromAPI();
    
    // Setup alla event listeners
    setupEventListeners();
    
    // Initial filtrering och display
    updateBudget(9500);
    filterAndDisplayProperties();
    
    // Ladda sparade favoriter
    loadSavedFavorites();
    
    console.log('Dashboard redo!');
}

// Starta allt när sidan laddats
document.addEventListener('DOMContentLoaded', init);