# suppy-chain-apis

This repository creates a wrapper for querying and cleaning data from Census APIs which are relevant to the supply chain. The available data sources are listed below. It is specifically created to migrate data into the Supply Chain Information Portal (SCIP) database.

# Environment setup
Packages use are documented in sup_chain_env.yml. To create the conda environment, run `conda env create -f sup_chain_env.yml`.

# Getting started
1. Fill out api_endpoints.yml according to the example. There should be data sources at the highest level, each data source's endpoints within that, and then values for each URL parameter at the most nested level.
2. Fill out config.py according to the template with a Census API key and the path to a state to GEO_ID crosswalk. To work with SCIP, all data will need a GEO_ID field. We place a crosswalk here in order to add GEO_IDs to endpoints that do not include GEO_ID, namely International Trade.

# Examples
```
import intltrade
i = intltrade.IntlTrade()
i.available_vars # Shows what variables are available by endpoint
dfs = i.lookup_all() # Pulls all data for International Trade that is documented within api_endpoints.yml and cleans it for SCIP migration.
```
