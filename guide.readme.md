## Run server

    python app.py

## Update database:

Run command to create migration:

    flask db migrate -m "Commit name"

Then, upgrade database:

    flask db upgrade
