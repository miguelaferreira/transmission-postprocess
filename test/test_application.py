import unittest

from trdone.application import Application


class TestApplication(unittest.TestCase):
    def test_parse_arguments_when_no_arguments_are_specified(self):
        application = Application()

        with self.assertRaises(SystemExit):
            application.parse_arguments([])
        self.assertIsNone(application.destination)
        self.assertIsNone(application.torrent)

    def test_parse_arguments_cmdline_when_only_destination_is_specified(self):
        application = Application()

        with self.assertRaises(SystemExit):
            application.parse_arguments(['cmdline', '--destination', 'some_destination'])
        self.assertIsNone(application.destination)
        self.assertIsNone(application.torrent)

    def test_parse_arguments_cmdline_when_only_torrent_is_specified(self):
        application = Application()

        with self.assertRaises(SystemExit):
            application.parse_arguments(['cmdline', '--torrent', 'some_torrent'])
        self.assertIsNone(application.destination)
        self.assertIsNone(application.torrent)

    def test_parse_arguments_cmdline_when_all_required_arguments_are_specified_in_long_form(self):
        application = Application()
        application.parse_arguments(['cmdline', '--destination', 'some_destination', '--torrent', 'some_torrent'])

        self.assertEquals(application.destination, 'some_destination')
        self.assertEquals(application.torrent, 'some_torrent')

    def test_parse_arguments_cmdline_when_all_required_arguments_are_specified_in_short_form(self):
        application = Application()
        application.parse_arguments(['cmdline', '-d', 'some_destination', '-t', 'some_torrent'])

        self.assertEquals(application.destination, 'some_destination')
        self.assertEquals(application.torrent, 'some_torrent')

    def test_parse_arguments_api_when_port_is_string(self):
        application = Application()

        with self.assertRaises(SystemExit):
            application.parse_arguments(['api', '-p', 'some_port'])

    def test_parse_arguments_api_when_port_is_int(self):
        application = Application()

        application.parse_arguments(['api', '-p', '90'])

        self.assertEquals(application.port, 90)

    def test_parse_arguments_api_when_map_is_default(self):
        application = Application()

        application.parse_arguments(['api', '-p', '90'])

        self.assertIsNone(application.path_mapper)

    def test_parse_arguments_api_when_map_is_custom(self):
        application = Application()

        application.parse_arguments(['api', '-p', '90', '-te', 'some_path', '-ti', 'another_path'])

        self.assertDictEqual(application.path_mapper, {'some_path': 'another_path'})
