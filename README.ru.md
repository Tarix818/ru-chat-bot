
# ru-chat-bot

![Python 3.11](https://img.shields.io/badge/Python-3.11-blue) ![MIT License](https://img.shields.io/badge/License-MIT-green) [![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red)](https://kvaytg.ru/donate.php?lang=ru)

## 🔍 О проекте

Это модульный чат-бот на базе глубокого обучения, спроектированный для понимания естественного языка и выполнения повседневных задач. В отличие от простых скриптовых ботов, Нейро анализирует намерения пользователя.

### 🚀 Ключевые технологии

Проект построен на современном стеке технологий обработки естественного языка (NLP):

* **Трансформеры (RuBERT):** Для векторизации текста используется модель `rubert-tiny2`, оптимизированная через **ONNX Runtime** для молниеносной работы даже на обычных процессорах.
* **NLU & Intent Classification:** Собственная нейросетевая модель классификации намерений с архитектурой ResNet, определяющая, чего именно хочет пользователь.
* **Semantic Search (DSSM):** Модуль "болталки" (Small Talk) работает на базе векторного поиска **FAISS**, подбирая наиболее подходящие по смыслу ответы.
* **NER (Named Entity Recognition):** Извлечение сущностей для точного прогноза погоды и поиска информации по Википедии.

### 🛠 Основные функции

1. **Погода:** Актуальный прогноз в любом городе России с учётом даты.
2. **Новости:** Свежие заголовки новостей в реальном времени.
3. **Википедия:** Быстрый поиск определений и биографий прямо в чате.
4. **Умный диалог:** Способность поддерживать простую беседу.
5. **Безопасность:** Детектор токсичности для фильтрации нежелательного контента.

## 📚 Использование

### 1. Настройка окружения

Для работы бота создайте в корне проекта файл `.env` и добавьте в него ваши ключи:

```env
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_TOKEN
WEATHER_API_KEY=YOUR_OPENWEATHERMAP_KEY
```

### 2. Запуск бота

Пример реализации Telegram-бота с использованием `aiogram 3.x`:

```python
import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from chat_bot import ChatBot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("chat-bot.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

bot = Bot(
    token=os.getenv("TELEGRAM_BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True)
)

dp = Dispatcher()

chat_bot = ChatBot()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота.")
    await message.answer("Напишите что-нибудь, чтобы начать беседу...")

@dp.message(F.text)
async def handle_text(message: types.Message):
    waiting_msg = await message.answer("Пожалуйста, подождите ⏳")
    response = await chat_bot.handle_message(message.from_user.id, message.text)
    try:
        await waiting_msg.edit_text(response)
    except Exception as e:
        logger.error(f"Ошибка отправки: {e}")

async def on_startup():
    logger.info("Бот успешно запущен и готов к работе.")

async def main():
    dp.startup.register(on_startup)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Ошибка: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("Сессия бота закрыта.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Бот остановлен вручную.")
```

## 📥 Установка

```bash
pip install git+https://github.com/KvaytG/ru-chat-bot.git
```

## 📝 Лицензия

Распространяется по лицензии **[MIT](LICENSE.txt)**.

Проект использует компоненты с открытым исходным кодом. Сведения о лицензиях см. в **[pyproject.toml](pyproject.toml)** и на официальных ресурсах зависимостей.
