import unittest

from gallerator import url_strategy


class DirectoryPageUrlStrategyTest(unittest.TestCase):
    def setUp(self):
        self.strategy = url_strategy.DirectoryPageUrlStrategy()

    def test_root(self):
        self.assertEqual(
            self.strategy.page_url([]),
            'index.html'
        )

    def test_page_num_root(self):
        self.assertEqual(
            self.strategy.page_url([], 2),
            'page003.html'
        )
        
    def test_single_path(self):
        self.assertEqual(
            self.strategy.page_url(['singlepath']),
            'singlepath/index.html'
        )

    def test_single_path_underscore(self):
        self.assertEqual(
            self.strategy.page_url(['single_path']),
            'single_path/index.html'
        )

    def test_multiple_path_underscore(self):
        self.assertEqual(
            self.strategy.page_url(['path_1', 'path_2']),
            'path_1/path_2/index.html'
        )

    def test_page_num(self):
        self.assertEqual(
            self.strategy.page_url(['path_1', 'path_2'], 2),
            'path_1/path_2/page003.html'
        )

class UnderscorePageUrlStrategyTest(unittest.TestCase):
    def setUp(self):
        self.strategy = url_strategy.UnderscorePageUrlStrategy()

    def test_root(self):
        self.assertEqual(
            self.strategy.page_url([]),
            'index.html'
        )

    def test_page_num_root(self):
        self.assertEqual(
            self.strategy.page_url([], 2),
            'index_page003.html'
        )
        
    def test_single_path(self):
        self.assertEqual(
            self.strategy.page_url(['singlepath']),
            'singlepath.html'
        )

    def test_single_path_underscore(self):
        self.assertEqual(
            self.strategy.page_url(['single_path']),
            'single__path.html'
        )

    def test_multiple_path_underscore(self):
        self.assertEqual(
            self.strategy.page_url(['path_1', 'path_2']),
            'path__1_path__2.html'
        )

    def test_page_num(self):
        self.assertEqual(
            self.strategy.page_url(['path_1', 'path_2'], 2),
            'path__1_path__2_page003.html'
        )
