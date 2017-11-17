import os
import errno
import pandas as pd
import json
import re
from astroquery.simbad import Simbad


def get_data_dir_path():
    data_dir_path = "tychoii_data"
    # thank you https://stackoverflow.com/a/273227
    try:
        os.makedirs(data_dir_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return data_dir_path

def get_datum_from_file(file_path):
    with open(file_path, 'r') as fp:
        try:
            datum = json.load(fp)
            return datum
        except json.decoder.JSONDecodeError:
            return None

def get_datum_from_simbad(name, file_path):
    print('Fetching Data for '+ name)
    table1 = Simbad.query_object(name)
    datum = dict(
        RA=table1['RA'][0],
        DEC=table1['DEC'][0],
        V=float(table1['FLUX_V'][0]),
        K=float(table1['FLUX_K'][0])
    )
    print(datum)
    with open(file_path, 'w') as fp:
        json.dump(datum, fp)
    return datum


def get_data(start=None, stop=None, names=None, all=False):
    data_dir_path = get_data_dir_path()
    saved_names = os.listdir(data_dir_path)
    data = {}
    Simbad.add_votable_fields('flux(V)', 'flux(K)')
    if names is None:
        names = pd.read_csv("TYCHOII_targs.txt", sep='|', names=['blank', 'name'], usecols=['blank','name'], skiprows=1)
        names = names.name
        if not all:
            names = names[start: stop]
    elif type(names) is str:
        # you can specify names as a string separated
        # by commas, spaces, or semicolons
        names = re.split('\s+|,\s*|;\s*')
    for name in names:
        name = name.strip()
        file_path = os.path.join(data_dir_path, name)
        datum = None
        if name in saved_names:
            datum = get_datum_from_file(file_path)
        if datum is None:
            datum = get_datum_from_simbad(name, file_path)
        data[name] = datum
    return data

data = get_data(all=True)
