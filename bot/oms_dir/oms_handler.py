from aiogram.types import Message, CallbackQuery
from bot.main import dp, mainbot
from bot.oms_dir.scene import manager, CALLBACK_PREFIX
from aiogram import F

@dp.message()
async def on_message(message: Message):
    user_id = message.from_user.id
    user_session = manager.get_scene(user_id)

    if user_session:
        await user_session.text_handler(message)

@dp.callback_query(
    F.data.split(":")[:2] == [CALLBACK_PREFIX, 'to_page']
                   )
async def to_page(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_session = manager.get_scene(user_id)

    prefix, c_type, scene_name, *args = callback.data.split(':')
    to_page = args[0]

    if user_session:
        await user_session.update_page(to_page)

@dp.callback_query(F.data.split(":")[0] == CALLBACK_PREFIX)
async def on_callback_query(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_session = manager.get_scene(user_id)

    prefix, c_type, scene_name, *args = callback.data.split(':')

    if user_session:
        await user_session.callback_handler(callback, args)

@dp.callback_query()
async def not_handled(callback: CallbackQuery):
    print(
        "not_handled", callback.data
    )