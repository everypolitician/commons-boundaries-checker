## Summary

This package assists in the common steps required to prepare a boundary layer for inclusion in the democratic commons. There are a number of common operations that are carried out, such as:

* Creating an appropriate directory in the repository
* Changing the encoding to UTF-8
* Reprojecting the features to EPSG 4326
* Ensuring the features are valid according to OGC Simple Features spec.
* Cleaning them if they aren’t
* Creating fields for, generating and adding an MS_FB and MS_FB_PARE id to each feature (except for the country which only gets an MS_FB)
* Creating a WIKIDATA field.
* Creating a shapefile to hold these features
* Creating a CSV which matches the attribute data stored in the source shapefile.
* Joining wikidata values back to the shapefile to ensure that the attribute table and the CSV file match.
* Run validity checks from the R package used by FB.

These steps are all fairly straightforward in QGIS or similar. However they can be fiddly, error prone and require a certain amount of time. In addition these steps are often repeated in order to generate differing attribute data for the same geometries. Having this state captured in a config file is helpful when trying to understand how to meaningfully represent the data.

There may be specific steps that are required prior to running these standard steps, for example if the boundaries have to be constructed from constituent parts. There is provision for this - see the usage file.


## Installation
'commons-boundaries' is a collection of command line tools that come as a python package.
Create a virtual env however you prefer, and then `pip install commons-boundaries`
Commands are run at the command line form within the virtual env.

__development__

If installing for development activate your virtualenv and run `pip install -e .[testing]` in the root directory.

## Usage

The typical workflow for adding a boundary file is as follows:

1. Add a sourcefile for your boundary to the source directory
2. Run: `create-config <source-file> <name-of-boundary>`
3. Fill out the missing elements of boundary-config.json
4. Run: `create-boundary <name-of-boundary>`
    * Assuming there is no `<name-of-boundary>-reconciled.csv` present this will fail after having created a shapefile, and prompt you to run:
5. `create-reconcilliation-input` Which creates a csv copy of the shapefile attribute table.
6. Reconcile values using OpenRefine, and save the output to `./boundaries/build/<name-of-boundary>/<name-of-boundary>-reconciled.csv`
7. Rerun `create-boundary <name-of-boundary>` which should run through to completion, which adds and populates a `WIKIDATA` field to the shapefile and writes a csv file which is a copy of the shapefile attribute table.

## Reference

### `./boundaries` Structure

The boundary directory of a democratic commons repository is structured as follows:

    .
    ├── boundaries
    │   ├── boundary-config.json
    │   ├── boundary-build-output.txt
    │   ├── build
    │   │   ├── country
    │   │   ├── national-constituencies
    │   │   ├── flacs (or localised name)
    │   │   └── index.json
    │   ├── scripts
    │   └── source
    ├── config.json
    ├── build_output.txt
    ├── executive
    └── legislative

* __boundary-config.json__ provides the parameters required to run  `create-boundary`.
* __boundary-build-output.txt__ collects warning messages thrown during boundary build process,
* __build__ Is a directory containing sub-directories which each contain one shapefile and one csv - corresponding to one layer of boundaries.
* __build/index.json__ is a record of boundary layers connecting them wtih legislativ and executive positions.
* __scripts__ Is a directory of pre-processing scripts that may be required to build the actual geometries from other geographical subdivisions.
* __source__ contains the source boundary files from boundary commissions, OSM, etc.

## boundary-config.json Reference

### Structure
```json
    [
      {
        "boundary": "country",
        "source-metadata": {
          "name": "name-of-source-file.shp",
          "crs": "+proj=utm +zone=32 +datum=WGS84 +units=m +no_defs",
          "encoding": "latin-1",
          "wikidata-field": ""
        },
        "parent": {
          "parent-name": "",
          "parent-key": "",
          "parent-foreign-key": ""
        },
        "output": {
          "method": "def generate_id(MS_FB_PARE, row): id = MS_FB_PARE + '/{}:{}'.format(row[x], row[y]) return id",
          "dissolve-all": "False"
        }
      }
    ]
```

#### What are the different parameters, and what do they do?

