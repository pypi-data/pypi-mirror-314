from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from typing import Union
import os
import shutil

def generate_file(file_path: Union[Path, str], template_path: Union[Path, str], **kwargs) -> None:
    """Generate a file at `file_path` using the jinja template located at `file_path`.

    kwargs are used to fill the template.

    :param file_path: path where to generate the file
    :type file_path: pathlib.Path or str
    :param template_path: Path to the template to use for code generation
    :type template_path: pathlib.Path or str
    """
    # Convert str -> Path for compatibility !
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if isinstance(template_path, str):
        template_path = Path(template_path)
    if not template_path.exists():
        raise ValueError(f"Path to template {template_path} is not valid !")
    # Make dir
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate file
    with open(file_path, mode="w", encoding="utf-8") as file:
        file.write(generate_str(template_path, **kwargs))


def generate_str(template_path: Union[Path, str], **kwargs) -> str:
    """Generate a string using the jinja template located at `file_path`.
    kwargs are used to fill the template.

    :param template_path: Path to the template to use for code generation
    :type template_path: pathlib.Path or str
    :return: A string of the interpreted template
    :rtype: str
    """
    # Convert str -> Path for compatibility !
    if isinstance(template_path, str):
        template_path = Path(template_path)
    return Environment(loader=FileSystemLoader(
        template_path.parent), undefined=StrictUndefined, keep_trailing_newline=True).get_template(template_path.name).render(kwargs)

def copy_file(filename, dst_folder):

    # If directory doesn't exist, create it
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    shutil.copy(filename, dst_folder)
