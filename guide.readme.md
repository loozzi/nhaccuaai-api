## Run server in developer mode

    python app.py

or run on production mode

    python app.py --production

## Update database:

Run command to create migration:

    flask db migrate -m "Commit name"

Then, upgrade database:

    flask db upgrade
