from app import app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup


migrate = Migrate()
migrate.init_app(app, db)
cli = FlaskGroup(app)

# manager.add_command('db',  MigrateCommand )
# FLASK_APP=app

if __name__ == '__main__':
   cli()