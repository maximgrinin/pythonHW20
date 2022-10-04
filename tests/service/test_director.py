from unittest.mock import MagicMock
import pytest as pytest
from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService

# Создаем фикстуру для тестирования сервисов DirectorService
@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    director_1 = Director(id=1, name='Тейлор Шеридан')
    director_2 = Director(id=2, name='Квентин Тарантино')
    director_3 = Director(id=3, name='Владимир Вайншток')

    director_dao.get_one = MagicMock(return_value=director_1)
    director_dao.get_all = MagicMock(return_value=[director_1, director_2, director_3])
    director_dao.create = MagicMock(return_value=Director(id=4, name='Декстер Флетчер'))
    director_dao.update = MagicMock()
    director_dao.delete = MagicMock()

    return director_dao


# Определяем класс с тестами для тестирования сервисов DirectorService
class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id is not None
        assert director.name == 'Тейлор Шеридан'

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0
        assert len(directors) == 3

    def test_create(self):
        director_d = {
            "name": "Декстер Флетчер"
        }
        director = self.director_service.create(director_d)
        assert director is not None
        assert director.id is not None
        assert director.name == 'Декстер Флетчер'

    def test_update(self):
        director_d = {
            "id": 4,
            "name": "Стив Энтин"
        }
        self.director_service.update(director_d)

    def test_partially_update(self):
        director_d = {
            "id": 4,
            "name": "Стив Энтин"
        }
        self.director_service.update(director_d)

    def test_delete(self):
        self.director_service.delete(1)
