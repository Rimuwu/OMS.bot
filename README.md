# OMS.bot

OMS.bot - это Telegram бот, построенный на базе aiogram, который реализует систему One Message System (OMS) для создания интерактивных сцен и страниц. Бот позволяет пользователям взаимодействовать с динамическими интерфейсами через кнопки и текстовые сообщения, управляя состояниями и данными пользователей.

## Функции

- **Интерактивные сцены**: Создание многостраничных интерактивных интерфейсов в одном сообщении.
- **Управление страницами**: Переход между страницами сцены с сохранением состояния.
- **Обработка текста и колбэков**: Поддержка различных типов ввода (числа, время, списки, произвольный текст) и колбэк-кнопок.
- **Сохранение состояния**: Автоматическое сохранение и загрузка сцен из базы данных (опционально).
- **Расширяемая архитектура**: Легкое добавление новых сцен и страниц.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/OMS.bot.git
   cd OMS.bot
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` в корне проекта и добавьте ваш токен Telegram бота:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   ```

## Запуск

Запустите бота командой:
```bash
python main.py
```

Бот будет запущен и начнет опрос Telegram API.

## Структура проекта

```
OMS.bot/
├── main.py                 # Точка входа в приложение
├── requirements.txt        # Зависимости Python
├── .env                    # Переменные окружения (не в репозитории)
├── bot/
│   ├── main.py            # Основная логика бота
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── test.py        # Обработчики команд
│   └── scenes/
│       └── user_task/
│           ├── task_scene.py      # Пример сцены
│           └── channels_page.py   # Пример страницы
├── oms/                    # One Message System
│   ├── __init__.py
│   ├── manager.py          # Менеджер сцен
│   ├── oms_handler.py      # Регистрация обработчиков
│   ├── utils.py            # Вспомогательные функции
│   ├── filters/
│   │   └── scene_filter.py # Фильтры для сцен
│   └── models/
│       ├── scene.py        # Базовый класс Scene
│       ├── page.py         # Базовый класс Page
│       └── json_scene.py   # Загрузчик сцен из JSON
└── images/                 # Статические изображения
    ├── 1.png
    └── 2.png
```

## Использование

### Создание новой сцены

1. Создайте класс сцены, наследующий от `Scene`:
   ```python
   from oms import Scene
   from your_pages import YourPage

   class YourScene(Scene):
       __scene_name__ = 'your-scene'
       __pages__ = [YourPage]
   ```

2. Создайте страницы, наследующие от `Page`:
   ```python
   from oms import Page
   from aiogram.types import Message

   class YourPage(Page):
       __page_name__ = 'your-page'

       async def buttons_worker(self):
           return [{'text': 'Кнопка', 'callback_data': 'callback_type'}]

       @Page.on_callback('callback_type')
       async def handle_callback(self, callback, args):
           await callback.answer("Обработано!")
   ```

3. Зарегистрируйте сцену в обработчике команды:
   ```python
   from bot.main import dp, mainbot
   from oms import scene_manager

   @dp.message(CommandStart())
   async def start(message: Message):
       user_id = message.from_user.id
       scene = scene_manager.create_scene(user_id, YourScene, mainbot)
       await scene.start()
   ```

### Типы обработчиков

- `@Page.on_text(data_type='int')` - обработка целых чисел
- `@Page.on_text(data_type='time')` - обработка времени
- `@Page.on_text(data_type='list', separator=';')` - обработка списков
- `@Page.on_text(data_type='all')` - обработка любого текста
- `@Page.on_callback('type')` - обработка колбэк-кнопок

## Конфигурация

Сцены настраиваются программно через классы. Для использования JSON-конфигурации создайте папку `scenes/` с соответствующими файлами (опционально).

## Разработка

Для добавления новых функций:

1. Создайте новые сцены в `bot/scenes/`
2. Добавьте обработчики в `bot/handlers/`
3. Обновите модели в `oms/models/` при необходимости