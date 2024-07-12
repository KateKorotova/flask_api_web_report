# Flask API & Web Report using SQLite database for Report of Monaco 2018 racing
## Overview

The Racing Report API is a RESTful web service that provides racing statistics and driver information. It supports JSON and XML formats and includes Swagger documentation for easy API exploration.
Also it contains a Flask web application that generates and displays racing reports. The application includes multiple routes to display common statistics, a list of drivers, and detailed information about individual drivers. The data is read from SQLite database.

## Features
### Access the application in your web browser:
- Main report: http://localhost:9999/report/
- Drivers list: http://localhost:9999/report/drivers/
- Driver info: http://localhost:9999/report/drivers/?driver_id=DRIVER_ID

### Get data through API:
- Retrieve a sorted racing report
- Get a list of drivers
- Get detailed information about a specific driver
- Support for JSON and XML formats
- Swagger documentation for easy API exploration

## Requirements

* Python 3.6+
* flask
* pytest
* pandas
* flasgger
* flask_restful
* lxml
* peewee
* BeautifulSoup4
* dicttoxml


## Usage
1. Install all required packages from requirement.txt:
```
pip install -r requirements.txt
```
2. Run the Flask API:
```
python run.py
```

## Routes
**/report/**: Displays the main racing report with an optional order parameter to sort by lap time. E.g., **/report/?order=asc**.

**/report/drivers/**: Shows a list of driver names and codes. Each driver code is a link to detailed information about the driver.

**/report/drivers/?driver_id=DRIVER_ID**: Displays detailed information about the specified driver.


## API Endpoints
### Get Racing Report

```
GET /api/v1/report/
```
Parameters:
* version (string): API version (default: v1)
* response_format (string): Response format, either json or xml (default: json)
* order (string): Sort order, either asc or desc (default: asc)

Response:

200 OK with a list of racing reports in the specified format
### Get Drivers
```
GET /api/v1/drivers/
```
Parameters:

* version (string): API version (default: v1)
* response_format (string): Response format, either json or xml (default: json)
* driver_id (string): (Optional) ID of a specific driver
* order (string): Sort order, either asc or desc (default: asc)

Response:

200 OK with a list of drivers or specific driver information in the specified format

## Directory Structure
```
task-9-rest-convert-and-store-data-to-the-database/
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
├── database/
│   └── race.db.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_api_routes.py
├── scripts/
│   ├── data/
│   │   ├── abbreviations.txt
│   │   ├── end.log
│   │   └── start.log
│   ├── __init__.py
│   └── write_database.py
├── run.py
├── requirements.txt
└── README.md
```

## Authors and acknowledgment
Author: Yekatierina Korotova