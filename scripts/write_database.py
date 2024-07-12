from peewee import *
from app.models import Driver, Racing
from datetime import datetime, timedelta
import os


ABBR_FILE = 'data/abbreviations.txt'
START_LOG = 'data/start.log'
END_LOG = 'data/end.log'
DATABASE = os.path.join(os.path.dirname(__file__), '../database/race.db')

database = SqliteDatabase(DATABASE)
os.makedirs(os.path.dirname(DATABASE), exist_ok=True)


def create_tables():
    with database:
        database.create_tables([Driver, Racing])


def format_lap_time(total_seconds):
    if total_seconds is None:
        return None
    td = timedelta(seconds=total_seconds)
    minutes = td.seconds // 60
    seconds = td.seconds % 60
    milliseconds = td.microseconds // 1000
    return f'{minutes:01d}.{seconds:02d}.{milliseconds:03d}'


# Parse abbr.txt
def parse_abbr_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            abbr, name, team = line.strip().split('_')
            Driver.create(abbr=abbr, name=name, team=team)


def parse_log_file(file_path, log_type):
    with open(file_path, 'r') as file:
        for line in file:
            abbr = line[:3]
            timestamp = datetime.strptime(line[3:].strip(), '%Y-%m-%d_%H:%M:%S.%f')
            driver_instance = Driver.get(Driver.abbr == abbr)
            log, created = Racing.get_or_create(driver=driver_instance)

            if log_type == 'start':
                if log.end_time and timestamp > log.end_time:
                    log.end_time, log.start_time = timestamp, log.end_time  # Swap incorrect entries
                else:
                    log.start_time = timestamp
            else:
                if log.start_time and timestamp < log.start_time:
                    log.start_time, log.end_time = timestamp, log.start_time  # Swap incorrect entries
                else:
                    log.end_time = timestamp

            if log.start_time and log.end_time:
                log.lap_time = format_lap_time((log.end_time - log.start_time).total_seconds())
            log.name = 'Monaco_2018'
            log.save()


create_tables()
with database:
    parse_abbr_file(ABBR_FILE)
    parse_log_file(START_LOG, 'start')
    parse_log_file(END_LOG, 'end')
