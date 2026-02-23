# Учебные паттерны AI-агентов (Python)

Минимальный учебный проект с базовыми паттернами из книги **Agentic Design Patterns**.
Есть два варианта реализации:
- прямой клиент DeepSeek через OpenAI SDK
- через LangChain

## Архитектура проекта
```
AIProject/
  src/
    agentic/            # паттерны без LangChain
    agentic_lc/         # паттерны с LangChain
  examples/             # сценарии запуска
    demo.py
    demo_langchain.py
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

## Запуск (без LangChain)
```powershell
.\.venv\Scripts\python .\examples\demo.py
```

## Запуск (LangChain)
```powershell
.\.venv\Scripts\python .\examples\demo_langchain.py
```

Если в Windows консоли появляются ошибки кодировки, переключите консоль на UTF-8:
```powershell
chcp 65001
```

## Где смотреть код
- `src\agentic\llm_deepseek.py` — прямой клиент DeepSeek (OpenAI SDK)
- `src\agentic_lc\llm.py` — клиент DeepSeek через LangChain
- `src\agentic\patterns\` — паттерны без LangChain
- `src\agentic_lc\patterns\` — паттерны с LangChain
- `examples\demo.py` — демо без LangChain
- `examples\demo_langchain.py` — демо с LangChain

## Режим заглушки
В проекте есть `src\agentic\llm_stub.py`, можно использовать его вместо реального API при отладке.
