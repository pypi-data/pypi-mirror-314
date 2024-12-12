import datetime as dt
import os
import unittest
from rumorz.client import RumorzClient
from rumorz.enums import AssetClass, EntityType, EntityMetrics, Lookback

rumorz = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'],
                      api_url='http://localhost:8000')  #  http://localhost:8000 - https://rumorz.azurewebsites.net


class TestRumorz(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        entities = rumorz.graph.search_entities(**{
            "name_search": "Bitcoin",
            "symbol_search": "BTC",
            "asset_class": AssetClass.CRYPTO,
            "entity_type": EntityType.FINANCIAL_ASSET,
            "limit": 1
        })
        assert len(entities) == 1, "Bitcoin entity search returned an unexpected number of results"
        cls.bitcoin_entity_id = 115176#entities[0]['id']

    def test_time_series(self):
        timeseries = rumorz.graph.get_metrics(**{
            "ids": [self.bitcoin_entity_id],
            "metrics":  [EntityMetrics.SENTIMENT],
            "lookback": Lookback.ONE_DAY,
            "page": 1,
            "limit": 100
        })
        self.assertTrue(len(timeseries) > 0)

    def test_entity_summary(self):
        entity_update = rumorz.agent.summarize(**{
            "id": self.bitcoin_entity_id,
            "timestamp": dt.datetime.utcnow().isoformat(),
            "sentiment_gte": 0.5,
            "sentiment_lte": 1.0
        })
        self.assertTrue(len(entity_update) > 0)

    def test_get_ranking(self):
        screener = rumorz.graph.get_ranking(**{
            "lookback": Lookback.ONE_DAY,
            "entity_type": EntityType.FINANCIAL_ASSET,
            "sort_by": EntityMetrics.MENTIONS,
            "ascending": False,
            "page": 1,
            "limit": 10,
        })
        self.assertTrue(len(screener) > 0)

    def test_limit_validation(self):
        try:
            rumorz.graph.get_ranking(**{
                "lookback": Lookback.THREE_MONTHS,
                "sort_by": EntityMetrics.MENTIONS,
                "entity_type": EntityType.FINANCIAL_ASSET,
                "page": 1,
                "limit": 1000,
            })
        except Exception as e:
            self.assertTrue("limit" in str(e).lower())

    def test_get_feed(self):
        posts = rumorz.graph.get_feed(**{
            "ids": [self.bitcoin_entity_id],
            "lookback": Lookback.ONE_WEEK,
            "sentiment_gte": 0.5,
            "sentiment_lte": 1.0,
            "page": 1,
            "limit": 10
        })
        self.assertTrue(len(posts) > 0)

    def test_get_price_stats(self):
        summary = rumorz.graph.get_price_stats(**{
            "id": self.bitcoin_entity_id,
        })
        print(summary)
        self.assertTrue(len(summary) > 0)

