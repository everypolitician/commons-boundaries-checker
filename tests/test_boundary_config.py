import unittest

from collections import OrderedDict
from commons_boundaries.boundary_config import BoundaryConfig


class TestBoundaryConfig(unittest.TestCase):

    def setUp(self):
        self.shp_path = "./tests/data/italy-source/CAMERA_PLURI_2017.shp"

    def test_as_dict_blank_config(self):
        blank_config = BoundaryConfig()
        assert blank_config.as_dict() == OrderedDict([
            ('boundary', ''),
            ('source-metadata', OrderedDict([
                ('name', ''),
                ('crs', ''),
                ('encoding', ''),
                ('wikidata-field', '')])),
            ('parent', OrderedDict([
                ('parent-name', ''),
                ('parent-key', ''),
                ('parent-foreign-key', '')])),
            ('output', OrderedDict([
                ('method', "MS_FB_PARE + '/{}:{}'.format(row[x], row[y])"),
                ('dissolve-all', 'False')]))
        ])

    def test_as_dict_config(self):
        config = BoundaryConfig(self.shp_path,
                                boundary='camera-plurinominal-constituencies',
                                proj4='+init=epsg,32632',
                                encoding='UTF-8')
        assert config.as_dict() == OrderedDict([
            ('boundary', 'camera-plurinominal-constituencies'),
            ('source-metadata', OrderedDict([
                ('name', 'CAMERA_PLURI_2017'),
                ('crs', '+init=epsg,32632'),
                ('encoding', 'UTF-8'),
                ('wikidata-field', '')])),
            ('parent', OrderedDict([
                ('parent-name', ''),
                ('parent-key', ''),
                ('parent-foreign-key', '')])),
            ('output', OrderedDict([
                ('method', "MS_FB_PARE + '/{}:{}'.format(row[x], row[y])"),
                ('dissolve-all', 'False')]))
        ])
