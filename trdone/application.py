import argparse
import json

from api_handler import start_api
from log import init_logger
from processor import process_torrent


class Application(object):
    def __init__(self):
        super(Application, self).__init__()
        self.destination = None
        self.torrent = None
        self.port = None
        self.path_mapper = None
        self.mode = None
        self.logger = init_logger('Application')

    def parse_arguments(self, arguments):
        parser = argparse.ArgumentParser(prog='trdone', description='Processes torrent files')
        subparsers = parser.add_subparsers(help='help for subcommand')

        cmdline_parser = subparsers.add_parser('cmdline', help='process a single torrent from the command line')
        cmdline_parser.add_argument('-t', '--torrent', help='the torrent that should be processed', default='.', required=True)
        cmdline_parser.add_argument('-d', '--destination', help='the directory where files should be moved to', default='.', required=True)
        cmdline_parser.set_defaults(subcommand='cmdline')

        api_parser = subparsers.add_parser('api', help='spin up an api that processes torrents on demand')
        api_parser.add_argument('-p', '--port', help='the port the api should listen on', default='80', required=True, type=int)
        api_parser.add_argument('-te', '--torrent-external', help='the torrent directory path as seen by transmission', default=None, required=False, type=str)
        api_parser.add_argument('-ti', '--torrent-internal', help='the torrent directory path as seen by us', default=None, required=False, type=str)
        api_parser.set_defaults(subcommand='api')

        arguments = parser.parse_args(arguments)
        if arguments.subcommand == 'cmdline':
            self.destination = arguments.destination
            self.torrent = arguments.torrent
        else:
            self.port = arguments.port
            if arguments.torrent_external is not None and arguments.torrent_internal is not None:
                self.path_mapper = {arguments.torrent_external: arguments.torrent_internal}
        self.mode = arguments.subcommand

    def run(self):
        if self.mode == 'cmdline':
            self.logger.info('Processing torrent')
            process_torrent(self.torrent, self.destination)
        else:
            self.logger.info('Serving API')
            start_api(self.port, self.path_mapper)
