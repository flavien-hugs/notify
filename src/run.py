import typer
import uvicorn

from src.config import settings

app = typer.Typer(pretty_exceptions_enable=True)


@app.command(name="Run app server")
def run_app():
    uvicorn.run(
        app="src.main:app",
        host=settings.APP_HOSTNAME,
        port=settings.APP_DEFAULT_PORT,
        reload=settings.APP_RELOAD,
        log_level=settings.APP_LOG_LEVEL,
        access_log=settings.APP_ACCESS_LOG,
        loop=settings.APP_LOOP,
    )


if __name__ == "__main__":
    app()
