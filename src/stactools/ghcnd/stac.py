import logging
import mimetypes
from typing import Any, List, Optional, Callable

import fsspec
from pystac import (
    CatalogType,
    Collection,
    Extent,
    MediaType,
    SpatialExtent,
    TemporalExtent,
)
from pystac.asset import Asset
from pystac.extensions.file import FileExtension
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.projection import (
    ProjectionExtension,
    SummariesProjectionExtension,
)
from pystac.extensions.scientific import ScientificExtension
from pystac.item import Item
from pystac.link import Link
from pystac.rel_type import RelType
from pystac.utils import str_to_datetime
from shapely.geometry.geo import box

from stactools.ghcnd.constants import (
    ADDITIONAL_METADATA_URL,
    CITATION,
    DATA_TABLE_COLUMNS,
    DOI,
    ELEMENTS_VALUES,
    GHCND_CRS,
    GHCND_DESCRIPTION,
    GHCND_EPSG,
    GHCND_ID,
    GHCND_TITLE,
    HOMEPAGE_URL,
    LICENSE,
    LICENSE_LINK,
    METADATA_URL,
    PRIMARY_GEOMETRY_COLUMN,
    PROVIDERS,
    SPATIAL_EXTENT,
    STATION_TABLE_COLUMNS,
    STATIONS_URL,
    TEMPORAL_EXTENT,
)

logger = logging.getLogger(__name__)


def create_collection() -> Collection:
    """Create a STAC Collection
    Create a STAC Collection for the GHCNd.

    Returns:
        Collection: STAC Collection object
    """

    temporal_extent = [
        str_to_datetime(dt) if dt is not None else None
        for dt in TEMPORAL_EXTENT
    ]
    extent = Extent(
        SpatialExtent([SPATIAL_EXTENT]),
        TemporalExtent(temporal_extent),
    )

    collection = Collection(
        id=GHCND_ID,
        title=GHCND_TITLE,
        description=GHCND_DESCRIPTION,
        license=LICENSE,
        providers=PROVIDERS,
        extent=extent,
        catalog_type=CatalogType.RELATIVE_PUBLISHED,
    )

    proj_ext = SummariesProjectionExtension(collection)
    proj_ext.epsg = [GHCND_EPSG]

    sci_ext = ScientificExtension.ext(collection, add_if_missing=True)
    sci_ext.doi = DOI
    sci_ext.citation = CITATION

    collection.add_asset(
        "GHCNd Stations",
        Asset(media_type=MediaType.TEXT,
              roles=["metadata"],
              title="GHCNd Stations",
              href=STATIONS_URL))

    collection.add_asset(
        "Metadata",
        Asset(media_type=MediaType.TEXT,
              roles=["metadata"],
              title="Metadata",
              href=METADATA_URL))

    collection.add_asset(
        "Metadata, Additional",
        Asset(media_type=MediaType.TEXT,
              roles=["metadata"],
              title="Metadata, Additional",
              href=ADDITIONAL_METADATA_URL))

    collection.add_link(LICENSE_LINK)
    collection.add_link(
        Link(RelType.VIA, target=HOMEPAGE_URL, title="HOMEPAGE_URL"))

    item_asset_ext = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_asset_ext.item_assets = {
        "GHCNd":
        AssetDefinition({
            "types": ["application/zip"],
            "roles": ["data"],
            "title": "GHCNd Data",
            "proj:epsg": GHCND_EPSG
        }),
        "Stations":
        AssetDefinition({
            "types": [MediaType.TEXT],
            "roles": ["metadata"],
            "title": "GHCNd Stations",
            "proj:epsg": GHCND_EPSG
        }),
        "Metadata":
        AssetDefinition({
            "types": [MediaType.TEXT],
            "roles": ["metadata"],
            "title": "Metadata",
        })
    }

    return collection


