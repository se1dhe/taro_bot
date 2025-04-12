// Инициализация Telegram WebApp
const webApp = window.Telegram.WebApp;
webApp.expand();

// Получение данных от бота
const urlParams = new URLSearchParams(window.location.search);
const cardsData = JSON.parse(urlParams.get('cards') || '[]');

let selectedCards = [];
const MAX_SELECTED_CARDS = 3;

// Создание карт
function createCards() {
    const container = document.querySelector('.cards-container');
    container.innerHTML = '';

    cardsData.forEach((card, index) => {
        const cardElement = document.createElement('div');
        cardElement.className = 'card';
        cardElement.dataset.cardId = index;

        cardElement.innerHTML = `
            <div class="card-inner">
                <div class="card-front">
                    <img src="static/images/back.jpg" alt="Рубашка карты">
                </div>
                <div class="card-back">
                    <img src="static/${card.image_path}" alt="${card.name.ru}">
                </div>
            </div>
        `;

        cardElement.addEventListener('click', () => handleCardClick(cardElement, card));
        container.appendChild(cardElement);
    });
}

// Обработка клика по карте
function handleCardClick(cardElement, card) {
    if (cardElement.classList.contains('flipped')) return;
    if (selectedCards.length >= MAX_SELECTED_CARDS) return;

    cardElement.classList.add('flipped');
    selectedCards.push(card);

    // Добавление выбранной карты в список
    const selectedContainer = document.querySelector('.selected-cards-container');
    const selectedCardElement = document.createElement('div');
    selectedCardElement.className = 'selected-card';
    selectedCardElement.innerHTML = `<img src="static/${card.image_path}" alt="${card.name.ru}">`;
    selectedContainer.appendChild(selectedCardElement);

    // Активация кнопки "Продолжить" при выборе 3 карт
    if (selectedCards.length === MAX_SELECTED_CARDS) {
        document.getElementById('continue-btn').disabled = false;
    }
}

// Обработка нажатия кнопки "Продолжить"
document.getElementById('continue-btn').addEventListener('click', () => {
    if (selectedCards.length === MAX_SELECTED_CARDS) {
        // Отправка данных обратно боту
        webApp.sendData(JSON.stringify({
            selected_cards: selectedCards.map(card => ({
                name: card.name,
                meaning: card.meaning
            }))
        }));
        webApp.close();
    }
});

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    createCards();
}); 