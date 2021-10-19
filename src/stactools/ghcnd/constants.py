# flake8: noqa

from datetime import datetime
from typing import Any, Dict, List

from pyproj import CRS
from pystac import Link, Provider, ProviderRole

GHCND_ID = "ghcnd"
GHCND_EPSG = 4326
GHCND_CRS = CRS.from_epsg(GHCND_EPSG)
GHCND_EXTENT = [-180., 90., 180., -90.]
GHCND_TITLE = "Global Historical Climatology Network daily"
GHCND_DESCRIPTION = "The Global Historical Climatology Network daily (GHCNd) is an integrated database of daily climate summaries from land surface stations across the globe. GHCNd is made up of daily climate records from numerous sources that have been integrated and subjected to a common suite of quality assurance reviews."

LICENSE = "CC-BY-4.0"
LICENSE_LINK = Link(
    rel="license",
    target="https://creativecommons.org/licenses/by/4.0/",
    title="Attribution 4.0 International (CC BY 4.0)",
)

HOMEPAGE_URL = "https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00861/html"
METADATA_URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt"
ADDITIONAL_METADATA_URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/readme-by_year.txt"
STATIONS_URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
YEARS_URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/"

PROVIDERS = [
    Provider(name="NOAA",
             roles=[
                 ProviderRole.HOST,
                 ProviderRole.LICENSOR,
                 ProviderRole.PROCESSOR,
                 ProviderRole.PRODUCER,
             ],
             url=HOMEPAGE_URL),
]

KEYWORDS = ["NOAA", "ghcnd", "GHCNd", "GHCN-Daily"]

TEMPORAL_EXTENT: List[Any] = [
    "1763-01-01T00:00:00Z",
    datetime.today().strftime('%Y-%m-%dT00:00:00Z')
]
SPATIAL_EXTENT = [-180.0, -90.0, 180.0, 85.0]

CITATION = "Menne, Matthew J., Imke Durre, Bryant Korzeniewski, Shelley McNeal, Kristy Thomas, Xungang Yin, Steven Anthony, Ron Ray, Russell S. Vose, Byron E.Gleason, and Tamara G. Houston (2012): Global Historical Climatology Network - Daily (GHCN-Daily), Version 3. NOAA National Climatic Data Center. doi:10.7289/V5D21VHZ"
DOI = "10.7289/V5D21VHZ"

THUMBNAIL_HREF = "https://www1.ncdc.noaa.gov/pub/data/metadata/images/C00861_GHCN-D_stations.png"

DATA_TABLE_COLUMNS = [{
    "name": "ID",
    "description": "11 character station identification code.",
    "type": "str"
}, {
    "name": "YEAR/MONTH/DAY",
    "description":
    "8 character date in YYYYMMDD format (e.g. 19860529 = May 29, 1986).",
    "type": "str"
}, {
    "name": "ELEMENT",
    "description": "4 character indicator of element type.",
    "type": "str"
}, {
    "name": "DATA VALUE",
    "description": "5 character data value for ELEMENT.",
    "type": "int"
}, {
    "name": "M-FLAG",
    "description": "1 character Measurement Flag.",
    "type": "str"
}, {
    "name": "Q-FLAG",
    "description": "1 character Quality Flag.",
    "type": "str"
}, {
    "name": "S-FLAG",
    "description": "1 character Source Flag.",
    "type": "str"
}, {
    "name": "OBS-TIME",
    "description":
    "4-character time of observation in hour-minute format (i.e. 0700 = 7:00 am).",
    "type": "str"
}]

STATION_TABLE_COLUMNS = [{
    "name": "ID",
    "description": "11 character station identification code.",
    "type": "str"
}, {
    "name": "LATITUDE",
    "description": "Latitude of the station (in decimal degrees).",
    "type": "float"
}, {
    "name": "LONGITUDE",
    "description": "Longitude of the station (in decimal degrees).",
    "type": "float"
}, {
    "name": "ELEVATION",
    "description": "Elevation of the station (in meters, missing = -999.9).",
    "type": "float"
}, {
    "name": "STATE",
    "description": "U.S. postal code for the state (for U.S. stations only).",
    "type": "str"
}, {
    "name": "NAME",
    "description": "The name of the station.",
    "type": "str"
}, {
    "name": "GSN FLAG",
    "description":
    "A flag that indicates whether the station is part of the GCOS Surface Network (GSN).",
    "type": "str"
}, {
    "name": "HCN/CRN FLAT",
    "description":
    "A flag that indicates whether the station is part of the U.S. Historical Climatology Network (HCN) or U.S. Climate Refererence Network (CRN).",
    "type": "str"
}, {
    "name": "WMO ID",
    "description":
    "the World Meteorological Organization (WMO) number for the station. If the station has no WMO number (or one has not yet been matched to this station), then the field is blank.",
    "type": "str"
}]

