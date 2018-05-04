import csv
import fiona

from fiona.crs import to_string
from pathlib import Path


def write_csv_from_shp(shp_path, csv_path):
    with open(csv_path, 'w') as csvfile:
        with fiona.open(shp_path, 'r') as shp:
            fieldnames = shp.schema['properties'].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for feature in shp:
                writer.writerow(feature['properties'])


def proj4_from_shp(shp_path):
    shp_path = Path(shp_path)
    return to_string(fiona.open(str(shp_path)).crs)


def encoding_from_shp(shp_path):
    shp_path = Path(shp_path)
    cpg_path = shp_path.with_suffix('.cpg')
    if cpg_path.is_file():
        return open(str(cpg_path)).readline()
    return ''
