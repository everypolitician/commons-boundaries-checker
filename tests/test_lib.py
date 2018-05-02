# testing whether csv is correctly written.

from commons_boundaries.lib import write_csv_from_shape

import csv
import fiona
import tempfile
import unittest


class TestWriteCSV(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.shp_path = './tests/data/italy-source/CAMERA_PLURI_2017.shp'
        self.collection = fiona.open(self.shp_path, 'r')
        self.fieldnames = self.collection.schema['properties'].keys()

        self.csvfile = tempfile.NamedTemporaryFile(mode='w+t', suffix='.csv')
        write_csv_from_shape(self.shp_path, self.csvfile.name)

    @classmethod
    def tearDownClass(self):
        self.csvfile.close()

    def setup_method(self, method):
        self.reader = csv.DictReader(open(self.csvfile.name))

    def test_csv_field_names(self):
        assert self.reader.fieldnames == list(self.fieldnames)
