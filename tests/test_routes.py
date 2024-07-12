from bs4 import BeautifulSoup
from . import client


def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/report/'


def test_report_page(client):
    response = client.get('/report/')
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, 'html.parser')
    assert soup.find('table', {'class': 'table table-striped'}) is not None
    assert 'Racing Report' in soup.title.string
    assert 'Lap Time' in [a.text.strip() for a in soup.findAll('a')]


def test_drivers_page(client):
    response = client.get('/report/drivers/')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    assert soup.find('table', {'class': 'table table-hover'}) is not None
    assert 'Drivers List' in soup.title.string


def test_driver_info_page(client):
    response = client.get('/report/drivers/?driver_id=SVF')
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    assert soup.find('table', {'class': 'table table-bordered'}) is not None
    assert 'Driver Info' in soup.title.string


def test_driver_not_found(client):
    response = client.get('/report/drivers/?driver_id=XYZ')
    assert response.status_code == 404
    assert b'Driver ID not found' in response.data
