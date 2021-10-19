[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stactools-packages/ghcnd/main?filepath=docs/installation_and_basic_usage.ipynb)

# ghcnd

- Name: ghcnd
- Package: `stactools.ghcnd`
- Owner: @jamesvrt
- Dataset homepage: https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00861/html
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
  - [scientific](https://github.com/stac-extensions/scientific/)
  - [item-assets](https://github.com/stac-extensions/item-assets/)
  - [table](https://github.com/TomAugspurger/table)

The Global Historical Climatology Network daily (GHCNd) is an integrated database of daily climate summaries from land surface stations across the globe. GHCNd is made up of daily climate records from numerous sources that have been integrated and subjected to a common suite of quality assurance reviews.

This package builds a STAC Collection composed of one Item containing one data Asset. This data asset is assumed to be a concatenated version of all [individual GHCNd years](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/) left merged on [GHCNd stations](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt) by `ID`. An example is given for [1763](tests/data/1763-1764.csv)

## Examples

### STAC objects

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

### Command-line usage

Description of the command line functions

```bash
$ stac ghcnd create-item -s source -d destination

$ stac ghcnd create-collection -d destination

$ stac ghcnd populate-collection -s source -d destination
```

Use `stac ghcnd --help` to see all subcommands and options.
