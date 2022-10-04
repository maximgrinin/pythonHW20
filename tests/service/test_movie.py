from unittest.mock import MagicMock
import pytest as pytest
from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


# Создаем фикстуру для тестирования сервисов MovieService
@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_1 = Movie(id=1,
                    title='Йеллоустоун',
                    description='Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в...',
                    trailer='https://www.youtube.com/watch?v=UKei_d0cbP4',
                    year=2018,
                    rating=8.6,
                    genre_id=17,
                    director_id=1)
    movie_2 = Movie(id=2,
                    title='Омерзительная восьмерка',
                    description='США после Гражданской войны. Легендарный охотник за головами Джон Рут по кличке...',
                    trailer='https://www.youtube.com/watch?v=lmB9VWm0okU',
                    year=2015,
                    rating=7.8,
                    genre_id=4,
                    director_id=2)
    movie_3 = Movie(id=3,
                    title='Вооружен и очень опасен',
                    description='События происходят в конце XIX века на Диком Западе, в Америке. В основе сюжета...',
                    trailer='https://www.youtube.com/watch?v=hLA5631F-jo',
                    year=1978,
                    rating=6,
                    genre_id=17,
                    director_id=3)

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create = MagicMock(return_value=Movie(id=4,
                                                    title='Джанго освобожденный',
                                                    description='Эксцентричный охотник за головами, также известный...',
                                                    trailer='https://www.youtube.com/watch?v=2Dty-zwcPv4',
                                                    year=2012,
                                                    rating=8.4,
                                                    genre_id=17,
                                                    director_id=2))
    movie_dao.update = MagicMock()
    movie_dao.delete = MagicMock()

    return movie_dao


# Определяем класс с тестами для тестирования сервисов MovieService
class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None
        assert movie.title == 'Йеллоустоун'
        assert movie.description == 'Владелец ранчо пытается сохранить землю своих предков. Кевин Костнер в...'
        assert movie.trailer == 'https://www.youtube.com/watch?v=UKei_d0cbP4'
        assert movie.year == 2018
        assert movie.rating == 8.6
        assert movie.genre_id == 17
        assert movie.director_id == 1

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0
        assert len(movies) == 3

    def test_create(self):
        movie_d = {
            "title": "Джанго освобожденный",
            "description": "Эксцентричный охотник за головами, также известный...",
            "trailer": "https://www.youtube.com/watch?v=2Dty-zwcPv4",
            "year": 2012,
            "rating": 8.4,
            "genre_id": 17,
            "director_id": 2
        }
        movie = self.movie_service.create(movie_d)
        assert movie is not None
        assert movie.id is not None
        assert movie.title == 'Джанго освобожденный'
        assert movie.description == 'Эксцентричный охотник за головами, также известный...'
        assert movie.trailer == 'https://www.youtube.com/watch?v=2Dty-zwcPv4'
        assert movie.year == 2012
        assert movie.rating == 8.4
        assert movie.genre_id == 17
        assert movie.director_id == 2

    def test_update(self):
        movie_d = {
            "id": 4,
            "title": "Рокетмен",
            "description": "История превращения застенчивого парня Реджинальда Дуайта...",
            "trailer": "https://youtu.be/VISiqVeKTq8",
            "year": 2019,
            "rating": 7.3,
            "genre_id": 18,
            "director_id": 4
        }
        self.movie_service.update(movie_d)

    def test_partially_update(self):
        movie_d = {
            "id": 4,
            "title": "Рокетвумен",
            "description": "История превращения застенчивой девушки Реджинальды Дуайт...",
        }
        self.movie_service.update(movie_d)

    def test_delete(self):
        self.movie_service.delete(1)
