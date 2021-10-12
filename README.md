[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/stactools-packages/ghcnd/main?filepath=docs/installation_and_basic_usage.ipynb)

# stactools-ghcnd

- Name: ghcnd
- Package: `stactools.ghcnd`
- Owner: @jamesvrt
- Dataset homepage: https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00861/html
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
  - [scientific](https://github.com/stac-extensions/scientific/)
  - [item-assets](https://github.com/stac-extensions/item-assets/)

The Global Historical Climatology Network daily (GHCNd) is an integrated database of daily climate summaries from land surface stations across the globe. GHCNd is made up of daily climate records from numerous sources that have been integrated and subjected to a common suite of quality assurance reviews.

## Examples

### STAC objects

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

### Command-line usage

Description of the command line functions

```bash
$ stac ghcnd create-item -s source -d destination

$ stac ghcnd create-collection -d destination

$ stac ghcnd populate-collection -s source -d destination --start_year 1900 --end_year 1910
```

Use `stac ghcnd --help` to see all subcommands and options.
