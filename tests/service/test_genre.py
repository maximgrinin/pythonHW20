from unittest.mock import MagicMock
import pytest as pytest
from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService

# Создаем фикстуру для тестирования сервисов GenreService
@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)

    genre_1 = Genre(id=1, name='Комедия')
    genre_2 = Genre(id=2, name='Семейный')
    genre_3 = Genre(id=3, name='Фэнтези')

    genre_dao.get_one = MagicMock(return_value=genre_1)
    genre_dao.get_all = MagicMock(return_value=[genre_1, genre_2, genre_3])
    genre_dao.create = MagicMock(return_value=Genre(id=4, name='Драма'))
    genre_dao.update = MagicMock()
    genre_dao.delete = MagicMock()

    return genre_dao


# Определяем класс с тестами для тестирования сервисов GenreService
class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id is not None
        assert genre.name == 'Комедия'

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0
        assert len(genres) == 3

    def test_create(self):
        genre_d = {
            "name": "Драма"
        }
        genre = self.genre_service.create(genre_d)
        assert genre is not None
        assert genre.id is not None
        assert genre.name == 'Драма'

    def test_update(self):
        genre_d = {
            "id": 4,
            "name": "Драмeди"
        }
        self.genre_service.update(genre_d)

    def test_partially_update(self):
        genre_d = {
            "id": 4,
            "name": "Драмeди"
        }
        self.genre_service.update(genre_d)

    def test_delete(self):
        self.genre_service.delete(1)
