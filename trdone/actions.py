from os.path import isfile, basename, isabs
from shutil import copy2, copytree, move

from unrar.rarfile import RarFile

from log import init_logger


class Action(object):
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.logger = init_logger('Action')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self):
        return "[%s] source=%s target=%s" % (self.__class__.__name__, self.source, self.target)


class NoAction(Action):
    def run(self):
        pass


class FileAction(Action):
    def __init__(self, source, target):
        super(FileAction, self).__init__(source, target)

    @staticmethod
    def _is_file(path):
        return isfile(path)


class CopyAction(FileAction):
    def run(self):
        if self._is_file(self.source):
            self.logger.info("Copying file %s" % self.source)
            copy2(self.source, self.target)
        else:
            self.logger.info("Copying directory %s" % self.source)
            copytree(self.source, self.target + '/' + basename(self.source))


class MoveAction(FileAction):
    def run(self):
        self.logger.info("Moving file %s" % self.source)
        move(self.source, self.target)


class UnrarAction(FileAction):
    def run(self):
        if self.is_main_rar_file(self.source):
            rar_file = RarFile(self.source)
            files = rar_file.NameToInfo.keys()
            for archived_file in files:
                if not isabs(archived_file) and not archived_file.startswith('.'):
                    self.logger.info("Extracting file %s" % self.source)
                    rar_file.extract(archived_file, self.target)
                else:
                    self.logger.warn("Found a suspicious file (%s) in %s" % (archived_file, self.source))
        else:
            self.logger.debug("Skipping partial rar file %s" % self.source)

    @staticmethod
    def is_main_rar_file(f):
        return f.endswith('.rar')
