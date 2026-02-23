# Простое демо AI-агентов (LangChain + DeepSeek)

Минимальный проект, чтобы увидеть, как LLM:
- строит цепочки промптов
- выбирает маршрут (routing)
- вызывает инструменты (tool-calling)
- строит план

## Установка
```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## Ключ
Добавь в `.env`:
```
DEEPSEEK_API_KEY=YOUR_KEY
```

## Запуск
```powershell
.\.venv\Scripts\python .\main.py
```
