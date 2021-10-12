# flake8: noqa

from typing import Any, Dict

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

HOMEPAGE = "https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00861/html"
METADATA_URL = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/readme-by_year.txt"
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
             url=HOMEPAGE),
    Provider(name="Microsoft",
             roles=[ProviderRole.HOST],
             url="https://planetarycomputer.microsoft.com"),
]

KEYWORDS = ["NOAA", "ghcnd", "GHCNd", "GHCN-Daily"]

TEMPORAL_EXTENT = ["1763-01-01T00:00:00Z", None]
SPATIAL_EXTENT = [-180.0, -90.0, 180.0, 85.0]

CITATION = "Menne, Matthew J., Imke Durre, Bryant Korzeniewski, Shelley McNeal, Kristy Thomas, Xungang Yin, Steven Anthony, Ron Ray, Russell S. Vose, Byron E.Gleason, and Tamara G. Houston (2012): Global Historical Climatology Network - Daily (GHCN-Daily), Version 3. NOAA National Climatic Data Center. doi:10.7289/V5D21VHZ"
DOI = "10.7289/V5D21VHZ"

THUMBNAIL_HREF = "https://ai4edatasetspublicassets.blob.core.windows.net/assets/pc_thumbnails/ghcnd.png"

MSFT_SHORT_DESCRIPTION = "Global Historical Climatology Network - Daily (GHCN-Daily), Version 3"
MSFT_STORAGE_ACCOUNT = "ai4edataeuwest"
MSFT_CONTAINER = "noaa-ghcnd"
