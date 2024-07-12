from flask import request
from flask_restful import Resource
from app.utils import get_report, get_driver_list, get_driver_info, make_api_response
from playhouse.shortcuts import model_to_dict
import peewee


class Report(Resource):
    def get(self):
        """
          Get racing report
          ---
          parameters:
            - name: version
              in: query
              type: string
              required: true
              default: v1
            - name: response_format
              in: query
              type: string
              required: false
              enum: ['json', 'xml']
              default: json
            - name: order
              in: query
              type: string
              required: false
              enum: ['asc', 'desc']
              default: asc
          responses:
            200:
              description: Report of Monaco 2018 racing
          """
        version = request.args.get('version', 'v1')
        response_format = request.args.get('response_format', 'json')
        order = request.args.get('order', 'asc')

        if version != 'v1':
            return {"message": "Version not supported"}, 400

        report_data = list(get_report(order).dicts())
        return make_api_response(report_data, response_format)


class Drivers(Resource):
    def get(self):
        """
            Get list of drivers
            ---
            parameters:
              - name: version
                in: query
                type: string
                required: true
                default: v1
              - name: response_format
                in: query
                type: string
                required: false
                enum: ['json', 'xml']
                default: json
              - name: driver_id
                in: query
                type: string
                required: false
              - name: order
                in: query
                type: string
                required: false
                enum: ['asc', 'desc']
                default: asc
            responses:
              200:
                description: A list of drivers or specific driver inresponse_formation
            """
        version = request.args.get('version', 'v1')
        response_format = request.args.get('response_format', 'json')
        driver_id = request.args.get('driver_id')
        order = request.args.get('order', 'asc')

        if version != 'v1':
            return {"message": "Version not supported"}, 400

        if driver_id:
            try:
                driver_data = model_to_dict(get_driver_info(driver_id).get())
            except peewee.DoesNotExist:
                return {"message": "Driver ID not found"}, 404
            return make_api_response(driver_data, response_format)

        drivers_list = list(get_driver_list(order).dicts())
        return make_api_response(drivers_list, response_format)
