from oms_dir.models.scene import SceneLoader

class OMS_Base:

    __scenes_path__ = "scenes"
    __scene__ = None

    # Это вызываем для получения данных
    def data_getter(self, *args, **kwargs):
        pass

    # Это переопределяем для получения с внешними данными
    def __getter(self, **kwargs):
        raise NotImplementedError("Метод __getter должен быть реализован в подклассе")


    # Это вызываем для установки данных
    def data_setter(self, *args, **kwargs):
        pass

    # Это переопределяем для взаимодействия с внешними данными
    def __setter(self, **kwargs):
        raise NotImplementedError("Метод __setter должен быть реализован в подклассе")


    def set_state(self):
        pass
        # if self.__scene__:
        #     self.__scene__.set_state(state)
        # else:
        #     raise ValueError("Сцена не загружена")

    def update_state(self):
        pass


    def set_page(self, page_name: str):
        pass

    def get_page(self, page_name: str):
        pass

    def get_pages(self):
        pass


    def send_message(self, page_name: str):
        pass

    def update_message(self, page_name: str):
        pass


    def content_worker(self):
        pass


    def buttons_worker(self):
        pass


    # contetn functions


    # buttons functions


class OMS_Manager:
    
    