from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image

from . import constants, data_types, video_images
from . import thumbnails as thumbnails_module

image_suffixes = {'.' + ext for ext in {
    "png",
    "jpg",
    "jpeg",
    "bmp",
    "gif",
    "svg"
}}

video_suffixes = {'.' + ext for ext in {
    "avi",
    "mp4",
    "wmv",
    "mov",
    "ram"
}}


def determine_media_type(path):
    """Determine the media type of path, perhaps being UKNOWN"""
    suffix = path.suffix.lower()
    if suffix in image_suffixes:
        return data_types.MediaType.IMAGE
    elif suffix in video_suffixes:
        return data_types.MediaType.VIDEO
    else:
        return data_types.MediaType.UNKNOWN

def determine_known_media_type(path):
    """Determine the media type of path, UKNOWN being an error"""
    mediatype = determine_media_type(path)
    if mediatype == data_types.MediaType.UNKNOWN:
        raise ValueError(f"{path} does not have a known file extension")
    return mediatype



def find_media(src_path: Path, recursive: bool) -> list[Path]:
    media = []
    for root, dirs, files in src_path.walk():
        if recursive:
            # Skip over any _generated-images directories so we don't make
            # thumbnails of thumnails ad nauseam.
            if constants.generated_dir_basename in dirs:
                dirs.remove(constants.generated_dir_basename)
            # Skip over any static directories containing a favicon.ico,
            # assuming they've been created by the gallery on a previous run.
            # Yeah, this is a little ugly, with a hardcoded file name and all. I
            # just couldn't bring myself to make 'static' a constant and
            # incorporate it in templates and everything. So it is what it is.
            # Patches welcome.
            if 'static' in dirs and (root / 'static' / 'favicon.ico').exists():
                dirs.remove('static')
        else:
            # If not recursive, don't go into any subdirs
            dirs.clear()
        for f in files:
            fpath = root / f
            if determine_media_type(fpath) == data_types.MediaType.UNKNOWN:
                continue
            media.append(fpath)
    return sorted(media)


def group_media_in_directories(media: list[Path], src_path):
    directories = {}
    for path in sorted(media):
        dir = str(path.parent.relative_to(src_path))
        # special case for the root of the tree
        if dir == '.':
            dir = ''
        directories[dir] = directories.get(dir, []) + [path]
    return directories


@dataclass
class DerivedMedia:
    thumbnails: thumbnails_module.Thumbnails
    video_samples: video_images.VideoSamples
    video_contact_sheets: video_images.VideoContactSheets


def register_derived_media(media, generated_dir):
    thumbnails = thumbnails_module.Thumbnails(generated_dir)
    video_samples = video_images.VideoSamples(generated_dir)
    video_contact_sheets = video_images.VideoContactSheets(generated_dir)
    for path in media:
        match determine_known_media_type(path):
            case data_types.MediaType.IMAGE:
                thumbnails.register_source(path)
            case data_types.MediaType.VIDEO:
                video_samples.register_source(path)
                video_contact_sheets.register_source(path)
            case _:
                raise RuntimeError(f"Unknown type for {path}")
    return DerivedMedia(
        thumbnails=thumbnails,
        video_samples=video_samples,
        video_contact_sheets=video_contact_sheets)


def create_image_info(abs_path):
    im = Image.open(abs_path)
    width, height = im.size
    return data_types.ImageInfo(
        path = abs_path,
        width = width,
        height = height,
    )



def create_media_items(media, derived_media, gallery_path):
    items = []
    for path in media:
        type = determine_known_media_type(path)
        match type:
            case data_types.MediaType.IMAGE:
                thumbnail = derived_media.thumbnails.generated_path(path)
                image = path
                video = None
            case data_types.MediaType.VIDEO:
                thumbnail = derived_media.video_samples.generated_path(path)
                image = derived_media.video_contact_sheets.generated_path(path)
                video = path
            case _:
                raise ValueError(f"Uknown type for {path}")
        item = data_types.MediaItem(
            type=type,
            title=path.name,
            thumbnail=create_image_info(thumbnail),
            image=create_image_info(image),
            source=path,
            video=video
        )
        items.append(item)
    return items


def create_missing_media(derived_media):
    for (disp, obj) in [
        ('Thumbnails', derived_media.thumbnails),
        ('Video Samples', derived_media.video_samples),
        ('Video Contact Sheets', derived_media.video_contact_sheets),
    ]:
        missing, obsolete = obj.divergence()
        if len(missing) > 0:
            print(f"Creating {len(missing)} missing {disp}")
            obj.create_missing(missing)
        if len(obsolete) > 0:
            print(f"Removing {len(obsolete)} obsolete {disp}")
            obj.unlink_obsolete(obsolete)


def create_directory_media(
    src_path: Path,
    gallery_path: Path,
    recursive=True):
    media = find_media(src_path, recursive)
    generated_dir = gallery_path / constants.generated_dir_basename
    derived_media = register_derived_media(media, generated_dir)
    create_missing_media(derived_media)
    directory_media = group_media_in_directories(media, src_path)
    flat_directory_items = {}
    for directory in directory_media:
        flat_directory_items[directory] = create_media_items(
            directory_media[directory], derived_media, gallery_path)

    directory_names = sorted(list(directory_media.keys()))
    if '' in flat_directory_items:
        root_items = flat_directory_items['']
    else:
        root_items = []
    root = data_types.Directory(name='', path_segments=[], items=root_items)
    for dir in directory_names:
        # already setup root
        if dir == '':
            continue
        current_dir = root
        current_path_segments = []
        for part in Path(dir).parts:
            current_path_segments.append(part)
            if part not in current_dir.subdirectories:
                current_dir.subdirectories[part] = data_types.Directory(
                    name=part, path_segments=current_path_segments.copy()
                )
            current_dir = current_dir.subdirectories[part]
        current_dir.items = flat_directory_items[dir]
    return root


if __name__ == "__main__":
    sample = Path(__file__).parent.parent.parent / "sample"
    gallery_path = sample.parent / 'gallery'
    root = create_directory_media(sample, gallery_path, True)

    print(root)
