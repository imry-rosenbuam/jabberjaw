import mkt_coord_defaults
import pandas_datareader as pdr
from datetime import datetime
import dpath.util as dp

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





if __name__ == "__main__":
    name = "DFF"
    source = "fred"
    start_date = datetime(year=2022,month=1,day=1)
    end_date = datetime(year=2022,month=4,day=24)
    xx = pdr.DataReader(name,source,start_date,end_date)
    print(xx)
    print("Hello Nurse")