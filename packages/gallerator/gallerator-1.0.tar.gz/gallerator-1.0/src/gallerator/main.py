import argparse
from pathlib import Path

from . import constants, data_types, dynimport, gallery

from .renderer import Renderer
gallery_name_help = '''
The name of the gallery. Defaults the base name of the 'source_dir'.
'''

source_dir_help = f'''
The directory containing the source images and videos over which we want to
create a gallery.
'''

gallery_dir_help = '''
The directory in which to store the generated gallery. Defaults to the same as
the 'source_dir' containing the images.

Note that this directory should be "close" to the `source_dir` since relative
paths are used when referencing source images from the gallery or you'll get
many '../' elements in the image paths.
'''

recursive_help = '''
Whether to search for image and video files recursively.
'''

renderer_help = '''
Which renderer to use to actually produce the output galleries. At the moment,
there are two built-in ones: "PhotoSwipe" and "nanogallery2". Advanced: Other
values will be loaded as a module that is expected to have a renderer() method
that returns an instance of gallerator.data_types.Renderer. That way you can
render the gallery exactly like you want.
'''

pagination_help = '''
The maximum number of images per page. 0 means unlimited.
'''


def get_renderer(renderer_arg):
    def get_renderer(path):
        if not Path(path).exists():
            raise FileNotFoundError(path)
        module = dynimport.import_random_module_from_path(path)
        if not hasattr(module, 'renderer'):
            raise ValueError(
                f'Renderer {path} does not have a renderer method')
        renderer = module.renderer()
        if not isinstance(renderer, Renderer):
            raise ValueError(
                f'Renderer {path}.render() does not return a Renderer instance')
        return renderer

    match renderer_arg:
        case "PhotoSwipe":
            return get_renderer(
                Path(__file__).parent / "renderers" /
                "photoswipe" / "photoswipe.py")
        case "nanogallery2":
            return get_renderer(
                Path(__file__).parent / "renderers" /
                "nanogallery2" / "nanogallery2.py")
        case _:
            return get_renderer(renderer_arg)


def parse_args():
    def add_renderer_argument(parser):
        parser.add_argument(
            '--renderer', default='PhotoSwipe', help=renderer_help)

    preparser = argparse.ArgumentParser(
        prog='gallerator',
        add_help=False
    )
    add_renderer_argument(preparser)
    preargs, _ = preparser.parse_known_args()
    renderer = get_renderer(preargs.renderer)

    parser = argparse.ArgumentParser(
        prog='gallerator',
        description='Create static thumbnail galleries',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('source_dir', help=source_dir_help)
    parser.add_argument('--name-of-gallery',
                        help=gallery_name_help, default=None)
    parser.add_argument('--gallery-dir', '-g',
                        help=gallery_dir_help, default=None)
    parser.add_argument('--recursive', '-r', help=recursive_help,
                        default=False, action='store_true')
    parser.add_argument('--pagination', '-p',
                        type=int,
                        default=0, help=pagination_help)
    add_renderer_argument(parser)

    renderer.add_argparse_args(parser)

    args = parser.parse_args()

    renderer.update_args(args)

    return args, renderer


def cli_main():
    args, renderer = parse_args()
    if args.name_of_gallery is None:
        gallery_name = Path(args.source_dir).stem
    else:
        gallery_name = args.name_of_gallery
    if args.gallery_dir is None:
        gallery_dir = args.source_dir
    else:
        gallery_dir = args.gallery_dir
    gallery.write_gallery(
        gallery_name,
        Path(args.source_dir).absolute(),
        Path(gallery_dir).absolute(),
        args.recursive,
        renderer,
        args.pagination)
