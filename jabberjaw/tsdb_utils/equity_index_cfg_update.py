from urllib import response
from xml.etree.ElementPath import xpath_tokenizer
import bs4 as bs
import requests
import yaml
import jabberjaw.utils.mkt_classes as mkt_classes
import mkt_coord_defaults
import dpath.util as dp

def load_index_tickers() -> list[str]:
    """loads a list of tickers from yahoo for indices"""
    resp = requests.get("https://finance.yahoo.com/world-indices/")
    soup = bs.BeautifulSoup(resp.text,'lxml')
    table = soup.find('table')
    tickers=[]
    for row in table.find_all('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('\n', '')
        tickers.append(ticker)
    return tickers

def save_index_tickers(tickers:list[str]) -> None:
    """Update the YAML coordinates cfg with equity indices"""
    mkt_class = "equity".upper()
    mkt_type = "index".upper()
    mkt_coordinates = mkt_classes.mkt_data_cfg()
    # let us load the defaults
    defaults = mkt_coord_defaults.defaults.copy()
    mkt_default_cfg_load = mkt_classes.mkt_defaults_cfg()
    dp.merge(defaults, mkt_default_cfg_load)
    
    equity_defaults = [i for i in dp.search(defaults, f"{mkt_class}/{mkt_type}", yielded=True)].pop()[1]
    
    for ticker in tickers:
        mkt_asset = ticker
        points_defaults = [i for i in dp.search(defaults,f"{mkt_class}/{mkt_type}/{mkt_asset}",yielded=True)]
        points_defaults = points_defaults.pop()[1] if  len(points_defaults) else []
        points = list(set(points_defaults))
        existing_value = {'points':points}
        value = equity_defaults.copy()
        value.update(existing_value)
        xpath = f'{mkt_class}/{mkt_type}/{mkt_asset}'
        dp.new(mkt_coordinates,xpath,value)
        
    print('data ready to be saved')
    mkt_data_cfg = {'defaults':defaults, 'market_coordinates': mkt_coordinates}
    
    with open(mkt_classes.tsdb_path() + 'market_coord_cfg.YAML','w+') as f:
        yaml.dump(mkt_data_cfg,f)
        print("data saved successfully to mkt data config")    
    return None

def update_mkt_cfg_equitu() -> None:
    """add indices tickers to the config"""
    tickers = load_index_tickers()
    save_index_tickers(tickers)

if __name__ == "__main__":
    
    print(load_index_tickers())
    update_mkt_cfg_equitu()
    print("Le Fin")