|Parameter | Definition | Function |
|--------------|--------------|-------------|
|boundary | Name of boundary, eg national-uninominal-districts’ | Identifies the directory be created in ./boundaries/build and the name of the layer created within that directory. (Since they are the same.)|
|source-metadata    | Metadata about sourcefile |
|name | Name as appears in source file |
|crs | Proj4 string as derived from ogrinfo | Defines the source features projection/Coordinate Reference System. Allows correct georeferencing and reprojection of features|
|encoding | Encoding of text. | Allows source character set to be read correctly.|
|wikidata-field | Optional - eg OSM imports | If present `create-boundary` adds and populates wikidata field.|
|Parent | Dictionary of information about the parent features |
|parent-name | Name of boundary which contains parent directories | Identifies file to search for Parent ids.|
|parent-key | Name of field in Parent to uniquely identify features | Allows child features to be joined to parent features |
|parent-foreign-key | Name of field in boundary which contains values from parent key | Allows child features to be joined to parent features |
|output | Dictionary determining output parameters.
|method | python function of the form `def generate_id(MS_FB_PARE, row): id = MS_FB_PARE + '/{}:{}'.format(row[x], row[y[) return id` where `x` and `y` are field names |Generates the ms_fb id|
|dissolve-all| `True` or `False` | used for disolving all features from source |


### Command Reference
##### Wouldn't it be nice if:
* commands (except for create-config) which were run from within the specific boundary subdirectory didn't need the <name-of-boundary> parameter.

#### `create-config source boundary`
* `source` - is the name of the source file in `./boundaries/source`. There will be a 1-to-1 relationship between features in the source file and the boundary finally created.
* `boundary` - is the name of the boundary directory and file to be created.

This command carries out the following steps:

1. Creates the directory:`./boundaries/build/<name-of-boundary\>`
2. Open `<source>` with OGRinfo or similar and establish:
    - crs
    - encoding (if possible)
3. Create an entry in boundaries/boundary-config.json filling in:
    - country
    - boundary
    - source-metadata
        - name
        - crs
        - encoding

and leaving the other values filled in as `""`

#### `create-boundary boundary`
* `boundary` - is the name of the boundary directory and file to be created.

This command carries out the following steps:

Check for existing shapefile, if found skip to **2**
1. Geomtery operations:
    1. read source features
    2. Apply a zero buffer
    3. Generalise to 1m, (nb preserve topology)
    4. Reject small exteriors
    5. Reject small interiors
    6. Reject invalid polygons
    7. If there are fewer records at end of this than at start raise warnings
    8. Add fields 'MS_FB', 'MS_FB_PARE' and 'WIKIDATA' to schema.
        * Country is a special case with no Parent.
    8. write a shapefile to build
    9. Run R-Checks - raise a warning if they fail.

2. id creation
Check for MS_FB_PARE if found skip to **2.ii**
    1. Open shapefile as append and iterate through features calculating MS_FB_PARE writing a new feature with these attributes and deleting the old one. This is done by building a dictionary of `parent-key: MS_FB` from the parent layer and using it as a look up.The all back on doing a point in polygon serach, but that will take much longer.
Check for MS_FB if found skip to **3**
    2. Repeat but for MS_FB id. This is calculated by passing each row as a dict to the function defined in `method`.
3. Wikidata id attribution
    1. Checks for existance of `build/<boundary>/<boundary>-reconciled.csv`. If not found fail with message `build/<boundary>/<boundary>-reconciled.csv not found please supply. Hint: you might need to run create-reconcilliation-input <boundary>`
    2. If `build/<boundary>/<boundary>-reconciled.csv` is found, then Wikidata ids are written to field WIKIDATA.
4. If all id fields are present and populated attribute table is written to `build/<boundary>/<boundary>.csv`by calling `create-csv`

#### `create-reconciliation-input boundary`
* `boundary` - is the name of the boundary directory and file to be created.
1. Copies shapefile attribute table to `build/<boundary>/<boundary>-for-reconciliation.csv`

This command carries out the following steps:

#### `create-csv boundary`
* `boundary` - is the name of the boundary directory and file to be created.

This command carries out the following steps:

1. Writes `build/<boundary>/<boundary>.csv` as a copy of shapefile attribute table.

## Geometry cleaning

## Geometric error handling.

## Using OpenRefine to get wikidata ids.
