# stdlib imports
from io import BytesIO
from urllib import request

# third party imports
import h5py
import pandas as pd

from sampling.hdf_sampling import (
    get_hdf_url,
    get_stations,
    sample_locations_hdf,
    sample_shakemap_hdf,
)

# local imports
from sampling.utils import get_products_path


def set_coordinate_precision(dataframe):
    def lamba_func(x):
        return "{0:.5f}".format(x)

    dlat = dataframe["lat"]
    dlon = dataframe["lon"]
    dataframe["lat"] = dlat.map(lambda x: "{0:.5f}".format(x))
    dataframe["lon"] = dlon.map(lambda x: "{0:.5f}".format(x))
    if "sample_lat" in dataframe.columns:
        slat = dataframe["sample_lat"]
        slon = dataframe["sample_lon"]
        dataframe["sample_lat"] = slat.map(lambda x: "{0:.5f}".format(x))
        dataframe["sample_lon"] = slon.map(lambda x: "{0:.5f}".format(x))
    if "sample_distance_m" in dataframe.columns:
        sdist = dataframe["sample_distance_m"]
        dataframe["sample_distance_m"] = sdist.map(lambda x: "{0:.4f}".format(x))
    return dataframe


def get_stations_handler(args):
    if args.local:
        pfolder = get_products_path(args.eventid)
        hdf = pfolder / "shake_result.hdf"
        if not hdf.exists():
            raise FileNotFoundError(f"HDF file {hdf} does not exist.")
        fileobj = h5py.File(hdf, "r")
    else:
        hdf_url = get_hdf_url(args.eventid)
        with request.urlopen(hdf_url) as f:
            fbytes = f.read()
            fileio = BytesIO(fbytes)
            fileobj = h5py.File(fileio, "r")
    dataframe = get_stations(fileobj, get_max_horizontal=args.max_horizontal)
    fileobj.close()
    dataframe = set_coordinate_precision(dataframe)
    if args.outfile is None:
        print(dataframe.to_string(index=False))
        return
    nrecords = len(dataframe)
    if args.outfile.endswith(".xlsx"):
        dataframe.to_excel(args.outfile, index=False)
    else:
        dataframe.to_csv(args.outfile, index=False)
    print(f"Wrote {nrecords} stations to {args.outfile}")
    return


def get_locations_handler(args):
    pfolder = get_products_path(args.eventid)
    hdf = pfolder / "shake_result.hdf"
    if not hdf.exists():
        raise FileNotFoundError(f"HDF file {hdf} does not exist.")
    fileobj = h5py.File(hdf, "r")
    dataframe = sample_locations_hdf(fileobj)

    dataframe = set_coordinate_precision(dataframe)
    if args.outfile is None:
        print(dataframe.to_string(index=False))
        return
    nrecords = len(dataframe)
    if args.outfile.endswith(".xlsx"):
        dataframe.to_excel(args.outfile, index=False, engine="openpyxl")
    else:
        dataframe.to_csv(args.outfile, index=False)
    print(f"Wrote {nrecords} stations to {args.outfile}")
    fileobj.close()


def get_sample_handler(args):
    if args.local:
        pfolder = get_products_path(args.eventid)
        hdf = pfolder / "shake_result.hdf"
        if not hdf.exists():
            raise FileNotFoundError(f"HDF file {hdf} does not exist.")
        fileobj = h5py.File(hdf, "r")
    else:
        hdf_url = get_hdf_url(args.eventid)
        with request.urlopen(hdf_url) as f:
            fbytes = f.read()
            fileio = BytesIO(fbytes)
            fileobj = h5py.File(fileio, "r")
    if args.stations is not None:
        dataframe = get_stations(fileobj)
        ids = []
        lats = []
        lons = []
        for station in args.stations:
            row = dataframe[dataframe["id"] == station]
            if len(row):
                ids.append(row.iloc[0]["id"])
                lats.append(row.iloc[0]["lat"])
                lons.append(row.iloc[0]["lon"])
            else:
                print(f"{station} not found in list of stations.")
        if not len(ids):
            msg = (
                "No stations were found in this ShakeMap run. "
                "Returning empty dataframe."
            )
            print(msg)
            dataframe = pd.DataFrame([])
        else:
            dataframe = sample_shakemap_hdf(fileobj, lats, lons, ids=ids)
    elif args.all_stations:
        dataframe = get_stations(fileobj)
        ids = dataframe["id"]
        lats = dataframe["lat"]
        lons = dataframe["lon"]
        dataframe = sample_shakemap_hdf(fileobj, lats, lons, ids=ids)
    elif args.coordinates:
        ids = [args.coordinates[0]]
        lats = [float(args.coordinates[1])]
        lons = [float(args.coordinates[2])]
        dataframe = sample_shakemap_hdf(fileobj, lats, lons, ids=ids)
    elif args.file is not None:
        if args.file.endswith(".xlsx"):
            filename = args.file
            dataframe = pd.read_excel(filename, engine="openpyxl")
        else:
            dataframe = pd.read_csv(args.file)
        # check columns
        # columns = [col.lower() for col in dataframe.columns]
        columns = dataframe.columns
        latcol = [col for col in columns if col.lower().startswith("lat")]
        loncol = [col for col in columns if col.lower().startswith("lon")]
        idcol = [col for col in columns if col.lower().startswith("id")]
        if not len(latcol) or not len(loncol):
            raise KeyError("Missing either latitude or longitude column.")
        if len(latcol) > 1:
            raise KeyError(f"Ambiguous latitude columns: {latcol}.")
        if len(loncol) > 1:
            raise KeyError(f"Ambiguous longitude columns: {latcol}.")
        if len(idcol) == 1:
            ids = dataframe[idcol[0]]
        else:
            ids = [f"Point{i}" for i in range(0, len(dataframe))]
        lats = dataframe[latcol[0]]
        lons = dataframe[loncol[0]]
        dataframe = sample_shakemap_hdf(fileobj, lats, lons, ids=ids)

    fileobj.close()
    dataframe = set_coordinate_precision(dataframe)
    if args.outfile is None:
        print(dataframe.to_string(index=False))
        return
    nrecords = len(dataframe)
    if args.outfile.endswith(".xlsx"):
        dataframe.to_excel(args.outfile, index=False)
    else:
        dataframe.to_csv(args.outfile, index=False)
    print(f"Wrote {nrecords} stations to {args.outfile}")
