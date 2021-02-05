#JabberJaw Package Readme
## Env Variables
In order to run the package you will need to set an environment variable **TSDB_DATA** for the path to which we will be saving all data.
## Set up the Mkt Coordinates config
Mkt coordinates ( the way we call up data) is driven by a config that exist in the path mentioned above. However, if it does not exist
there is a need to generate it first. There are few scripts in the package that can do so:
- **tsdb_utils.equity_stock_cfg_update** can be run in order to generate the cfg/update it with the data needed for equity stock data.
##Equity
### Market Coordinates Setup
Run **tsdb_utils.equity_stock_cfg_update** in order to generate the Mkt coordinates to support equity stock market data.
### Equity Marketiser
**Equity_stock_marketsier** can be run in order to demonstrate how to download the S&P500 data to the path mentioned above.
### Equity Viewer
These model (** equity_stick_viewer **) has an example on how to view an already downloaded equity data.