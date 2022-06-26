import yaml
import jabberjaw.utils.mkt_classes as mkt_classes
import bs4 as bs
import requests
import re
import dpath.util as dp
import numpy as np
import mkt_coord_defaults as mktc_defaults
from itertools import permutations

excluded_ccy = []

ccy_pairs = list(map(str.upper,['gbp', 'usd', 'eur', 'ils', 'sek',
             'cad', 'dkk', 'aud', 'nzd', 'jpy', 'chf', 'nok'])) #effectively for start it is G11 and ILS

link = "https://en.wikipedia.org/wiki/ISO_4217"

def generate_pairs() -> list[tuple]:
    return(list(permutations(ccy_pairs,2)))

def load_ccy() -> None:

    resp = requests.get(link)
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': "wikitable sortable collapsible"})
    ticker = []
    for row in table.find_all('tr')[1:]:
        elements = row.find_all('td')
        ccy = elements[0].text
        num = elements[1].text
        minor = elements[2].text
        tpl = (ccy, num, minor)
        ticker.append(tpl)
    return ticker


def save_ccy(tickers: list[tuple]) -> None:
    """Update the config with list of currencies we have downloaded"""

    ccy_static_data = dict()

    for ticker in tickers:
        ccy_static_data[ticker[0]] = {"num": int(
            ticker[1]), "D": np.nan if ticker[2] == '.' else int(ticker[2][0])}

    with open(mkt_classes.tsdb_path() + "ccy_list.YAML", 'w+') as f:
        yaml.dump(ccy_static_data, f)
        print('generated the static data for currencies')


def generate_config_ccy_pairs() -> None:
    """generate all of the ccy paris that we will be intereseted in during our research"""
    mkt_class = "fx".upper()
    mkt_type = "currency pair".upper()
    market_coordinates = mkt_classes.mkt_data_cfg()
    defaults = mktc_defaults.defaults.copy()
    mkt_default_cfg_load = mkt_classes.mkt_defaults_cfg()
    dp.merge(defaults, mkt_default_cfg_load)
    
    fx_defaults = [i for i in dp.search(
            defaults, '{0}/{1}'.format(mkt_class, mkt_type), yielded=True)].pop()[1]

    for ticker in generate_pairs():
        sym = ticker[0] + ticker[1]
        mkt_asset = sym
        points_default = [i for i in dp.search(market_coordinates,f'{mkt_class}/{mkt_type}/{mkt_asset}/points',yielded=True)]
        points_default = points_default.pop()[1] if len(points_default) else []
        points = list(set(points_default))
        existing_value = {'points':points, 'tickers': ticker[0] +ticker[1] + '=X'}
        value = fx_defaults.copy()
        value.update(existing_value)

        xpath = f'{mkt_class}/{mkt_type}/{mkt_asset}'
        dp.new(market_coordinates,xpath,value)

    print('data is ready to be saved')

    mkt_data_cfg = {'market_coordinates': market_coordinates, 'defaults': defaults}

    with open(mkt_classes.tsdb_path() + 'market_coord_cfg.YAML','w+') as f:
        yaml.dump(mkt_data_cfg,f)
        print("data saved successfuly to mkt coord config")

if __name__ == "__main__":
    ccy_tickers = load_ccy()
    save_ccy(ccy_tickers)
    generate_config_ccy_pairs()