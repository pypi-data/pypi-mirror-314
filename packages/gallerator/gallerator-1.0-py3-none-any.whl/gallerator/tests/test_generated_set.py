import hashlib
import os
import tempfile
import unittest
from pathlib import Path

from gallerator import constants, generated_set


def expected_file_digest(path):
    with open(path, 'rb', buffering=0) as f:
        digest = hashlib.file_digest(f, constants.digest).hexdigest()
    return digest


class TestGeneratedSetImpl(generated_set.GeneratedSet):
    """Test instance of generated set that implements generated_path()"""

    def generated_file_prefix(self):
        return "test"

    def create_file(self, source, destination):
        with open(destination, 'w') as f:
            f.write(f'A file for {source}')


class GeneratedSetTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.source_path = Path(__file__).parent / '../../../../demo-gallerator/media'
        self.sample_images = list(self.source_path.glob('*.jpg'))
        self.sample_videos = sorted(
            list((self.source_path / 'Videos').glob('*.mp4')))
        self.assertTrue(self.source_path.exists())
        self.assertGreater(len(self.sample_images), 0)
        self.assertGreater(len(self.sample_videos), 0)

        self.tempdir = tempfile.TemporaryDirectory(
            prefix="gallerator-" + self._testMethodName,
            delete=not (self.keep_test_data()))
        self.output_dir = Path(self.tempdir.name)
        if self.keep_test_data():
            print('Keeping test data in %s' % self.output_dir)

        return super().setUp()

    def tearDown(self) -> None:
        if not (self.keep_test_data()):
            self.tempdir.cleanup()
        return super().tearDown()

    def keep_test_data(self):
        return "KEEPTESTDATA" in os.environ and os.environ["KEEPTESTDATA"]


class TestGeneratedSet(GeneratedSetTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.generatedset = TestGeneratedSetImpl(self.output_dir)

    def test_digests(self):
        expected = [expected_file_digest(
            self.source_path / f) for f in self.sample_images[0:2]]
        actual = [self.generatedset.digest(
            f) for f in self.sample_images[0:2]]
        self.assertEqual(actual, expected)

    def test_divergence(self):
        bogus_test_file = self.output_dir / \
            f'test-{expected_file_digest(__file__)}.txt'
        with open(bogus_test_file, 'w') as f:
            f.write('bogus contents')
        for i in range(2):
            self.generatedset.register_source(self.sample_images[i])
        missing, obsolete = self.generatedset.divergence()
        self.assertEqual(
            (missing, obsolete,),
            ([self.output_dir / f for f in self.sample_images[0:2]],
             [bogus_test_file],)
        )
        self.generatedset.create_missing(missing)
        self.generatedset.unlink_obsolete(obsolete)
        missing, obsolete = self.generatedset.divergence()
        self.assertEqual(
            (missing, obsolete,),
            ([], [],)
        )

    def test_paths(self):
        expected = []
        for f in self.sample_images[0:2]:
            digest = expected_file_digest(self.source_path / f)
            path = "%s/test-%s.jpg" % (self.output_dir, digest)
            expected.append(Path(path))
            # self.generatedset.thumbnail_path
        actual = [self.generatedset.generated_path(
            f) for f in self.sample_images[0:2]]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
