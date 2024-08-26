from config_reader import config
from peewee import Model, PrimaryKeyField, PostgresqlDatabase, CharField, IntegerField, BlobField, ForeignKeyField

db = PostgresqlDatabase(
    host=config.host.get_secret_value(),
    user=config.user.get_secret_value(),
    port=config.port.get_secret_value(),
    database=config.database.get_secret_value(),
    password=config.password.get_secret_value()
)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class Positions(BaseModel):
    title = CharField(null=True)


class Users(BaseModel):
    tg_id = IntegerField()
    position_id = ForeignKeyField(Positions)
    tg_username = CharField(null=True)
    personalQRCode = BlobField()
    coffe_number = IntegerField(default=0)