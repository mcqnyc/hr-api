import os
import redis
import pathlib
import connexion

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from rq import Queue
from dotenv import load_dotenv

load_dotenv()

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
connection = redis.from_url(os.getenv("REDIS_URL"))
app.queue = Queue("emails", connection=connection)

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
