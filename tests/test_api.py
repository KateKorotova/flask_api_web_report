import json
import xml.etree.ElementTree as ET
from . import client


def test_report_type_json(client):
    response = client.get('/api/v1/report/?response_format=json')
    data = json.loads(response.data)
    assert response.content_type == 'application/json'
    assert response.status_code == 200
    assert isinstance(data, list)
    assert all('lap_time' in item for item in data)
    assert any('Mercedes' in item['team'] for item in data)


def test_report_content_type_xml(client):
    response = client.get('/api/v1/report/?response_format=xml')
    root = ET.fromstring(response.data)
    items = root.findall('item')
    assert response.content_type == 'application/xml'
    assert root.tag == 'racings'
    assert len(items) == 2
    for index, item in enumerate(items):
        driver_elem = item.find('name')
        lap_time_elem = item.find('lap_time')

        assert driver_elem is not None
        assert lap_time_elem is not None


def test_drivers_content_type_json(client):
    response = client.get('/api/v1/drivers/?response_format=json')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert isinstance(data, list)
    assert all('name' in item and 'abbr' in item for item in data)
    assert any('Lewis Hamilton' in item['name'] for item in data)


def test_drivers_content_type_xml(client):
    response = client.get('/api/v1/drivers/?response_format=xml')
    root = ET.fromstring(response.data)
    items = root.findall('item')

    assert response.content_type == 'application/xml'
    assert root.tag == 'racings'
    assert len(items) == 2


def test_single_driver_type_json(client):
    response = client.get('/api/v1/drivers/?driver_id=HAM&response_format=json')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'HAM' == data['abbr']
    assert 'Lewis Hamilton' == data['name']
    assert 'Mercedes' == data['team']


def test_single_driver_content_type_xml(client):
    response = client.get('/api/v1/drivers/?driver_id=HAM&response_format=xml')
    root = ET.fromstring(response.data)

    assert response.content_type == 'application/xml'
    assert root.tag == 'racings'
    assert root.find('abbr').text == 'HAM'


def test_single_driver_not_found_status_code(client):
    response = client.get('/api/v1/drivers/?driver_id=XYZ&response_format=json')

    assert response.status_code == 404
