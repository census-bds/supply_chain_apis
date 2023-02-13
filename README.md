# suppy-chain-apis

This repository creates a wrapper for querying and cleaning data from Census APIs which are relevant to the supply chain. The available data sources are listed below. It is specifically created to migrate data into the Supply Chain Information Portal (SCIP) database. Those migrations are done in [this repo](https://github.com/census-bds/supply-chain-app). At a high level, the following steps need to be performed for each API call to prepare for migration. These can vary by data source.
1. Flags for missing or invalid data need to be cleaned and removed accordingly.
2. All data should correspond to a geographic area and have a [GEO_ID](https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html#:~:text=What%20are%20GEOIDs%3F%20The%20Census%20Bureau%20and%20other,presentation%2C%20and%20exchange%20of%20geographic%20and%20statistical%20data).
3. All data should correspond to either an industry or a product. Industry is primarily queried at the NAICS level, but product codes can vary between NAPCS, HS, and SCTG.

# Environment setup
Packages use are documented in sup_chain_env.yml. To create the conda environment, run `conda env create -f sup_chain_env.yml`.

# Getting started
1. Familiarize yourself with various datasets available on Census APIs by going to https://api.census.gov/data/. I recommend doing a Ctrl+F of your dataset of interest. The "c_variablesLink" value will link you to a site where you can see an endpoint's available URL parameters and variables. Those URLs tend to end with "variables.json". You can replace that with "variables.html" for a more readable view. For example, https://api.census.gov/data/2012/cbp/variables.json and https://api.census.gov/data/2012/cbp/variables.html. Most endpoints are not very well documented as far as how to format API calls. The best way to figure it out is to look at example pages. That can be reached by replacing "variables" with "examples" in the URL. For example, https://api.census.gov/data/2012/cbp/examples.html. Links with more detailed information about each data source can be foudn in this repo's wiki.
2. Fill out api_endpoints.yml according to the example. There should be data sources at the highest level, each data source's endpoints within that, and then values for each URL parameter at the most nested level.
3. Fill out config.py according to the template with a Census API key and the path to a state to GEO_ID crosswalk. To work with SCIP, all data will need a GEO_ID field. We place a crosswalk here in order to add GEO_IDs to endpoints that do not include GEO_ID, namely International Trade.

# Examples
```
import intltrade
i = intltrade.IntlTrade()
i.available_vars # Shows what variables are available by endpoint
dfs = i.lookup_all() # Pulls all data for International Trade that is documented within api_endpoints.yml and cleans it for SCIP migration. Returns data as a list of dataframes.
```
