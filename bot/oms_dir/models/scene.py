from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import json


@dataclass
class FunctionWorker:
    """Класс для описания функций-обработчиков"""
    function: Optional[str] = None
    arguments: List[str] = field(default_factory=list)
    return_fields: Optional[List[str]] = field(default_factory=list)


@dataclass
class DataGetter(FunctionWorker):
    """Класс для описания функции получения данных"""
    return_fields: List[str] = field(default_factory=list)

    def __post_init__(self):
        if hasattr(self, 'return'):
            self.return_fields = getattr(self, 'return')


@dataclass 
class DataSetter(FunctionWorker):
    """Класс для описания функции установки данных"""

    arguments: List[str] = field(default_factory=list)

    def __post_init__(self):
        if hasattr(self, 'args'):
            self.arguments = getattr(self, 'args')


@dataclass
class SceneSettings:
    """Настройки сцены"""
    worker_class: Optional[str] = None
    data_getter: Optional[DataGetter] = None
    data_setter: Optional[DataSetter] = None
    state: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneSettings':
        """Создание объекта из словаря"""
        data_getter = None
        if 'data-getter' in data:
            getter_data = data['data-getter'].copy()
            if 'return' in getter_data:
                getter_data['return_fields'] = getter_data.pop('return')
            data_getter = DataGetter(**getter_data)

        data_setter = None
        if 'data-setter' in data:
            data_setter = DataSetter(**data['data-setter'])

        return cls(
            worker_class=data.get('worker-class'),
            data_getter=data_getter,
            data_setter=data_setter,
            state=data.get('state')
        )


@dataclass
class ScenePage:
    """Страница сцены"""
    title: str
    content: str
    to_pages: Dict[str, str] = field(default_factory=dict)
    content_worker: Optional[FunctionWorker] = None
    buttons_worker: Optional[FunctionWorker] = None
    text_waiter: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScenePage':
        """Создание объекта из словаря"""
        content_worker = None
        if 'content-worker' in data:
            content_worker = FunctionWorker(**data['content-worker'])

        buttons_worker = None
        if 'buttons-worker' in data:
            buttons_worker = FunctionWorker(**data['buttons-worker'])

        return cls(
            title=data['title'],
            content=data['content'],
            to_pages=data.get('to_pages', {}),
            content_worker=content_worker,
            buttons_worker=buttons_worker,
            text_waiter=data.get('text-waiter')
        )


@dataclass
class Scene:
    """Основной класс сцены"""
    name: str
    settings: SceneSettings
    pages: Dict[str, ScenePage]

    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> 'Scene':
        """Создание сцены из словаря"""
        settings = SceneSettings.from_dict(data['settings'])

        pages = {}
        for page_name, page_data in data['pages'].items():
            pages[page_name] = ScenePage.from_dict(page_data)

        return cls(
            name=name,
            settings=settings,
            pages=pages
        )

    def get_page(self, page_name: str) -> Optional[ScenePage]:
        """Получение страницы по имени"""
        return self.pages.get(page_name)

    def get_main_page(self) -> Optional[ScenePage]:
        """Получение главной страницы (первой в списке)"""
        if self.pages:
            return next(iter(self.pages.values()))
        return None


@dataclass
class SceneLoader:
    """Класс для загрузки сцен из JSON"""
    scenes: Dict[str, Scene] = field(default_factory=dict)

    def load_from_file(self, file_path: str) -> None:
        """Загрузка сцен из JSON файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Удаляем комментарии из JSON
                content = f.read()
                lines = content.split('\n')
                cleaned_lines = []
                for line in lines:
                    # Удаляем комментарии начинающиеся с //
                    if '//' in line:
                        line = line[:line.index('//')]
                    cleaned_lines.append(line)

                cleaned_content = '\n'.join(cleaned_lines)
                data = json.loads(cleaned_content)

            self.scenes.clear()
            for scene_name, scene_data in data.items():
                self.scenes[scene_name] = Scene.from_dict(scene_name, scene_data)

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл конфигурации сцен не найден: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка парсинга JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки сцен: {e}")

    def get_scene(self, scene_name: str) -> Optional[Scene]:
        """Получение сцены по имени"""
        return self.scenes.get(scene_name)

    def get_all_scenes(self) -> Dict[str, Scene]:
        """Получение всех загруженных сцен"""
        return self.scenes.copy()

    def reload_from_file(self, file_path: str) -> None:
        """Перезагрузка сцен из файла"""
        self.load_from_file(file_path)