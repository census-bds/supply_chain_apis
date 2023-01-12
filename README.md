# suppy-chain-apis

This repository creates a wrapper for querying and cleaning data from Census APIs which are relevant to the supply chain. The available data sources are listed below. It is specifically created to migrate data into the Supply Chain Information Portal (SCIP) database.

# Environment setup
Packages use are documented in sup_chain_env.yml. To create the conda environment, run `conda env create -f sup_chain_env.yml`.

# Data sources

## Annual Survey of Manufacturers 
https://www.census.gov/data/developers/data-sets/Annual-Survey-of-Manufactures.html

## International Trade 
https://www.census.gov/data/developers/data-sets/international-trade.html

## Economic Census 
https://www.census.gov/data/developers/data-sets/economic-census.html

## CFS 
https://www.census.gov/data/developers/data-sets/cfs.html

## NAICS Concordance Files
https://www.census.gov/naics/?68967
Different survey years use different NAICS codes. We use these concordance files to harmonize all codes to 2022.
