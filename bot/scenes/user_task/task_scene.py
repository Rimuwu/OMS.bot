from bot.oms_dir.scene import Scene
from bot.scenes.user_task.channels_page import ChannelsPage

class TaskScene(Scene):

    __scene_name__ = 'user-task'
    __pages__ = [
        ChannelsPage
    ]

    def __init__(self, user_id: int):
        super().__init__(user_id)