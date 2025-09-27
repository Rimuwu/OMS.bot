from datetime import datetime
from oms import Page
from aiogram.types import Message, CallbackQuery

from oms.utils import callback_generator

class ChannelsPage(Page):

    __page_name__ = 'channels-settings'
    
    
    async def buttons_worker(self):
        buttons = []
        buttons.append({
            'text': "@",
            'callback_data': callback_generator(
                self.scene.__scene_name__,
                "my_type", 13
            )
        })
        return buttons

    @Page.on_text(data_type='int')
    async def handle_int(self, message: Message, value: int):
        print(f"Получено число: {value}")

    @Page.on_text(data_type='time')
    async def handle_time(self, message: Message, value: datetime):
        print(f"Получено время: {value}")

    @Page.on_text(data_type='list', separator=';')
    async def handle_list(self, message: Message, value: list):
        print(f"Получен список: {value}")

    @Page.on_text(data_type='all')
    async def handle_all_text(self, message: Message):
        print(f"Получен любой текст: {message.text}")

    @Page.on_callback('my_type')
    async def my_callback_handler(self, 
        callback: CallbackQuery, args: list):
        print(args) # ['additional', 'args']
        await callback.answer("Нажата кнопка!")