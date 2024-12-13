# stdlib imports
import json
from urllib import request

import numpy as np

# third party imports
import pandas as pd

# local imports
from sampling.utils import get_row_col

URLT = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query?"
    "format=geojson&eventid=[EVENTID]&includesuperseded=true"
)
HDF = "download/shake_result.hdf"

#: Earth radius in km.
EARTH_RADIUS = 6371.0


def is_points_hdf(fileobj):
    if "ids" in fileobj["arrays"]["imts"]["GREATER_OF_TWO_HORIZONTAL"]["MMI"]:
        return True
    return False


def _prepare_coords(lons1, lats1, lons2, lats2):
    """
    Convert two pairs of spherical coordinates in decimal degrees
    to numpy arrays of radians. Makes sure that respective coordinates
    in pairs have the same shape.
    """
    lons1 = np.radians(lons1)
    lats1 = np.radians(lats1)
    assert lons1.shape == lats1.shape
    lons2 = np.radians(lons2)
    lats2 = np.radians(lats2)
    assert lons2.shape == lats2.shape
    return lons1, lats1, lons2, lats2


def geodetic_distance(lons1, lats1, lons2, lats2, diameter=2 * EARTH_RADIUS):
    """
    Calculate the geodetic distance between two points or two collections
    of points.
    Parameters are coordinates in decimal degrees. They could be scalar
    float numbers or numpy arrays, in which case they should "broadcast
    together".
    Implements http://williams.best.vwh.net/avform.htm#Dist
    :returns:
        Distance in km, floating point scalar or np array of such.
    """
    lons1, lats1, lons2, lats2 = _prepare_coords(lons1, lats1, lons2, lats2)
    distance = np.arcsin(
        np.sqrt(
            np.sin((lats1 - lats2) / 2.0) ** 2.0
            + np.cos(lats1) * np.cos(lats2) * np.sin((lons1 - lons2) / 2.0) ** 2.0
        )
    )
    return diameter * distance


def get_hdf_url(eventid):
    url = URLT.replace("[EVENTID]", eventid)
    with request.urlopen(url) as f:
        data = f.read().decode("utf8")
    jdict = json.loads(data)
    products = jdict["properties"]["products"]
    if "shakemap" not in products:
        print(f"No ShakeMap for event {eventid}. Exiting.")
    # find the most recent US ShakeMap
    idx = -1
    max_time = -1
    shakemaps = products["shakemap"]
    for ic, shakemap in enumerate(shakemaps):
        if shakemap["source"] not in ["us", "atlas"]:
            continue
        if shakemap["updateTime"] > max_time:
            max_time = shakemap["updateTime"]
            idx = ic
    shakemap = shakemaps[idx]
    contents = shakemap["contents"]
    if HDF not in contents:
        print(f"No HDF file found for ShakeMap for event {eventid}. Exiting.")
    grid_url = contents[HDF]["url"]

    return grid_url


def sample_locations_hdf(fileobj):
    arrays = fileobj["arrays"]["imts"]["GREATER_OF_TWO_HORIZONTAL"]
    val_columns = {}
    val_columns["id"] = [rowid.decode("utf8") for rowid in arrays["PGA"]["ids"][:]]
    val_columns["lat"] = arrays["PGA"]["lats"][:]
    val_columns["lon"] = arrays["PGA"]["lons"][:]

    for imt, group in arrays.items():
        for stat, array in group.items():
            if stat in ["ids", "lats", "lons"]:
                continue
            key = f"{imt}_{stat}"
            val_columns[key] = array[:]

    dataframe = pd.DataFrame(data=val_columns)
    return dataframe


