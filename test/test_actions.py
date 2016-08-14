import unittest
from os import listdir
from os.path import basename, dirname, realpath
from tempfile import NamedTemporaryFile, mkdtemp

from trdone.actions import CopyAction, FileAction, MoveAction, UnrarAction


class TestFileAction(unittest.TestCase):
    def test_is_file_when_it_is_a_file(self):
        tmp_file = NamedTemporaryFile()

        self.assertTrue(FileAction._is_file(tmp_file.name))

    def test_is_file_when_it_is_a_directory(self):
        tmp_dir = mkdtemp()

        self.assertFalse(FileAction._is_file(tmp_dir))


class TestCopyAction(unittest.TestCase):
    def test_run_when_src_is_a_file(self):
        source = NamedTemporaryFile()
        target = mkdtemp()
        action = CopyAction(source.name, target)

        action.run()

        self.assertTrue(basename(source.name) in listdir(target))

    def test_run_when_src_is_a_directory(self):
        source = mkdtemp()
        target = mkdtemp()
        action = CopyAction(source, target)

        action.run()

        self.assertTrue(basename(source) in listdir(target))


class TestMoveAction(unittest.TestCase):
    def test_run_when_src_is_a_file(self):
        source = NamedTemporaryFile()
        target = mkdtemp()
        action = MoveAction(source.name, target)

        action.run()

        self.assertTrue(basename(source.name) in listdir(target))
        self.assertTrue(basename(source.name) not in listdir(dirname(source.name)))

    def test_run_when_src_is_a_directory(self):
        source = mkdtemp()
        tmp_file = NamedTemporaryFile(dir=source)
        target = mkdtemp()
        action = MoveAction(source, target)

        action.run()

        self.assertTrue(basename(source) in listdir(target))
        self.assertTrue(basename(tmp_file.name) in listdir(target + '/' + basename(source)))
        self.assertTrue(basename(source) not in listdir(dirname(source)))


class TestUnrarAction(unittest.TestCase):
    def test_run(self):
        target = mkdtemp()
        pwd = dirname(realpath(__file__))
        action = UnrarAction(pwd + '/file.rar', target)

        action.run()

        self.assertTrue('file.txt' in listdir(target))
