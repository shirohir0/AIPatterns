# Учебные паттерны AI-агентов (LangChain)

Минимальный учебный проект с базовыми паттернами из книги **Agentic Design Patterns**.
Реализация выполнена **только через LangChain** и DeepSeek (OpenAI-compatible API).

## Архитектура проекта
```
AIProject/
  src/
    agentic_lc/         # паттерны на LangChain
    common/             # общие утилиты (логирование, память)
  main.py               # единая точка входа
  .env
  .env.example
  README.md
  requirements.txt
```

## Что есть
- Цепочка промптов (Prompt Chaining)
- Маршрутизация (Routing)
- Использование инструментов (Tool Use)
- Планирование (Planning)
- Рефлексия (Reflection)
- Память (упрощенная)

## Установка
```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## Настройка DeepSeek
Укажите ключ в переменной окружения или в `.env`:
```powershell
DEEPSEEK_API_KEY=YOUR_KEY
```

## Запуск
```powershell
.\.venv\Scripts\python .\main.py
```

Уровень логирования:
```powershell
.\.venv\Scripts\python .\main.py --log-level DEBUG
```

Если в Windows консоли появляются ошибки кодировки, переключите консоль на UTF-8:
```powershell
chcp 65001
```

## Тесты (best practice)
По умолчанию запускаются только unit-тесты.

Unit:
```powershell
.\.venv\Scripts\python -m pytest
```

Integration (реальные запросы в DeepSeek):
```powershell
$env:DEEPSEEK_API_KEY="YOUR_KEY"
.\.venv\Scripts\python -m pytest --run-integration -m integration
```

## Где смотреть код
- `src\agentic_lc\llm.py` — клиент DeepSeek через LangChain
- `src\agentic_lc\patterns\` — паттерны
- `src\agentic_lc\demo.py` — демонстрация
- `src\common\logging_utils.py` — логирование
- `src\common\memory.py` — простая память
- `src\common\safe_eval.py` — безопасный eval
- `main.py` — единый вход
