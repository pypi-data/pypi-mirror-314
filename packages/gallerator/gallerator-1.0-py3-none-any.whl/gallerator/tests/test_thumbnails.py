import unittest

from gallerator import thumbnails
from gallerator.tests.test_generated_set import GeneratedSetTestCase


class TestThumbnails(GeneratedSetTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.thumbnails = thumbnails.Thumbnails(self.output_dir)

    def test_create_missing(self):
        for i in range(2):
            self.thumbnails.register_source(self.sample_images[i])
        missing, obsolete = self.thumbnails.divergence()
        self.thumbnails.create_missing(missing)
        def expected1(f):
            digest = self.thumbnails.digest(f)
            return self.output_dir / ('thumb-%s.jpg' % digest)
        expected = [expected1(f) for f in self.sample_images[0:2]]
        actual = list(self.output_dir.glob('*'))
        self.assertEqual(actual, expected)
        self.assertEqual(
            self.thumbnails.divergence(),
            ([], [],)
        )

if __name__ == '__main__':
    unittest.main()
