# Module for boundaryConfig class.

import json

from collections import OrderedDict
from pathlib import Path


class BoundaryConfig(object):
    """
        Class to represent the JSON objects found in boundary-config.json
    """
    def __init__(self, shp_path='', proj4='', encoding='', boundary=''):
        self.shp_path = Path(shp_path)
        self.boundary = boundary
        self.source_metadata = OrderedDict([
            ('name', self.shp_path.stem),
            ('crs', proj4),
            ('encoding', encoding),
            ('wikidata-field', '')
        ])
        self.parent = OrderedDict([
            ('parent-name', ''),
            ('parent-key', ''),
            ('parent-foreign-key', '')
        ])
        self.output = OrderedDict([
            ('method', "MS_FB_PARE + '/{}:{}'.format(row[x], row[y])"),
            ('dissolve-all', 'False')
        ])

    def as_dict(self):
        config = OrderedDict([
            ('boundary', self.boundary),
            ('source-metadata', self.source_metadata),
            ('parent', self.parent),
            ('output', self.output)
        ])
        return config
