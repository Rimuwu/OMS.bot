from oms import Scene
from bot.scenes.user_task.channels_page import ChannelsPage

class TaskScene(Scene):

    __scene_name__ = 'user-task'
    __pages__ = [
        ChannelsPage
    ]