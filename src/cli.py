import typer
import uvicorn

from src.config import settings

app = typer.Typer(pretty_exceptions_enable=True)


@app.command(name="runserver")
def run():
    uvicorn.run(
        app="src.main:app",
        host=settings.APP_HOSTNAME,
        port=settings.APP_PORT,
        loop=settings.APP_LOOP,
        reload=False if settings.APP_ENVIRONMENT != "dev" else True,
    )


if __name__ == "__main__":
    app()
