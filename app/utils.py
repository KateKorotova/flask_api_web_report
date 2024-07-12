from app.models import Driver, Racing
from peewee import fn
from flask import make_response
import dicttoxml
import json


def get_report(order):
    sort_order = Racing.lap_time.asc() if order == 'asc' else Racing.lap_time.desc()
    return (
        Racing
        .select(
            Driver.name,
            Driver.team,
            Racing.lap_time,
            fn.RANK().over(order_by=[Racing.lap_time]).alias('place')
        )
        .join(Driver)
        .order_by(sort_order)
    )


def get_driver_list(order):
    sort_order = Driver.abbr.asc() if order == 'asc' else Driver.abbr.desc()
    return (
        Driver
        .select(Driver.abbr, Driver.name)
        .order_by(sort_order)
    )


def get_driver_info(driver_id):
    return (
            Driver.select(Driver.abbr, Driver.name, Driver.team, Racing.lap_time)
            .join(Racing, on=Racing.driver)
            .where(Driver.abbr == driver_id)
        )


def make_api_response(data, response_format):
    if response_format == 'xml':
        response = make_response(dicttoxml.dicttoxml(data,
                                                     custom_root='racings',
                                                     attr_type=False))
        response.headers['Content-Type'] = 'application/xml'
        return response
    response = make_response(json.dumps(data))
    response.headers['Content-Type'] = 'application/json'
    return response
