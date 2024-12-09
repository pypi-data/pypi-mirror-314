from pathlib import Path

from . import constants, data_types, media_items, url_strategy


def create_template_vars_plural(
    gallery_name: str,
    gallery_path: Path,
    directory: data_types.Directory,
    parent: data_types.Directory,
    page_url_strategy: url_strategy.PageUrlStrategy,
    pagination: int,
):
    subdirectories = []
    for dir in sorted(directory.subdirectories):
        subdirectories.append(directory.subdirectories[dir])

    breadcrumbs = [
        data_types.Breadcrumb(
            name=gallery_name,
            path_segments=[]
        )
    ]
    path_segments_so_far = []
    for p in directory.path_segments:
        path_segments_so_far.append(p)
        breadcrumbs.append(data_types.Breadcrumb(
            name=p,
            path_segments=path_segments_so_far.copy(),
        ))

    # This is the absolute linux path of the current "directory", not the
    # current directory of the running python process.
    current_dir = (
        gallery_path / page_url_strategy.page_url(directory.path_segments)
    ).parent

    def path_segments_to_url(path_segments: list[Path]) -> str:
        abs_page = gallery_path / page_url_strategy.page_url(path_segments)
        return str(abs_page.relative_to(current_dir, walk_up=True))

    def relative_url(path: Path) -> str:
        return str(path.relative_to(current_dir, walk_up=True))

    def url_for_page_num(page_num: int) -> str:
        abs_page = gallery_path / page_url_strategy.page_url(
            directory.path_segments, page_num
        )
        return str(abs_page.relative_to(current_dir, walk_up=True))

    current_media_item_index = 0
    template_vars_plural = []

    def append_template_vars_plural(items, page_num, total_pages):
        template_vars = data_types.TemplateVars(
            gallery_name=gallery_name,
            gallery_root_url=str(gallery_path.relative_to(
                current_dir, walk_up=True)),
            parent=parent,
            breadcrumbs=breadcrumbs,
            media_items=items,
            subdirectories=subdirectories,
            path_segments_to_url=path_segments_to_url,
            relative_url=relative_url,
            page_num=page_num,
            total_pages=total_pages,
            url_for_page_num=url_for_page_num,
        )
        template_vars_plural.append(template_vars)

    # Some very large number to ensure we don't create more than one page
    if pagination is None or pagination == 0:
        pagination = 100000000

    if len(directory.items) == 0:
        # Every directory needs at least one page
        append_template_vars_plural([], 0, 1)
    else:
        total_pages = 1 + int(len(directory.items) / pagination)
        page_num = 0
        while current_media_item_index < len(directory.items):
            remaining = len(directory.items) - current_media_item_index
            nr_items = min(remaining, pagination)
            items = directory.items[current_media_item_index:
                                    current_media_item_index + nr_items]
            append_template_vars_plural(items, page_num, total_pages)
            current_media_item_index += nr_items
            page_num += 1

    return template_vars_plural


def write_gallery_directory(renderer,
                            gallery_name: str,
                            gallery_path: Path,
                            directory: data_types.Directory,
                            parent: data_types.Directory | None,
                            page_url_strategy: url_strategy.PageUrlStrategy,
                            pagination: int | None):
    template_vars_plural = create_template_vars_plural(
        gallery_name,
        gallery_path,
        directory,
        parent,
        page_url_strategy,
        pagination,
    )
    for template_vars in template_vars_plural:
        fname = gallery_path / \
            page_url_strategy.page_url(
                directory.path_segments, template_vars.page_num)
        fname.parent.mkdir(exist_ok=True)
        print(f'Creating {fname}')
        html = renderer.render(template_vars)
        with open(fname, 'w') as file:
            file.write(html)
    # recursive!
    for subdir in directory.subdirectories:
        write_gallery_directory(renderer,
                                gallery_name,
                                gallery_path,
                                directory.subdirectories[subdir],
                                directory,
                                page_url_strategy,
                                pagination)


def write_gallery(
        gallery_name,
        src_path,
        gallery_path,
        recursive,
        renderer,
        pagination):

    root = media_items.create_directory_media(
        src_path, gallery_path, recursive)

    # page_url_strategy = url_strategy.UnderscorePageUrlStrategy()
    page_url_strategy = url_strategy.DirectoryPageUrlStrategy()

    write_gallery_directory(
        renderer,
        gallery_name,
        gallery_path,
        root,
        None,
        page_url_strategy,
        pagination
    )

    print(f"Copying static files to {gallery_path}")
    renderer.copy_static(gallery_path)
