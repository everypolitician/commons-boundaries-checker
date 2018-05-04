# testing whether csv is correctly written.

from commons_boundaries.lib import write_csv_from_shp

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
