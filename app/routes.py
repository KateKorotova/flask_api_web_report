from flask import Blueprint, render_template, request, redirect, url_for
from app.utils import get_report, get_driver_list, get_driver_info

bp = Blueprint('main', __name__, template_folder='templates')


@bp.route('/')
def index():
    return redirect(url_for('main.report'))


@bp.route('/report/')
def report():
    order = request.args.get('order', 'asc')
    report_data = get_report(order)
    return render_template('report.html', report=report_data, order=order)


@bp.route('/report/drivers/')
def drivers():
    driver_id = request.args.get('driver_id')
    order = request.args.get('order', 'asc')

    if driver_id:
        driver_data = get_driver_info(driver_id)
        if not driver_data:
            return "Driver ID not found", 404
        return render_template('driver_info.html', driver=driver_data)

    else:
        drivers_list = get_driver_list(order)
        return render_template('drivers.html', drivers=drivers_list, order=order)
