import csv
import fiona


def write_csv_from_shp(shp_path, csv_path):
    with open(csv_path, 'w') as csvfile:
        with fiona.open(shp_path, 'r') as shp:
            fieldnames = shp.schema['properties'].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for feature in shp:
                writer.writerow(feature['properties'])