def create_item(data_asset_href: str,
    data_href_modifier: Optional[Callable] = None,
) -> Item:
    """Create a STAC Item
    Create a STAC Item for one year of the GHCNd.

    Args:
        data_asset_href (str): The HREF pointing to the data asset associated with the item

    Returns:
        Item: STAC Item object
    """
    if data_href_modifier is not None:
        data_mod_href = data_href_modifier(data_asset_href)
    else:
        data_mod_href = data_asset_href

    polygon = box(*SPATIAL_EXTENT, ccw=True)
    coordinates = [list(i) for i in list(polygon.exterior.coords)]
    geometry = {"type": "Polygon", "coordinates": [coordinates]}

    # Data & Station tables assumed to be left merged on column "ID"
    table_columns = DATA_TABLE_COLUMNS + STATION_TABLE_COLUMNS + [
        PRIMARY_GEOMETRY_COLUMN
    ]
    table_columns = [
        i for n, i in enumerate(table_columns)
        if i not in table_columns[n + 1:]
    ]

    properties = {
        "title": "GHCNd",
        "description": "Global Historical Climate Network-daily",
        "start_datetime": TEMPORAL_EXTENT[0],
        "end_datetime": TEMPORAL_EXTENT[1],
        "table:columns": table_columns,
        "table:primary_geometry": PRIMARY_GEOMETRY_COLUMN["name"],
    }

    item = Item(
        id="GHCNd",
        geometry=geometry,
        bbox=SPATIAL_EXTENT,
        datetime=str_to_datetime(TEMPORAL_EXTENT[0]),
        properties=properties,
        stac_extensions=[
            "https://stac-extensions.github.io/table/v1.0.0/schema.json"
        ])

    # Scientific Extension
    sci_ext = ScientificExtension.ext(item, add_if_missing=True)
    sci_ext.doi = DOI
    sci_ext.citation = CITATION

    # Projection Extensions
    proj_ext = ProjectionExtension.ext(item, add_if_missing=True)
    proj_ext.epsg = GHCND_EPSG
    proj_ext.wkt2 = GHCND_CRS.to_wkt()
    proj_ext.bbox = SPATIAL_EXTENT
    proj_ext.geometry = geometry

    media_type = mimetypes.guess_type(data_asset_href)[0]
    data_asset = Asset(href=data_asset_href,
                       media_type=media_type,
                       roles=["data"],
                       title="GHCNd Values",
                       extra_fields={
                           "table:columns": table_columns,
                       })
    item.add_asset("data", data_asset)

    item.add_asset(
        "GHCNd Stations",
        Asset(media_type=MediaType.TEXT,
              roles=["metadata"],
              title="GHCNd Stations",
              href=STATIONS_URL,
              extra_fields={
                  "table:columns": STATION_TABLE_COLUMNS,
              }))

    item.add_asset(
        "Metadata",
        Asset(media_type=MediaType.TEXT,
              roles=["metadata"],
              title="GHCNd Metadata",
              href=METADATA_URL))

    item.add_asset(
        "Metadata, Additional",
        Asset(media_type=MediaType.TEXT,
              roles=["metadata"],
              title="Metadata, Additional",
              href=ADDITIONAL_METADATA_URL))

    # Asset Projection Extension
    data_asset_proj_ext = ProjectionExtension.ext(data_asset,
                                                  add_if_missing=True)
    data_asset_proj_ext.epsg = proj_ext.epsg
    data_asset_proj_ext.wkt2 = proj_ext.wkt2
    data_asset_proj_ext.bbox = proj_ext.bbox
    data_asset_proj_ext.geometry = proj_ext.geometry

    # File Extension
    data_asset_file_ext = FileExtension.ext(data_asset, add_if_missing=True)
    # The following odd type annotation is needed
    mapping: List[Any] = [{
        "values": [value],
        "summary": summary,
    } for value, summary in ELEMENTS_VALUES.items()]
    data_asset_file_ext.values = mapping
    with fsspec.open(data_mod_href) as file:
        size = file.size
        if size is not None:
            data_asset_file_ext.size = size

    return item