def sample_shakemap_hdf(fileobj, lats, lons, ids=None):
    if ids is None:
        ids = [f"Point{i}" for i in range(1, len(lats) + 1)]

    arrays = fileobj["arrays"]["imts"]["GREATER_OF_TWO_HORIZONTAL"]
    array = arrays["PGA"]["mean"]
    gdict = dict(array.attrs)

    rows = {}
    rows["id"] = ids
    rows["lat"] = lats
    rows["lon"] = lons
    sample_lats = []
    sample_lons = []
    # this is not efficient...
    for lat, lon in zip(lats, lons):
        row, col, newlat, newlon = get_row_col(gdict, lat, lon)
        sample_lats.append(newlat)
        sample_lons.append(newlon)
    for imt, group in arrays.items():
        for stat, array in group.items():
            if len(array.shape) == 1:
                continue
            nrows, ncols = array.shape
            colname = f"{imt}_{stat}"
            imtcolumn = []
            for lat, lon in zip(lats, lons):
                row, col, newlat, newlon = get_row_col(gdict, lat, lon)
                if row > nrows - 1 or col > ncols - 1 or row < 0 or col < 0:
                    value = np.nan
                else:
                    value = array[row, col]
                imtcolumn.append(value)
            rows[colname] = imtcolumn

    # vs30 is not an imt, so we have to grab it here
    vs30 = fileobj["arrays"]["vs30"]
    vs30_column = []
    for lat, lon in zip(lats, lons):
        row, col, newlat, newlon = get_row_col(gdict, lat, lon)
        if row > nrows - 1 or col > ncols - 1 or row < 0 or col < 0:
            value = np.nan
        else:
            value = vs30[row, col]
        vs30_column.append(value)
    rows["vs30"] = vs30_column
    rows["sample_lat"] = sample_lats
    rows["sample_lon"] = sample_lons

    dataframe = pd.DataFrame(rows)

    # calculate distance between desired and sampled coordinates
    dlon = dataframe["lon"].values
    dlat = dataframe["lat"].values
    slon = dataframe["sample_lon"].values
    slat = dataframe["sample_lat"].values
    dataframe["sample_distance_m"] = geodetic_distance(dlon, dlat, slon, slat) * 1000.0

    # order the rows by id, lat, lon, sample_lat, sample_lon, vs30, then imts
    all_columns = dataframe.columns
    keepcols = [
        "id",
        "lat",
        "lon",
        "sample_lat",
        "sample_lon",
        "sample_distance_m",
        "vs30",
    ]
    imtcols = [col for col in all_columns if col not in keepcols]
    newcols = keepcols + imtcols
    dataframe = dataframe[newcols]

    return dataframe


def get_stations(fileobj, get_max_horizontal=False):
    station_str = fileobj["dictionaries"]["stations_dict"][()]
    stations = json.loads(station_str)
    rows = []
    for station in stations["features"]:
        for channel in station["properties"]["channels"]:
            row = {}
            row["id"] = station["id"]
            lon, lat = station["geometry"]["coordinates"]
            row["lat"] = lat
            row["lon"] = lon
            # TODO get the max of horizontal channels?
            channel_name = channel["name"]
            row["channel"] = channel_name
            for amplitude in channel["amplitudes"]:
                amp_name = amplitude["name"]
                mean_name = f"{amp_name}_mean"
                std_name = f"{amp_name}_std"
                mean_value = amplitude["value"]
                std_value = amplitude["ln_sigma"]
                if mean_value == "null":
                    mean_value = np.nan
                if std_value == "null":
                    std_value = np.nan
                if std_value != 0:
                    std_value = np.log(std_value / 100)
                mean_value = np.log(mean_value / 100)
                row[mean_name] = mean_value
                row[std_name] = std_value
            rows.append(row)

    # get a list of all the column names
    dataframe = pd.DataFrame(rows)

    # sometimes there are duplicates
    dataframe.drop_duplicates(subset=["id", "channel"], inplace=True)

    imt_cols = [col for col in dataframe.columns if col.endswith("mean")]
    if get_max_horizontal:
        rows = []
        for station, group in dataframe.groupby("id"):
            zidx = group["channel"].str.endswith("Z")
            idx = ~zidx
            if zidx.all():
                continue  # no horizontal channels
            if idx.any():
                horizontals = group.loc[idx]
                # loop over MMI columns, grab max of each one, and
                # accompanying STD
                max_values = {}
                for imt_col in imt_cols:
                    std_col = imt_col.replace("mean", "std")
                    imax = horizontals[imt_col].argmax()
                    max_mean = horizontals[imt_col].max()
                    max_std = horizontals.iloc[imax][std_col]
                    max_values[imt_col] = (max_mean, max_std)
                row = horizontals.iloc[imax][["id", "lat", "lon"]].to_dict()
                row["channel"] = "H1"
                for key, mtuple in max_values.items():
                    std_key = key.replace("mean", "std")
                    row[key] = mtuple[0]
                    row[std_key] = mtuple[1]
                rows.append(row)
            else:
                raise NotImplementedError("")
        dataframe = pd.DataFrame(data=rows)

    return dataframe
