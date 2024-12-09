import argparse
import json
import sys
from pathlib import Path

from gallerator import data_types, renderer
from gallerator.renderers import renderer_util

description = """
These are the arguments for the nanogallery2 renderer.
Beware of its license.
"""


height_help = """
The height of the thumbnails.
"""

not_downloaded_message = """
**************************************************************
* !!! Nanogallery2 distribution files could not be found !!! *
**************************************************************

It looks like the nanogallery2 distribution files have not
been downoaded. They are needed but not included with this
distribution due to their GPLv3 license.

If you have the source checked out, you can run

    make download-nanogallery2

from the top-level directory, or run

    $module)location/renderers/nanogallery2/download.sh

if you have installed the module with by some other means (e.g. pip), this could
be something like:

    ./venv/lib/python3.12/site-packages/gallerator/renderers/nanogallery2/download.sh
"""

def json_dumps_media_items(media_items, relative_url):
    items = []
    for i in media_items:
        item = {
            "title": i.title,
            "src": relative_url(i.image.path),
            "srct": relative_url(i.thumbnail.path),
        }
        if i.video is not None:
            item['customData'] = {"video": relative_url(i.video)}
        items.append(item)
    return json.dumps(items, indent=4)


class Nanongallery2(renderer.Renderer):
    def __init__(self):
        self.jenv = renderer_util.jinja2_env(
            Path(__file__).parent / 'templates')

    def add_argparse_args(self, parser: argparse.ArgumentParser):
        group = parser.add_argument_group(
            'nanogallery2', description=description)
        group.add_argument('--height', default=300, help=height_help)

    def render(self, template_vars: data_types.TemplateVars):
        template = self.jenv.get_template("page.html")
        render_vars = template_vars.__dict__
        render_vars["media_items_json"] = json_dumps_media_items(
            template_vars.media_items,
            template_vars.relative_url,
        )
        render_vars['thumbnail_height'] = self.args.height
        return template.render(render_vars)

    def copy_static(self, gallery_path: Path):
        static = Path(__file__).parent / 'static'
        if not (static / 'jquery.nanogallery2.min.js').exists():
            print(not_downloaded_message, file=sys.stderr)            
            sys.exit(1)
        renderer_util.copy_static(
            static, gallery_path)


def renderer() -> renderer.Renderer:
    return Nanongallery2()
