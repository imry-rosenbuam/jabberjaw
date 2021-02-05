import bs4 as bs
import requests
import yaml
import jabberjaw.mkt_utils.mkt_classes as mkt_classes
import mkt_coord_defaults as mkt_coord_defaults
import dpath.util as dp


def load_sp500_tickers() -> list:
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace('\n', '').replace(".", "-")
        tickers.append(ticker)
    return tickers


def save_snp_500_tickers(tickers: list) -> None:
    mkt_class = "equity".upper()
    mkt_type = "stock".upper()
    mkt_asset = "cash".upper()
    market_coordinates = mkt_classes.mkt_data_cfg()
    # lets load the defaults and then see if there is tsdb yaml to overwrite base defaults
    defaults = mkt_coord_defaults.defaults.copy()
    mkt_default_cfg_load = mkt_classes.mkt_defaults_cfg()
    defaults.update(mkt_default_cfg_load)

    equity_defaults = [i for i in dp.search(defaults, '{0}/{1}'.format(mkt_class, mkt_type), yielded=True)].pop()[1]
    points_default = [i for i in
                      dp.search(market_coordinates, '{0}/{1}/{2}/points'.format(mkt_class, mkt_type, mkt_asset),
                                yielded=True)]
    points_default = points_default.pop()[1] if len(points_default) else []

    points = tickers.copy()
    points = list(set(points_default) | set(points))
    value = {'points': points}
    value.update(equity_defaults)

    xpath = '{0}/{1}/{2}'.format(mkt_class, mkt_type, mkt_asset)
    dp.new(market_coordinates, xpath, value)

    mkt_data_cfg = {'market_coordinates': market_coordinates, 'defaults': defaults}

    with open(mkt_classes.tsdb_path() + 'market_coord_cfg.YAML', "w") as f:
        yaml.dump(mkt_data_cfg, f)


if __name__ == '__main__':
    tickers1 = load_sp500_tickers()
    save_snp_500_tickers(tickers1)
