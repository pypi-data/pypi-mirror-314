from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable


class MediaType(Enum):
    UNKNOWN = 1
    IMAGE = 2
    VIDEO = 3


@dataclass
class ImageInfo:
    path: Path
    width: int
    height: int

@dataclass
class MediaItem:
    """
        Representation of a gallery media item. Uses absolute paths for files.
    """
    type: MediaType
    title: str
    thumbnail: ImageInfo
    image: ImageInfo
    source: Path
    video: Path | None


@dataclass
class Directory:
    """
        Representation of a gallery directory. Uses absolute paths for files.
    """
    name: str
    path_segments: list[str]
    items: list[MediaItem] = field(default_factory=list)
    subdirectories: "dict[Directory]" = field(default_factory=dict)

@dataclass
class Breadcrumb:
    name: str
    path_segments: list[str]

@dataclass
class TemplateVars:
    gallery_name: str
    gallery_root_url: str
    parent: Directory | None
    # Each element contains a name and a url
    breadcrumbs: list[Breadcrumb]
    media_items: list[MediaItem]
    subdirectories: list[Directory]
    path_segments_to_url: Callable[[list[Path]],str]
    relative_url: Callable[[Path],str]
    # 0 based - first page has page_num = 0
    page_num: int
    # total_pages == 1 (and page_num = 0) if pagination is disabled
    total_pages: int
    url_for_page_num: Callable[[int],str]
