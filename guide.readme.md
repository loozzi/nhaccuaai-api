## Run server in developer mode

    python app.py

or run on production mode

    python app.py --production

## Update database:

Run command to create migration:

    flask db migrate -m "Commit name"

Then, upgrade database:

    flask db upgrade

If you using FastAPI, go to folder has file `alembic.ini` and run:

    alembic upgrade head

or

    flask src:flask_app db upgrade
