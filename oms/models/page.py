from typing import TYPE_CHECKING, Optional

from .json_scene import ScenePage, SceneModel
from aiogram.types import Message, CallbackQuery
from ..utils import use_inspect

if TYPE_CHECKING:
    from .scene import Scene

class Page:

    __page_name__: str = ''

    def __init__(self, 
                 scene: SceneModel, 
                 this_scene: 'Scene',
                 page_name: str = ''):
        if page_name and not self.__page_name__: 
            self.__page_name__ = page_name

        self.__scene__: SceneModel = scene
        self.__page__: ScenePage = scene.pages.get(
            self.__page_name__) # type: ignore

        self.__callback_handlers__ = {}

        if not self.__page__:
            raise ValueError(f"Страница {self.__page_name__} не найдена в сцене {scene.name} -> {list(scene.pages.keys())}")

        self.title: str = self.__page__.title
        self.content: str = self.__page__.content
        self.to_pages: dict = self.__page__.to_pages

        self.scene: Scene = this_scene

    def __call__(self, *args, **kwargs):
        return self

    def get_data(self, key: Optional[str] = None):
        """ Получение данных страницы (всех или по ключу)
        """
        if key:
            return self.scene.get_key(self.__page_name__, key)
        return self.scene.get_data(self.__page_name__)

    def set_data(self, data: dict) -> bool:
        """ Установка данных (с польной перезаписью) страницы
        """
        return self.scene.set_data(self.__page_name__, data)

    def update_data(self, key: str, value) -> bool:
        """ Обновление данных страницы по ключу
        """
        return self.scene.update_key(self.__page_name__, key, value)

    def on_callback(self, callback_type: str):
        """ Декоратор для регистрации обработчиков нажатий кнопок
            Пример использования:
            
            @page.on_callback('my_callback')
            async def my_callback_handler(self, 
                callback: CallbackQuery, args: list):
                print(args) # ['additional', 'args']

            Пример создания кнопки для такого обработчика:
            {
                'text': 'Нажми меня',
                'callback_data': callback_generator(
                    self.scene.__scene_name__, 
                    'my_callback', 
                    'additional', 'args'
                )
            }

            Нельзя ставить 2 обработчика на один callback_type!
        """
        def decorator(func):
            if callback_type in self.__callback_handlers__:
                raise ValueError(f"Обработчик для {callback_type} уже зарегистрирован.")

            self.__callback_handlers__[callback_type] = func
            return func
        return decorator

    async def callback_handler(self, 
                    callback: CallbackQuery, args: list) -> None:
        """ Обработка и получение нажатий
        """
        if args and args[0] in self.__callback_handlers__:
            callback_type = args[0]
            handler = self.__callback_handlers__[callback_type]
            use_inspect(handler, callback=callback, args=args)

        if 'all' in self.__callback_handlers__:
            handler = self.__callback_handlers__['all']
            use_inspect(handler, callback=callback, args=args)

    def clear_content(self):
        """ Очистка контента до значения из конфига
        """
        self.content = self.__page__.content



    # МОЖНО И НУЖНО МЕНЯТЬ !

    async def content_worker(self) -> str:
        return self.content

    async def buttons_worker(self) -> list[dict]:
        return []

    async def text_handler(self, message: Message) -> None:
        """ Обработка и получение сообщения на странице
        """
        pass