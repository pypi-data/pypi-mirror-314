from pathlib import Path

import argparse
import re

from gallerator import constants, data_types, renderer
from gallerator.renderers import renderer_util

description = """
These are the arguments for Photoswipe, the default renderer. Different
renderers have different options, so try "--renderer name-of-renderer --help" to
see options for other renderers.
"""

justified_help = """
Use a justified layout (the default), where all images have the same height, but
the width depends on the image. This is the most dense but different pages may
not have the same height if used with pagination, so perhaps one other layouts
are better with pagination.
"""

auto_grid_help = """
Use a grid layout but fit as many columns as will fit depending on screen width.
"""

grid_help = """
By default, Photoswipe uses a justified layout, but this will create a grid
layout. Try e.g. "--grid 4x5", for 4 columns by 5 rows, but supply your own
"XxY" value to set your own grid layout. This will override any --pagination
value. Beware that this is not responsive, so it will either be too wide on
mobile or too narrow for large desktop users, or both.
"""

width_help = """
The width of the thumbnails. Only used by --auto-grid and --grid
"""

height_help = """
The height of the thumbnails.
"""
no_filename_captions_help = """
Don't add the filenames of the images as a caption in the thumbnail gallery.
This makes it look cleaner (especially for --grid and --auto-grid), but less
information for the user. When the full image is shown in a lightbox, the file
name is always shown, regardless of this setting.
"""


class Photoswipe(renderer.Renderer):
    def __init__(self):
        self.jenv = renderer_util.jinja2_env(
            Path(__file__).parent / 'templates')

    def add_argparse_args(self, parser: argparse.ArgumentParser):
        group = parser.add_argument_group(
            'Photoswipe', description=description)
        group.add_argument('--justified', action='store_true', help=grid_help)
        group.add_argument('--auto-grid', action='store_true', help=grid_help)
        group.add_argument('--grid', help=grid_help)
        group.add_argument('--width', default=300, help=width_help)
        group.add_argument('--height', default=300, help=height_help)
        group.add_argument('--no-filename-captions',
                           action="store_true", help=no_filename_captions_help)

    def _set_grid_dimensions(self, args):
        self.grid = None
        if args.grid is not None:
            matches = re.match(r'^(\d+)x(\d+)$', args.grid)
            if matches is None:
                raise ValueError(
                    "Please sepecify --grid as XxY, where X and Y are "
                    "integers, e.g. 4x5"
                )
            x = int(matches[1])
            y = int(matches[2])
            args.pagination = x * y
            self.grid = {
                "type": "fixed-columns",
                "x": x,
                "y": y,
            }
        elif args.auto_grid:
            self.grid = {
                "type": "auto",
            }

    def update_args(self, args: argparse.Namespace):
        self._set_grid_dimensions(args)
        super().update_args(args)

    def render(self, template_vars: data_types.TemplateVars):
        pagination = renderer_util.pagination_controls(
            template_vars.page_num,
            template_vars.total_pages,
            template_vars.url_for_page_num
        )
        template = self.jenv.get_template("page.html")
        vars = template_vars.__dict__.copy()
        vars.update({
            'data_types': data_types,
            'layout': 'justified' if self.grid is None else 'grid',
            'pagination': pagination,
        })
        return template.render(vars)

    def copy_static(self, gallery_path: Path):
        renderer_util.copy_static(
            Path(__file__).parent / 'static', gallery_path)
        template = self.jenv.get_template('page.css')
        with open(gallery_path / 'static' / 'page.css', 'w') as f:
            f.write(template.render(
                thumbnail_height=self.args.height,
                thumbnail_width=self.args.width,
                grid=self.grid,
                filename_captions=not(self.args.no_filename_captions)
            ))


def renderer() -> renderer.Renderer:
    return Photoswipe()
