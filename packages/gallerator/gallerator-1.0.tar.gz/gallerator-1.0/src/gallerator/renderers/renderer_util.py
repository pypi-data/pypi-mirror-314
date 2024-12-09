import shutil
from pathlib import Path

from jinja2 import (
    ChoiceLoader,
    Environment,
    FileSystemLoader,
    select_autoescape,
)

from gallerator import data_types


def jinja2_env(renderer_templates):
    """
    Sets up a Jinja2 environment that looks for renderer-specific templates
    first and then generic ones.
    """
    loader = ChoiceLoader([
        FileSystemLoader(renderer_templates),
        FileSystemLoader(Path(__file__).parent / 'templates'),
    ])
    return Environment(
        loader=loader,
        autoescape=select_autoescape()
    )


def copy_static(renderer_static: Path, gallery_path: Path):
    """
    Copies renderer-specific static files first and then generic ones.
    """
    for src in [
        renderer_static,
        Path(__file__).parent / 'static',
    ]:
        shutil.copytree(
            src,
            gallery_path / 'static', dirs_exist_ok=True
        )
    (gallery_path / 'static' / 'README.md').unlink()


def pagination_controls(page_num, total_pages, url_for_page_num):
    controls = []

    def add(page_i, special_page_name=None):
        if special_page_name:
            name = special_page_name
        else:
            name = str(page_i+1)
        enabled = page_i >= 0 and page_i < total_pages and page_i != page_num
        url = url_for_page_num(page_i) if enabled else None
        controls.append({
            "name": name,
            "enabled": enabled,
            "current_page": not (special_page_name) and page_i == page_num,
            "url": url
        })
    # No reason to show any controls at all if there only is one page
    if total_pages == 1:
        return []
    # 0 .. nside page_num nside .. total_pages-1
    n_side = 4
    total_controls = 5 + 2 * n_side
    if total_pages <= total_controls:
        add(page_num - 1, 'Previous')
        for i in range(total_pages):
            add(i)
        add(page_num + 1, 'Next')
        return controls

    div = {
        "name": '..',
        "enabled": False,
        "current_page": False,
        "url": None,
    }

    add(page_num - 1, 'Previous')
    add(0)
    if page_num < 3 + n_side:
        win_begin = 1
        win_end = total_controls - 2
    elif page_num > total_pages - 3 - n_side:
        win_begin = total_pages - total_controls + 2
        win_end = total_pages - 1
    else:
        win_begin = page_num - n_side
        win_end = page_num + n_side + 1

    if win_begin > 2:
        controls.append(div)
    for i in range(win_begin, win_end):
        add(i)
    if win_end < total_pages - 1:
        controls.append(div)
    add(total_pages-1)

    add(page_num + 1, 'Next')
    return controls
