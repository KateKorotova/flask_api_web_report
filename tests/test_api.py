import pytest
from app.main import create_app
import json
import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_database_queries():
    with patch('app.api.get_report') as mock_report, \
         patch('app.api.get_driver_list') as mock_driver_list, \
         patch('app.api.get_driver_info') as mock_driver_info:

        yield mock_report, mock_driver_list, mock_driver_info


def mock_single_driver():
    mock_driver_instance = MagicMock()
    mock_driver_instance.abbr = 'HAM'
    mock_driver_instance.name = 'Lewis Hamilton'
    mock_driver_instance.team = 'Mercedes'
    return mock_driver_instance


def model_to_dict_mock(instance):
    return {
        'abbr': instance.abbr,
        'name': instance.name,
        'team': instance.team
    }


def mock_report_data():
    data = [
        {"driver": {"name": "Lewis Hamilton", "team": "Mercedes"}, "lap_time": "1:12.345"},
        {"driver": {"name": "Max Verstappen", "team": "Red Bull Racing"}, "lap_time": "1:12.789"},
        {"driver": {"name": "Charles Leclerc", "team": "Ferrari"}, "lap_time": "1:13.123"}
    ]
    return data


def mock_driver_list_data():
    data = [
        {"abbr": "FAM", "name": "Fernando Alonso"},
        {"abbr": "LAH", "name": "Lewis Hamilton"},
    ]
    return data


def test_report_type_json(client, mock_database_queries):
    mock_report, _, _ = mock_database_queries
    mock_report.return_value.dicts.return_value = mock_report_data()

    response = client.get('/api/v1/report/?response_format=json')
    data = json.loads(response.data)

    assert response.content_type == 'application/json'
    assert response.status_code == 200
    assert isinstance(data, list)
    assert all('lap_time' in item for item in data)
    assert any('Mercedes' in item['driver']['team'] for item in data)


def test_report_content_type_xml(client, mock_database_queries):
    mock_report, _, _ = mock_database_queries
    mock_report.return_value.dicts.return_value = mock_report_data()

    response = client.get('/api/v1/report/?response_format=xml')
    root = ET.fromstring(response.data)
    items = root.findall('item')
    assert response.content_type == 'application/xml'
    assert root.tag == 'racings'
    assert len(items) == 3
    expected_data = mock_report_data()
    for index, item in enumerate(items):
        driver_elem = item.find('driver')
        lap_time_elem = item.find('lap_time')

        assert driver_elem is not None
        assert lap_time_elem is not None

        driver_name = driver_elem.find('name').text
        driver_team = driver_elem.find('team').text
        lap_time = lap_time_elem.text

        assert driver_name == expected_data[index]['driver']['name']
        assert driver_team == expected_data[index]['driver']['team']
        assert lap_time == expected_data[index]['lap_time']


def test_drivers_content_type_json(client, mock_database_queries):
    _, mock_driver_list, _ = mock_database_queries
    mock_driver_list.return_value.dicts.return_value = mock_driver_list_data()

    response = client.get('/api/v1/drivers/?response_format=json')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert isinstance(data, list)
    assert all('name' in item and 'abbr' in item for item in data)
    assert any('Lewis Hamilton' in item['name'] for item in data)


def test_drivers_content_type_xml(client, mock_database_queries):
    _, mock_driver_list, _ = mock_database_queries
    mock_driver_list.return_value.dicts.return_value = mock_driver_list_data()

    response = client.get('/api/v1/drivers/?response_format=xml')
    root = ET.fromstring(response.data)
    items = root.findall('item')

    assert response.content_type == 'application/xml'
    assert root.tag == 'racings'
    assert len(items) == 2


def test_single_driver_type_json(client, mock_database_queries):
    _, _, mock_driver_info = mock_database_queries

    mock_driver_info.return_value.get.return_value = mock_single_driver()
    with patch('app.api.model_to_dict', side_effect=model_to_dict_mock):
        response = client.get('/api/v1/drivers/?driver_id=HAM&response_format=json')
        data = json.loads(response.data)

    assert response.status_code == 200
    assert 'HAM' == data['abbr']
    assert 'Lewis Hamilton' == data['name']
    assert 'Mercedes' == data['team']


def test_single_driver_content_type_xml(client, mock_database_queries):
    _, _, mock_driver_info = mock_database_queries
    mock_driver_info.return_value.get.return_value = mock_single_driver()
    with patch('app.api.model_to_dict', side_effect=model_to_dict_mock):
        response = client.get('/api/v1/drivers/?driver_id=HAM&response_format=xml')
        root = ET.fromstring(response.data)

    assert response.content_type == 'application/xml'
    assert root.tag == 'racings'
    assert root.find('abbr').text == 'HAM'


def test_single_driver_not_found_status_code(client, mock_database_queries):
    _, _, mock_driver_info = mock_database_queries

    mock_driver_info.return_value.get.return_value = mock_single_driver()
    response = client.get('/api/v1/drivers/?driver_id=XYZ&response_format=json')

    assert response.status_code == 404
