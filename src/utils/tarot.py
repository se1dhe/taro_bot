"""
Утилиты для работы с картами Таро
"""
import random
import os

def get_random_tarot_cards(count: int = 7) -> list:
    """
    Возвращает список случайных карт Таро
    
    :param count: Количество карт для выбора
    :return: Список карт с их данными
    """
    # Список всех карт
    cards = [
        {
            "name": {"ru": "Маг", "en": "The Magician"},
            "image_path": "images/cups/1.jpg",
            "meaning": {
                "ru": "Творческая сила, мастерство, талант",
                "en": "Creative power, skill, talent"
            }
        },
        {
            "name": {"ru": "Верховная Жрица", "en": "The High Priestess"},
            "image_path": "images/cups/2.jpg",
            "meaning": {
                "ru": "Интуиция, тайны, духовность",
                "en": "Intuition, mystery, spirituality"
            }
        },
        {
            "name": {"ru": "Императрица", "en": "The Empress"},
            "image_path": "images/cups/3.jpg",
            "meaning": {
                "ru": "Плодородие, изобилие, материнство",
                "en": "Fertility, abundance, motherhood"
            }
        },
        {
            "name": {"ru": "Император", "en": "The Emperor"},
            "image_path": "images/cups/4.jpg",
            "meaning": {
                "ru": "Власть, стабильность, авторитет",
                "en": "Authority, stability, leadership"
            }
        },
        {
            "name": {"ru": "Иерофант", "en": "The Hierophant"},
            "image_path": "images/cups/5.jpg",
            "meaning": {
                "ru": "Традиции, обучение, духовное руководство",
                "en": "Tradition, learning, spiritual guidance"
            }
        },
        {
            "name": {"ru": "Влюбленные", "en": "The Lovers"},
            "image_path": "images/cups/6.jpg",
            "meaning": {
                "ru": "Любовь, гармония, выбор",
                "en": "Love, harmony, choices"
            }
        },
        {
            "name": {"ru": "Колесница", "en": "The Chariot"},
            "image_path": "images/cups/7.jpg",
            "meaning": {
                "ru": "Движение вперед, победа, самоконтроль",
                "en": "Forward movement, victory, self-control"
            }
        }
    ]
    
    # Перемешиваем карты
    random.shuffle(cards)
    
    # Возвращаем указанное количество карт
    return cards[:count] 