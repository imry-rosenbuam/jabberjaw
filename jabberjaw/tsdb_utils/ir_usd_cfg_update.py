from jabberjaw.utils import mkt_classes
import mkt_coord_defaults
import pandas_datareader as pdr
from datetime import datetime
import dpath.util as dp
import mkt_coord_defaults as mktc_defaults
import yaml

ccy = "USD"

symbols = {
    "FED-FUND": "DFF",
    "COM-PAPER-F": {"1M":"DCPF1M","2M":"DCPF2M","3M":"DCPF3M"},
    "COM-PAPER-NONF": {"1M":"DCPN30","2M":"DCPN2M","3M":"DCPN3M"},
    "PRIME-LOAN-RATE": "DPRIME",
    "DISCOUNT-WINDOW": "DPCREDIT",
    "T-BILL": {"4WK":"DTB4WK", "3M":"DTB3","6M":"DTB6","1Y":"DTB1YR"},
    "TREASURY-CM": {"1M":"DGS1MO","3M":"DGS3MO","6M": "DGS6MO", "1Y": "DGS1", "2Y": "DGS2"
                    ,"3Y": "DGS3", "5Y": "DGS5", "7Y": "DGS7", "10Y":"DGS10", "20Y": "DGS20", "30Y": "DGS30"} 
}


def update_cfg_ir_usd_coords() -> None:
    """Update the YAML config with USD IR coords"""
    mkt_class = "IR".upper()
    mkt_type = "USD"
    market_coordinates = mkt_classes.mkt_data_cfg()
    defaults = mkt_coord_defaults.defaults.copy()
    mkt_defaults_cfg_load =  mkt_classes.mkt_defaults_cfg()
    dp.merge(defaults, mkt_defaults_cfg_load)
    
    ir_defaults = [i for i in dp.search(defaults, f"{mkt_class}/{mkt_type}", yielded=True)].pop()[1]
    
    for k,v in symbols.items():
        mkt_asset = k
        #points_default = [i for i in dp.search(market_coordinates, f'{mkt_class}/{mkt_type}/{mkt_asset}/points', yielded=True)]
        #points_default = points_default.pop()[1] if len(points_default) else []
        points  = list(v.keys()) if isinstance(v, dict) else []
        tickers = list(v.values()) if isinstance(v, dict) else v
        
        existing_values = {"points": points, "tickers": tickers}
        value = ir_defaults.copy()
        value.update(existing_values)
        
        xpath = f'{mkt_class}/{mkt_type}/{mkt_asset}'
        dp.new(market_coordinates, xpath, value)
        
        print("data ready to be saved")
    mkt_data_cfg = {'market_coordinates': market_coordinates, 'defaults': defaults}

    with open(mkt_classes.tsdb_path() + 'market_coord_cfg.YAML', "w+") as f:
        yaml.dump(mkt_data_cfg, f)
        print("added USD IR tickers to the config")
    
    
    return None


if __name__ == "__main__":
    name = "DFF"
    source = "fred"
    start_date = datetime(year=2022,month=1,day=1)
    end_date = datetime(year=2022,month=4,day=24)
    #x = pdr.DataReader(name,source,start_date,end_date)
    update_cfg_ir_usd_coords()
    print("Hello Nurse")