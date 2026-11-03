# 🚀 Automation Exercise Test Framework

Профессиональный фреймворк для автоматизированного тестирования UI и API сайта [Automation Exercise](https://automationexercise.com/).

## 🛠 Стек технологий
- **Python 3.10+**
- **Playwright** (UI автоматизация)
- **Requests** (API автоматизация)
- **Pytest** (Тест-раннер, параметризация, фикстуры)
- **Pydantic** (Строгая валидация структур данных и ответов API)
- **Allure** (Формирование подробных HTML-отчетов)
- **GitHub Actions** (CI/CD пайплайн)

## 📂 Структура проекта
```text
├── .github/workflows/    # CI/CD конфигурация (автоматический запуск при push)
├── models/               # Pydantic-модели для валидации API-ответов и тестовых данных
├── pages/                # Page Object Model (POM) для UI-тестов
├── tests/
│   ├── api/              # Интеграционные тесты API
│   └── ui/               # E2E тесты пользовательского интерфейса
├── utils/                # Вспомогательные утилиты (генерация данных)
├── conftest.py           # Глобальные фикстуры Pytest (вкл. requests.Session)
└── requirements.txt      # Зависимости проекта