from flask_cache import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
cache = Cache(config={
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24 * 7
})


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    mail.init_app(app=app)
    cache.init_app(app=app)