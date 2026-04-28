# Цифровой Бадди - AI помощник для адаптации новичков

## 🚀 Быстрый старт

### Через Docker (рекомендуется)
```bash
# Запуск
docker-compose up -d --build

# Открыть в браузере
# http://localhost:8501

# Остановка
docker-compose down

# Логи
docker-compose logs -f
```

### Локально
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 🧪 Запуск тестов
```bash
python test_full.py      # Все тесты (33 теста)
python test_tasks.py     # Тесты для задач (6 тестов)
```
**33 теста** покрывают все функции: AI, БД, задачи, интеграцию

## 📖 Описание
AI-чат-бот для поддержки новичков в первые 90 дней работы. Отслеживает настроение, отвечает на вопросы, сигнализирует HR о проблемах.

## 🎯 Функционал

### Для новичков:
- 💬 Чат с AI-бадди
- 😊 Ежедневная проверка настроения
- 📊 История своего настроения
- 📋 Доска заданий с комментариями

### Для HR:
- ➕ Добавление новичков с стартовыми задачами
- 📊 Дашборд со всеми новичками
- 📈 Настроение каждого новичка
- 🚨 Алерты о проблемах
- ✏️ Создание/редактирование задач
- 💬 Просмотр комментариев к задачам

## ⚠️ Важные правила

**ПЕРЕД изменениями:**
1. Запусти тесты: `python test_full.py`
2. Проверь что все проходят

**НИКОГДА не:**
- Удаляй функции без запроса
- Игнорируй падающие тесты

Подробно в [DEVELOPMENT_RULES.md](DEVELOPMENT_RULES.md)

## 🛠 Технологии
- **Frontend:** Streamlit
- **Backend:** Python 3.11
- **AI:** AI Gateway (опционально) + fallback
- **Database:** SQLite
- **Deployment:** Docker + Docker Compose

## 📁 Структура
```
digital-buddy/
├── app.py              # Главное приложение
├── models/ai.py        # AI функции
├── utils/database.py   # Работа с БД
├── test_full.py        # Все автотесты (27 тестов)
├── DEVELOPMENT_RULES.md # Правила разработки
└── README.md          # Этот файл
```

## Docker Commands

### Запуск всех сервисов:
```bash
docker-compose up
```

### Запуск в фоне:
```bash
docker-compose up -d
```

### Остановка:
```bash
docker-compose down
```

### Пересборка:
```bash
docker-compose up --build
```

## 🔧 AI Gateway (опционально)

Используй свою AI модель:
```env
AI_GATEWAY_URL=https://твоя-aigateway.com
AI_GATEWAY_API_KEY=твой-ключ
```

## 🐛 Отладка

```bash
# Логи
docker-compose logs -f

# Перезапуск
docker-compose restart

# Полная пересборка
docker-compose down && docker-compose up -d --build
```

## 📝 Лицензия
Internal use only
