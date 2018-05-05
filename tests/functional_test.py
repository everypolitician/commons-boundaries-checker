import json
import pytest
import shutil
import subprocess
import tempfile
import unittest

from pathlib import Path


class AddCountryTest(unittest.TestCase):

    def setUp(self):
        # setup a mock repository
        self.tempdir = Path(tempfile.mkdtemp())
        self.build_path = self.tempdir / 'boundaries' / 'build'
        self.build_path.mkdir(parents=True)
        self.src_path = self.tempdir / 'boundaries' / 'source'
        self.src_path.mkdir(parents=True)
        self.config_path = self.tempdir / 'boundaries' / 'boundary-config.json'

        # copy a source file there
        camera = Path('./tests/data/italy-source/CAMERA_PLURI_2017')
        for ext in ('.shp', '.shx', '.cpg', '.dbf', '.prj'):
            shutil.copy(str(camera.with_suffix(ext)), str(self.src_path))

    def tearDown(self):
        # remove tempfolder
        shutil.rmtree(str(self.tempdir))

    def test_country_directory_is_created(self):
        camera_pluri_path = self.src_path / 'CAMERA_PLURI_2017.shp'
        subprocess.run(['create-config', str(camera_pluri_path), 'country'],
                       cwd=str(self.tempdir))
        assert (self.build_path / 'country').is_dir()

    def test_can_not_use_same_name_twice(self):
        camera_pluri_path = self.src_path / 'CAMERA_PLURI_2017.shp'
        subprocess.run(['create-config', str(camera_pluri_path), 'country'],
                       cwd=str(self.tempdir))
        with pytest.raises(subprocess.CalledProcessError) as e:
            subprocess.check_output(['create-config',
                                    str(camera_pluri_path),
                                    'country'], stderr=subprocess.STDOUT,
                                    cwd=str(self.tempdir))
        expected_error = 'country already exists. Please pick a new name\n'
        assert e.value.output.decode('UTF-8') == expected_error
        assert e.value.returncode == 1

    def test_config_for_country_written(self):
        camera_pluri_path = self.src_path / 'CAMERA_PLURI_2017.shp'
        subprocess.run(['create-config', str(camera_pluri_path), 'country'],
                       cwd=str(self.tempdir))
        with open(str(self.config_path), 'r') as config_json:
            boundary_config_contents = json.load(config_json)
        assert boundary_config_contents == [{
            'boundary': 'country',
            'source-metadata': {
                'name': 'CAMERA_PLURI_2017',
                'crs': '+init=epsg:32632',
                'encoding': 'UTF-8', 'wikidata-field': ''},
            'parent': {
                'parent-name': '',
                'parent-key': '',
                'parent-foreign-key': ''},
            'output': {
                'method': "MS_FB_PARE + '/{}:{}'.format(row[x], row[y])",
                'dissolve-all': 'False'}
        }]
