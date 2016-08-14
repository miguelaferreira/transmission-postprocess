import unittest
from os import listdir
from os.path import basename, dirname, realpath
from shutil import copy2
from tempfile import NamedTemporaryFile, mkdtemp

from trdone.actions import NoAction, CopyAction, UnrarAction
from trdone.processor import Processor


class TestProcessor(unittest.TestCase):
    def test_process_file_when_it_is_a_directory(self):
        processor = Processor(None, None)
        source = mkdtemp()
        action = processor._process_file(source, None)

        self.assertEquals(action, NoAction(source, None))

    def test_process_file_when_it_is_a_file(self):
        destination = 'destination'
        processor = Processor(None, destination)
        torrent = NamedTemporaryFile()
        action = processor._process_file(torrent.name, destination)

        self.assertEquals(action, CopyAction(torrent.name, destination))

    def test_process_file_when_it_is_an_archive(self):
        destination = 'destination'
        processor = Processor(None, destination)
        torrent = NamedTemporaryFile(suffix='.rar')
        action = processor._process_file(torrent.name, destination)

        self.assertEquals(action, UnrarAction(torrent.name, destination))

    def test_process(self):
        destination = mkdtemp()
        torrent = mkdtemp()
        ignored_dir = mkdtemp(prefix='ignored_dir', dir=torrent)
        some_file = NamedTemporaryFile(prefix='some_file', dir=torrent)
        rar_file = NamedTemporaryFile(suffix='.rar', dir=torrent)
        processor = Processor(torrent, destination)

        processor.process()

        self.assertTrue(len(processor.actions) == 3)
        new_torrent_dir = self._build_path(destination, torrent)
        self.assertTrue(NoAction(ignored_dir, new_torrent_dir) in processor.actions)
        self.assertTrue(CopyAction(some_file.name, new_torrent_dir) in processor.actions)
        self.assertTrue(UnrarAction(rar_file.name, new_torrent_dir) in processor.actions)

    def test_process_when_paths_are_mapped(self):
        destination = mkdtemp()
        torrent_base = mkdtemp()
        torrent = mkdtemp(dir=torrent_base)
        path_mapping = {'some_base': torrent_base}
        ignored_dir = mkdtemp(prefix='ignored_dir', dir=torrent)
        some_file = NamedTemporaryFile(prefix='some_file', dir=torrent)
        rar_file = NamedTemporaryFile(suffix='.rar', dir=torrent)
        processor = Processor(self._build_path('some_base', basename(torrent)), destination, path_mapping)

        processor.process()

        self.assertTrue(len(processor.actions) == 3)
        new_torrent_dir = self._build_path(destination, torrent)
        self.assertTrue(NoAction(ignored_dir, new_torrent_dir) in processor.actions)
        self.assertTrue(CopyAction(some_file.name, new_torrent_dir) in processor.actions)
        self.assertTrue(UnrarAction(rar_file.name, new_torrent_dir) in processor.actions)

    def test_execute(self):
        pwd = dirname(realpath(__file__))
        destination = mkdtemp()
        torrent = mkdtemp()
        copy2(self._build_path(pwd, 'file.rar'), torrent)
        _ = mkdtemp(prefix='ignored_dir', dir=torrent)
        some_file = NamedTemporaryFile(prefix='some_file', dir=torrent)
        _ = torrent + '/file.rar'
        processor = Processor(torrent, destination)
        processor.process()

        processor.execute()

        new_torrent_dir = listdir(self._build_path(destination, torrent))
        self.assertTrue(basename(torrent) in listdir(destination))
        self.assertTrue(basename(some_file.name) in new_torrent_dir)
        self.assertTrue('file.txt' in new_torrent_dir)
        self.assertTrue('file.rar' not in new_torrent_dir)

    @staticmethod
    def _build_path(destination, torrent):
        return destination + '/' + basename(torrent)
