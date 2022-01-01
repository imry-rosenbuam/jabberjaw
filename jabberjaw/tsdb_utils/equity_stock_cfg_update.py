import bs4 as bs
import requests
import yaml
import jabberjaw.utils.mkt_classes as mkt_classes
import mkt_coord_defaults as mkt_coord_defaults
import dpath.util as dp


def load_sp500_tickers() -> list:
    """loads the list of the S&P500 tickers"""
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('\n', '').replace(".", "-")
        tickers.append(ticker)
    print("loaded snp500 tickers")
    return tickers


def save_snp_500_tickers(tickers: list) -> None:
    """update the YAML market coordinates config with the SNP500 tickers"""
    mkt_class = "equity".upper()
    mkt_type = "single stock".upper()
    market_coordinates = mkt_classes.mkt_data_cfg()
    # lets load the defaults and then see if there is tsdb yaml to overwrite base defaults
    defaults = mkt_coord_defaults.defaults.copy()
    mkt_default_cfg_load = mkt_classes.mkt_defaults_cfg()
    dp.merge(defaults, mkt_default_cfg_load)

    equity_defaults = [i for i in dp.search(defaults, '{0}/{1}'.format(mkt_class, mkt_type), yielded=True)].pop()[1]

    for ticker in tickers:
        mkt_asset = ticker
        points_default = [i for i in
                          dp.search(market_coordinates, f'{mkt_type}/{mkt_class}/{mkt_asset}/points',
                                    yielded=True)]
        points_default = points_default.pop()[1] if len(points_default) else []
        points = list(set(points_default))
        exisiting_value = {'points': points}
        value = equity_defaults.copy()
        value.update(exisiting_value)

        xpath = '{0}/{1}/{2}'.format(mkt_class, mkt_type, mkt_asset)
        dp.new(market_coordinates, xpath, value)


    print("data ready to be saved")
    mkt_data_cfg = {'market_coordinates': market_coordinates, 'defaults': defaults}

    with open(mkt_classes.tsdb_path() + 'market_coord_cfg.YAML', "w+") as f:
        yaml.dump(mkt_data_cfg, f)
        print("added snp500 tickers to the config")



def update_mkt_cfg_equity():
    """ adds the equity tickers to the mkt data cfg"""
    snp_tickers = load_sp500_tickers()
    save_snp_500_tickers(snp_tickers)


if __name__ == '__main__':
    # an example of how to update the cfg with the equity symbols
    update_mkt_cfg_equity()

