import typer
from typing_extensions import Annotated

app = typer.Typer(add_completion=False)


@app.command()
def design(src, dest: Annotated[str, typer.Argument()] = ""):
    from ..image.svg.design import Manager
    manager = Manager()
    manager.load_path(src)
    manager.dump(dest or src)


@app.callback()
def callback():
    pass
