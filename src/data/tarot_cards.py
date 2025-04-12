"""
Модуль содержит описание карт Таро Райдера-Уэйта и их значений на русском и английском языках
"""

TAROT_CARDS = {
    "major_arcana": {
        "0": {
            "name": {
                "ru": "Шут",
                "en": "The Fool"
            },
            "meaning": {
                "ru": "Начало нового пути, невинность, спонтанность, свобода, приключения",
                "en": "New beginnings, innocence, spontaneity, freedom, adventure"
            },
            "reversed_meaning": {
                "ru": "Безрассудство, риск, неосторожность, импульсивность",
                "en": "Recklessness, risk, carelessness, impulsiveness"
            },
            "image_path": "images/major/0.jpg"
        },
        "1": {
            "name": {
                "ru": "Маг",
                "en": "The Magician"
            },
            "meaning": {
                "ru": "Сила воли, творчество, мастерство, концентрация, уверенность",
                "en": "Willpower, creativity, skill, concentration, confidence"
            },
            "reversed_meaning": {
                "ru": "Обман, манипуляции, нерешительность, слабость воли",
                "en": "Deception, manipulation, indecision, weakness of will"
            },
            "image_path": "images/major/1.jpg"
        },
        "2": {
            "name": {
                "ru": "Верховная Жрица",
                "en": "The High Priestess"
            },
            "meaning": {
                "ru": "Интуиция, тайны, мудрость, подсознание, духовное знание",
                "en": "Intuition, mysteries, wisdom, subconscious, spiritual knowledge"
            },
            "reversed_meaning": {
                "ru": "Скрытые мотивы, подавленная интуиция, невежество",
                "en": "Hidden motives, suppressed intuition, ignorance"
            },
            "image_path": "images/major/2.jpg"
        },
        "3": {
            "name": {
                "ru": "Императрица",
                "en": "The Empress"
            },
            "meaning": {
                "ru": "Плодородие, изобилие, материнство, творчество, природа",
                "en": "Fertility, abundance, motherhood, creativity, nature"
            },
            "reversed_meaning": {
                "ru": "Зависимость, излишества, бесплодие, пустота",
                "en": "Dependency, excess, infertility, emptiness"
            },
            "image_path": "images/major/3.jpg"
        },
        "4": {
            "name": {
                "ru": "Император",
                "en": "The Emperor"
            },
            "meaning": {
                "ru": "Власть, структура, стабильность, порядок, авторитет",
                "en": "Authority, structure, stability, order, leadership"
            },
            "reversed_meaning": {
                "ru": "Тирания, жесткость, негибкость, злоупотребление властью",
                "en": "Tyranny, rigidity, inflexibility, abuse of power"
            },
            "image_path": "images/major/4.jpg"
        },
        "5": {
            "name": {
                "ru": "Иерофант",
                "en": "The Hierophant"
            },
            "meaning": {
                "ru": "Традиции, духовность, образование, консерватизм, мораль",
                "en": "Tradition, spirituality, education, conservatism, morality"
            },
            "reversed_meaning": {
                "ru": "Догматизм, нетерпимость, отказ от традиций",
                "en": "Dogmatism, intolerance, rejection of tradition"
            },
            "image_path": "images/major/5.jpg"
        },
        "6": {
            "name": {
                "ru": "Влюбленные",
                "en": "The Lovers"
            },
            "meaning": {
                "ru": "Любовь, гармония, отношения, выбор, единство",
                "en": "Love, harmony, relationships, choice, unity"
            },
            "reversed_meaning": {
                "ru": "Дисгармония, неверность, конфликты, нерешительность",
                "en": "Disharmony, infidelity, conflicts, indecision"
            },
            "image_path": "images/major/6.jpg"
        },
        "7": {
            "name": {
                "ru": "Колесница",
                "en": "The Chariot"
            },
            "meaning": {
                "ru": "Победа, контроль, движение, прогресс, воля",
                "en": "Victory, control, movement, progress, willpower"
            },
            "reversed_meaning": {
                "ru": "Поражение, отсутствие контроля, застой",
                "en": "Defeat, lack of control, stagnation"
            },
            "image_path": "images/major/7.jpg"
        },
        "8": {
            "name": {
                "ru": "Сила",
                "en": "Strength"
            },
            "meaning": {
                "ru": "Сила духа, мужество, терпение, сострадание, контроль",
                "en": "Inner strength, courage, patience, compassion, control"
            },
            "reversed_meaning": {
                "ru": "Слабость, страх, неуверенность, отсутствие контроля",
                "en": "Weakness, fear, insecurity, lack of control"
            },
            "image_path": "images/major/8.jpg"
        },
        "9": {
            "name": {
                "ru": "Отшельник",
                "en": "The Hermit"
            },
            "meaning": {
                "ru": "Мудрость, самоанализ, одиночество, поиск истины",
                "en": "Wisdom, introspection, solitude, search for truth"
            },
            "reversed_meaning": {
                "ru": "Изоляция, одиночество, отказ от помощи",
                "en": "Isolation, loneliness, refusal of help"
            },
            "image_path": "images/major/9.jpg"
        },
        "10": {
            "name": {
                "ru": "Колесо Фортуны",
                "en": "Wheel of Fortune"
            },
            "meaning": {
                "ru": "Судьба, перемены, циклы, удача, движение",
                "en": "Destiny, change, cycles, luck, movement"
            },
            "reversed_meaning": {
                "ru": "Неудача, сопротивление переменам, застой",
                "en": "Misfortune, resistance to change, stagnation"
            },
            "image_path": "images/major/10.jpg"
        },
        "11": {
            "name": {
                "ru": "Справедливость",
                "en": "Justice"
            },
            "meaning": {
                "ru": "Баланс, справедливость, правда, закон, карма",
                "en": "Balance, justice, truth, law, karma"
            },
            "reversed_meaning": {
                "ru": "Несправедливость, дисбаланс, нечестность",
                "en": "Injustice, imbalance, dishonesty"
            },
            "image_path": "images/major/11.jpg"
        },
        "12": {
            "name": {
                "ru": "Повешенный",
                "en": "The Hanged Man"
            },
            "meaning": {
                "ru": "Жертва, пауза, новый взгляд, сдача, переоценка",
                "en": "Sacrifice, pause, new perspective, surrender, reevaluation"
            },
            "reversed_meaning": {
                "ru": "Жертва без цели, застой, сопротивление",
                "en": "Sacrifice without purpose, stagnation, resistance"
            },
            "image_path": "images/major/12.jpg"
        },
        "13": {
            "name": {
                "ru": "Смерть",
                "en": "Death"
            },
            "meaning": {
                "ru": "Трансформация, конец, новое начало, изменение",
                "en": "Transformation, end, new beginning, change"
            },
            "reversed_meaning": {
                "ru": "Сопротивление переменам, застой, страх",
                "en": "Resistance to change, stagnation, fear"
            },
            "image_path": "images/major/13.jpg"
        },
        "14": {
            "name": {
                "ru": "Умеренность",
                "en": "Temperance"
            },
            "meaning": {
                "ru": "Баланс, гармония, терпение, умеренность, исцеление",
                "en": "Balance, harmony, patience, moderation, healing"
            },
            "reversed_meaning": {
                "ru": "Дисбаланс, излишества, нетерпение",
                "en": "Imbalance, excess, impatience"
            },
            "image_path": "images/major/14.jpg"
        },
        "15": {
            "name": {
                "ru": "Дьявол",
                "en": "The Devil"
            },
            "meaning": {
                "ru": "Страсть, зависимость, материализм, ограничения",
                "en": "Passion, addiction, materialism, limitations"
            },
            "reversed_meaning": {
                "ru": "Освобождение, преодоление ограничений, контроль",
                "en": "Liberation, overcoming limitations, control"
            },
            "image_path": "images/major/15.jpg"
        },
        "16": {
            "name": {
                "ru": "Башня",
                "en": "The Tower"
            },
            "meaning": {
                "ru": "Внезапные перемены, разрушение, освобождение, откровение",
                "en": "Sudden change, destruction, liberation, revelation"
            },
            "reversed_meaning": {
                "ru": "Сопротивление переменам, избегание правды",
                "en": "Resistance to change, avoiding truth"
            },
            "image_path": "images/major/16.jpg"
        },
        "17": {
            "name": {
                "ru": "Звезда",
                "en": "The Star"
            },
            "meaning": {
                "ru": "Надежда, вера, вдохновение, исцеление, духовность",
                "en": "Hope, faith, inspiration, healing, spirituality"
            },
            "reversed_meaning": {
                "ru": "Отчаяние, потеря веры, разочарование",
                "en": "Despair, loss of faith, disappointment"
            },
            "image_path": "images/major/17.jpg"
        },
        "18": {
            "name": {
                "ru": "Луна",
                "en": "The Moon"
            },
            "meaning": {
                "ru": "Иллюзия, страх, подсознание, интуиция, тайны",
                "en": "Illusion, fear, subconscious, intuition, mysteries"
            },
            "reversed_meaning": {
                "ru": "Ясность, преодоление страхов, правда",
                "en": "Clarity, overcoming fears, truth"
            },
            "image_path": "images/major/18.jpg"
        },
        "19": {
            "name": {
                "ru": "Солнце",
                "en": "The Sun"
            },
            "meaning": {
                "ru": "Радость, успех, счастье, жизненная сила, ясность",
                "en": "Joy, success, happiness, vitality, clarity"
            },
            "reversed_meaning": {
                "ru": "Временные трудности, задержка успеха",
                "en": "Temporary difficulties, delayed success"
            },
            "image_path": "images/major/19.jpg"
        },
        "20": {
            "name": {
                "ru": "Суд",
                "en": "Judgement"
            },
            "meaning": {
                "ru": "Возрождение, призыв, прощение, новое начало",
                "en": "Rebirth, calling, forgiveness, new beginning"
            },
            "reversed_meaning": {
                "ru": "Сожаление, застой, отказ от изменений",
                "en": "Regret, stagnation, refusal to change"
            },
            "image_path": "images/major/20.jpg"
        },
        "21": {
            "name": {
                "ru": "Мир",
                "en": "The World"
            },
            "meaning": {
                "ru": "Завершение, успех, путешествие, целостность, гармония",
                "en": "Completion, success, journey, wholeness, harmony"
            },
            "reversed_meaning": {
                "ru": "Незавершенность, задержка, отсутствие целостности",
                "en": "Incompletion, delay, lack of wholeness"
            },
            "image_path": "images/major/21.jpg"
        }
    },
    "minor_arcana": {
        "wands": {
            "ace": {
                "name": {
                    "ru": "Туз Жезлов",
                    "en": "Ace of Wands"
                },
                "meaning": {
                    "ru": "Новые начинания, творческая энергия, вдохновение, потенциал",
                    "en": "New beginnings, creative energy, inspiration, potential"
                },
                "reversed_meaning": {
                    "ru": "Задержки, отсутствие направления, нерешительность",
                    "en": "Delays, lack of direction, indecision"
                },
                "image_path": "images/minor/wands/ace.jpg"
            },
            "two": {
                "name": {
                    "ru": "Двойка Жезлов",
                    "en": "Two of Wands"
                },
                "meaning": {
                    "ru": "Планирование, принятие решений, баланс, перспективы",
                    "en": "Planning, decision making, balance, perspectives"
                },
                "reversed_meaning": {
                    "ru": "Неуверенность, страх перед будущим, нерешительность",
                    "en": "Uncertainty, fear of future, indecision"
                },
                "image_path": "images/minor/wands/two.jpg"
            },
            "three": {
                "name": {
                    "ru": "Тройка Жезлов",
                    "en": "Three of Wands"
                },
                "meaning": {
                    "ru": "Расширение, рост, прогресс, дальновидность",
                    "en": "Expansion, growth, progress, foresight"
                },
                "reversed_meaning": {
                    "ru": "Задержки, препятствия, отсутствие прогресса",
                    "en": "Delays, obstacles, lack of progress"
                },
                "image_path": "images/minor/wands/three.jpg"
            },
            "four": {
                "name": {
                    "ru": "Четверка Жезлов",
                    "en": "Four of Wands"
                },
                "meaning": {
                    "ru": "Празднование, гармония, стабильность, дом",
                    "en": "Celebration, harmony, stability, home"
                },
                "reversed_meaning": {
                    "ru": "Отсутствие стабильности, переходный период",
                    "en": "Lack of stability, transition period"
                },
                "image_path": "images/minor/wands/four.jpg"
            },
            "five": {
                "name": {
                    "ru": "Пятерка Жезлов",
                    "en": "Five of Wands"
                },
                "meaning": {
                    "ru": "Конкуренция, конфликт, соревнование, вызов",
                    "en": "Competition, conflict, challenge, rivalry"
                },
                "reversed_meaning": {
                    "ru": "Избегание конфликта, сотрудничество, мир",
                    "en": "Avoiding conflict, cooperation, peace"
                },
                "image_path": "images/minor/wands/five.jpg"
            },
            "six": {
                "name": {
                    "ru": "Шестерка Жезлов",
                    "en": "Six of Wands"
                },
                "meaning": {
                    "ru": "Победа, успех, признание, достижения",
                    "en": "Victory, success, recognition, achievement"
                },
                "reversed_meaning": {
                    "ru": "Задержка успеха, отсутствие признания",
                    "en": "Delayed success, lack of recognition"
                },
                "image_path": "images/minor/wands/six.jpg"
            },
            "seven": {
                "name": {
                    "ru": "Семерка Жезлов",
                    "en": "Seven of Wands"
                },
                "meaning": {
                    "ru": "Защита, настойчивость, отстаивание своих позиций",
                    "en": "Defense, persistence, standing your ground"
                },
                "reversed_meaning": {
                    "ru": "Сдача позиций, усталость, отступление",
                    "en": "Giving up, exhaustion, retreat"
                },
                "image_path": "images/minor/wands/seven.jpg"
            },
            "eight": {
                "name": {
                    "ru": "Восьмерка Жезлов",
                    "en": "Eight of Wands"
                },
                "meaning": {
                    "ru": "Быстрое движение, новости, прогресс, изменения",
                    "en": "Rapid movement, news, progress, change"
                },
                "reversed_meaning": {
                    "ru": "Задержки, препятствия, медленный прогресс",
                    "en": "Delays, obstacles, slow progress"
                },
                "image_path": "images/minor/wands/eight.jpg"
            },
            "nine": {
                "name": {
                    "ru": "Девятка Жезлов",
                    "en": "Nine of Wands"
                },
                "meaning": {
                    "ru": "Сила, стойкость, защита, бдительность",
                    "en": "Strength, resilience, protection, vigilance"
                },
                "reversed_meaning": {
                    "ru": "Усталость, слабость, отсутствие защиты",
                    "en": "Exhaustion, weakness, lack of protection"
                },
                "image_path": "images/minor/wands/nine.jpg"
            },
            "ten": {
                "name": {
                    "ru": "Десятка Жезлов",
                    "en": "Ten of Wands"
                },
                "meaning": {
                    "ru": "Бремя, ответственность, давление, достижения",
                    "en": "Burden, responsibility, pressure, achievement"
                },
                "reversed_meaning": {
                    "ru": "Освобождение от бремени, делегирование",
                    "en": "Release from burden, delegation"
                },
                "image_path": "images/minor/wands/ten.jpg"
            },
            "page": {
                "name": {
                    "ru": "Паж Жезлов",
                    "en": "Page of Wands"
                },
                "meaning": {
                    "ru": "Энтузиазм, новости, творчество, исследование",
                    "en": "Enthusiasm, news, creativity, exploration"
                },
                "reversed_meaning": {
                    "ru": "Неуверенность, отсутствие направления",
                    "en": "Uncertainty, lack of direction"
                },
                "image_path": "images/minor/wands/page.jpg"
            },
            "knight": {
                "name": {
                    "ru": "Рыцарь Жезлов",
                    "en": "Knight of Wands"
                },
                "meaning": {
                    "ru": "Действие, приключения, энергия, движение",
                    "en": "Action, adventure, energy, movement"
                },
                "reversed_meaning": {
                    "ru": "Импульсивность, безрассудство, задержки",
                    "en": "Impulsiveness, recklessness, delays"
                },
                "image_path": "images/minor/wands/knight.jpg"
            },
            "queen": {
                "name": {
                    "ru": "Королева Жезлов",
                    "en": "Queen of Wands"
                },
                "meaning": {
                    "ru": "Уверенность, харизма, лидерство, вдохновение",
                    "en": "Confidence, charisma, leadership, inspiration"
                },
                "reversed_meaning": {
                    "ru": "Неуверенность, отсутствие вдохновения",
                    "en": "Insecurity, lack of inspiration"
                },
                "image_path": "images/minor/wands/queen.jpg"
            },
            "king": {
                "name": {
                    "ru": "Король Жезлов",
                    "en": "King of Wands"
                },
                "meaning": {
                    "ru": "Лидерство, предпринимательство, энергия, харизма",
                    "en": "Leadership, entrepreneurship, energy, charisma"
                },
                "reversed_meaning": {
                    "ru": "Тирания, импульсивность, отсутствие контроля",
                    "en": "Tyranny, impulsiveness, lack of control"
                },
                "image_path": "images/minor/wands/king.jpg"
            }
        },
        "cups": {
            "ace": {
                "name": {
                    "ru": "Туз Кубков",
                    "en": "Ace of Cups"
                },
                "meaning": {
                    "ru": "Новые эмоции, любовь, творчество, духовность",
                    "en": "New emotions, love, creativity, spirituality"
                },
                "reversed_meaning": {
                    "ru": "Эмоциональная пустота, потеря чувств",
                    "en": "Emotional emptiness, loss of feelings"
                },
                "image_path": "images/minor/cups/ace.jpg"
            },
            "two": {
                "name": {
                    "ru": "Двойка Кубков",
                    "en": "Two of Cups"
                },
                "meaning": {
                    "ru": "Партнерство, любовь, дружба, гармония",
                    "en": "Partnership, love, friendship, harmony"
                },
                "reversed_meaning": {
                    "ru": "Разрыв, дисгармония, неверность",
                    "en": "Breakup, disharmony, infidelity"
                },
                "image_path": "images/minor/cups/two.jpg"
            },
            "three": {
                "name": {
                    "ru": "Тройка Кубков",
                    "en": "Three of Cups"
                },
                "meaning": {
                    "ru": "Празднование, дружба, радость, изобилие",
                    "en": "Celebration, friendship, joy, abundance"
                },
                "reversed_meaning": {
                    "ru": "Одиночество, изоляция, излишества",
                    "en": "Loneliness, isolation, excess"
                },
                "image_path": "images/minor/cups/three.jpg"
            },
            "four": {
                "name": {
                    "ru": "Четверка Кубков",
                    "en": "Four of Cups"
                },
                "meaning": {
                    "ru": "Апатия, размышления, упущенные возможности",
                    "en": "Apathy, contemplation, missed opportunities"
                },
                "reversed_meaning": {
                    "ru": "Новые возможности, принятие, движение",
                    "en": "New opportunities, acceptance, movement"
                },
                "image_path": "images/minor/cups/four.jpg"
            },
            "five": {
                "name": {
                    "ru": "Пятерка Кубков",
                    "en": "Five of Cups"
                },
                "meaning": {
                    "ru": "Потеря, горе, разочарование, сожаление",
                    "en": "Loss, grief, disappointment, regret"
                },
                "reversed_meaning": {
                    "ru": "Принятие, прощение, движение вперед",
                    "en": "Acceptance, forgiveness, moving forward"
                },
                "image_path": "images/minor/cups/five.jpg"
            },
            "six": {
                "name": {
                    "ru": "Шестерка Кубков",
                    "en": "Six of Cups"
                },
                "meaning": {
                    "ru": "Ностальгия, детство, невинность, радость",
                    "en": "Nostalgia, childhood, innocence, joy"
                },
                "reversed_meaning": {
                    "ru": "Живя в прошлом, неспособность двигаться вперед",
                    "en": "Living in the past, inability to move forward"
                },
                "image_path": "images/minor/cups/six.jpg"
            },
            "seven": {
                "name": {
                    "ru": "Семерка Кубков",
                    "en": "Seven of Cups"
                },
                "meaning": {
                    "ru": "Выбор, иллюзии, мечты, возможности",
                    "en": "Choice, illusions, dreams, possibilities"
                },
                "reversed_meaning": {
                    "ru": "Ясность, принятие решений, реализм",
                    "en": "Clarity, decision making, realism"
                },
                "image_path": "images/minor/cups/seven.jpg"
            },
            "eight": {
                "name": {
                    "ru": "Восьмерка Кубков",
                    "en": "Eight of Cups"
                },
                "meaning": {
                    "ru": "Уход, движение вперед, поиск, изменение",
                    "en": "Departure, moving forward, search, change"
                },
                "reversed_meaning": {
                    "ru": "Застой, страх перемен, избегание",
                    "en": "Stagnation, fear of change, avoidance"
                },
                "image_path": "images/minor/cups/eight.jpg"
            },
            "nine": {
                "name": {
                    "ru": "Девятка Кубков",
                    "en": "Nine of Cups"
                },
                "meaning": {
                    "ru": "Исполнение желаний, удовлетворение, радость",
                    "en": "Wish fulfillment, satisfaction, joy"
                },
                "reversed_meaning": {
                    "ru": "Неудовлетворенность, материализм",
                    "en": "Dissatisfaction, materialism"
                },
                "image_path": "images/minor/cups/nine.jpg"
            },
            "ten": {
                "name": {
                    "ru": "Десятка Кубков",
                    "en": "Ten of Cups"
                },
                "meaning": {
                    "ru": "Гармония, семья, счастье, любовь",
                    "en": "Harmony, family, happiness, love"
                },
                "reversed_meaning": {
                    "ru": "Дисгармония, семейные проблемы",
                    "en": "Disharmony, family problems"
                },
                "image_path": "images/minor/cups/ten.jpg"
            },
            "page": {
                "name": {
                    "ru": "Паж Кубков",
                    "en": "Page of Cups"
                },
                "meaning": {
                    "ru": "Творчество, мечты, интуиция, новые чувства",
                    "en": "Creativity, dreams, intuition, new feelings"
                },
                "reversed_meaning": {
                    "ru": "Эмоциональная незрелость, иллюзии",
                    "en": "Emotional immaturity, illusions"
                },
                "image_path": "images/minor/cups/page.jpg"
            },
            "knight": {
                "name": {
                    "ru": "Рыцарь Кубков",
                    "en": "Knight of Cups"
                },
                "meaning": {
                    "ru": "Романтика, творчество, чувствительность, идеализм",
                    "en": "Romance, creativity, sensitivity, idealism"
                },
                "reversed_meaning": {
                    "ru": "Эмоциональная нестабильность, разочарование",
                    "en": "Emotional instability, disappointment"
                },
                "image_path": "images/minor/cups/knight.jpg"
            },
            "queen": {
                "name": {
                    "ru": "Королева Кубков",
                    "en": "Queen of Cups"
                },
                "meaning": {
                    "ru": "Интуиция, эмоции, забота, сострадание",
                    "en": "Intuition, emotions, care, compassion"
                },
                "reversed_meaning": {
                    "ru": "Эмоциональная нестабильность, зависимость",
                    "en": "Emotional instability, dependency"
                },
                "image_path": "images/minor/cups/queen.jpg"
            },
            "king": {
                "name": {
                    "ru": "Король Кубков",
                    "en": "King of Cups"
                },
                "meaning": {
                    "ru": "Эмоциональная зрелость, мудрость, дипломатия",
                    "en": "Emotional maturity, wisdom, diplomacy"
                },
                "reversed_meaning": {
                    "ru": "Эмоциональная нестабильность, манипуляции",
                    "en": "Emotional instability, manipulation"
                },
                "image_path": "images/minor/cups/king.jpg"
            }
        },
        "swords": {
            "ace": {
                "name": {
                    "ru": "Туз Мечей",
                    "en": "Ace of Swords"
                },
                "meaning": {
                    "ru": "Новые идеи, ясность ума, интеллект, правда",
                    "en": "New ideas, mental clarity, intellect, truth"
                },
                "reversed_meaning": {
                    "ru": "Путаница, неясность, ложь",
                    "en": "Confusion, unclear thinking, lies"
                },
                "image_path": "images/minor/swords/ace.jpg"
            },
            "two": {
                "name": {
                    "ru": "Двойка Мечей",
                    "en": "Two of Swords"
                },
                "meaning": {
                    "ru": "Трудный выбор, баланс, дилемма, компромисс",
                    "en": "Difficult choice, balance, dilemma, compromise"
                },
                "reversed_meaning": {
                    "ru": "Нерешительность, избегание выбора",
                    "en": "Indecision, avoiding choice"
                },
                "image_path": "images/minor/swords/two.jpg"
            },
            "three": {
                "name": {
                    "ru": "Тройка Мечей",
                    "en": "Three of Swords"
                },
                "meaning": {
                    "ru": "Сердечная боль, горе, разрыв, печаль",
                    "en": "Heartbreak, grief, separation, sorrow"
                },
                "reversed_meaning": {
                    "ru": "Исцеление, прощение, движение вперед",
                    "en": "Healing, forgiveness, moving forward"
                },
                "image_path": "images/minor/swords/three.jpg"
            },
            "four": {
                "name": {
                    "ru": "Четверка Мечей",
                    "en": "Four of Swords"
                },
                "meaning": {
                    "ru": "Отдых, восстановление, медитация, покой",
                    "en": "Rest, recovery, meditation, peace"
                },
                "reversed_meaning": {
                    "ru": "Беспокойство, стресс, отсутствие отдыха",
                    "en": "Anxiety, stress, lack of rest"
                },
                "image_path": "images/minor/swords/four.jpg"
            },
            "five": {
                "name": {
                    "ru": "Пятерка Мечей",
                    "en": "Five of Swords"
                },
                "meaning": {
                    "ru": "Конфликт, победа любой ценой, агрессия",
                    "en": "Conflict, victory at any cost, aggression"
                },
                "reversed_meaning": {
                    "ru": "Примирение, компромисс, прощение",
                    "en": "Reconciliation, compromise, forgiveness"
                },
                "image_path": "images/minor/swords/five.jpg"
            },
            "six": {
                "name": {
                    "ru": "Шестерка Мечей",
                    "en": "Six of Swords"
                },
                "meaning": {
                    "ru": "Переход, движение, изменения, исцеление",
                    "en": "Transition, movement, change, healing"
                },
                "reversed_meaning": {
                    "ru": "Застой, сопротивление переменам",
                    "en": "Stagnation, resistance to change"
                },
                "image_path": "images/minor/swords/six.jpg"
            },
            "seven": {
                "name": {
                    "ru": "Семерка Мечей",
                    "en": "Seven of Swords"
                },
                "meaning": {
                    "ru": "Обман, хитрость, стратегия, скрытность",
                    "en": "Deception, cunning, strategy, secrecy"
                },
                "reversed_meaning": {
                    "ru": "Честность, открытость, прямота",
                    "en": "Honesty, openness, directness"
                },
                "image_path": "images/minor/swords/seven.jpg"
            },
            "eight": {
                "name": {
                    "ru": "Восьмерка Мечей",
                    "en": "Eight of Swords"
                },
                "meaning": {
                    "ru": "Ограничения, чувство ловушки, беспомощность",
                    "en": "Restrictions, feeling trapped, helplessness"
                },
                "reversed_meaning": {
                    "ru": "Освобождение, новые перспективы",
                    "en": "Liberation, new perspectives"
                },
                "image_path": "images/minor/swords/eight.jpg"
            },
            "nine": {
                "name": {
                    "ru": "Девятка Мечей",
                    "en": "Nine of Swords"
                },
                "meaning": {
                    "ru": "Тревога, страх, кошмары, беспокойство",
                    "en": "Anxiety, fear, nightmares, worry"
                },
                "reversed_meaning": {
                    "ru": "Надежда, преодоление страхов",
                    "en": "Hope, overcoming fears"
                },
                "image_path": "images/minor/swords/nine.jpg"
            },
            "ten": {
                "name": {
                    "ru": "Десятка Мечей",
                    "en": "Ten of Swords"
                },
                "meaning": {
                    "ru": "Конец, разрушение, новое начало",
                    "en": "End, destruction, new beginning"
                },
                "reversed_meaning": {
                    "ru": "Восстановление, возрождение",
                    "en": "Recovery, rebirth"
                },
                "image_path": "images/minor/swords/ten.jpg"
            },
            "page": {
                "name": {
                    "ru": "Паж Мечей",
                    "en": "Page of Swords"
                },
                "meaning": {
                    "ru": "Любознательность, новые идеи, коммуникация",
                    "en": "Curiosity, new ideas, communication"
                },
                "reversed_meaning": {
                    "ru": "Сплетни, обман, нечестность",
                    "en": "Gossip, deception, dishonesty"
                },
                "image_path": "images/minor/swords/page.jpg"
            },
            "knight": {
                "name": {
                    "ru": "Рыцарь Мечей",
                    "en": "Knight of Swords"
                },
                "meaning": {
                    "ru": "Действие, решительность, интеллект",
                    "en": "Action, determination, intellect"
                },
                "reversed_meaning": {
                    "ru": "Импульсивность, агрессия, необдуманность",
                    "en": "Impulsiveness, aggression, thoughtlessness"
                },
                "image_path": "images/minor/swords/knight.jpg"
            },
            "queen": {
                "name": {
                    "ru": "Королева Мечей",
                    "en": "Queen of Swords"
                },
                "meaning": {
                    "ru": "Ясность, независимость, интеллект",
                    "en": "Clarity, independence, intellect"
                },
                "reversed_meaning": {
                    "ru": "Холодность, жестокость, манипуляции",
                    "en": "Coldness, cruelty, manipulation"
                },
                "image_path": "images/minor/swords/queen.jpg"
            },
            "king": {
                "name": {
                    "ru": "Король Мечей",
                    "en": "King of Swords"
                },
                "meaning": {
                    "ru": "Интеллект, власть, справедливость, логика",
                    "en": "Intellect, authority, justice, logic"
                },
                "reversed_meaning": {
                    "ru": "Манипуляции, жестокость, тирания",
                    "en": "Manipulation, cruelty, tyranny"
                },
                "image_path": "images/minor/swords/king.jpg"
            }
        },
        "pentacles": {
            "ace": {
                "name": {
                    "ru": "Туз Пентаклей",
                    "en": "Ace of Pentacles"
                },
                "meaning": {
                    "ru": "Новые возможности, материальное благополучие, изобилие",
                    "en": "New opportunities, material well-being, abundance"
                },
                "reversed_meaning": {
                    "ru": "Упущенные возможности, финансовые потери",
                    "en": "Missed opportunities, financial losses"
                },
                "image_path": "images/minor/pentacles/ace.jpg"
            },
            "two": {
                "name": {
                    "ru": "Двойка Пентаклей",
                    "en": "Two of Pentacles"
                },
                "meaning": {
                    "ru": "Баланс, адаптация, гибкость, изменения",
                    "en": "Balance, adaptation, flexibility, change"
                },
                "reversed_meaning": {
                    "ru": "Дисбаланс, неорганизованность, стресс",
                    "en": "Imbalance, disorganization, stress"
                },
                "image_path": "images/minor/pentacles/two.jpg"
            },
            "three": {
                "name": {
                    "ru": "Тройка Пентаклей",
                    "en": "Three of Pentacles"
                },
                "meaning": {
                    "ru": "Работа в команде, мастерство, сотрудничество",
                    "en": "Teamwork, mastery, collaboration"
                },
                "reversed_meaning": {
                    "ru": "Отсутствие сотрудничества, некомпетентность",
                    "en": "Lack of cooperation, incompetence"
                },
                "image_path": "images/minor/pentacles/three.jpg"
            },
            "four": {
                "name": {
                    "ru": "Четверка Пентаклей",
                    "en": "Four of Pentacles"
                },
                "meaning": {
                    "ru": "Стабильность, безопасность, консерватизм",
                    "en": "Stability, security, conservatism"
                },
                "reversed_meaning": {
                    "ru": "Жадность, страх потерь, нестабильность",
                    "en": "Greed, fear of loss, instability"
                },
                "image_path": "images/minor/pentacles/four.jpg"
            },
            "five": {
                "name": {
                    "ru": "Пятерка Пентаклей",
                    "en": "Five of Pentacles"
                },
                "meaning": {
                    "ru": "Трудности, бедность, болезнь, изоляция",
                    "en": "Hardship, poverty, illness, isolation"
                },
                "reversed_meaning": {
                    "ru": "Восстановление, помощь, надежда",
                    "en": "Recovery, help, hope"
                },
                "image_path": "images/minor/pentacles/five.jpg"
            },
            "six": {
                "name": {
                    "ru": "Шестерка Пентаклей",
                    "en": "Six of Pentacles"
                },
                "meaning": {
                    "ru": "Щедрость, помощь, благотворительность",
                    "en": "Generosity, help, charity"
                },
                "reversed_meaning": {
                    "ru": "Жадность, эгоизм, несправедливость",
                    "en": "Greed, selfishness, injustice"
                },
                "image_path": "images/minor/pentacles/six.jpg"
            },
            "seven": {
                "name": {
                    "ru": "Семерка Пентаклей",
                    "en": "Seven of Pentacles"
                },
                "meaning": {
                    "ru": "Терпение, ожидание, оценка, рост",
                    "en": "Patience, waiting, evaluation, growth"
                },
                "reversed_meaning": {
                    "ru": "Нетерпение, разочарование, потери",
                    "en": "Impatience, disappointment, losses"
                },
                "image_path": "images/minor/pentacles/seven.jpg"
            },
            "eight": {
                "name": {
                    "ru": "Восьмерка Пентаклей",
                    "en": "Eight of Pentacles"
                },
                "meaning": {
                    "ru": "Мастерство, обучение, развитие, работа",
                    "en": "Mastery, learning, development, work"
                },
                "reversed_meaning": {
                    "ru": "Отсутствие прогресса, лень, некомпетентность",
                    "en": "Lack of progress, laziness, incompetence"
                },
                "image_path": "images/minor/pentacles/eight.jpg"
            },
            "nine": {
                "name": {
                    "ru": "Девятка Пентаклей",
                    "en": "Nine of Pentacles"
                },
                "meaning": {
                    "ru": "Благополучие, комфорт, независимость",
                    "en": "Well-being, comfort, independence"
                },
                "reversed_meaning": {
                    "ru": "Зависимость, материальные потери",
                    "en": "Dependency, material losses"
                },
                "image_path": "images/minor/pentacles/nine.jpg"
            },
            "ten": {
                "name": {
                    "ru": "Десятка Пентаклей",
                    "en": "Ten of Pentacles"
                },
                "meaning": {
                    "ru": "Богатство, наследие, семья, стабильность",
                    "en": "Wealth, inheritance, family, stability"
                },
                "reversed_meaning": {
                    "ru": "Финансовые проблемы, семейные конфликты",
                    "en": "Financial problems, family conflicts"
                },
                "image_path": "images/minor/pentacles/ten.jpg"
            },
            "page": {
                "name": {
                    "ru": "Паж Пентаклей",
                    "en": "Page of Pentacles"
                },
                "meaning": {
                    "ru": "Обучение, новые возможности, потенциал",
                    "en": "Learning, new opportunities, potential"
                },
                "reversed_meaning": {
                    "ru": "Отсутствие прогресса, лень, нерешительность",
                    "en": "Lack of progress, laziness, indecision"
                },
                "image_path": "images/minor/pentacles/page.jpg"
            },
            "knight": {
                "name": {
                    "ru": "Рыцарь Пентаклей",
                    "en": "Knight of Pentacles"
                },
                "meaning": {
                    "ru": "Трудолюбие, ответственность, надежность",
                    "en": "Hard work, responsibility, reliability"
                },
                "reversed_meaning": {
                    "ru": "Лень, безответственность, застой",
                    "en": "Laziness, irresponsibility, stagnation"
                },
                "image_path": "images/minor/pentacles/knight.jpg"
            },
            "queen": {
                "name": {
                    "ru": "Королева Пентаклей",
                    "en": "Queen of Pentacles"
                },
                "meaning": {
                    "ru": "Изобилие, практичность, забота, стабильность",
                    "en": "Abundance, practicality, care, stability"
                },
                "reversed_meaning": {
                    "ru": "Материализм, жадность, нестабильность",
                    "en": "Materialism, greed, instability"
                },
                "image_path": "images/minor/pentacles/queen.jpg"
            },
            "king": {
                "name": {
                    "ru": "Король Пентаклей",
                    "en": "King of Pentacles"
                },
                "meaning": {
                    "ru": "Богатство, бизнес, стабильность, безопасность",
                    "en": "Wealth, business, stability, security"
                },
                "reversed_meaning": {
                    "ru": "Жадность, нестабильность, риск",
                    "en": "Greed, instability, risk"
                },
                "image_path": "images/minor/pentacles/king.jpg"
            }
        }
    }
} 