PRIMARY_GEOMETRY_COLUMN = {
    "name": "geometry",
    "description": "Location of measurement.",
    "type": "geometry"
}

ELEMENTS_VALUES = {
    "PRCP": "Precipitation (tenths of mm)",
    "SNOW": "Snowfall (mm)",
    "SNWD": "Snow depth (mm)",
    "TMAX": "Maximum temperature (tenths of degrees C)",
    "TMIN": "Minimum temperature (tenths of degrees C)",
    "ACMC":
    "Average cloudiness midnight to midnight from 30-second ceilometer data (percent)",
    "ACMH":
    "Average cloudiness midnight to midnight from manual observations (percent)",
    "ACSC":
    "Average cloudiness sunrise to sunset from 30-second ceilometer data (percent)",
    "ACSH":
    "Average cloudiness sunrise to sunset from manual observations (percent)",
    "AWDR": "Average daily wind direction (degrees)",
    "AWND": "Average daily wind speed (tenths of meters per second)",
    "DAEV": "Number of days included in the multiday evaporation total (MDEV)",
    "DAPR":
    "Number of days included in the multiday precipiation total (MDPR)",
    "DASF": "Number of days included in the multiday snowfall total (MDSF)",
    "DATN":
    "Number of days included in the multiday minimum temperature (MDTN)",
    "DATX":
    "Number of days included in the multiday maximum temperature (MDTX)",
    "DAWM": "Number of days included in the multiday wind movement (MDWM)",
    "DWPR":
    "Number of days with non-zero precipitation included in multiday precipitation total (MDPR)",
    "EVAP": "Evaporation of water from evaporation pan (tenths of mm)",
    "FMTM":
    "Time of fastest mile or fastest 1-minute wind (hours and minutes, i.e., HHMM)",
    "FRGB": "Base of frozen ground layer (cm)",
    "FRGT": "Top of frozen ground layer (cm)",
    "FRTH": "Thickness of frozen ground layer (cm)",
    "GAHT": "Difference between river and gauge height (cm)",
    "MDEV": "Multiday evaporation total (tenths of mm; use with DAEV)",
    "MDPR":
    "Multiday precipitation total (tenths of mm; use with DAPR and DWPR, if available)",
    "MDSF": "Multiday snowfall total ",
    "MDTN":
    "Multiday minimum temperature (tenths of degrees C; use with DATN)",
    "MDTX":
    "Multiday maximum temperature (tenths of degress C; use with DATX)",
    "MDWM": "Multiday wind movement (km)",
    "MNPN":
    "Daily minimum temperature of water in an evaporation pan (tenths of degrees C)",
    "MXPN":
    "Daily maximum temperature of water in an evaporation pan (tenths of degrees C)",
    "PGTM": "Peak gust time (hours and minutes, i.e., HHMM)",
    "PSUN": "Daily percent of possible sunshine (percent)",
    "SN*#":
    "Minimum soil temperature (tenths of degrees C) where * corresponds to a code for ground cover and # corresponds to a code for soil depth. See metadata for codes.",
    "SX*# ":
    "Maximum soil temperature (tenths of degrees C) where * corresponds to a code for ground cover and # corresponds to a code for soil depth. See metadata for codes.",
    "TAVG": "Average temperature (tenths of degrees C)",
    "THIC": "Thickness of ice on water (tenths of mm)",
    "TOBS": "Temperature at the time of observation (tenths of degrees C)",
    "TSUN": "Daily total sunshine (minutes)",
    "WDF1": "Direction of fastest 1-minute wind (degrees)",
    "WDF2": "Direction of fastest 2-minute wind (degrees)",
    "WDF5": "Direction of fastest 5-second wind (degrees)",
    "WDFG": "Direction of peak wind gust (degrees)",
    "WDFI": "Direction of highest instantaneous wind (degrees)",
    "WDFM": "Fastest mile wind direction (degrees)",
    "WDMV": "24-hour wind movement (km)",
    "WESD": "Water equivalent of snow on the ground (tenths of mm)",
    "WESF": "Water equivalent of snowfall (tenths of mm)",
    "WSF1": "Fastest 1-minute wind speed (tenths of meters per second)",
    "WSF2": "Fastest 2-minute wind speed (tenths of meters per second)",
    "WSF5": "Fastest 5-second wind speed (tenths of meters per second)",
    "WSFG": "Peak gust wind speed (tenths of meters per second)",
    "WSFI": "Highest instantaneous wind speed (tenths of meters per second)",
    "WSFM": "Fastest mile wind speed (tenths of meters per second)",
    "WT**": "Weather Type, see metadata for ** categories",
    "WV**": "Weather in the Vicinity, see metadata for ** categories",
}
