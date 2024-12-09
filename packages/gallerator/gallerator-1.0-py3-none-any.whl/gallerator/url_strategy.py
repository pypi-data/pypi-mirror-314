import re
from pathlib import Path


class PageUrlStrategy:
    def page_url(self, paths: list[Path], page_num: int = 0) -> str:
        """page_num is zero based"""
        raise NotImplementedError


class DirectoryPageUrlStrategy(PageUrlStrategy):
    def page_url(self, paths: list[Path], page_num: int = 0) -> str:
        """page_num is zero based"""
        local_paths = paths.copy()
        if page_num == 0:
            local_paths.append('index.html')
        else:
            local_paths.append(f'page{page_num+1:03}.html')
        return "/".join(list(local_paths))


class UnderscorePageUrlStrategy(PageUrlStrategy):
    def page_url(self, paths: list[Path], page_num: int = 0) -> str:
        """page_num is zero based"""

        if len(paths) == 0:
            prefix = 'index'
        else:
            # Escape any ":" chars in directory names
            prefix = ("_".join([re.sub(r"_", "__", p) for p in paths]))
        if page_num > 0:
            prefix += f'_page{page_num+1:03}'
        return prefix + '.html'
