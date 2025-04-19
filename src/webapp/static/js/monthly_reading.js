document.addEventListener('DOMContentLoaded', () => {
    const tg = window.Telegram.WebApp;
    tg.expand();
    tg.ready();

    // Константы
    const MAX_SELECTED_CARDS = 6;
    const TOTAL_CARDS = 16;
    
    // Пути к картам
    const cardImages = [
        // Старшие арканы
        'static/images/major/0.jpg', 'static/images/major/1.jpg', 'static/images/major/2.jpg',
        'static/images/major/3.jpg', 'static/images/major/4.jpg', 'static/images/major/5.jpg',
        'static/images/major/6.jpg', 'static/images/major/7.jpg', 'static/images/major/8.jpg',
        'static/images/major/9.jpg', 'static/images/major/10.jpg', 'static/images/major/11.jpg',
        'static/images/major/12.jpg', 'static/images/major/13.jpg', 'static/images/major/14.jpg',
        'static/images/major/15.jpg', 'static/images/major/16.jpg', 'static/images/major/17.jpg',
        'static/images/major/18.jpg', 'static/images/major/19.jpg', 'static/images/major/20.jpg',
        'static/images/major/21.jpg',
        // Кубки
        'static/images/minor/cups/1.jpg', 'static/images/minor/cups/2.jpg',
        'static/images/minor/cups/3.jpg', 'static/images/minor/cups/4.jpg',
        'static/images/minor/cups/5.jpg', 'static/images/minor/cups/6.jpg',
        'static/images/minor/cups/7.jpg', 'static/images/minor/cups/8.jpg',
        'static/images/minor/cups/9.jpg', 'static/images/minor/cups/10.jpg',
        'static/images/minor/cups/11.jpg', 'static/images/minor/cups/12.jpg',
        'static/images/minor/cups/13.jpg', 'static/images/minor/cups/14.jpg'
    ];

    // Состояние
    const selectedCards = new Set();
    const flippedCards = new Set();
    let currentSelectedCard = null;

    // DOM элементы
    const cards = document.querySelectorAll('.card');
    const continueBtn = document.querySelector('.continue-btn');
    const title = document.querySelector('h1');
    const modal = document.getElementById('resultModal');
    const closeBtn = document.querySelector('.close');
    const modalBody = document.querySelector('.modal-body');

    // Функция для показа модального окна
    function showModal(content) {
        modalBody.innerHTML = content;
        modal.style.display = 'block';
    }

    // Закрытие модального окна
    closeBtn.onclick = () => {
        modal.style.display = 'none';
    };

    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };

    // Перемешивание карт
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    const shuffledCardImages = shuffleArray([...cardImages]).slice(0, TOTAL_CARDS);

    // Обработка клика по карте
    function handleCardClick(card) {
        const index = card.getAttribute('data-index');

        if (flippedCards.has(index)) {
            return;
        }

        if (currentSelectedCard !== null) {
            if (currentSelectedCard === index) {
                const cardFront = card.querySelector('.card-front');
                cardFront.style.backgroundImage = `url(${shuffledCardImages[index]})`;
                card.classList.add('flipped');
                flippedCards.add(index);
                currentSelectedCard = null;
                checkContinueButton();
                return;
            }
            const prevCard = document.querySelector(`[data-index="${currentSelectedCard}"]`);
            prevCard.classList.remove('selected');
            selectedCards.delete(currentSelectedCard);
            currentSelectedCard = null;
        }

        if (selectedCards.size < MAX_SELECTED_CARDS && !selectedCards.has(index)) {
            selectedCards.add(index);
            currentSelectedCard = index;
            card.classList.add('selected');
        }

        checkContinueButton();
    }

    // Проверка условий для показа кнопки "Продолжить"
    function checkContinueButton() {
        if (selectedCards.size === MAX_SELECTED_CARDS && flippedCards.size === MAX_SELECTED_CARDS) {
            title.classList.add('hide');
            continueBtn.classList.add('visible');
        } else {
            title.classList.remove('hide');
            continueBtn.classList.remove('visible');
        }
    }

    // Обработчик кнопки "Продолжить"
    continueBtn.addEventListener('click', () => {
        if (selectedCards.size === MAX_SELECTED_CARDS && flippedCards.size === MAX_SELECTED_CARDS) {
            const selectedIndices = Array.from(selectedCards);
            const selectedCardData = selectedIndices.map(index => {
                const path = shuffledCardImages[index];
                // Определяем, перевернута ли карта (случайно)
                const isReversed = Math.random() < 0.5;
                return {
                    path: path,
                    isReversed: isReversed
                };
            });
            
            showModal('Отправка данных...');
            tg.sendData(JSON.stringify(selectedCardData));
            tg.close();
        }
    });

    // Инициализация
    cards.forEach(card => {
        card.addEventListener('click', () => handleCardClick(card));
    });
}); 