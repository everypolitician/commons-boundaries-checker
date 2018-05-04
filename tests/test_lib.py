# testing whether csv is correctly written.

from commons_boundaries.lib import write_csv_from_shp, proj4_from_shp, encoding_from_shp
from pathlib import Path

import csv
import os
import tempfile
import unittest


class TestWriteCSV(unittest.TestCase):

    def test_italian_house_plurinominal(self):
        with tempfile.NamedTemporaryFile(mode='w',
                                         suffix='.csv',
                                         delete=False) as csvfile:
            write_csv_from_shp('tests/data/italy-source/CAMERA_PLURI_2017.shp',
                               csvfile.name)
        # Read the CSV file back in:
        with open(csvfile.name) as f:
            csv_rows = list(csv.reader(f))
        # There are 64 features in the file plus one header row:
        assert len(csv_rows) == 65
        # Check the header row is as expected:
        assert csv_rows[0] == [
            'OBJECTID',
            'CAM17P_COD',
            'CAM17P_DEN',
            'POP_2011',
            'SEGGI_TOT',
            'SEGGI_UNI',
            'SEGGI_PRO',
            'Shape_Leng',
            'Shape_Area',
        ]
        # And check that the first row of data is as expected:
        assert csv_rows[1] == [
            '1',
            '99999999',
            '99999999',
            '126806.0',
            '1',
            '1',
            '0',
            '325836.368101',
            '3260854220.04',
        ]
        os.remove(csvfile.name)


class TestCreateConfig(unittest.TestCase):

    def setUp(self):
        test_data = Path(__file__).parent / 'data'
        self.shp_path = test_data / 'italy-source' / 'CAMERA_PLURI_2017.shp'
        self.no_meta_shp_path = test_data / 'no_meta' / 'CAMERA_PLURI_2017.shp'

    def test_get_proj4_from_shp(self):
        assert proj4_from_shp(self.shp_path) == '+init=epsg:32632'

    def test_get_proj4_from_shp_fails_without_prj(self):
        assert proj4_from_shp(self.no_meta_shp_path) == ''

    def test_encoding_from_shp(self):
        assert encoding_from_shp(self.shp_path) == 'UTF-8'

    def test_encoding_from_shp_fails_without_cpg(self):
        assert encoding_from_shp(self.no_meta_shp_path) == ''
