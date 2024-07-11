from peewee import *
import os

DATABASE = os.path.join(os.path.dirname(__file__), '../database/race.db')
database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class Driver(BaseModel):
    abbr = CharField(unique=True, primary_key=True)
    name = CharField()
    team = CharField(null=True)


class Racing(BaseModel):
    driver = ForeignKeyField(Driver, backref='races', field='abbr')
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)
    name = CharField(null=True)
    lap_time = CharField(null=True)
