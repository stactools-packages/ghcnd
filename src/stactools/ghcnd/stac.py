import logging

from pystac import (CatalogType, Collection, Extent, MediaType, SpatialExtent,
                    TemporalExtent)
from pystac.asset import Asset
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.projection import (ProjectionExtension,
                                          SummariesProjectionExtension)
from pystac.extensions.scientific import ScientificExtension
from pystac.item import Item
from pystac.link import Link
from pystac.rel_type import RelType
from pystac.utils import str_to_datetime
from shapely.geometry.geo import box

from stactools.ghcnd.constants import (CITATION, DOI, GHCND_DESCRIPTION,
                                       GHCND_EPSG, GHCND_ID, GHCND_TITLE,
                                       HOMEPAGE, LICENSE, METADATA_URL,
                                       PROVIDERS, SPATIAL_EXTENT, STATIONS_URL,
                                       TEMPORAL_EXTENT)

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

    collection.add_link(Link(RelType.VIA, target=HOMEPAGE, title="Homepage"))

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


def create_item(asset_href: str) -> Item:
    """Create a STAC Item
    Create a STAC Item for one year of the GHCNd. The asset_href should include
     the observation year as the first part of the filename.

    Args:
        asset_href (str): The HREF pointing to an asset associated with the item

    Returns:
        Item: STAC Item object
    """

    year = asset_href.split("/")[-1][:4]
    try:
        int(year)
    except ValueError:
        print("Asset URL does not contain the year")

    polygon = box(*SPATIAL_EXTENT, ccw=True)
    coordinates = [list(i) for i in list(polygon.exterior.coords)]
    geometry = {"type": "Polygon", "coordinates": [coordinates]}

    properties = {
        "title": f"GHCNd {year}",
        "description":
        f"Global Historical Climate Network-daily for the year {year}",
        "start_datetime": f"{year}-01-01T00:00:00Z",
        "end_datetime": f"{int(year)+1}-01-01T00:00:00Z",
    }

    item = Item(
        id=f"GHCNd_{year}",
        geometry=geometry,
        bbox=SPATIAL_EXTENT,
        datetime=str_to_datetime(f"{year}, 1, 1"),
        properties=properties,
    )

    sci_ext = ScientificExtension.ext(item, add_if_missing=True)
    sci_ext.doi = DOI
    sci_ext.citation = CITATION

    proj_attrs = ProjectionExtension.ext(item, add_if_missing=True)
    proj_attrs.epsg = GHCND_EPSG

    item.add_asset(
        "data",
        Asset(
            href=asset_href,
            media_type="application/zip",
            roles=["data"],
            title=f"GHCNd {year}",
        ),
    )

    item.add_asset(
        "GHCNd Stations",
        Asset(media_type=MediaType.TEXT,
              roles=["metadata"],
              title="GHCNd Stations",
              href=STATIONS_URL))

    item.add_asset(
        "Metadata",
        Asset(media_type=MediaType.TEXT,
              roles=["metadata"],
              title="GHCNd Metadata",
              href=METADATA_URL))

    return item
