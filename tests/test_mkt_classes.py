"""Tests for jabberjaw.utils.mkt_classes"""
import pytest
from jabberjaw.utils.mkt_classes import (
    MktCoord,
    parse_mkt_coord,
    tenor_parse,
)
from dateutil.relativedelta import relativedelta


class TestMktCoord:
    def test_construction_uppercases_fields(self):
        c = MktCoord("equity", "single stock", "aapl", "spot")
        assert c.mkt_class == "EQUITY"
        assert c.mkt_type == "SINGLE STOCK"
        assert c.mkt_asset == "AAPL"
        assert c.point == "SPOT"

    def test_optional_fields_default_to_none(self):
        c = MktCoord("fx", "currency pair", "USDEUR")
        assert c.quote is None
        assert c.point is None

    def test_get_mkt_tuple_returns_tuple(self):
        c = MktCoord("ir", "usd", "T-BILL", "3M")
        t = c.get_mkt_tuple()
        assert isinstance(t, tuple)
        assert t[0] == "IR"
        assert t[2] == "T-BILL"

    def test_copy_is_independent(self):
        c = MktCoord("equity", "index", "SP500", "spot")
        c2 = c.copy()
        c2.point = "FORWARD"
        assert c.point == "SPOT"

    def test_deepcopy_is_independent(self):
        c = MktCoord("equity", "index", "SP500", "spot")
        c2 = c.deepcopy()
        c2.point = "FORWARD"
        assert c.point == "SPOT"


class TestParseMktCoord:
    def test_full_string_parsed_correctly(self):
        c = parse_mkt_coord("equity_index_snp500_spot.bid@yahoo")
        assert c.mkt_class == "EQUITY"
        assert c.mkt_type == "INDEX"
        assert c.mkt_asset == "SNP500"
        assert c.point == "SPOT"
        assert c.quote == "BID"
        assert c.source == "YAHOO"

    def test_minimal_string_parsed(self):
        c = parse_mkt_coord("fx_currencypair_USDEUR")
        assert c.mkt_class == "FX"
        assert c.mkt_type == "CURRENCYPAIR"
        assert c.mkt_asset == "USDEUR"

    def test_default_source_applied(self):
        c = parse_mkt_coord("equity_stock_aapl")
        assert c.source == "DEFAULT"


class TestTenorParse:
    def test_months_parsed(self):
        result = tenor_parse("3M")
        assert result == relativedelta(months=3)

    def test_years_parsed(self):
        result = tenor_parse("2Y")
        assert result == relativedelta(years=2)

    def test_invalid_tenor_raises(self):
        with pytest.raises(ValueError):
            tenor_parse("INVALID")

    def test_invalid_tenor_too_long_raises(self):
        with pytest.raises(ValueError):
            tenor_parse("100M")
