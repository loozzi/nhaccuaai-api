import uvicorn

from src import app, config

app = app

if __name__ == "__main__":
    if config.DEBUG:
        uvicorn.run(
            "src:app",
            host=config.HOST,
            port=config.PORT,
            reload=True,
            reload_dirs=["./src"],
        )
    else:
        uvicorn.run("src:app", host=config.HOST, port=config.PORT)
