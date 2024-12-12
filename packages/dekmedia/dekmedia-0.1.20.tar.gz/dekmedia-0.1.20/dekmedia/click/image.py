import os
import typer
from typing import List
from typing_extensions import Annotated
from dektools.file import read_file
from . import svg as svg_command

app = typer.Typer(add_completion=False)
app.add_typer(svg_command.app, name='svg')


@app.command()
def trans(src, outputs: Annotated[List[str], typer.Argument()] = None, sizes=''):
    if not outputs:
        return
    if os.path.splitext(src)[-1].lower() == '.svg':
        from ..image.svg.load import load_svg
        image = load_svg(read_file(src))
    else:
        from PIL import Image
        image = Image.open(src)
    from ..image.core import resize_image
    resize_image(image, outputs, parse_sizes(sizes))


def parse_sizes(sizes):
    if sizes:
        ss = [int(n) for n in sizes.split(',')]
        return list(zip(ss[::2], ss[1::2]))


@app.command()
def design(src, dest: Annotated[str, typer.Argument()] = ""):
    from ..image.design import Manager
    manager = Manager()
    manager.load_path(src)
    manager.dump(dest or src)
