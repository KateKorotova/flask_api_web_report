from peewee import SqliteDatabase
from app.models import Driver, Racing
import pytest
from app.main import create_app


@pytest.fixture
def client():
    test_database = SqliteDatabase(':memory:')
    app = create_app(database=test_database)
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            test_database.bind([Driver, Racing])
            test_database.create_tables([Driver, Racing])

            driver_1 = Driver.create(abbr='HAM', name='Lewis Hamilton', team='Mercedes')
            driver_2 = Driver.create(abbr='SVF', name='Sebastian Vettel', team='Ferrari')
            Racing.create(driver=driver_1, lap_time='1:12.345')
            Racing.create(driver=driver_2, lap_time='1:12.397')

            yield client
            test_database.drop_tables([Driver, Racing])
            test_database.close()