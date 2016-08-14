import unittest

from trdone.path_mapper import PathMapper


class TestPathMapper(unittest.TestCase):
    def test_map_when_key_does_not_exist(self):
        path = 'some_path'
        mapper = PathMapper({})
        mapped_path = mapper.map(path)

        self.assertEquals(mapped_path, path)

    def test_map_when_only_one_exact_match_exist(self):
        path = 'some_path'
        other_path = 'other_path'
        mapper = PathMapper({path: other_path})
        mapped_path = mapper.map(path)

        self.assertEquals(mapped_path, other_path)

    def test_map_when_only_several_matches_exist_it_should_take_the_longest(self):
        path = 'some_path/to/a/dir'
        other_path = 'other_path'
        mapper = PathMapper({'some_path': other_path, 'some_path/to': 'deeper_path', 'some_path/to/a/dir': 'deepest_path'})
        mapped_path = mapper.map(path)

        self.assertEquals(mapped_path, 'deepest_path')

    def test_map_when_match_is_partial_and_unmatched_end_needs_to_be_kept(self):
        path = 'some_path/to/a/dir'
        other_path = 'other_path'
        mapper = PathMapper({'some_path': other_path, 'some_path/to': 'deepest_path'})
        mapped_path = mapper.map(path)

        self.assertEquals(mapped_path, 'deepest_path/a/dir')
