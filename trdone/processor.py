from os import listdir, mkdir
from os.path import basename

from actions import UnrarAction, CopyAction, NoAction
from log import init_logger
from path_mapper import PathMapper
from torrent_detector import isdir, TorrentDetector


def process_torrent(torrent, destination, path_mapping={}):
    processor = Processor(torrent, destination, path_mapping)
    processor.process()
    processor.execute()


class Processor(object):
    def __init__(self, torrent, destination, path_mapping={}):
        super(Processor, self).__init__()
        path_mapper = PathMapper(path_mapping)
        self.torrent = path_mapper.map(torrent)
        self.destination = destination
        self.actions = []
        self.logger = init_logger('Processor')

    def process(self):
        self.logger.info("Processing torrent %s to %s" % (self.torrent, self.destination))
        if isdir(self.torrent):
            files_in_torrent = listdir(self.torrent)
            self.logger.info("Since torrent is a directory I will iterate over all files (count %s)" % len(files_in_torrent))
            torrent_dir_name = basename(self.torrent)
            target_directory = self._build_path(self.destination, torrent_dir_name)
            mkdir(target_directory)
            self.actions = [self._process_file(self._build_path(self.torrent, f), target_directory) for f in files_in_torrent]
        else:
            self.actions = [self._process_file(self.torrent, self.destination)]

    def execute(self):
        self.logger.info("Executing %s actions" % len(self.actions))
        for action in self.actions:
            action.run()

    @staticmethod
    def _build_path(base, name):
        return base + '/' + name

    def _process_file(self, file_to_process, target_directory):
        if isdir(file_to_process):
            self.logger.info("Ignoring directory %s" % file_to_process)
            return NoAction(file_to_process, target_directory)
        if TorrentDetector.is_archive(file_to_process):
            self.logger.info("Creating action to unrar %s" % file_to_process)
            return UnrarAction(file_to_process, target_directory)
        else:
            self.logger.info("Creating action to copy %s" % file_to_process)
            return CopyAction(file_to_process, target_directory)
