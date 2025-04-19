// Инициализация Telegram WebApp
window.Telegram.WebApp.ready();

// Отладочная информация
console.log('WebApp initialized');

document.addEventListener('DOMContentLoaded', () => {
    const tg = window.Telegram.WebApp;
    tg.expand();

    // Отладочная информация
    console.log('DOM loaded');

    // Получаем все элементы
    const cards = document.querySelectorAll('.card');
    const continueBtn = document.querySelector('.continue-btn');
    let selectedCards = new Set();
    let flippedCards = new Set();
    let currentSelectedCard = null;

    // Отладочная информация
    console.log('Found cards:', cards.length);

    // Массив путей к изображениям карт
    const cardImages = [
        'static/images/minor/cups/1.jpg',
        'static/images/minor/cups/2.jpg',
        'static/images/minor/cups/3.jpg',
        'static/images/minor/cups/4.jpg',
        'static/images/minor/cups/5.jpg',
        'static/images/minor/cups/6.jpg',
        'static/images/minor/cups/7.jpg'
    ];

    // Перемешиваем карты
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    const shuffledCards = shuffleArray([...cardImages]);

    // Инициализация карт
    cards.forEach((card, index) => {
        card.setAttribute('data-image', shuffledCards[index]);
        card.setAttribute('data-index', index);
    });

    // Функция для обработки клика по карте
    function handleCardClick(card) {
        const index = card.getAttribute('data-index');

        // Если карта уже перевернута, ничего не делаем
        if (flippedCards.has(index)) {
            return;
        }

        // Если есть выбранная карта (не перевернутая)
        if (currentSelectedCard !== null) {
            // Если кликнули по той же карте - переворачиваем её
            if (currentSelectedCard === index) {
                const cardFront = card.querySelector('.card-front');
                cardFront.style.backgroundImage = `url(${shuffledCards[index]})`;
                card.classList.add('flipped');
                flippedCards.add(index);
                currentSelectedCard = null;
                checkContinueButton();
                return;
            }
            // Если кликнули по другой карте - отменяем предыдущий выбор
            const prevCard = document.querySelector(`[data-index="${currentSelectedCard}"]`);
            prevCard.classList.remove('selected');
            selectedCards.delete(currentSelectedCard);
            currentSelectedCard = null;
        }

        // Если можно выбрать новую карту
        if (selectedCards.size < 3 && !selectedCards.has(index)) {
            selectedCards.add(index);
            currentSelectedCard = index;
            card.classList.add('selected');
        }

        checkContinueButton();
    }

    // Добавляем обработчики для каждой карты
    cards.forEach(card => {
        card.addEventListener('click', () => {
            handleCardClick(card);
        });
    });

    // Функция проверки условий для показа кнопки "Продолжить"
    function checkContinueButton() {
        if (selectedCards.size === 3 && flippedCards.size === 3) {
            // Скрываем заголовок
            const title = document.querySelector('h1');
            title.classList.add('hide');

            // Скрываем невыбранные карты
            const selectedCardsArray = Array.from(selectedCards);
            const cardWidth = 70; // Ширина карты
            const gap = 20; // Отступ между картами
            const totalWidth = cardWidth * 3 + gap * 2; // Общая ширина всех карт с отступами
            const startX = -totalWidth / 2 + cardWidth / 2; // Начальная позиция для первой карты

            cards.forEach(card => {
                const index = card.getAttribute('data-index');
                if (!selectedCards.has(index)) {
                    // Плавно скрываем карты
                    card.style.transition = 'opacity 0.3s ease';
                    card.style.opacity = '0';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                } else {
                    // Вычисляем позицию для каждой карты
                    const cardIndex = selectedCardsArray.indexOf(index);
                    const xPosition = startX + (cardWidth + gap) * cardIndex;
                    
                    // Позиционируем карты в линию с плавным переходом
                    card.style.transition = 'all 0.5s ease';
                    card.style.position = 'absolute';
                    card.style.left = '50%';
                    card.style.top = '50%';
                    card.style.transform = `translate(calc(-50% + ${xPosition}px), -50%)`;
                    card.style.zIndex = '10';
                }
            });
            
            // Показываем кнопку
            continueBtn.classList.add('visible');
        } else {
            // Показываем заголовок
            const title = document.querySelector('h1');
            title.classList.remove('hide');

            // Возвращаем карты в исходное положение
            cards.forEach(card => {
                card.style.transition = 'all 0.3s ease';
                card.style.opacity = '1';
                card.style.display = '';
                card.style.position = '';
                card.style.left = '';
                card.style.top = '';
                card.style.transform = '';
                card.style.zIndex = '';
            });
            continueBtn.classList.remove('visible');
        }
    }

    // Обработчик для кнопки продолжить
    continueBtn.addEventListener('click', () => {
        const selectedCardData = Array.from(selectedCards).map(index => {
            const card = document.querySelector(`[data-index="${index}"]`);
            const path = card.getAttribute('data-image');
            console.log('Processing path:', path); // Добавляем отладочный вывод
            const matches = path.match(/(\w+)\/(\w+)\/(\d+)\.jpg$/);
            if (matches) {
                const [_, type, suit, number] = matches;
                return {
                    path: path,
                    suit: suit,
                    number: parseInt(number)
                };
            }
            return null;
        }).filter(card => card !== null);
        
        if (selectedCardData.length === 3) {
            console.log('Sending data:', selectedCardData); // Добавляем отладочный вывод
            const data = JSON.stringify(selectedCardData);
            tg.sendData(data);
            tg.close();
        }
    });

    function showContinueButton() {
        const title = document.querySelector('h1');
        title.classList.add('hide');
        
        const continueBtn = document.querySelector('.continue-btn');
        continueBtn.style.display = 'block';
        setTimeout(() => {
            continueBtn.classList.add('visible');
        }, 50);
    }
}); 