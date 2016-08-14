from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import simplejson

from log import init_logger
from processor import process_torrent


def start_api(port, path_mappping={}):
    handler_class = ApiHandler
    handler_class.path_mapping = path_mappping
    httpd = HTTPServer(("", port), handler_class)
    httpd.serve_forever()


class ApiHandler(BaseHTTPRequestHandler):
    logger = init_logger('ApiHandler')
    path_mapping = {}

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.data_string = None

    def log_message(self, message_format, *args):
        self.logger.info("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), message_format % args))

    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        data = simplejson.loads(self.data_string)
        print "{}".format(data)

        if 'torrent' in data and 'destination' in data:
            self.logger.info("Got good request for processing torrent: %s" % data)
            process_torrent(data['torrent'], data['destination'], self.path_mapping)
            self.send_response(200)
        else:
            self.logger.error("Invalid arguments, need a torrent and a destination directory. Got: %s" % data)
            self.send_response(500)
        self.end_headers()

        return
