from os import listdir
from os.path import isdir
from re import search


class TorrentDetector(object):
    def __init__(self, torrent):
        super(TorrentDetector, self).__init__()
        self.torrent = torrent

    def is_directory(self):
        return isdir(self.torrent)

    def has_archive(self):
        if not self.is_directory():
            raise ValueError("Can't list files of a file %s" % self.torrent)
        files = listdir(self.torrent)
        return len([f for f in files if self.is_archive(f)]) > 0

    @staticmethod
    def is_archive(f):
        return search(r'(\.rar|\.r[0-9]+|\.zip)+$', f) is not None
