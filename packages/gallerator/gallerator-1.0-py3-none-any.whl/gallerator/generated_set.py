import hashlib
from pathlib import Path

from tqdm import tqdm

from . import constants


class GeneratedSet:
    """
    Bookkeeping for generation of thumbnails and contact sheets.
    """

    def __init__(self, generated_dir):
        self.source_images = []
        self.generated_dir = generated_dir
        # keys are Paths, values are digests
        self.digest_cache = {}

    def register_source(self, image):
        """registers an image for thumnail generation."""
        self.source_images.append(image)

    def divergence(self) -> tuple[list[Path], list[Path]]:
        obsolete = set(self.generated_dir.glob(self.generated_file_prefix() + '-*'))
        missing = []
        for f in self.source_images:
            generated_path = self.generated_path(f)
            obsolete.discard(generated_path)
            if not generated_path.exists():
                missing.append(f)
        return missing, list(obsolete)

    def digest(self, path):
        if path not in self.digest_cache:
            with open(path, 'rb', buffering=0) as f:
                digest = hashlib.file_digest(f, constants.digest).hexdigest()
            self.digest_cache[path] = digest
        return self.digest_cache[path]

    def generated_path(self, fpath):
        digest = self.digest(fpath)
        basename = "%s-%s%s" % (
            self.generated_file_prefix(),
            digest,
            self.generated_file_suffix(fpath))
        return self.generated_dir / basename

    def generated_file_suffix(self, fpath):
        """Default to the same suffix as the source file"""
        return fpath.suffix

    def generated_file_prefix(self):
        raise NotImplementedError

    def create_missing(self, missing):
        self.generated_dir.mkdir(exist_ok=True, parents=True)
        for source in tqdm(missing):
            destination = self.generated_dir / self.generated_path(source)
            # print("creating", source, destination)
            self.create_file(source, destination)

    def unlink_obsolete(self, obsolete):
        for path in obsolete:
            path.unlink()

    def create_file(self, source, destination):
        raise NotImplementedError
