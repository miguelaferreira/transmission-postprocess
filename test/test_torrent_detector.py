import unittest
from tempfile import NamedTemporaryFile, mkdtemp

from trdone.torrent_detector import TorrentDetector


class TestTorrentDetector(unittest.TestCase):
    def test_is_directory_when_it_is_a_file(self):
        tmp_file = NamedTemporaryFile()
        detector = TorrentDetector(tmp_file.name)

        self.assertFalse(detector.is_directory())

    def test_is_directory_when_it_is_a_directory(self):
        tmp_dir = mkdtemp()
        detector = TorrentDetector(tmp_dir)

        self.assertTrue(detector.is_directory())

    def test_has_archive_when_rar_is_present(self):
        tmp_dir = mkdtemp()
        _ = NamedTemporaryFile(suffix='.rar', dir=tmp_dir)
        detector = TorrentDetector(tmp_dir)

        self.assertTrue(detector.has_archive())

    def test_has_archive_when_partial_rar_is_present(self):
        tmp_dir = mkdtemp()
        _ = NamedTemporaryFile(suffix='.r01', dir=tmp_dir)
        detector = TorrentDetector(tmp_dir)

        self.assertTrue(detector.has_archive())

    def test_has_archive_when_zip_is_present(self):
        tmp_dir = mkdtemp()
        _ = NamedTemporaryFile(suffix='.zip', dir=tmp_dir)
        detector = TorrentDetector(tmp_dir)

        self.assertTrue(detector.has_archive())
