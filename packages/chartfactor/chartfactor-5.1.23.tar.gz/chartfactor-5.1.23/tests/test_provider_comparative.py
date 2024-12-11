import os
import json
import unittest
import pandas as pd
import sys

sys.path.append("..")
from chartfactor.src.provider import Provider
from data.provider_comparative_data import ProviderComparativeData as prov_data


class TestProviderComparative(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.realpath(__file__)) + '/csv/ticket_sales.csv'
        path_ctt = os.path.dirname(os.path.realpath(__file__)) + '/csv/chicago_taxi_trips.csv'
        path_lfb = os.path.dirname(os.path.realpath(__file__)) + '/csv/london_fire_brigade.csv'
        ts = pd.read_csv(path, low_memory=False)
        cls.df = ts
        cls.df_ctt = pd.read_csv(path_ctt, low_memory=False)
        cls.df_lfb = pd.read_csv(path_lfb, low_memory=False)

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    # TODO: Fix this test
    # def test_visualize_pivot_table_benchmark(self):
    #     # Fist query
    #     config = {
    #         "config": {
    #             "filters": [
    #                 {
    #                     "path": "eventname",
    #                     "label": "eventname",
    #                     "enabled": True,
    #                     "operation": "IN",
    #                     "value": [
    #                         "Macbeth"
    #                     ],
    #                     "relative": False,
    #                     "presetValue": False,
    #                     "isTextFilter": False,
    #                     "origin": {
    #                         "name": "eventname",
    #                         "label": "eventname",
    #                         "type": "ATTRIBUTE",
    #                         "originName": "eventname",
    #                         "originalType": "object",
    #                         "originLabel": "Event"
    #                     }
    #                 }
    #             ],
    #             "groups": [],
    #             "metrics": [
    #                 {
    #                     "name": "pricepaid",
    #                     "func": "sum",
    #                     "customLabel": False,
    #                     "label": "pricepaid",
    #                     "hideFunction": False,
    #                     "is": "Metric",
    #                     "type": "INTEGER",
    #                     "originName": "pricepaid",
    #                     "originalType": "int64",
    #                     "originLabel": "Price Paid"
    #                 }
    #             ],
    #             "comparative": [
    #                 {
    #                     "id": "27e5834a-e6f4-4e2b-bdba-010ad9b478bb",
    #                     "name": "pricepaid",
    #                     "filters": {
    #                         "q1": []
    #                     },
    #                     "func": "sum",
    #                     "label": "benchmark",
    #                     "benchmarkLabel": None,
    #                     "useName": "benchmark",
    #                     "isComparative": True,
    #                     "compareType": "benchmark",
    #                     "usingFilters": [
    #                         "eventname"
    #                     ],
    #                     "removeAfter": [],
    #                     "with": "-1|frame",
    #                     "benchmarkFunction": "avg",
    #                     "against": [],
    #                     "hideFunction": False,
    #                     "originalIndex": 1,
    #                     "is": "ComparativeMetric",
    #                     "type": "INTEGER",
    #                     "originName": "pricepaid",
    #                     "originalType": "int64",
    #                     "originLabel": "Price Paid",
    #                     "baseMetric": {
    #                         "name": "pricepaid",
    #                         "label": "pricepaid",
    #                         "type": "INTEGER",
    #                         "originName": "pricepaid",
    #                         "originalType": "int64",
    #                         "func": "sum",
    #                         "originLabel": "Price Paid"
    #                     },
    #                     "execute": True,
    #                     "originalMetricType": "INTEGER",
    #                     "groups": [
    #                         {
    #                             "name": "venuename",
    #                             "label": "venuename",
    #                             "limit": None,
    #                             "is": "Row",
    #                             "type": "ATTRIBUTE",
    #                             "originName": "venuename",
    #                             "originalType": "object",
    #                             "originLabel": "Venue",
    #                             "sort": {
    #                                 "dir": "asc",
    #                                 "name": "venuename"
    #                             }
    #                         },
    #                         {
    #                             "name": "likerock",
    #                             "label": "likerock",
    #                             "limit": None,
    #                             "is": "Row",
    #                             "type": "ATTRIBUTE",
    #                             "originName": "likerock",
    #                             "originalType": "object",
    #                             "originLabel": "Likes Rock",
    #                             "sort": {
    #                                 "dir": "asc",
    #                                 "name": "likerock"
    #                             }
    #                         },
    #                         {
    #                             "name": "eventname",
    #                             "label": "eventname",
    #                             "type": "ATTRIBUTE",
    #                             "originName": "eventname",
    #                             "originalType": "object",
    #                             "originLabel": "Event",
    #                             "sort": {
    #                                 "dir": "asc",
    #                                 "name": "eventname"
    #                             }
    #                         }
    #                     ]
    #                 }
    #             ]
    #         },
    #         "aggregate": True,
    #         "limit": 20000,
    #         "offset": 0,
    #         "rows": [
    #             {
    #                 "name": "venuename",
    #                 "label": "venuename",
    #                 "limit": None,
    #                 "is": "Row",
    #                 "type": "ATTRIBUTE",
    #                 "originName": "venuename",
    #                 "originalType": "object",
    #                 "originLabel": "Venue"
    #             },
    #             {
    #                 "name": "likerock",
    #                 "label": "likerock",
    #                 "limit": None,
    #                 "is": "Row",
    #                 "type": "ATTRIBUTE",
    #                 "originName": "likerock",
    #                 "originalType": "object",
    #                 "originLabel": "Likes Rock"
    #             }
    #         ],
    #         "columns": [],
    #         "visualization": "Pivot Table",
    #         "element": "visualization"
    #     }

    #     result = json.loads(Provider(self.df, config).visualize()).get('data')
    #     self.assertDictEqual(result, prov_data.TS_PIVOT_TABLE_BENCHMARK_FIRST)

    #     # Benchmark query
    #     config = {
    #         "config": {
    #             "filters": [
    #                 {
    #                     "path": "venuename",
    #                     "operation": "IN",
    #                     "label": "venuename",
    #                     "type": "ATTRIBUTE",
    #                     "origin": {
    #                         "name": "venuename",
    #                         "label": "venuename",
    #                         "limit": None,
    #                         "is": "Row",
    #                         "type": "ATTRIBUTE",
    #                         "originName": "venuename",
    #                         "originalType": "object",
    #                         "originLabel": "Venue",
    #                         "sort": {
    #                             "dir": "asc",
    #                             "name": "venuename"
    #                         }
    #                     },
    #                     "value": [
    #                         "American Airlines Theatre",
    #                         "August Wilson Theatre",
    #                         "Belasco Theatre",
    #                         "Bernard B. Jacobs Theatre",
    #                         "Biltmore Theatre",
    #                         "Booth Theatre",
    #                         "Broadhurst Theatre",
    #                         "Brooks Atkinson Theatre",
    #                         "Carnegie Hall",
    #                         "Charles Playhouse",
    #                         "Cort Theatre",
    #                         "Ethel Barrymore Theatre",
    #                         "Eugene O'Neill Theatre",
    #                         "Geffen Playhouse",
    #                         "George Gershwin Theatre",
    #                         "Greek Theatre",
    #                         "Helen Hayes Theatre",
    #                         "John Golden Theatre",
    #                         "Lincoln Center for the Performing Arts",
    #                         "Longacre Theatre",
    #                         "Lunt-Fontanne Theatre",
    #                         "Lyceum Theatre",
    #                         "Majestic Theatre",
    #                         "Marquis Theatre",
    #                         "Music Box Theatre",
    #                         "Nederlander Theatre",
    #                         "Neil Simon Theatre",
    #                         "New Amsterdam Theatre",
    #                         "Palace Theatre",
    #                         "Paramount Theatre",
    #                         "Pasadena Playhouse",
    #                         "Royce Hall",
    #                         "San Jose Repertory Theatre",
    #                         "Shubert Theatre",
    #                         "St. James Theatre",
    #                         "The Guthrie Theater",
    #                         "Vivian Beaumont Theatre",
    #                         "Walter Kerr Theatre",
    #                         "Winter Garden Theatre"
    #                     ]
    #                 }
    #             ],
    #             "groups": [
    #                 {
    #                     "name": "venuename",
    #                     "label": "venuename",
    #                     "limit": None,
    #                     "is": "Row",
    #                     "type": "ATTRIBUTE",
    #                     "originName": "venuename",
    #                     "originalType": "object",
    #                     "originLabel": "Venue",
    #                     "sort": {
    #                         "dir": "asc",
    #                         "name": "venuename"
    #                     }
    #                 },
    #                 {
    #                     "name": "likerock",
    #                     "label": "likerock",
    #                     "limit": None,
    #                     "is": "Row",
    #                     "type": "ATTRIBUTE",
    #                     "originName": "likerock",
    #                     "originalType": "object",
    #                     "originLabel": "Likes Rock",
    #                     "sort": {
    #                         "dir": "asc",
    #                         "name": "likerock"
    #                     }
    #                 },
    #                 {
    #                     "name": "eventname",
    #                     "label": "eventname",
    #                     "type": "ATTRIBUTE",
    #                     "originName": "eventname",
    #                     "originalType": "object",
    #                     "originLabel": "Event",
    #                     "sort": {
    #                         "dir": "asc",
    #                         "name": "eventname"
    #                     }
    #                 }
    #             ],
    #             "metrics": [
    #                 {
    #                     "name": "pricepaid",
    #                     "func": "sum",
    #                     "customLabel": False,
    #                     "label": "pricepaid",
    #                     "hideFunction": False,
    #                     "is": "Metric",
    #                     "type": "INTEGER",
    #                     "originName": "pricepaid",
    #                     "originalType": "int64",
    #                     "originLabel": "Price Paid"
    #                 }
    #             ],
    #             "comparative": [
    #                 {
    #                     "id": "4c00702d-3ae3-492d-b800-89bbeacde149",
    #                     "name": "pricepaid",
    #                     "filters": {
    #                         "q1": []
    #                     },
    #                     "func": "sum",
    #                     "label": "benchmark",
    #                     "benchmarkLabel": None,
    #                     "useName": "benchmark",
    #                     "isComparative": True,
    #                     "compareType": "benchmark",
    #                     "usingFilters": [
    #                         "eventname"
    #                     ],
    #                     "removeAfter": [],
    #                     "with": "-1|frame",
    #                     "benchmarkFunction": "avg",
    #                     "against": [],
    #                     "hideFunction": False,
    #                     "originalIndex": 1,
    #                     "is": "ComparativeMetric",
    #                     "type": "INTEGER",
    #                     "originName": "pricepaid",
    #                     "originalType": "int64",
    #                     "originLabel": "Price Paid",
    #                     "baseMetric": {
    #                         "name": "pricepaid",
    #                         "label": "pricepaid",
    #                         "type": "INTEGER",
    #                         "originName": "pricepaid",
    #                         "originalType": "int64",
    #                         "func": "sum",
    #                         "originLabel": "Price Paid"
    #                     },
    #                     "execute": True,
    #                     "originalMetricType": "INTEGER",
    #                     "groups": [
    #                         {
    #                             "name": "venuename",
    #                             "label": "venuename",
    #                             "limit": None,
    #                             "is": "Row",
    #                             "type": "ATTRIBUTE",
    #                             "originName": "venuename",
    #                             "originalType": "object",
    #                             "originLabel": "Venue",
    #                             "sort": {
    #                                 "dir": "asc",
    #                                 "name": "venuename"
    #                             }
    #                         },
    #                         {
    #                             "name": "likerock",
    #                             "label": "likerock",
    #                             "limit": None,
    #                             "is": "Row",
    #                             "type": "ATTRIBUTE",
    #                             "originName": "likerock",
    #                             "originalType": "object",
    #                             "originLabel": "Likes Rock",
    #                             "sort": {
    #                                 "dir": "asc",
    #                                 "name": "likerock"
    #                             }
    #                         },
    #                         {
    #                             "name": "eventname",
    #                             "label": "eventname",
    #                             "type": "ATTRIBUTE",
    #                             "originName": "eventname",
    #                             "originalType": "object",
    #                             "originLabel": "Event",
    #                             "sort": {
    #                                 "dir": "asc",
    #                                 "name": "eventname"
    #                             }
    #                         }
    #                     ]
    #                 }
    #             ]
    #         },
    #         "aggregate": True,
    #         "limit": 20000,
    #         "offset": 0,
    #         "rows": [
    #             {
    #                 "name": "venuename",
    #                 "label": "venuename",
    #                 "limit": None,
    #                 "is": "Row",
    #                 "type": "ATTRIBUTE",
    #                 "originName": "venuename",
    #                 "originalType": "object",
    #                 "originLabel": "Venue"
    #             },
    #             {
    #                 "name": "likerock",
    #                 "label": "likerock",
    #                 "limit": None,
    #                 "is": "Row",
    #                 "type": "ATTRIBUTE",
    #                 "originName": "likerock",
    #                 "originalType": "object",
    #                 "originLabel": "Likes Rock"
    #             }
    #         ],
    #         "columns": [],
    #         "visualization": "Pivot Table",
    #         "element": "visualization",
    #         "benchmarkQuery": True
    #     }
    #     result = json.loads(Provider(self.df, config).visualize()).get('data')
    #     self.assertDictEqual(result, prov_data.TS_PIVOT_TABLE_BENCHMARK_BENCHMARK)

    def test_visualize_pivot_table_standard_rate(self):
        # Fist query
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "eventname",
                        "label": "eventname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Macbeth"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "eventname",
                            "label": "eventname",
                            "type": "ATTRIBUTE",
                            "originName": "eventname",
                            "originalType": "object",
                            "originLabel": "Event"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "type": "PERCENT",
                        "label": "Rate",
                        "is": "Metric",
                        "func": "sum"
                    }
                ],
                "comparative": [
                    {
                        "id": "5b5f235d-d625-4af8-a023-9a56abf52773",
                        "name": "pricepaid",
                        "filters": {
                            "q1": []
                        },
                        "func": "sum",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate",
                        "usingFilters": [
                            "eventname"
                        ],
                        "removeAfter": [
                            {
                                "name": "pricepaid",
                                "func": "sum"
                            }
                        ],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 0,
                        "is": "ComparativeMetric",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "Price Paid",
                        "baseMetric": {
                            "name": "pricepaid",
                            "label": "pricepaid",
                            "type": "INTEGER",
                            "originName": "pricepaid",
                            "originalType": "int64",
                            "func": "sum",
                            "originLabel": "Price Paid"
                        },
                        "execute": True,
                        "originalMetricType": "PERCENT",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "limit": None,
                                "is": "Row",
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "object",
                                "originLabel": "Category Name",
                                "sort": {
                                    "dir": "asc",
                                    "name": "catname"
                                }
                            }
                        ]
                    }
                ]
            },
            "hasDerivedFields": False,
            "aggregate": True,
            "limit": 20000,
            "offset": 0,
            "rows": [
                {
                    "name": "catname",
                    "label": "catname",
                    "limit": None,
                    "is": "Row",
                    "type": "ATTRIBUTE",
                    "originName": "catname",
                    "originalType": "object",
                    "originLabel": "Category Name"
                }
            ],
            "columns": [],
            "visualization": "Pivot Table",
            "element": "visualization"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_PIVOT_TABLE_STANDARD_RATE_FIRST)

        # Benchmark query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "catname",
                        "operation": "IN",
                        "label": "catname",
                        "type": "ATTRIBUTE",
                        "origin": {
                            "name": "catname",
                            "label": "catname",
                            "limit": None,
                            "is": "Row",
                            "type": "ATTRIBUTE",
                            "originName": "catname",
                            "originalType": "object",
                            "originLabel": "Category Name",
                            "sort": {
                                "dir": "asc",
                                "name": "catname"
                            }
                        },
                        "enabled": True,
                        "value": [
                            "Plays"
                        ]
                    }
                ],
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "limit": None,
                        "is": "Row",
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "object",
                        "originLabel": "Category Name",
                        "sort": {
                            "dir": "asc",
                            "name": "catname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "type": "PERCENT",
                        "label": "Rate",
                        "is": "Metric",
                        "func": "sum"
                    }
                ],
                "comparative": [
                    {
                        "id": "5b5f235d-d625-4af8-a023-9a56abf52773",
                        "name": "pricepaid",
                        "filters": {
                            "q1": []
                        },
                        "func": "sum",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate",
                        "usingFilters": [
                            "eventname"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 0,
                        "is": "ComparativeMetric",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "Price Paid",
                        "baseMetric": {
                            "name": "pricepaid",
                            "label": "pricepaid",
                            "type": "INTEGER",
                            "originName": "pricepaid",
                            "originalType": "int64",
                            "func": "sum",
                            "originLabel": "Price Paid"
                        },
                        "execute": True,
                        "originalMetricType": "PERCENT",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "limit": None,
                                "is": "Row",
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "object",
                                "originLabel": "Category Name",
                                "sort": {
                                    "dir": "asc",
                                    "name": "catname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": True,
            "limit": 20000,
            "offset": 0,
            "rows": [
                {
                    "name": "catname",
                    "label": "catname",
                    "limit": None,
                    "is": "Row",
                    "type": "ATTRIBUTE",
                    "originName": "catname",
                    "originalType": "object",
                    "originLabel": "Category Name"
                }
            ],
            "columns": [],
            "visualization": "Pivot Table",
            "element": "visualization",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_PIVOT_TABLE_STANDARD_RATE_BENCHMARK)

    def test_visualize_kpi_transactions_rate(self):
        # Fist query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "catgroup",
                        "label": "Catgroup",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catgroup",
                            "label": "catgroup",
                            "type": "ATTRIBUTE",
                            "originName": "catgroup",
                            "originalType": "object",
                            "originLabel": "catgroup"
                        }
                    },
                    {
                        "path": "saletime",
                        "label": "Saletime",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "label": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "object",
                            "timestampGranularity": "YEAR",
                            "originLabel": "saletime"
                        }
                    },
                    {
                        "path": "eventname",
                        "label": "Eventname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "All My Sons"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "eventname",
                            "label": "eventname",
                            "type": "ATTRIBUTE",
                            "originName": "eventname",
                            "originalType": "object",
                            "originLabel": "eventname"
                        }
                    },
                    {
                        "path": "likemusicals",
                        "label": "Likemusicals",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "True"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "likemusicals",
                            "label": "likemusicals",
                            "type": "ATTRIBUTE",
                            "originName": "likemusicals",
                            "originalType": "object",
                            "originLabel": "likemusicals"
                        }
                    },
                    {
                        "path": "catname",
                        "label": "Catname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catname",
                            "label": "catname",
                            "type": "ATTRIBUTE",
                            "originName": "catname",
                            "originalType": "object",
                            "originLabel": "catname"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [],
                "metrics": [
                    {
                        "name": "count",
                        "func": "",
                        "customLabel": False,
                        "label": "Transactions",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER"
                    }
                ],
                "comparative": [
                    {
                        "id": "df12b34c-a387-4eb9-a7fa-bec97cd746dd",
                        "name": "count",
                        "filters": {
                            "q1": [
                                {
                                    "path": "catgroup",
                                    "label": "Catgroup",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "Shows"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "catgroup",
                                        "label": "catgroup",
                                        "type": "ATTRIBUTE",
                                        "originName": "catgroup",
                                        "originalType": "object",
                                        "originLabel": "catgroup"
                                    }
                                },
                                {
                                    "path": "saletime",
                                    "label": "Saletime",
                                    "enabled": True,
                                    "operation": "BETWEEN",
                                    "value": [
                                        "2008-04-01 00:00:00.000",
                                        "2008-07-31 23:59:59.999"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "saletime",
                                        "label": "saletime",
                                        "type": "TIME",
                                        "originName": "saletime",
                                        "originalType": "object",
                                        "timestampGranularity": "YEAR",
                                        "originLabel": "saletime"
                                    }
                                },
                                {
                                    "path": "likemusicals",
                                    "label": "Likemusicals",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "True"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "likemusicals",
                                        "label": "likemusicals",
                                        "type": "ATTRIBUTE",
                                        "originName": "likemusicals",
                                        "originalType": "object",
                                        "originLabel": "likemusicals"
                                    }
                                },
                                {
                                    "path": "catname",
                                    "label": "Catname",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "Plays"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "catname",
                                        "label": "catname",
                                        "type": "ATTRIBUTE",
                                        "originName": "catname",
                                        "originalType": "object",
                                        "originLabel": "catname"
                                    }
                                }
                            ]
                        },
                        "func": "",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate",
                        "usingFilters": [
                            "eventname"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "baseMetric": {
                            "label": "Transactions",
                            "func": "",
                            "type": "INTEGER",
                            "name": "count"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": []
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "KPI"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_KPI_FIRS)

        # Benchmark query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "catgroup",
                        "label": "Catgroup",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catgroup",
                            "label": "catgroup",
                            "type": "ATTRIBUTE",
                            "originName": "catgroup",
                            "originalType": "object",
                            "originLabel": "catgroup"
                        }
                    },
                    {
                        "path": "saletime",
                        "label": "Saletime",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "label": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "object",
                            "timestampGranularity": "YEAR",
                            "originLabel": "saletime"
                        }
                    },
                    {
                        "path": "likemusicals",
                        "label": "Likemusicals",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "True"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "likemusicals",
                            "label": "likemusicals",
                            "type": "ATTRIBUTE",
                            "originName": "likemusicals",
                            "originalType": "object",
                            "originLabel": "likemusicals"
                        }
                    },
                    {
                        "path": "catname",
                        "label": "Catname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catname",
                            "label": "catname",
                            "type": "ATTRIBUTE",
                            "originName": "catname",
                            "originalType": "object",
                            "originLabel": "catname"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [],
                "metrics": [
                    {
                        "name": "count",
                        "func": "",
                        "customLabel": False,
                        "label": "Transactions",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER"
                    }
                ],
                "comparative": [
                    {
                        "id": "df12b34c-a387-4eb9-a7fa-bec97cd746dd",
                        "name": "count",
                        "filters": {
                            "q1": [
                                {
                                    "path": "catgroup",
                                    "label": "Catgroup",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "Shows"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "catgroup",
                                        "label": "catgroup",
                                        "type": "ATTRIBUTE",
                                        "originName": "catgroup",
                                        "originalType": "object",
                                        "originLabel": "catgroup"
                                    }
                                },
                                {
                                    "path": "saletime",
                                    "label": "Saletime",
                                    "enabled": True,
                                    "operation": "BETWEEN",
                                    "value": [
                                        "2008-04-01 00:00:00.000",
                                        "2008-07-31 23:59:59.999"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "saletime",
                                        "label": "saletime",
                                        "type": "TIME",
                                        "originName": "saletime",
                                        "originalType": "object",
                                        "timestampGranularity": "YEAR",
                                        "originLabel": "saletime"
                                    }
                                },
                                {
                                    "path": "likemusicals",
                                    "label": "Likemusicals",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "True"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "likemusicals",
                                        "label": "likemusicals",
                                        "type": "ATTRIBUTE",
                                        "originName": "likemusicals",
                                        "originalType": "object",
                                        "originLabel": "likemusicals"
                                    }
                                },
                                {
                                    "path": "catname",
                                    "label": "Catname",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "Plays"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "catname",
                                        "label": "catname",
                                        "type": "ATTRIBUTE",
                                        "originName": "catname",
                                        "originalType": "object",
                                        "originLabel": "catname"
                                    }
                                }
                            ]
                        },
                        "func": "",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate",
                        "usingFilters": [
                            "eventname"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "baseMetric": {
                            "label": "Transactions",
                            "func": "",
                            "type": "INTEGER",
                            "name": "count"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": []
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "KPI"
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_KPI_BENCHMARK)

    def test_visualize_rate_against_benchmark(self):
        # Fist query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "catgroup",                
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ]
                    },
                    {
                        "path": "saletime",                               
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ]
                    },
                    {
                        "path": "eventname",
                        "operation": "IN",
                        "value": [
                            "All My Sons"
                        ]
                    },
                    {
                        "path": "likemusicals",               
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ]
                    },
                    {
                        "path": "catname",               
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ]
                    }
                ],        
                "groups": [
                    {
                        "name": "catgroup",
                        "label": "catgroup",
                        "sort": {
                            "name": "count",
                            "func": "",                    
                            "label": "",                
                            "dir": "desc"
                        },
                        "limit": 10                
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Like Musicals rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {                
                        "name": "count",
                        "func": "",
                        "label": "Like Musicals rate",
                        "benchmarkLabel": "Avg event in the group",
                        "useName": "like_musicals_rate",
                        "isComparative": True,
                        "compareType": "rate-benchmark",
                        "usingFilters": [
                            "likemusicals"
                        ],
                        "removeAfter": [
                            {
                                "name": "count",
                                "func": ""
                            }
                        ],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [
                            "eventname"
                        ],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 0,
                        "is": "ComparativeMetric",
                        "baseMetric": {
                            "label": "Transactions",
                            "func": "",
                            "type": "INTEGER",
                            "name": "count"
                        },
                        "groups": [
                            {
                                "name": "catgroup",
                                "label": "catgroup",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "type": "ATTRIBUTE",
                                "originName": "catgroup",
                                "originalType": "object",
                                "originLabel": "catgroup"
                            },
                            {
                                "name": "eventname",
                                "label": "eventname",
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "object",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars"
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_RATE_AGAINST_BENCHMARK_FIRST)

        # Benchmark first query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "catgroup",               
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ]
                    },
                    {
                        "path": "saletime",                
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ]
                    },
                    {
                        "path": "eventname",                
                        "operation": "IN",
                        "value": [
                            "All My Sons"
                        ]
                    },
                    {
                        "path": "catname",                
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ]
                    }
                ],        
                "groups": [
                    {
                        "name": "catgroup",
                        "label": "catgroup",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 10                
                    },
                    {
                        "name": "eventname",
                        "label": "eventname",
                        "type": "ATTRIBUTE",
                        "sort": {
                            "dir": "asc",
                            "name": "eventname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Like Musicals rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {
                        "name": "count",               
                        "func": "",
                        "label": "Like Musicals rate",               
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [
                            "eventname"
                        ],
                        "hideFunction": False,
                        "type": "PERCENT",                
                        "groups": [
                            {
                                "name": "catgroup",
                                "label": "catgroup",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "type": "ATTRIBUTE",
                                "originName": "catgroup",
                                "originalType": "object",
                                "originLabel": "catgroup"
                            },
                            {
                                "name": "eventname",
                                "label": "eventname",
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "object",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_RATE_AGAINST_BENCHMARK_BENCHMARK_FIRST)

        # Benchmark Second query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "catgroup",
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ]
                    },
                    {
                        "path": "saletime",               
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ]
                    },
                    {
                        "path": "likemusicals",                
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ]
                    },
                    {
                        "path": "catname",                
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ]
                    },
                    {
                        "path": "catgroup",
                        "operation": "IN",               
                        "value": [
                            "Shows"
                        ]
                    }
                ],        
                "groups": [
                    {
                        "name": "catgroup",
                        "label": "catgroup",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 10
                    },
                    {
                        "name": "eventname",
                        "label": "eventname",                
                        "sort": {
                            "dir": "asc",
                            "name": "eventname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Like Musicals rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {
                        "name": "count",             
                        "func": "",
                        "label": "Like Musicals rate",
                        "benchmarkLabel": "Avg event in the group",
                        "useName": "like_musicals_rate",
                        "isComparative": True,
                        "compareType": "rate-benchmark",
                        "usingFilters": [
                            "likemusicals"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [
                            "eventname"
                        ],
                        "type": "PERCENT",
                        "groups": [
                            {
                                "name": "catgroup",
                                "label": "catgroup",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "type": "ATTRIBUTE",
                                "originName": "catgroup",
                                "originalType": "object",
                                "originLabel": "catgroup"
                            },
                            {
                                "name": "eventname",
                                "label": "eventname",
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "object",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_RATE_AGAINST_BENCHMARK_BENCHMARK_SECOND)

        # Benchmark third query
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "catgroup",                
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ]
                    },
                    {
                        "path": "saletime",                
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ]
                    },
                    {
                        "path": "catname",                
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ]
                    },
                    {
                        "path": "catgroup",
                        "operation": "IN",                
                        "value": [
                            "Shows"
                        ]
                    }
                ],        
                "groups": [
                    {
                        "name": "catgroup",
                        "label": "catgroup",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 10
                    },
                    {
                        "name": "eventname",
                        "label": "eventname",
                        "type": "ATTRIBUTE",                
                        "sort": {
                            "dir": "asc",
                            "name": "eventname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Like Musicals rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {
                        "id": "47e11b70-1bc8-4eb9-b096-248509d9866f",
                        "name": "count",                
                        "func": "",
                        "label": "Like Musicals rate",
                        "benchmarkLabel": "Avg event in the group",
                        "useName": "like_musicals_rate",
                        "isComparative": True,
                        "compareType": "rate-benchmark",
                        "usingFilters": [
                            "likemusicals"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [
                            "eventname"
                        ],
                        "type": "PERCENT",
                        "groups": [
                            {
                                "name": "catgroup",
                                "label": "catgroup",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "type": "ATTRIBUTE",
                                "originName": "catgroup",
                                "originalType": "object",
                                "originLabel": "catgroup"
                            },
                            {
                                "name": "eventname",
                                "label": "eventname",
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "object",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_RATE_AGAINST_BENCHMARK_BENCHMARK_THIRD)

    def test_visualize_event_revenue_vs_benchmark(self):
        # Fist query
        config = {   
            "config": {
                "filters": [
                    {
                        "path": "catgroup",
                        "label": "Catgroup",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catgroup",
                            "label": "catgroup",
                            "type": "ATTRIBUTE",
                            "originName": "catgroup",
                            "originalType": "object",
                            "originLabel": "catgroup"
                        }
                    },
                    {
                        "path": "saletime",
                        "label": "Saletime",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "label": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "object",
                            "timestampGranularity": "YEAR",
                            "originLabel": "saletime"
                        }
                    },
                    {
                        "path": "eventname",
                        "label": "Eventname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "All My Sons"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "eventname",
                            "label": "eventname",
                            "type": "ATTRIBUTE",
                            "originName": "eventname",
                            "originalType": "object",
                            "originLabel": "eventname"
                        }
                    },
                    {
                        "path": "likemusicals",
                        "label": "Likemusicals",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "likemusicals",
                            "label": "likemusicals",
                            "type": "ATTRIBUTE",
                            "originName": "likemusicals",
                            "originalType": "object",
                            "originLabel": "likemusicals"
                        }
                    },
                    {
                        "path": "catname",
                        "label": "Catname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catname",
                            "label": "catname",
                            "type": "ATTRIBUTE",
                            "originName": "catname",
                            "originalType": "object",
                            "originLabel": "catname"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "pricepaid",
                            "func": "sum",
                            "customLabel": False,
                            "label": "pricepaid",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "INTEGER",
                            "originName": "pricepaid",
                            "originalType": "int64",
                            "originLabel": "pricepaid"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "object",
                        "originLabel": "catname"
                    }
                ],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "func": "sum",
                        "customLabel": False,
                        "label": "pricepaid",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "pricepaid"
                    }
                ],
                "comparative": [
                    {
                        "id": "991115c3-594f-4115-9ecd-e37d1d699cb6",
                        "name": "pricepaid",
                        "filters": {
                            "q1": [
                                {
                                    "path": "catgroup",
                                    "label": "Catgroup",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "Shows"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "catgroup",
                                        "label": "catgroup",
                                        "type": "ATTRIBUTE",
                                        "originName": "catgroup",
                                        "originalType": "object",
                                        "originLabel": "catgroup"
                                    }
                                },
                                {
                                    "path": "saletime",
                                    "label": "Saletime",
                                    "enabled": True,
                                    "operation": "BETWEEN",
                                    "value": [
                                        "2008-04-01 00:00:00.000",
                                        "2008-07-31 23:59:59.999"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "saletime",
                                        "label": "saletime",
                                        "type": "TIME",
                                        "originName": "saletime",
                                        "originalType": "object",
                                        "timestampGranularity": "YEAR",
                                        "originLabel": "saletime"
                                    }
                                },
                                {
                                    "path": "likemusicals",
                                    "label": "Likemusicals",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "TRUE"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "likemusicals",
                                        "label": "likemusicals",
                                        "type": "ATTRIBUTE",
                                        "originName": "likemusicals",
                                        "originalType": "object",
                                        "originLabel": "likemusicals"
                                    }
                                },
                                {
                                    "path": "catname",
                                    "label": "Catname",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "Plays"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "catname",
                                        "label": "catname",
                                        "type": "ATTRIBUTE",
                                        "originName": "catname",
                                        "originalType": "object",
                                        "originLabel": "catname"
                                    }
                                }
                            ]
                        },
                        "func": "sum",
                        "label": "Benchmark",
                        "benchmarkLabel": None,
                        "useName": "benchmark",
                        "isComparative": True,
                        "compareType": "benchmark",
                        "usingFilters": "eventname",
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [],
                        "hideFunction": False,
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "type": "INTEGER",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "pricepaid",
                        "baseMetric": {
                            "name": "pricepaid",
                            "label": "pricepaid",
                            "type": "INTEGER",
                            "originName": "pricepaid",
                            "originalType": "int64",
                            "func": "sum",
                            "originLabel": "pricepaid"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "sort": {
                                    "name": "pricepaid",
                                    "func": "sum",
                                    "customLabel": False,
                                    "label": "pricepaid",
                                    "hideFunction": False,
                                    "metricFunc": "sum",
                                    "dir": "desc",
                                    "is": "Metric",
                                    "type": "INTEGER",
                                    "originName": "pricepaid",
                                    "originalType": "int64",
                                    "originLabel": "pricepaid"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "object",
                                "originLabel": "catname"
                            },
                            {
                                "name": "eventname",
                                "label": "eventname",
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "object",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_EVENT_REVENUE_VS_BENCHMARK_FIRST)

        # Benchmark query
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "catgroup",
                        "label": "Catgroup",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catgroup",
                            "label": "catgroup",
                            "type": "ATTRIBUTE",
                            "originName": "catgroup",
                            "originalType": "object",
                            "originLabel": "catgroup"
                        }
                    },
                    {
                        "path": "saletime",
                        "label": "Saletime",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "label": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "object",
                            "timestampGranularity": "YEAR",
                            "originLabel": "saletime"
                        }
                    },
                    {
                        "path": "likemusicals",
                        "label": "Likemusicals",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "likemusicals",
                            "label": "likemusicals",
                            "type": "ATTRIBUTE",
                            "originName": "likemusicals",
                            "originalType": "object",
                            "originLabel": "likemusicals"
                        }
                    },
                    {
                        "path": "catname",
                        "label": "Catname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catname",
                            "label": "catname",
                            "type": "ATTRIBUTE",
                            "originName": "catname",
                            "originalType": "object",
                            "originLabel": "catname"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "pricepaid",
                            "func": "sum",
                            "customLabel": False,
                            "label": "pricepaid",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "INTEGER",
                            "originName": "pricepaid",
                            "originalType": "int64",
                            "originLabel": "pricepaid"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "object",
                        "originLabel": "catname"
                    },
                    {
                        "name": "eventname",
                        "label": "eventname",
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "object",
                        "originLabel": "eventname",
                        "sort": {
                            "dir": "asc",
                            "name": "eventname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "func": "sum",
                        "customLabel": False,
                        "label": "pricepaid",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "pricepaid"
                    }
                ],
                "comparative": [
                    {
                        "id": "991115c3-594f-4115-9ecd-e37d1d699cb6",
                        "name": "pricepaid",               
                        "func": "sum",
                        "label": "Benchmark",
                        "benchmarkLabel": None,
                        "useName": "benchmark",
                        "isComparative": True,
                        "compareType": "benchmark",
                        "usingFilters": "eventname",
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [],
                        "hideFunction": False,
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "type": "INTEGER",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "pricepaid",
                        "baseMetric": {
                            "name": "pricepaid",
                            "label": "pricepaid",
                            "type": "INTEGER",
                            "originName": "pricepaid",
                            "originalType": "int64",
                            "func": "sum",
                            "originLabel": "pricepaid"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "sort": {
                                    "name": "pricepaid",
                                    "func": "sum",
                                    "customLabel": False,
                                    "label": "pricepaid",
                                    "hideFunction": False,
                                    "metricFunc": "sum",
                                    "dir": "desc",
                                    "is": "Metric",
                                    "type": "INTEGER",
                                    "originName": "pricepaid",
                                    "originalType": "int64",
                                    "originLabel": "pricepaid"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "object",
                                "originLabel": "catname"
                            },
                            {
                                "name": "eventname",
                                "label": "eventname",
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "object",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_EVENT_REVENUE_VS_BENCHMARK_BENCHMARK)

    def test_visualize_benchmark_revenue_by_events_pricepaid_100(self):
        # Fist query
        config = {            
            "config": {
                "filters": [
                    {
                        "path": "catgroup",
                        "label": "Catgroup",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catgroup",
                            "keyword": True,
                            "type": "ATTRIBUTE",
                            "originName": "catgroup",
                            "originalType": "keyword",
                            "label": "catgroup",
                            "originLabel": "catgroup"
                        }
                    },
                    {
                        "path": "saletime",
                        "label": "Saletime",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "date",
                            "label": "saletime",
                            "format": "YYYY-MM-DD HH:mm:ss",
                            "timestampGranularity": "YEAR",
                            "originLabel": "saletime"
                        }
                    },
                    {
                        "path": "eventname",
                        "label": "Eventname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "All My Sons"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "eventname",
                            "keyword": True,
                            "type": "ATTRIBUTE",
                            "originName": "eventname",
                            "originalType": "keyword",
                            "label": "eventname",
                            "originLabel": "eventname"
                        }
                    },
                    {
                        "path": "likemusicals",
                        "label": "Likemusicals",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "likemusicals",
                            "type": "ATTRIBUTE",
                            "originName": "likemusicals",
                            "originalType": "keyword",
                            "label": "likemusicals",
                            "keyword": True,
                            "originLabel": "likemusicals"
                        }
                    },
                    {
                        "path": "catname",
                        "label": "Catname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catname",
                            "keyword": True,
                            "type": "ATTRIBUTE",
                            "originName": "catname",
                            "originalType": "keyword",
                            "label": "catname",
                            "originLabel": "catname"
                        }
                    }
                ],        
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "asc"
                        },
                        "limit": 30,
                        "is": "Attribute",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "keyword",
                        "originLabel": "catname"
                    }
                ],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "type": "MONEY",
                        "originName": "pricepaid",
                        "originalType": "double",
                        "label": "pricepaid",
                        "func": "sum",
                        "originLabel": "pricepaid",
                        "is": "Metric",
                        "customLabel": False,
                        "hideFunction": False
                    }
                ],
                "comparative": [
                    {
                        "id": "92c20518-1cfc-4254-b475-35ecc1138974",
                        "name": "pricepaid_100",
                        "func": "derived",
                        "label": "Benchmark",
                        "benchmarkLabel": None,
                        "useName": "benchmark",
                        "isComparative": True,
                        "compareType": "benchmark",
                        "usingFilters": "eventname",
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [],
                        "hideFunction": False,
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "type": "MONEY",
                        "dependencies": [
                            {
                                "name": "pricepaid",
                                "type": "MONEY",
                                "originName": "pricepaid",
                                "originalType": "double",
                                "label": "pricepaid",
                                "func": "sum",
                                "originLabel": "pricepaid",
                                "is": "Metric",
                                "customLabel": False,
                                "hideFunction": False
                            }
                        ],
                        "originalType": "CFT_DERIVED",
                        "originLabel": "PricePaid 100",
                        "baseMetric": {
                            "name": "pricepaid_100",
                            "label": "PricePaid 100",
                            "type": "MONEY",
                            "dependencies": [
                                {
                                    "name": "pricepaid",
                                    "func": "sum",
                                    "customLabel": False,
                                    "label": "pricepaid",
                                    "hideFunction": False
                                }
                            ],
                            "originalType": "CFT_DERIVED",
                            "originLabel": "PricePaid 100",
                            "func": "derived"
                        },
                        "execute": True,
                        "originalMetricType": "MONEY",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "asc"
                                },
                                "limit": 30,
                                "is": "Attribute",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "keyword",
                                "originLabel": "catname"
                            },
                            {
                                "name": "eventname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "keyword",
                                "label": "eventname",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars"
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_BENCHMARK_REVENUE_PRICEPAID_100_FIRST)

        # Benchmark query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "catgroup",
                        "label": "Catgroup",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Shows"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catgroup",
                            "keyword": True,
                            "type": "ATTRIBUTE",
                            "originName": "catgroup",
                            "originalType": "keyword",
                            "label": "catgroup",
                            "originLabel": "catgroup"
                        }
                    },
                    {
                        "path": "saletime",
                        "label": "Saletime",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-04-01 00:00:00.000",
                            "2008-07-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "date",
                            "label": "saletime",
                            "format": "YYYY-MM-DD HH:mm:ss",
                            "timestampGranularity": "YEAR",
                            "originLabel": "saletime"
                        }
                    },
                    {
                        "path": "likemusicals",
                        "label": "Likemusicals",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "likemusicals",
                            "type": "ATTRIBUTE",
                            "originName": "likemusicals",
                            "originalType": "keyword",
                            "label": "likemusicals",
                            "keyword": True,
                            "originLabel": "likemusicals"
                        }
                    },
                    {
                        "path": "catname",
                        "label": "Catname",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Plays"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "catname",
                            "keyword": True,
                            "type": "ATTRIBUTE",
                            "originName": "catname",
                            "originalType": "keyword",
                            "label": "catname",
                            "originLabel": "catname"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "asc"
                        },
                        "limit": 30,
                        "is": "Attribute",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "keyword",
                        "originLabel": "catname"
                    },
                    {
                        "name": "eventname",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "keyword",
                        "label": "eventname",
                        "originLabel": "eventname",
                        "sort": {
                            "dir": "asc",
                            "name": "eventname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "type": "MONEY",
                        "originName": "pricepaid",
                        "originalType": "double",
                        "label": "pricepaid",
                        "func": "sum",
                        "originLabel": "pricepaid",
                        "is": "Metric",
                        "customLabel": False,
                        "hideFunction": False
                    }
                ],
                "comparative": [
                    {
                        "id": "92c20518-1cfc-4254-b475-35ecc1138974",
                        "name": "pricepaid_100",
                        "filters": {
                            "q1": [
                                {
                                    "path": "catgroup",
                                    "label": "Catgroup",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "Shows"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "catgroup",
                                        "keyword": True,
                                        "type": "ATTRIBUTE",
                                        "originName": "catgroup",
                                        "originalType": "keyword",
                                        "label": "catgroup",
                                        "originLabel": "catgroup"
                                    }
                                },
                                {
                                    "path": "saletime",
                                    "label": "Saletime",
                                    "enabled": True,
                                    "operation": "BETWEEN",
                                    "value": [
                                        "2008-04-01 00:00:00.000",
                                        "2008-07-31 23:59:59.999"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "saletime",
                                        "type": "TIME",
                                        "originName": "saletime",
                                        "originalType": "date",
                                        "label": "saletime",
                                        "format": "YYYY-MM-DD HH:mm:ss",
                                        "timestampGranularity": "YEAR",
                                        "originLabel": "saletime"
                                    }
                                },
                                {
                                    "path": "likemusicals",
                                    "label": "Likemusicals",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "TRUE"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "likemusicals",
                                        "type": "ATTRIBUTE",
                                        "originName": "likemusicals",
                                        "originalType": "keyword",
                                        "label": "likemusicals",
                                        "keyword": True,
                                        "originLabel": "likemusicals"
                                    }
                                },
                                {
                                    "path": "catname",
                                    "label": "Catname",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "Plays"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "catname",
                                        "keyword": True,
                                        "type": "ATTRIBUTE",
                                        "originName": "catname",
                                        "originalType": "keyword",
                                        "label": "catname",
                                        "originLabel": "catname"
                                    }
                                }
                            ]
                        },
                        "func": "derived",
                        "label": "Benchmark",
                        "benchmarkLabel": None,
                        "useName": "benchmark",
                        "isComparative": True,
                        "compareType": "benchmark",
                        "usingFilters": "eventname",
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [],
                        "hideFunction": False,
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "type": "MONEY",
                        "dependencies": [
                            {
                                "name": "pricepaid",
                                "type": "MONEY",
                                "originName": "pricepaid",
                                "originalType": "double",
                                "label": "pricepaid",
                                "func": "sum",
                                "originLabel": "pricepaid",
                                "is": "Metric",
                                "customLabel": False,
                                "hideFunction": False
                            }
                        ],
                        "originalType": "CFT_DERIVED",
                        "originLabel": "PricePaid 100",
                        "baseMetric": {
                            "name": "pricepaid_100",
                            "label": "PricePaid 100",
                            "type": "MONEY",
                            "dependencies": [
                                {
                                    "name": "pricepaid",
                                    "func": "sum",
                                    "customLabel": False,
                                    "label": "pricepaid",
                                    "hideFunction": False
                                }
                            ],
                            "originalType": "CFT_DERIVED",
                            "originLabel": "PricePaid 100",
                            "func": "derived"
                        },
                        "execute": True,
                        "originalMetricType": "MONEY",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "asc"
                                },
                                "limit": 30,
                                "is": "Attribute",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "keyword",
                                "originLabel": "catname"
                            },
                            {
                                "name": "eventname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "keyword",
                                "label": "eventname",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_BENCHMARK_REVENUE_PRICEPAID_100_BENCHMARK)

    def test_visualize_top_10_venue_cities_by_commission(self):
        # Fist query
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "saletime",
                        "label": "Sale Time",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-01-01 01:00:00.000",
                            "2008-01-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "date",
                            "label": "Sale Time",
                            "format": "YYYY-MM-DD HH:mm:ss",
                            "timestampGranularity": "YEAR",
                            "originLabel": "Sale Time"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "venuecity",
                        "label": "Venue City",
                        "sort": {
                            "name": "commission",
                            "func": "sum",
                            "customLabel": False,
                            "label": "commission",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "MONEY",
                            "originName": "commission",
                            "originalType": "double",
                            "originLabel": "commission"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "venuecity",
                        "originalType": "keyword",
                        "originLabel": "Venue City"
                    }
                ],
                "metrics": [
                    {
                        "name": "commission",
                        "func": "sum",
                        "customLabel": False,
                        "label": "commission",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "MONEY",
                        "originName": "commission",
                        "originalType": "double",
                        "originLabel": "commission"
                    }
                ],
                "comparative": [
                    {
                        "id": "1fd9e97b-b5e3-4a78-8986-7c12403af9c7",
                        "name": "commission",                
                        "func": "sum",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate-flat",
                        "usingFilters": [],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "originName": "commission",
                        "originalType": "double",
                        "originLabel": "commission",
                        "baseMetric": {
                            "name": "commission",
                            "type": "MONEY",
                            "originName": "commission",
                            "originalType": "double",
                            "label": "commission",
                            "func": "sum",
                            "originLabel": "commission"
                        },
                        "execute": True,
                        "originalMetricType": "PERCENT",
                        "groups": []
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TOP_10_VENUE_CITIES_BY_COMMISSION_FIRST)

        # Benchmark query
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "saletime",
                        "label": "Sale Time",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-01-01 01:00:00.000",
                            "2008-01-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "date",
                            "label": "Sale Time",
                            "format": "YYYY-MM-DD HH:mm:ss",
                            "timestampGranularity": "YEAR",
                            "originLabel": "Sale Time"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [],
                "metrics": [
                    {
                        "name": "commission",
                        "func": "sum",
                        "customLabel": False,
                        "label": "commission",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "MONEY",
                        "originName": "commission",
                        "originalType": "double",
                        "originLabel": "commission"
                    }
                ],
                "comparative": [
                    {
                        "id": "1fd9e97b-b5e3-4a78-8986-7c12403af9c7",
                        "name": "commission",
                        "func": "sum",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate-flat",
                        "usingFilters": [],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "originName": "commission",
                        "originalType": "double",
                        "originLabel": "commission",
                        "baseMetric": {
                            "name": "commission",
                            "type": "MONEY",
                            "originName": "commission",
                            "originalType": "double",
                            "label": "commission",
                            "func": "sum",
                            "originLabel": "commission"
                        },
                        "execute": True,
                        "originalMetricType": "PERCENT",
                        "groups": []
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TOP_10_VENUE_CITIES_BY_COMMISSION_BENCHMARK)

    def test_visualize_commission_rates_by_category_venue_states(self):
        # Fist query
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "saletime",
                        "label": "Sale Time",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-01-01 01:00:00.000",
                            "2008-01-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "date",
                            "label": "Sale Time",
                            "format": "YYYY-MM-DD HH:mm:ss",
                            "timestampGranularity": "YEAR",
                            "originLabel": "Sale Time"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catname",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "keyword",
                        "label": "Category Name",
                        "originLabel": "Category Name",
                        "is": "Attribute",
                        "sort": {
                            "dir": "desc",
                            "name": "catname"
                        },
                        "origin": "cat_str",
                        "limit": 10
                    },
                    {
                        "name": "venuestate",
                        "type": "ATTRIBUTE",
                        "originName": "venuestate",
                        "originalType": "keyword",
                        "label": "Venue State",
                        "keyword": True,
                        "originLabel": "Venue State",
                        "is": "Attribute",
                        "sort": {
                            "dir": "desc",
                            "name": "venuestate"
                        },
                        "origin": "state_str",
                        "limit": 100
                    }
                ],
                "metrics": [
                    {
                        "name": "commission",
                        "func": "sum",
                        "customLabel": False,
                        "label": "commission",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "MONEY",
                        "originName": "commission",
                        "originalType": "double",
                        "originLabel": "commission"
                    }
                ],
                "comparative": [
                    {
                        "id": "ee27f1e4-4590-4ce9-94ae-82efac24fce6",
                        "name": "commission",
                        "filters": {
                            "q1": [
                                {
                                    "path": "saletime",
                                    "label": "Sale Time",
                                    "enabled": True,
                                    "operation": "BETWEEN",
                                    "value": [
                                        "2008-01-01 01:00:00.000",
                                        "2008-01-31 23:59:59.999"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "saletime",
                                        "type": "TIME",
                                        "originName": "saletime",
                                        "originalType": "date",
                                        "label": "Sale Time",
                                        "format": "YYYY-MM-DD HH:mm:ss",
                                        "timestampGranularity": "YEAR",
                                        "originLabel": "Sale Time"
                                    }
                                }
                            ]
                        },
                        "func": "sum",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate-flat",
                        "usingFilters": [
                            "catname",
                            "state_str"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "originName": "commission",
                        "originalType": "double",
                        "originLabel": "commission",
                        "baseMetric": {
                            "name": "commission",
                            "type": "MONEY",
                            "originName": "commission",
                            "originalType": "double",
                            "label": "commission",
                            "func": "sum",
                            "originLabel": "commission"
                        },
                        "execute": True,
                        "originalMetricType": "PERCENT",
                        "groups": [
                            {
                                "name": "catname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "keyword",
                                "label": "Category Name",
                                "originLabel": "Category Name",
                                "is": "Attribute",
                                "sort": {
                                    "dir": "desc",
                                    "name": "catname"
                                },
                                "origin": "cat_str",
                                "limit": 10
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_COMMISSION_RATE_BY_CATEGORY_VENUE_STATE_FIRST)

        # Benchmark query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "saletime",
                        "label": "Sale Time",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-01-01 01:00:00.000",
                            "2008-01-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "date",
                            "label": "Sale Time",
                            "format": "YYYY-MM-DD HH:mm:ss",
                            "timestampGranularity": "YEAR",
                            "originLabel": "Sale Time"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catname",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "keyword",
                        "label": "Category Name",
                        "originLabel": "Category Name",
                        "is": "Attribute",
                        "sort": {
                            "dir": "desc",
                            "name": "catname"
                        },
                        "origin": "cat_str",
                        "limit": 10
                    }
                ],
                "metrics": [
                    {
                        "name": "commission",
                        "func": "sum",
                        "customLabel": False,
                        "label": "commission",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "MONEY",
                        "originName": "commission",
                        "originalType": "double",
                        "originLabel": "commission"
                    }
                ],
                "comparative": [
                    {
                        "id": "ee27f1e4-4590-4ce9-94ae-82efac24fce6",
                        "name": "commission",
                        "filters": {
                            "q1": [
                                {
                                    "path": "saletime",
                                    "label": "Sale Time",
                                    "enabled": True,
                                    "operation": "BETWEEN",
                                    "value": [
                                        "2008-01-01 01:00:00.000",
                                        "2008-01-31 23:59:59.999"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "saletime",
                                        "type": "TIME",
                                        "originName": "saletime",
                                        "originalType": "date",
                                        "label": "Sale Time",
                                        "format": "YYYY-MM-DD HH:mm:ss",
                                        "timestampGranularity": "YEAR",
                                        "originLabel": "Sale Time"
                                    }
                                }
                            ]
                        },
                        "func": "sum",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate-flat",
                        "usingFilters": [
                            "catname",
                            "state_str"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "originName": "commission",
                        "originalType": "double",
                        "originLabel": "commission",
                        "baseMetric": {
                            "name": "commission",
                            "type": "MONEY",
                            "originName": "commission",
                            "originalType": "double",
                            "label": "commission",
                            "func": "sum",
                            "originLabel": "commission"
                        },
                        "execute": True,
                        "originalMetricType": "PERCENT",
                        "groups": [
                            {
                                "name": "catname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "keyword",
                                "label": "Category Name",
                                "originLabel": "Category Name",
                                "is": "Attribute",
                                "sort": {
                                    "dir": "desc",
                                    "name": "catname"
                                },
                                "origin": "cat_str",
                                "limit": 10
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_COMMISSION_RATE_BY_CATEGORY_VENUE_STATE_BENCHMARK)

    def test_visualize_standard_count_rate_bars(self):
        # Fist query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "saletime",
                        "label": "Sale Time",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-01-01 01:00:00.000",
                            "2008-01-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "label": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "object",
                            "timestampGranularity": "YEAR",
                            "originLabel": "Sale Time"
                        }
                    }
                ],        
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "object",
                        "originLabel": "Category Name"
                    },
                    {
                        "name": "venuestate",
                        "label": "venuestate",
                        "type": "ATTRIBUTE",
                        "originName": "venuestate",
                        "originalType": "object",
                        "originLabel": "Venue State",
                        "is": "Attribute",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "asc"
                        },
                        "origin": "state_str",
                        "limit": 100
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {
                        "id": "2723a29a-7509-4e32-98ee-fb50205bfde1",
                        "name": "count",
                        "filters": {
                            "q1": [
                                {
                                    "path": "saletime",
                                    "label": "Sale Time",
                                    "enabled": True,
                                    "operation": "BETWEEN",
                                    "value": [
                                        "2008-01-01 01:00:00.000",
                                        "2008-01-31 23:59:59.999"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "saletime",
                                        "label": "saletime",
                                        "type": "TIME",
                                        "originName": "saletime",
                                        "originalType": "object",
                                        "timestampGranularity": "YEAR",
                                        "originLabel": "Sale Time"
                                    }
                                }
                            ]
                        },
                        "func": "",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate-flat",
                        "usingFilters": [],
                        "removeAfter": [
                            {
                                "name": "count",
                                "func": ""
                            }
                        ],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 0,
                        "is": "ComparativeMetric",
                        "baseMetric": {
                            "label": "Transactions",
                            "func": "",
                            "type": "INTEGER",
                            "name": "count"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "object",
                                "originLabel": "Category Name"
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_STANDARD_COUNT_RATE_BARS_FIRST)

        # Benchmark query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "saletime",
                        "label": "Sale Time",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2008-01-01 01:00:00.000",
                            "2008-01-31 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "saletime",
                            "label": "saletime",
                            "type": "TIME",
                            "originName": "saletime",
                            "originalType": "object",
                            "timestampGranularity": "YEAR",
                            "originLabel": "Sale Time"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "object",
                        "originLabel": "Category Name"
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {
                        "id": "2723a29a-7509-4e32-98ee-fb50205bfde1",
                        "name": "count",
                        "filters": {
                            "q1": [
                                {
                                    "path": "saletime",
                                    "label": "Sale Time",
                                    "enabled": True,
                                    "operation": "BETWEEN",
                                    "value": [
                                        "2008-01-01 01:00:00.000",
                                        "2008-01-31 23:59:59.999"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "saletime",
                                        "label": "saletime",
                                        "type": "TIME",
                                        "originName": "saletime",
                                        "originalType": "object",
                                        "timestampGranularity": "YEAR",
                                        "originLabel": "Sale Time"
                                    }
                                }
                            ]
                        },
                        "func": "",
                        "label": "Rate",
                        "benchmarkLabel": None,
                        "useName": "rate",
                        "isComparative": True,
                        "compareType": "rate-flat",
                        "usingFilters": [],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 0,
                        "is": "ComparativeMetric",
                        "baseMetric": {
                            "label": "Transactions",
                            "func": "",
                            "type": "INTEGER",
                            "name": "count"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "object",
                                "originLabel": "Category Name"
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_STANDARD_COUNT_RATE_BARS_BENCHMARK)

    def test_visualize_kpi_percent_of_growth(self):
        # Fist query
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "saletime",                
                        "operation": "BETWEEN",
                        "value": [
                            "2008-02-23 00:00:00.000",
                            "2008-02-23 23:59:59.999"
                        ]
                    },
                    {
                        "path": "eventname",                
                        "operation": "IN",
                        "value": [
                            "A Doll's House",
                            "A Bronx Tale",
                            "At The Gates",
                            "A Streetcar Named Desire"
                        ]
                    },
                    {
                        "path": "likemusicals",               
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ]
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "func": "sum",
                        "customLabel": False,
                        "label": "pricepaid",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "pricepaid"
                    }
                ],
                "comparative": [
                    {
                        "id": "caa70e79-918c-4307-8b36-d958594988bb",
                        "name": "pricepaid",
                        "filters": {
                            "q1": [
                                {
                                    "path": "eventname",
                                    "label": "eventname",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "A Doll's House",
                                        "A Bronx Tale",
                                        "At The Gates",
                                        "A Streetcar Named Desire"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "eventname",
                                        "label": "eventname",
                                        "type": "ATTRIBUTE",
                                        "originName": "eventname",
                                        "originalType": "object",
                                        "originLabel": "eventname"
                                    }
                                },
                                {
                                    "path": "likemusicals",
                                    "label": "likemusicals",
                                    "enabled": True,
                                    "operation": "IN",
                                    "value": [
                                        "TRUE"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "likemusicals",
                                        "label": "likemusicals",
                                        "type": "ATTRIBUTE",
                                        "originName": "likemusicals",
                                        "originalType": "object",
                                        "originLabel": "likemusicals"
                                    }
                                },
                                {
                                    "path": "saletime",
                                    "label": "saletime",
                                    "enabled": True,
                                    "operation": "BETWEEN",
                                    "value": [
                                        "2008-02-22 00:00:00.000",
                                        "2008-02-22 23:59:59.999"
                                    ],
                                    "relative": False,
                                    "presetValue": False,
                                    "isTextFilter": False,
                                    "origin": {
                                        "name": "saletime",
                                        "label": "saletime",
                                        "type": "TIME",
                                        "originName": "saletime",
                                        "originalType": "object",
                                        "timestampGranularity": "YEAR",
                                        "originLabel": "saletime"
                                    }
                                }
                            ]
                        },
                        "func": "sum",
                        "label": "Growth against yesterday",
                        "benchmarkLabel": None,
                        "useName": "growth_against_yesterday",
                        "isComparative": True,
                        "compareType": "rate-growth",
                        "usingFilters": [
                            "saletime"
                        ],
                        "removeAfter": [],
                        "with": "-1|day",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "pricepaid",
                        "baseMetric": {
                            "name": "pricepaid",
                            "label": "pricepaid",
                            "type": "INTEGER",
                            "originName": "pricepaid",
                            "originalType": "int64",
                            "func": "sum",
                            "originLabel": "pricepaid"
                        },
                        "execute": True,
                        "originalMetricType": "PERCENT",
                        "groups": [],
                        "offset": -1,
                        "unit": "day"
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "KPI"
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_KPI_PERCENT_GROWTH_FIRST)

        # Benchmark query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "eventname",
                        "operation": "IN",
                        "value": [
                            "A Doll's House",
                            "A Bronx Tale",
                            "At The Gates",
                            "A Streetcar Named Desire"
                        ]
                    },
                    {
                        "path": "likemusicals",
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ]
                    },
                    {
                        "path": "saletime",
                        "operation": "BETWEEN",
                        "value": [
                            "2008-02-22 00:00:00.000",
                            "2008-02-22 23:59:59.999"
                        ]
                    }
                ],
                "groups": [],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "func": "sum",
                        "customLabel": False,
                        "label": "pricepaid",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "pricepaid"
                    }
                ],
                "comparative": [
                    {
                        "id": "caa70e79-918c-4307-8b36-d958594988bb",
                        "name": "pricepaid",
                        "func": "sum",
                        "label": "Growth against yesterday",
                        "benchmarkLabel": None,
                        "useName": "growth_against_yesterday",
                        "isComparative": True,
                        "compareType": "rate-growth",
                        "usingFilters": [
                            "saletime"
                        ],
                        "removeAfter": [],
                        "with": "-1|day",
                        "benchmarkFunction": None,
                        "against": [],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "pricepaid",
                        "baseMetric": {
                            "name": "pricepaid",
                            "label": "pricepaid",
                            "type": "INTEGER",
                            "originName": "pricepaid",
                            "originalType": "int64",
                            "func": "sum",
                            "originLabel": "pricepaid"
                        },
                        "execute": True,
                        "originalMetricType": "PERCENT",
                        "groups": [],
                        "offset": -1,
                        "unit": "day"
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "KPI"
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_KPI_PERCENT_GROWTH_BENCHMARK)

    def test_visualize_rate_compared_against_benchmark_category_group(self):
        # Fist query
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "saletime",                
                        "operation": "BETWEEN",
                        "value": [
                            "2008-02-23 00:00:00.000",
                            "2008-02-23 23:59:59.999"
                        ]
                    },
                    {
                        "path": "eventname",               
                        "operation": "IN",
                        "value": [
                            "A Doll's House",
                            "A Bronx Tale",
                            "At The Gates",
                            "A Streetcar Named Desire"
                        ]
                    },
                    {
                        "path": "likemusicals",                
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ]
                    }
                ],      
                "groups": [
                    {
                        "name": "catgroup",
                        "label": "catgroup",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 10               
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Like Musicals rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {
                        "id": "036c8e2b-54b7-4607-83df-5617f1fb7b32",
                        "name": "count",             
                        "func": "",
                        "label": "Like Musicals rate",
                        "benchmarkLabel": "Avg event in the group",
                        "useName": "like_musicals_rate",
                        "isComparative": True,
                        "compareType": "rate-benchmark",
                        "usingFilters": [
                            "likemusicals"
                        ],
                        "removeAfter": [
                            {
                                "name": "count",
                                "func": ""
                            }
                        ],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [
                            "eventname"
                        ],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 0,
                        "is": "ComparativeMetric",
                        "baseMetric": {
                            "label": "Transactions",
                            "func": "",
                            "type": "INTEGER",
                            "name": "count"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": [
                            {
                                "name": "catgroup",
                                "label": "catgroup",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catgroup",
                                "originalType": "keyword",
                                "originLabel": "catgroup"
                            },
                            {
                                "name": "eventname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "keyword",
                                "label": "eventname",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars"
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_COMPARED_AGAINST_BENCHMARK_CATEGORY_GROUP_FIRST)

        # Benchmark query 1
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "saletime",               
                        "operation": "BETWEEN",
                        "value": [
                            "2008-02-23 00:00:00.000",
                            "2008-02-23 23:59:59.999"
                        ]
                    },
                    {
                        "path": "eventname",               
                        "operation": "IN",
                        "value": [
                            "A Doll's House",
                            "A Bronx Tale",
                            "At The Gates",
                            "A Streetcar Named Desire"
                        ]
                    }
                ],      
                "groups": [
                    {
                        "name": "catgroup",
                        "label": "catgroup",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 10
                    },
                    {
                        "name": "eventname",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "keyword",
                        "label": "eventname",
                        "originLabel": "eventname",
                        "sort": {
                            "dir": "asc",
                            "name": "eventname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Like Musicals rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {
                        "id": "036c8e2b-54b7-4607-83df-5617f1fb7b32",
                        "name": "count",             
                        "func": "",
                        "label": "Like Musicals rate",
                        "benchmarkLabel": "Avg event in the group",
                        "useName": "like_musicals_rate",
                        "isComparative": True,
                        "compareType": "rate-benchmark",
                        "usingFilters": [
                            "likemusicals"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [
                            "eventname"
                        ],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 0,
                        "is": "ComparativeMetric",
                        "baseMetric": {
                            "label": "Transactions",
                            "func": "",
                            "type": "INTEGER",
                            "name": "count"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": [
                            {
                                "name": "catgroup",
                                "label": "catgroup",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catgroup",
                                "originalType": "keyword",
                                "originLabel": "catgroup"
                            },
                            {
                                "name": "eventname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "keyword",
                                "label": "eventname",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_COMPARED_AGAINST_BENCHMARK_CATEGORY_GROUP_BENCHMARK1)

        # Benchmark query 2
        config = {
            "config": {
                "filters": [
                    {
                        "path": "saletime",                
                        "operation": "BETWEEN",
                        "value": [
                            "2008-02-23 00:00:00.000",
                            "2008-02-23 23:59:59.999"
                        ]
                    },
                    {
                        "path": "likemusicals",               
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ]
                    },
                    {
                        "path": "catgroup",
                        "operation": "IN",
                        "label": "catgroup",
                        "type": "ATTRIBUTE",
                        "origin": {
                            "name": "catgroup",
                            "label": "catgroup",
                            "sort": {
                                "name": "count",
                                "func": "",
                                "customLabel": False,
                                "label": "",
                                "hideFunction": False,
                                "metricFunc": "",
                                "dir": "desc"
                            },
                            "limit": 10
                        },
                        "enabled": True,
                        "value": [
                            "Shows",
                            "Concerts"
                        ]
                    }
                ],       
                "groups": [
                    {
                        "name": "catgroup",
                        "label": "catgroup",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "catgroup",
                        "originalType": "keyword",
                        "originLabel": "catgroup"
                    },
                    {
                        "name": "eventname",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "keyword",
                        "label": "eventname",
                        "originLabel": "eventname",
                        "sort": {
                            "dir": "asc",
                            "name": "eventname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Like Musicals rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {
                        "id": "036c8e2b-54b7-4607-83df-5617f1fb7b32",
                        "name": "count",               
                        "func": "",
                        "label": "Like Musicals rate",
                        "benchmarkLabel": "Avg event in the group",
                        "useName": "like_musicals_rate",
                        "isComparative": True,
                        "compareType": "rate-benchmark",
                        "usingFilters": [
                            "likemusicals"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [
                            "eventname"
                        ],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 0,
                        "is": "ComparativeMetric",
                        "baseMetric": {
                            "label": "Transactions",
                            "func": "",
                            "type": "INTEGER",
                            "name": "count"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": [
                            {
                                "name": "catgroup",
                                "label": "catgroup",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catgroup",
                                "originalType": "keyword",
                                "originLabel": "catgroup"
                            },
                            {
                                "name": "eventname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "keyword",
                                "label": "eventname",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_COMPARED_AGAINST_BENCHMARK_CATEGORY_GROUP_BENCHMARK2)

        # Benchmark query 3
        config = {    
            "config": {
                "filters": [
                    {
                        "path": "saletime",               
                        "operation": "BETWEEN",
                        "value": [
                            "2008-02-23 00:00:00.000",
                            "2008-02-23 23:59:59.999"
                        ]
                    },
                    {
                        "path": "catgroup",
                        "operation": "IN",
                        "label": "catgroup",
                        "type": "ATTRIBUTE",
                        "origin": {
                            "name": "catgroup",
                            "label": "catgroup",
                            "sort": {
                                "name": "count",
                                "func": "",
                                "customLabel": False,
                                "label": "",
                                "hideFunction": False,
                                "metricFunc": "",
                                "dir": "desc"
                            },
                            "limit": 10
                        },
                        "enabled": True,
                        "value": [
                            "Shows",
                            "Concerts"
                        ]
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catgroup",
                        "label": "catgroup",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 10
                    },
                    {
                        "name": "eventname",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "keyword",
                        "label": "eventname",
                        "originLabel": "eventname",
                        "sort": {
                            "dir": "asc",
                            "name": "eventname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "count",
                        "type": "PERCENT",
                        "label": "Like Musicals rate",
                        "is": "Metric",
                        "func": ""
                    }
                ],
                "comparative": [
                    {               
                        "name": "count",              
                        "func": "",
                        "label": "Like Musicals rate",
                        "benchmarkLabel": "Avg event in the group",
                        "useName": "like_musicals_rate",
                        "isComparative": True,
                        "compareType": "rate-benchmark",
                        "usingFilters": [
                            "likemusicals"
                        ],
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [
                            "eventname"
                        ],
                        "hideFunction": False,
                        "type": "PERCENT",
                        "originalIndex": 0,
                        "is": "ComparativeMetric",
                        "baseMetric": {
                            "label": "Transactions",
                            "func": "",
                            "type": "INTEGER",
                            "name": "count"
                        },
                        "execute": True,
                        "originalMetricType": "INTEGER",
                        "groups": [
                            {
                                "name": "catgroup",
                                "label": "catgroup",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "desc"
                                },
                                "limit": 10,
                                "is": "Attribute",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catgroup",
                                "originalType": "keyword",
                                "originLabel": "catgroup"
                            },
                            {
                                "name": "eventname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "keyword",
                                "label": "eventname",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_COMPARED_AGAINST_BENCHMARK_CATEGORY_GROUP_BENCHMARK3)

    def test_visualize_benchmark_revenue_events_with_pricepaid_100(self):
        # Fist query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "saletime",
                        "operation": "BETWEEN",
                        "value": [
                            "2008-02-23 00:00:00.000",
                            "2008-02-23 23:59:59.999"
                        ]
                    },
                    {
                        "path": "eventname",
                        "operation": "IN",
                        "value": [
                            "A Doll's House",
                            "A Bronx Tale",
                            "At The Gates",
                            "A Streetcar Named Desire"
                        ]
                    },
                    {
                        "path": "likemusicals",
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ]
                    }
                ],
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "asc"
                        },
                        "limit": 30
                    }
                ],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "type": "MONEY",
                        "originName": "pricepaid",
                        "originalType": "double",
                        "label": "pricepaid",
                        "func": "sum",
                        "originLabel": "pricepaid",
                        "is": "Metric",
                        "customLabel": False,
                        "hideFunction": False
                    }
                ],
                "comparative": [
                    {
                        "id": "ef98f946-6bc9-4298-9aae-2bfd49624dfd",
                        "name": "pricepaid_100",
                        "func": "derived",
                        "label": "Benchmark",
                        "benchmarkLabel": None,
                        "useName": "benchmark",
                        "isComparative": True,
                        "compareType": "benchmark",
                        "usingFilters": "eventname",
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [],
                        "hideFunction": False,
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "type": "MONEY",
                        "dependencies": [
                            {
                                "name": "pricepaid",
                                "type": "MONEY",
                                "originName": "pricepaid",
                                "originalType": "double",
                                "label": "pricepaid",
                                "func": "sum",
                                "originLabel": "pricepaid",
                                "is": "Metric",
                                "customLabel": False,
                                "hideFunction": False
                            }
                        ],
                        "originalType": "CFT_DERIVED",
                        "originLabel": "PricePaid 100",
                        "baseMetric": {
                            "name": "pricepaid_100",
                            "label": "PricePaid 100",
                            "type": "MONEY",
                            "dependencies": [
                                {
                                    "name": "pricepaid",
                                    "func": "sum",
                                    "customLabel": False,
                                    "label": "pricepaid",
                                    "hideFunction": False
                                }
                            ],
                            "originalType": "CFT_DERIVED",
                            "originLabel": "PricePaid 100",
                            "func": "derived"
                        },
                        "execute": True,
                        "originalMetricType": "MONEY",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "asc"
                                },
                                "limit": 30,
                                "is": "Attribute",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "keyword",
                                "originLabel": "catname"
                            },
                            {
                                "name": "eventname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "keyword",
                                "label": "eventname",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars"
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_BENCHMARK_REVENUE_EVENTS_WITH_PRICEPAID_100_FIRST)

        # Benchmark query
        config = {
            "config": {
                "filters": [
                    {
                        "path": "saletime",                
                        "operation": "BETWEEN",
                        "value": [
                            "2008-02-23 00:00:00.000",
                            "2008-02-23 23:59:59.999"
                        ]
                    },
                    {
                        "path": "likemusicals",               
                        "operation": "IN",
                        "value": [
                            "TRUE"
                        ]
                    }
                ],       
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "asc"
                        },
                        "limit": 30
                    },
                    {
                        "name": "eventname",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "keyword",
                        "label": "eventname",
                        "originLabel": "eventname",
                        "sort": {
                            "dir": "asc",
                            "name": "eventname"
                        }
                    }
                ],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "type": "MONEY",
                        "originName": "pricepaid",
                        "originalType": "double",
                        "label": "pricepaid",
                        "func": "sum",
                        "originLabel": "pricepaid",
                        "is": "Metric",
                        "customLabel": False,
                        "hideFunction": False
                    }
                ],
                "comparative": [
                    {
                        "name": "pricepaid_100",
                        "func": "derived",
                        "label": "Benchmark",
                        "benchmarkLabel": None,
                        "useName": "benchmark",
                        "isComparative": True,
                        "compareType": "benchmark",
                        "usingFilters": "eventname",
                        "removeAfter": [],
                        "with": "-1|frame",
                        "benchmarkFunction": "avg",
                        "against": [],
                        "hideFunction": False,
                        "originalIndex": 1,
                        "is": "ComparativeMetric",
                        "type": "MONEY",
                        "dependencies": [
                            {
                                "name": "pricepaid",
                                "type": "MONEY",
                                "originName": "pricepaid",
                                "originalType": "double",
                                "label": "pricepaid",
                                "func": "sum",
                                "originLabel": "pricepaid",
                                "is": "Metric",
                                "customLabel": False,
                                "hideFunction": False
                            }
                        ],
                        "originalType": "CFT_DERIVED",
                        "originLabel": "PricePaid 100",
                        "baseMetric": {
                            "name": "pricepaid_100",
                            "label": "PricePaid 100",
                            "type": "MONEY",
                            "dependencies": [
                                {
                                    "name": "pricepaid",
                                    "func": "sum",
                                    "customLabel": False,
                                    "label": "pricepaid",
                                    "hideFunction": False
                                }
                            ],
                            "originalType": "CFT_DERIVED",
                            "originLabel": "PricePaid 100",
                            "func": "derived"
                        },
                        "execute": True,
                        "originalMetricType": "MONEY",
                        "groups": [
                            {
                                "name": "catname",
                                "label": "catname",
                                "sort": {
                                    "name": "count",
                                    "func": "",
                                    "customLabel": False,
                                    "label": "",
                                    "hideFunction": False,
                                    "metricFunc": "",
                                    "dir": "asc"
                                },
                                "limit": 30,
                                "is": "Attribute",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "catname",
                                "originalType": "keyword",
                                "originLabel": "catname"
                            },
                            {
                                "name": "eventname",
                                "keyword": True,
                                "type": "ATTRIBUTE",
                                "originName": "eventname",
                                "originalType": "keyword",
                                "label": "eventname",
                                "originLabel": "eventname",
                                "sort": {
                                    "dir": "asc",
                                    "name": "eventname"
                                }
                            }
                        ]
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Bars",
            "benchmarkQuery": True
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_BENCHMARK_REVENUE_EVENTS_WITH_PRICEPAID_100_BENCHMARK)
    # endregion


if __name__ == '__main__':
    unittest.main()
