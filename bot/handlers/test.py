from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.main import dp
from bot.oms_dir.scene import manager
from bot.scenes.user_task.task_scene import TaskScene

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    user_id = message.from_user.id
    scene = manager.create_scene(user_id,
                                 TaskScene)

    if scene:
        await scene.start()
    else:
        await message.answer("No active scene. Please start a new one.")