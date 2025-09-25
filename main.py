

from bot.oms_dir.models.scene import SceneLoader


from pprint import pprint


scene = SceneLoader()
scene.load_from_file('json/scenes.json')

pprint(
    scene.get_scene('user-task').get_page('main-page').buttons_worker.function
)