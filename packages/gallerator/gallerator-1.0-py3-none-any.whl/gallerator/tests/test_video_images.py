from gallerator import video_images
from gallerator.tests.test_generated_set import GeneratedSetTestCase


class TestVideoSamples(GeneratedSetTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.video_samples = video_images.VideoSamples(self.output_dir)

    def test_create_missing_video_samples(self):
        for i in range(2):
            self.video_samples.register_source(self.sample_videos[i])
        missing, obsolete = self.video_samples.divergence()
        self.video_samples.create_missing(missing)
        for i in range(2):
            path = self.video_samples.generated_path(self.sample_videos[i])
            self.assertTrue(path.exists())
        self.assertEqual(
            self.video_samples.divergence(),
            ([], [],)
        )

class TestVideoContactSheets(GeneratedSetTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.video_contact_sheets = \
            video_images.VideoContactSheets(self.output_dir)

    def test_create_missing_contact_sheets(self):
        for i in range(2):
            self.video_contact_sheets.register_source(self.sample_videos[i])
        missing, obsolete = self.video_contact_sheets.divergence()
        self.video_contact_sheets.create_missing(missing)
        for i in range(2):
            path = self.video_contact_sheets.generated_path(self.sample_videos[i])
            self.assertTrue(path.exists())
        self.assertEqual(
            self.video_contact_sheets.divergence(),
            ([], [],)
        )
