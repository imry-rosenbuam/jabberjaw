defaults = {
    "EQUITY": {
        "ETF":
            {"default_source": "yahoo",
             'extractor': 'default',
             'points': 'spot'},
        "INDEX": {
            "default_source": "yahoo",
            "extractor": "default"},
        "SINGLE STOCK": {
            'default_source': 'yahoo',
            'extractor': 'default'}
    },
    "FX": {
        "CURRENCY PAIR": {
            "default_source": "yahoo",
            "extractor": "default"}
    },
    "IR": {
     "USD": {
         "default_source": "fred",
         "extractor": "default"}
    }
}
