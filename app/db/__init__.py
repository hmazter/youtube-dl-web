import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)

    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    click.echo('Initialized the database.')


class Job(db.Model):
    """ Job model """

    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    file_type = db.Column(db.String, nullable=False)
    start = db.Column(db.String, nullable=True)
    end = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=False)
    downloaded_file = db.Column(db.String, nullable=True)
    filename = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Job:(%r)>' % self.url

    def mime(self):
        if self.file_type == 'mp4':
            return 'video/mp4'
        else:
            return 'audio/mp3'
