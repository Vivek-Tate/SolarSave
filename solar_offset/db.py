import sqlite3

import click
from flask import current_app, g


# !! Consider using sql-alchemy since this provides an ORM and is easier to use


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')



# Register with the App
def init_app(app):
    # Closes database every time that a request is cleaned up
    app.teardown_appcontext(close_db)

    # adds a new command that can be called with the flask command to initialize a database
    app.cli.add_command(init_db_command)