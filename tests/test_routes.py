import pytest
from bs4 import BeautifulSoup
from app.main import create_app
from unittest.mock import patch
from peewee import ModelSelect


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_database_queries():
    with patch('app.utils.get_report') as mock_report, \
            patch('app.utils.get_driver_list') as mock_driver_list, \
            patch('app.utils.get_driver_info') as mock_driver_info:
        yield mock_report, mock_driver_list, mock_driver_info


def mock_report_data():
    data = [
        {"name": "Monaco GP", "driver": {"name": "Lewis Hamilton", "team": "Mercedes"}, "lap_time": "1:12.345"},
        {"name": "Monaco GP", "driver": {"name": "Max Verstappen", "team": "Red Bull Racing"}, "lap_time": "1:12.789"},
        {"name": "Monaco GP", "driver": {"name": "Charles Leclerc", "team": "Ferrari"}, "lap_time": "1:13.123"}
    ]
    return data


def mock_driver_list_data():
    data = [
        {"abbr": "HAM", "name": "Lewis Hamilton"},
        {"abbr": "VER", "name": "Max Verstappen"},
        {"abbr": "LEC", "name": "Charles Leclerc"}
    ]
    return data


def mock_driver_info_data():
    return {"abbr": "SVF", "name": "Sebastian Vettel", "team": "Aston Martin"}


def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/report/'


def test_report_page(client, mock_database_queries):
    mock_report, _, _ = mock_database_queries
    mock_report.return_value = ModelSelect(mock_report, mock_report_data())
    response = client.get('/report/')
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')
    assert soup.find('table', {'class': 'table table-striped'}) is not None
    assert 'Racing Report' in soup.title.string
    assert 'Lap Time' in [a.text.strip() for a in soup.findAll('a')]


def test_drivers_page(client, mock_database_queries):
    _, mock_driver_list, _ = mock_database_queries
    mock_driver_list.return_value = ModelSelect(mock_driver_list, mock_driver_list_data())
    response = client.get('/report/drivers/')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    assert soup.find('table', {'class': 'table table-hover'}) is not None
    assert 'Drivers List' in soup.title.string


def test_driver_info_page(client, mock_database_queries):
    _, _, mock_driver_info = mock_database_queries
    mock_driver_info.return_value.get.return_value = mock_driver_info_data()
    response = client.get('/report/drivers/?driver_id=SVF')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    assert soup.find('table', {'class': 'table table-bordered'}) is not None
    assert 'Driver Info' in soup.title.string


def test_driver_not_found(client, mock_database_queries):
    _, _, mock_driver_info = mock_database_queries
    mock_driver_info.return_value.get.return_value = mock_driver_info_data()
    response = client.get('/report/drivers/?driver_id=XYZ')
    assert response.status_code == 404
    assert b'Driver ID not found' in response.data
