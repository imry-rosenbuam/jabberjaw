import jabberjaw.mkt_utils.mkt_classes as mkt_classes
import jabberjaw.mkt_utils.data_manager_parquet as dmp
import jabberjaw.equity.equity_stock_extractor as ese


def view_equity_cash_data(symbol: str) -> None:
    df = ese.load_equity_cash_market_data(symbol)


if __name__ == '__main__':
    x = 1
