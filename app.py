from src import app, config

if __name__ == "__main__":
    if config.DEBUG:
        app.run(
            debug=config.DEBUG,
            host=config.HOST,
            port=config.PORT,
            use_reloader=True,
            extra_files=["./src"],
        )
    else:
        app.run(use_reloader=True, extra_files=["./src"])
