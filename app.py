from flask import Flask
from config import Configuration
from posts.blueprint import posts
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.register_blueprint(posts, url_prefix='/post')