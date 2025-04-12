document.addEventListener('DOMContentLoaded', () => {
    // Инициализация Telegram WebApp
    let tg = window.Telegram.WebApp;
    tg.expand();

    // Получаем все элементы
    const cards = document.querySelectorAll('.card');
    const continueBtn = document.querySelector('.continue-btn');
    const bgMusic = document.getElementById('bgMusic');
    const soundToggle = document.getElementById('soundToggle');
    let selectedCards = new Set();
    let isMusicPlaying = false;

    // Настройка аудио
    bgMusic.volume = 0.3;
    bgMusic.load();

    // Функция для управления музыкой
    async function toggleMusic() {
        try {
            if (!isMusicPlaying) {
                await bgMusic.play();
                soundToggle.textContent = '🔊';
                soundToggle.classList.add('playing');
                isMusicPlaying = true;
            } else {
                bgMusic.pause();
                soundToggle.textContent = '🔇';
                soundToggle.classList.remove('playing');
                isMusicPlaying = false;
            }
        } catch (error) {
            console.error('Ошибка воспроизведения:', error);
        }
    }

    // Функция для обработки взаимодействия с картой
    function handleCardClick(card) {
        const index = card.getAttribute('data-index');
        
        if (selectedCards.has(index)) {
            selectedCards.delete(index);
            card.classList.remove('selected');
        } else if (selectedCards.size < 3) {
            selectedCards.add(index);
            card.classList.add('selected');
        }

        // Управление видимостью кнопки
        if (selectedCards.size === 3) {
            continueBtn.classList.add('visible');
        } else {
            continueBtn.classList.remove('visible');
        }
    }

    // Обработчик для кнопки звука
    soundToggle.addEventListener('click', (e) => {
        e.stopPropagation(); // Предотвращаем всплытие события
        toggleMusic().catch(error => console.error('Ошибка toggleMusic:', error));
    });

    // Добавляем обработчики для каждой карты
    cards.forEach(card => {
        card.addEventListener('click', () => {
            handleCardClick(card);
        });
    });

    // Обработчик для кнопки продолжить
    continueBtn.addEventListener('click', () => {
        if (selectedCards.size === 3) {
            const selectedIndices = Array.from(selectedCards);
            if (window.Telegram.WebApp) {
                window.Telegram.WebApp.sendData(JSON.stringify({
                    selected_cards: selectedIndices
                }));
                window.Telegram.WebApp.close();
            }
        }
    });
}); 