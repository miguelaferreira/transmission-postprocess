from log import init_logger


class PathMapper(object):
    def __init__(self, mapping):
        super(PathMapper, self).__init__()
        self.mapping = mapping
        self.logger = init_logger('PathMapper')

    def map(self, path):
        potential_keys = [key for key in self.mapping.keys() if path.startswith(key)]
        potential_keys.sort(key=len, reverse=True)
        if len(potential_keys) > 0:
            resulting_path = self.build_resulting_path(potential_keys[0], path)
            self.logger.info("Path %s mapped to %s" % (path, resulting_path))
            return resulting_path
        else:
            return path

    def build_resulting_path(self, match, path):
        mapped_match = self.mapping[match]
        return mapped_match.join(path.rsplit(match))
