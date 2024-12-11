import os
import copy
import unittest
import pandas as pd
import sys
import io
import json
from colorama import Fore, Style

sys.path.append("..")
from chartfactor.src.provider import Provider
from data.provider_data import ProviderData as prov_data


class TestProvider(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.realpath(__file__)) + '/csv/ticket_sales.csv'
        path_ctt = os.path.dirname(os.path.realpath(__file__)) + '/csv/chicago_taxi_trips.csv'
        path_lfb = os.path.dirname(os.path.realpath(__file__)) + '/csv/london_fire_brigade.csv'
        path_ttn = os.path.dirname(os.path.realpath(__file__)) + '/csv/titanic.csv'
        path_ifr = os.path.dirname(os.path.realpath(__file__)) + '/csv/funding_rounds.csv'
        path_hlc = os.path.dirname(os.path.realpath(__file__)) + '/csv/healthy_lifestyle_city_2021.csv'
        path_dbr = os.path.dirname(os.path.realpath(__file__)) + '/csv/Data_Breaches_EN_V2_2004_2017_20180220.csv'
        path_nflx = os.path.dirname(os.path.realpath(__file__)) + '/csv/netflix_titles.csv'
        ts = pd.read_csv(path, low_memory=False, parse_dates=['saletime', 'starttime'], infer_datetime_format=True)
        cls.df = ts
        cls.df_ctt = pd.read_csv(path_ctt, low_memory=False)
        cls.df_lfb = pd.read_csv(path_lfb, low_memory=False, parse_dates=['date_of_call', 'timestamp_of_call'], infer_datetime_format=True)
        cls.df_lfb['date_of_call'] = pd.to_datetime(cls.df_lfb['date_of_call']).dt.date
        cls.df_ttn = pd.read_csv(path_ttn, low_memory=False)
        cls.df_ifr = pd.read_csv(path_ifr, low_memory=False)
        cls.df_hlc = pd.read_csv(path_hlc, low_memory=False)
        cls.df_dbr = pd.read_csv(path_dbr, low_memory=False)
        cls.df_nflx = pd.read_csv(path_nflx, low_memory=False)
        cls.prov = Provider(ts, prov_data.JSON_CONFIG)

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_run_count_query(self):
        """
        Testing the count query
        :return:
        """
        result = json.loads(Provider(self.df, prov_data.JSON_CONFIG).run_count_query())[0]
        self.assertDictEqual(result, prov_data.TS_COUNT_QUERY_RESULT)

    # region RAW QUERIES
    def test_run_raw_query_limit(self):
        """
        Testing the raw query with a limit of 8 defined
        :return:
        """
        result = json.loads(Provider(self.df, prov_data.JSON_CONFIG).run_raw_query()).get('data')
        self.assertDictEqual(result, prov_data.TS_RAW_QUERY_LIMIT_RESULT)

    def test_run_raw_query_offset(self):
        """
        Testing the raw query with a offset of 4 defined
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["limit"] = 8
        config["offset"] = 4
        result = json.loads(Provider(self.df, config).run_raw_query()).get('data')
        self.assertDictEqual(result, prov_data.TS_RAW_QUERY_OFFSET_RESULT)

    def test_run_raw_query_full(self):
        """
        Testing that the raw query without limit should returns all the rows
        :return:
        """
        count = json.loads(Provider(self.df, prov_data.JSON_CONFIG).run_count_query())[0].get('current').get('count')
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["limit"] = 0
        result = json.loads(Provider(self.df, config).run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), count)

    def test_run_raw_query_with_fields(self):
        """
        Testing raw query with specific fields
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        fields = [
            {
                "name": "salesid",
                "label": "salesid"
            },
            {
                "name": "listid",
                "label": "listid"
            }
        ]
        config["config"]["fields"] = fields
        result = json.loads(Provider(self.df, config).run_raw_query()).get('data')
        self.assertDictEqual(result, prov_data.TS_RAW_QUERY_FIELDS_RESULT)

    def test_run_raw_query_with_exclude(self):
        """
        Testing raw query excluding one field
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        fields = [
            {
                "name": "salesid",
                "label": "salesid"
            },
            {
                "name": "listid",
                "label": "listid"
            }
        ]
        config["config"]["fields"] = fields
        config["config"]["exclude"] = ["listid"]
        result = json.loads(Provider(self.df, config).run_raw_query()).get('data')
        self.assertDictEqual(result, prov_data.TS_RAW_QUERY_EXCLUDE_RESULT)

    # region TESTING FILTERS
    def test_run_raw_query_with_ts_filters(self):
        """
        Testing raw query with the Text Search filter
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        filters = [
            {
                "path": "catdesc",
                "operation": "TS",
                "value": [
                    "rock", "non-musical"
                ]
            }
        ]
        config["config"]["filters"] = filters
        config["limit"] = 0

        prov = Provider(self.df, config)
        result = json.loads(prov.run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), 136805)

    def test_run_raw_query_with_NOT_IN_filters(self):
        """
        Testing raw query with the NOT IN filter
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        filters = [
            {
                "path": "venuecity",
                "operation": "NOT IN",
                "value": [
                    "Dayton"
                ]
            }
        ]
        config["config"]["filters"] = filters
        config["limit"] = 0

        prov = Provider(self.df, config)
        result = json.loads(prov.run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), 171659)

    def test_run_raw_query_with_in_filters(self):
        """
        Testing raw query with the IN filter
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        filters = [
            {
                "path": "venuecity",
                "operation": "IN",
                "value": [
                    "Dayton"
                ]
            }
        ]
        config["config"]["filters"] = filters
        config["limit"] = 0

        prov = Provider(self.df, config)
        result = json.loads(prov.run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), 797)

    def test_run_raw_query_with_equals_filters(self):
        """
        Testing raw query with the = filter
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        filters = [
            {
                "path": "pricepaid",
                "operation": "=",
                "value": [
                    728
                ]
            }
        ]
        config["config"]["filters"] = filters
        config["limit"] = 0

        prov = Provider(self.df, config)
        result = json.loads(prov.run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), 167)

    def test_run_raw_query_with_not_equals_filters(self):
        """
        Testing raw query with the != filter
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        filters = [
            {
                "path": "pricepaid",
                "operation": "!=",
                "value": [
                    728
                ]
            }
        ]
        config["config"]["filters"] = filters
        config["limit"] = 0

        prov = Provider(self.df, config)
        result = json.loads(prov.run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), 172289)

    def test_run_raw_query_with_gt_filters(self):
        """
        Testing raw query with the GT filter
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        filters = [
            {
                "path": "pricepaid",
                "operation": "GT",
                "value": [
                    728
                ]
            }
        ]
        config["config"]["filters"] = filters
        config["limit"] = 0

        prov = Provider(self.df, config)
        result = json.loads(prov.run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), 45313)

    def test_run_raw_query_with_lt_filters(self):
        """
        Testing raw query with the LT filter
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        filters = [
            {
                "path": "pricepaid",
                "operation": "LT",
                "value": [
                    728
                ]
            }
        ]
        config["config"]["filters"] = filters
        config["limit"] = 0

        prov = Provider(self.df, config)
        result = json.loads(prov.run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), 126976)

    def test_run_raw_query_with_ge_filters(self):
        """
        Testing raw query with the GE filter
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        filters = [
            {
                "path": "pricepaid",
                "operation": "GE",
                "value": [
                    1000
                ]
            }
        ]
        config["config"]["filters"] = filters
        config["limit"] = 0

        prov = Provider(self.df, config)
        result = json.loads(prov.run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), 26240)

    def test_run_raw_query_with_le_filters(self):
        """
        Testing raw query with the LE filter
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        filters = [
            {
                "path": "pricepaid",
                "operation": "LE",
                "value": [
                    65
                ]
            }
        ]
        config["config"]["filters"] = filters
        config["limit"] = 0

        prov = Provider(self.df, config)
        result = json.loads(prov.run_raw_query()).get('data')
        self.assertEqual(len(result.get('data')), 9381)

    # endregion
    # endregion

    # region GROUPS FUNCTIONS
    def test_process_single_group(self):
        """
        Testing One Group function
        :return:
        """
        result = json.loads(Provider(self.df, prov_data.JSON_CONFIG).__process_single_group__()).get('data')
        self.assertDictEqual(result, prov_data.TS_ONE_GROUP_QUERY_RESULT)

    def test_process_box_plot(self):
        """
        Testing Box plot function
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [],
                "metrics": [
                    {
                        "name": "extras",
                        "func": "percentiles",
                        "label": "extras",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "extras",
                        "originalType": "float64"
                    }
                ],
                "comparative": []
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Box Plot"
        }
        result = json.loads(Provider(self.df_ctt, config).__process_boxplot__()).get('data')
        self.assertDictEqual(result, prov_data.TS_BOX_PLOT_NO_GROUP_RESULT)

    def test_slicer_filter_text(self):
        """
        Testing slicer filter text
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "salesid",
                        "label": "salesid",
                        "limit": 10000,
                        "sort": {
                            "dir": "asc",
                            "name": "salesid"
                        },
                        "is": "Attribute",
                        "type": "INTEGER",
                        "originName": "salesid",
                        "originalType": "int64"
                    }
                ],
                "colgroups": [],
                "metrics": [],
                "comparative": [],
                "slicerColumnTextFilter": "172450",
                "slicerTextFilter": "172450"
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Slicer"
        }
        result = Provider(self.df, config).__apply_filters__(self.df)
        result_len = len(result)
        result_first = result['salesid'][0]

        self.assertEqual(result_len, 1)
        self.assertEqual(result_first, 172450)

    def test_process_two_groups_scenario1(self):
        """
        Testing Two Group function
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "commission",
                            "func": "sum",
                            "customLabel": False,
                            "label": "commission",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "commission",
                            "originalType": "float64"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "object"
                    },
                    {
                        "name": "eventname",
                        "label": "eventname",
                        "sort": {
                            "dir": "desc",
                            "name": "eventname"
                        },
                        "limit": 5,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "object"
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
                        "originalType": "int64"
                    }
                ],
                "comparative": []
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars"
        }
        result = json.loads(Provider(self.df, config).__process_two_groups__()).get('data')
        self.assertDictEqual(result, prov_data.TS_TWO_GROUPS_QUERY_RESULT)

    def test_process_two_groups_scenario2(self):
        """
        Testing Two Group function
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "dir": "desc",
                            "name": "catname"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "keyword"
                    },
                    {
                        "name": "eventname",
                        "label": "eventname",
                        "sort": {
                            "dir": "desc",
                            "name": "eventname"
                        },
                        "limit": 5,
                        "is": "Attribute",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "keyword"
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
                        "type": "NUMBER",
                        "originName": "pricepaid",
                        "originalType": "double"
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars",
            "element": "visualization"
        }
        result = json.loads(Provider(self.df, config).__process_two_groups__()).get('data')
        self.assertDictEqual(result, prov_data.TS_TWO_GROUPS_QUERY_RESULT2)

    def test_process_two_groups_scenario3(self):
        """
        Testing Two Group function
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catname",
                        "label": "catname",
                        "sort": {
                            "name": "commission",
                            "func": "sum",
                            "customLabel": False,
                            "label": "commission",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "asc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "commission",
                            "originalType": "double"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "catname",
                        "originalType": "keyword"
                    },
                    {
                        "name": "eventname",
                        "label": "eventname",
                        "sort": {
                            "name": "pricepaid",
                            "func": "avg",
                            "customLabel": False,
                            "label": "pricepaid",
                            "hideFunction": False,
                            "metricFunc": "avg",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "pricepaid",
                            "originalType": "double"
                        },
                        "limit": 5,
                        "is": "Attribute",
                        "keyword": True,
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "keyword"
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
                        "type": "NUMBER",
                        "originName": "pricepaid",
                        "originalType": "double"
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars"
        }

        result = json.loads(Provider(self.df, config).__process_two_groups__()).get('data')
        self.assertDictEqual(result, prov_data.TS_TWO_GROUPS_QUERY_RESULT3)

    def test_process_two_groups_scenario4_count_metrics(self):
        """
        Testing Two Group function
        :return:
        """
        config = {
            "uid": "3668cc83-4689-4ed4-8ad8-4bfe65ba60f7",
            "providerName": "Pandas DataFrames",
            "serieLabel": {
                "show": True,
                "initialAlign": None,
                "initialVerticalAlign": None
            },
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "rating",
                        "label": "rating",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "desc"
                        },
                        "limit": 100,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "rating",
                        "originalType": "string"
                    },
                    {
                        "name": "type",
                        "label": "type",
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
                        "originName": "type",
                        "originalType": "string"
                    }
                ],
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
                "comparative": []
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars",
            "element": "visualization",
            "source": {
                "name": "netflix_titles"
            },
            "color": {
                "_metric": None
            }
        }

        result = json.loads(Provider(self.df_nflx, config).__process_two_groups__()).get('data')
        self.assertDictEqual(result, prov_data.NTFLX_TWO_GROUPS_QUERY_RESULT4_COUNTS)

    def test_process_two_groups_scenario5_count_metrics_heatmap(self):
        """
        Testing Two Group function
        :return:
        """
        config = {
            "uid": "c15d446e-d519-471b-a470-6c7cc61ce8d1",
            "providerName": "Pandas DataFrames",
            "showValues": True,
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "country",
                        "label": "country",
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
                        "originName": "country",
                        "originalType": "string"
                    },
                    {
                        "name": "listed_in",
                        "label": "listed_in",
                        "sort": {
                            "name": "count",
                            "func": "",
                            "customLabel": False,
                            "label": "",
                            "hideFunction": False,
                            "metricFunc": "",
                            "dir": "asc"
                        },
                        "limit": 100,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "listed_in",
                        "originalType": "string"
                    }
                ],
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
                "comparative": []
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Heat Map",
            "element": "visualization",
            "source": {
                "name": "netflix_titles"
            },
            "color": {
                "_metric": {
                    "name": "count",
                    "func": "",
                    "customLabel": False,
                    "label": "Transactions",
                    "hideFunction": False,
                    "is": "Metric",
                    "type": "INTEGER"
                }
            }
        }

        result = json.loads(Provider(self.df_nflx, config).__process_two_groups__()).get('data')
        self.assertDictEqual(result, prov_data.NTFLX_TWO_GROUPS_QUERY_RESULT5_COUNTS_HEATMAP)
    # endregion

    # region VISUALIZE FUNCTION
    def test_visualize_with_raw_query(self):
        """
        Testing the visualize function with "rawQuery": True
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        fields = [
            {
                "name": "salesid",
                "label": "salesid"
            },
            {
                "name": "listid",
                "label": "listid"
            }
        ]
        config["rawQuery"] = True
        config["visualization"] = 'Raw Data Table'
        config["config"]["fields"] = fields
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, {'data': [], 'visualization': 'Raw Data Table'})

    def test_visualize_with_box_plot_query(self):
        """
        Testing the visualize function with Box Plot configured
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["visualization"] = 'Box Plot'
        config["config"]["metrics"] = [{
            "name": "commission",
            "func": "sum"
        }]
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_BOX_PLOT_RESULT)

        # Testing with percentiles metric
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["visualization"] = 'Box Plot'
        config["config"]["metrics"] = [{
            "name": "commission",
            "func": "percentiles"
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_BOX_PLOT_RESULT)

    def test_visualize_with_time_range_query(self):
        """
        Testing the visualize function with Time Range configured
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["visualization"] = 'Time Range Picker'
        config["timeRangeVisual"] = True
        config["config"]["groups"] = [{
            "name": "saletime",
            "granularity": "YEAR",
            "sort": {
                "name": "commission",
                "func": "sum",
                "dir": "desc"
            },
            "limit": 10
        }]
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TIME_RANGE_YEAR)

        config["config"]["groups"] = [{
            "name": "saletime",
            "granularity": "MONTH",
            "sort": {
                "name": "commission",
                "func": "sum",
                "dir": "desc"
            },
            "limit": 10
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TIME_RANGE_MONTH)

        config["config"]["groups"] = [{
            "name": "saletime",
            "granularity": "WEEK",
            "sort": {
                "name": "commission",
                "func": "sum",
                "dir": "desc"
            },
            "limit": 10
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TIME_RANGE_WEEK)

        config["config"]["groups"] = [{
            "name": "saletime",
            "granularity": "DAY",
            "sort": {
                "name": "commission",
                "func": "sum",
                "dir": "desc"
            },
            "limit": 10
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TIME_RANGE_DAY)

        config["config"]["groups"] = [{
            "name": "saletime",
            "granularity": "HOUR",
            "sort": {
                "name": "commission",
                "func": "sum",
                "dir": "desc"
            },
            "limit": 10
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TIME_RANGE_HOUR)

        config["config"]["groups"] = [{
            "name": "saletime",
            "granularity": "MINUTE",
            "sort": {
                "name": "commission",
                "func": "sum",
                "dir": "desc"
            },
            "limit": 10
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TIME_RANGE_MINUTE)

        config["config"]["groups"] = [{
            "name": "saletime",
            "granularity": "SECOND",
            "sort": {
                "name": "commission",
                "func": "sum",
                "dir": "desc"
            },
            "limit": 10
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TIME_RANGE_SECOND)

    def test_visualize_with_time_range_query_with_time_field(self):
        """
        Testing the visualize function with time field and without visualization configured
        :return:
        """
        config = {
            "timeRangeVisual": True,
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [],
                "metrics": [],
                "comparative": [],
                "timefield": {
                    "name": "saletime",
                    "label": "saletime",
                    "func": "YEAR",
                    "is": "Attribute",
                    "type": "TIME",
                    "originName": "saletime",
                    "originalType": "object",
                    "timestampGranularity": "YEAR"
                }
            },
            "aggregate": False,
            "limit": None,
            "offset": 0
        }
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        compare = copy.deepcopy(prov_data.TS_TIME_RANGE_YEAR)
        compare['visualization'] = ''
        self.assertDictEqual(result, compare)

        config["config"]["timefield"]["func"] = "MONTH"
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        compare = copy.deepcopy(prov_data.TS_TIME_RANGE_MONTH)
        compare['visualization'] = ''
        self.assertDictEqual(result, compare)

        config["config"]["timefield"]["func"] = "WEEK"
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        compare = copy.deepcopy(prov_data.TS_TIME_RANGE_WEEK)
        compare['visualization'] = ''
        self.assertDictEqual(result, compare)

        config["config"]["timefield"]["func"] = "DAY"
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        compare = copy.deepcopy(prov_data.TS_TIME_RANGE_DAY)
        compare['visualization'] = ''
        self.assertDictEqual(result, compare)

        config["config"]["timefield"]["func"] = "HOUR"
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        compare = copy.deepcopy(prov_data.TS_TIME_RANGE_HOUR)
        compare['visualization'] = ''
        self.assertDictEqual(result, compare)

        config["config"]["timefield"]["func"] = "MINUTE"
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        compare = copy.deepcopy(prov_data.TS_TIME_RANGE_MINUTE)
        compare['visualization'] = ''
        self.assertDictEqual(result, compare)

        config["config"]["timefield"]["func"] = "SECOND"
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        compare = copy.deepcopy(prov_data.TS_TIME_RANGE_SECOND)
        compare['visualization'] = ''
        self.assertDictEqual(result, compare)

    def test_visualize_with_histogram_query(self):
        """
        Testing the visualize function with Histogram configured
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["visualization"] = 'Bars'
        config["limit"] = 100
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram"
        }]
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_HISTOGRAM_DEFAULT_RESULT)

        # Interval without offset
        config["limit"] = 10
        config["visualization"] = 'Bars'
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": 10,
            "offset": 0
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_HISTOGRAM_SCENARIO_1_RESULT)

        # Interval with offset
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": 10,
            "offset": 5
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_HISTOGRAM_SCENARIO_2_RESULT)

        # Using Fixed Bars without interval
        config["limit"] = 100
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "fixedBars": 20,
            "offset": 5
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_HISTOGRAM_SCENARIO_3_RESULT)

        # Using Fixed Bars with interval
        config["limit"] = 30
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": 10,
            "fixedBars": 20,
            "offset": 5
        }]

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_HISTOGRAM_SCENARIO_4_RESULT)

    def test_visualize_with_pivot_default_config(self):
        """
        Testing the visualize function with Pivot Table default config
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "groups": [],
                "metrics": [
                    {
                        "name": "count",
                        "func": "",
                        "label": "Transactions",
                    }
                ]
            },
            "aggregate": True,
            "limit": 1000,
            "offset": 0,
            "rows": [
                {
                    "name": "catdesc",
                    "limit": None,
                    "is": "Row",
                    "label": "catdesc",
                    "type": "ATTRIBUTE",
                    "originName": "catdesc",
                    "originalType": "object"
                }
            ],
            "columns": [],
            "visualization": "Pivot Table"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_PIVOT_DEFAULT_CONFIG)

    def test_visualize_with_pivot_columns_and_rows_no_metrics_query(self):
        """
        Testing the visualize function with Pivot Table rows and col without metrics configured
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["visualization"] = 'Pivot Table'
        config["aggregate"] = True
        config["columns"] = [{"name": 'catgroup'}, {"name": 'catname'}]
        config["rows"] = [{"name": 'venuestate'}, {"name": 'venuecity'}, {"name": 'venuename'}]
        config["config"]["metrics"] = []
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_PIVOT_COLUMNS_ROWS_RESULT)

    def test_visualize_with_pivot_rows_and_metrics_no_columns_query(self):
        """
        Testing the visualize function with Pivot Table rows, metrics but no col configured
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["visualization"] = 'Pivot Table'
        config["aggregate"] = True
        config["columns"] = []
        config["rows"] = [{"name": 'venuestate'}, {"name": 'venuecity'}, {"name": 'venuename'}]
        config["config"]["metrics"] = [
            {
                "name": "commission",
                "func": "avg"
            },
            {
                "name": "qtysold",
                "func": "sum"
            }
        ]
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_PIVOT_ROWS_METRICS_NO_COLUMNS_RESULT)

    def test_visualize_with_pivot_columns_and_rows_and_metrics_query(self):
        """
        Testing the visualize function with Pivot Table rows, columns and metrics configured
        :return:
        """
        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["visualization"] = 'Pivot Table'
        config["aggregate"] = True
        config["columns"] = [{"name": 'catgroup'}, {"name": 'catname'}]
        config["rows"] = [{"name": 'venuestate'}, {"name": 'venuecity'}, {"name": 'venuename'}]
        config["config"]["metrics"] = [
            {
                "name": "commission",
                "func": "avg"
            },
            {
                "name": "qtysold",
                "func": "sum"
            }
        ]
        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_PIVOT_COLUMNS_ROWS_METRICS_RESULT)

    def test_visualize_with_geo_hash_query(self):
        """
        Testing the visualize function with Geo Hash configured
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "groups": [],
                "metrics": [
                    {
                        "name": "extras",
                        "func": "avg"
                    },
                    {
                        "name": "fare",
                        "func": "sum"
                    }
                ],
                "fields": [

                ],
                "exclude": [],
                "location": "dropoff_location",
                "precision": 1
            },
            "aggregate": False,
            "columns": [],
            "rows": [],
            "visualization": "Geo Map"
        }

        self.df_ctt['dropoff_location'] = self.df_ctt[['dropoff_latitude', 'dropoff_longitude']].apply(lambda x: [x.dropoff_latitude, x.dropoff_longitude], axis=1)

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_1_RESULT)

        config['config']['precision'] = 2

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_2_RESULT)

        config['config']['precision'] = 3

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_3_RESULT)

        config['config']['precision'] = 4

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_4_RESULT)

        config['config']['precision'] = 5

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_5_RESULT)

        config['config']['precision'] = 6

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_6_RESULT)

        config['config']['precision'] = 7

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_7_RESULT)

        config['config']['precision'] = 8

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_8_RESULT)

        config['config']['precision'] = 9

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_9_RESULT)

        config['config']['precision'] = 10

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_10_RESULT)

        config['config']['precision'] = 11

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_GEO_HASH_PRECISION_11_RESULT)

    def test_visualize_with_one_group_two_func_one_metric_query(self):
        """
        Testing the visualize function using one metric with two functions (avg and sum)
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "groups": [
                    {
                        "name": "saletime",
                        "label": "saletime",
                        "sort": {
                            "name": "commission",
                            "func": "sum",
                            "dir": "desc"
                        },
                        "limit": 10,
                        "func": "YEAR"
                    }
                ],
                "metrics": [
                    {
                        "name": "commission",
                        "func": "avg",
                        "label": "commission"
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_ONE_GROUP_ONE_METRIC_TWO_FUNC_QUERY_RESULT)

    def test_visualize_with_one_group_query_point_in_name(self):
        """
        Testing the visualize function using one metric with two functions (avg and sum)
        :return:
        """
        config = {
            "uid": "1aa33b79-f3e9-4ea9-b3a7-96275c683f4e",
            "providerName": "Pandas DataFrames",
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [
                    {
                        "path": "venuecity",
                        "label": "venuecity",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Arlington"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "venuecity",
                            "label": "venuecity",
                            "type": "ATTRIBUTE",
                            "originName": "venuecity",
                            "originalType": "object",
                            "originLabel": "venuecity"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "catdesc",
                        "label": "catdesc",
                        "sort": {
                            "name": "catid.1",
                            "func": "sum",
                            "customLabel": False,
                            "label": "catid.1",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "INTEGER",
                            "originName": "catid.1",
                            "originalType": "int64",
                            "originLabel": "catid.1"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "catdesc",
                        "originalType": "object",
                        "originLabel": "catdesc"
                    }
                ],
                "metrics": [
                    {
                        "name": "catid.1",
                        "func": "sum",
                        "customLabel": False,
                        "label": "catid.1",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "catid.1",
                        "originalType": "int64",
                        "originLabel": "catid.1"
                    }
                ],
                "comparative": []
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars",
            "element": "visualization",
            "source": {
                "name": "ticket_sales"
            },
            "color": {
                "_metric": None
            }
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_ONE_GROUP_ONE_QUERY_POINT_IN_NAME_RESULT)

    def test_visualize_with_disk_visualization(self):
        """
        Testing the visualize function for the Disk visualization
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "groups": [
                    {
                        "name": "hour_of_call",
                        "label": "hour_of_call",
                        "sort": {
                            "dir": "asc",
                            "name": "hour_of_call"
                        },
                        "limit": 24
                    }
                ],
                "metrics": [
                    {
                        "name": "easting_m",
                        "func": "sum",
                        "label": "easting_m"
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Disk"
        }

        result = json.loads(Provider(self.df_lfb, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_DISK_VISUALIZATION)

    def test_visualize_with_tree_visualization(self):
        """
        Testing the visualize function for the Disk visualization
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "groups": [],
                "metrics": [
                    {
                        "name": "pricepaid",
                        "func": "sum",
                        "label": "pricepaid"
                    }
                ]
            },
            "aggregate": True,
            "limit": 1000,
            "offset": 0,
            "rows": [
                {
                    "name": "catdesc",
                    "limit": None,
                    "label": "catdesc"
                }
            ],
            "columns": [],
            "visualization": "Tree"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_TREE_VISUALIZATION)

    def test_visualize_with_sankey_visualization(self):
        """
        Testing the visualize function for the Sankey visualization
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "groups": [],
                "metrics": [
                    {
                        "name": "commission",
                        "func": "sum",
                        "label": "commission"
                    }
                ]
            },
            "aggregate": True,
            "limit": 50,
            "offset": 0,
            "rows": [
                {
                    "name": "firstname",
                    "limit": None,
                    "label": "firstname"
                },
                {
                    "name": "lastname",
                    "limit": None,
                    "label": "lastname"
                }
            ],
            "columns": [],
            "visualization": "Sankey"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_SANKEY_VISUALIZATION)

    def test_visualize_with_sunburst_visualization(self):
        """
        Testing the visualize function for the Sunburst visualization
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "groups": [],
                "metrics": [
                    {
                        "name": "count",
                        "func": "",
                        "label": "Transactions"
                    }
                ]
            },
            "aggregate": True,
            "limit": 1000,
            "offset": 0,
            "rows": [
                {
                    "name": "catdesc",
                    "limit": None,
                    "is": "Row",
                    "label": "catdesc",
                    "type": "ATTRIBUTE",
                    "originName": "catdesc",
                    "originalType": "object"
                }
            ],
            "columns": [],
            "visualization": "Sunburst"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_SUNBURST_VISUALIZATION)

    def test_visualize_with_slicer_visual_and_between_filter(self):
        """
        Testing the visualize function for the Slicer visualization and between filter
        :return:
        """
        config = {
            "config": {
                "filters": [
                    {
                        "path": "trip_end_timestamp",
                        "label": "trip_end_timestamp",
                        "operation": "BETWEEN",
                        "value": [
                            "2013-01-01 00:00:00.000",
                            "2013-01-31 23:59:59.999"
                        ]
                    }
                ],
                "groups": [
                    {
                        "name": "company",
                        "label": "company",
                        "sort": {
                            "dir": "asc",
                            "name": "company"
                        },
                        "limit": 10000
                    }
                ],
                "metrics": [
                    {
                        "name": "extras",
                        "func": "unique",
                        "label": "extras"
                    }
                ]
            },
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Slicer",
            "element": "visualization"
        }

        result = json.loads(Provider(self.df_ctt, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_SLICER_BETWEEN_FILTER_VISUALIZATION)

    def test_visualize_with_multi_metric_gauge(self):
        """
        Testing the visualize function for the Multimetric Gauge
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "groups": [],
                "metrics": [
                    {
                        "name": "commission",
                        "func": "avg",
                        "customLabel": False,
                        "label": "commission",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "commission",
                        "originalType": "float64",
                        "originLabel": "commission"
                    },
                    {
                        "name": "pricepaid",
                        "func": "avg",
                        "customLabel": False,
                        "label": "pricepaid",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "pricepaid",
                        "originalType": "int64",
                        "originLabel": "pricepaid"
                    },
                    {
                        "name": "count",
                        "func": "",
                        "customLabel": False,
                        "label": "Transactions",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER"
                    }
                ]
            },
            "limit": None,
            "offset": 0,
            "visualization": "Gauge"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_MULTIMETRIC_GAUGE_VISUALIZATION)

    def test_visualize_with_range_filter(self):
        """
        Testing the visualize function for the Range Filter
        :return:
        """
        config = {
            "config": {
                "filters": [],
                "groups": [],
                "metrics": [
                    {
                        "name": "commission",
                        "func": "max",
                        "customLabel": False,
                        "label": "commission",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "commission",
                        "originalType": "double"
                    },
                    {
                        "name": "commission",
                        "func": "min",
                        "customLabel": False,
                        "label": "commission",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "commission",
                        "originalType": "double"
                    },
                    {
                        "name": "qtysold",
                        "func": "max",
                        "customLabel": False,
                        "label": "qtysold",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "qtysold",
                        "originalType": "integer"
                    },
                    {
                        "name": "qtysold",
                        "func": "min",
                        "customLabel": False,
                        "label": "qtysold",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "qtysold",
                        "originalType": "integer"
                    },
                    {
                        "name": "venueseats",
                        "func": "max",
                        "customLabel": False,
                        "label": "venueseats",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "venueseats",
                        "originalType": "integer"
                    },
                    {
                        "name": "venueseats",
                        "func": "min",
                        "customLabel": False,
                        "label": "venueseats",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "venueseats",
                        "originalType": "integer"
                    },
                    {
                        "name": "count",
                        "func": "",
                        "label": "Transactions",
                        "is": "Metric",
                        "type": "INTEGER"
                    }
                ]
            },
            "limit": None,
            "offset": 0,
            "visualization": "Range Filter"
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_RANGE_FILTER_VISUALIZATION)

    def test_visualize_multi_metric_area_line(self):
        config = {
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "Parch",
                        "label": "Parch",
                        "sort": {
                            "dir": "asc",
                            "name": "Parch"
                        },
                        "limit": 1000,
                        "is": "Attribute",
                        "type": "INTEGER",
                        "originName": "Parch",
                        "originalType": "integer"
                    }
                ],
                "metrics": [
                    {
                        "name": "Age",
                        "func": "sum",
                        "customLabel": False,
                        "label": "Age",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "Age",
                        "originalType": "floating"
                    },
                    {
                        "name": "Fare",
                        "func": "sum",
                        "customLabel": False,
                        "label": "Fare",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "Fare",
                        "originalType": "floating"
                    },
                    {
                        "name": "Parch",
                        "func": "sum",
                        "customLabel": False,
                        "label": "Parch",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "INTEGER",
                        "originName": "Parch",
                        "originalType": "integer"
                    }
                ],
                "comparative": []
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Multimetric Area Line"
        }

        result = json.loads(Provider(self.df_ttn, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TTN_MULTI_METRIC_AREA_LINE)

    def test_visualize_with_none_in_equals_filter(self):
        config = {
            "config": {
                "filters": [
                    {
                        "path": "Age",
                        "label": "Age",
                        "enabled": True,
                        "operation": "EQUAL",
                        "value": [
                            None
                        ]
                    }
                ],
                "groups": [],
                "metrics": [
                    {
                        "name": "Age",
                        "func": "histogram",
                        "customLabel": False,
                        "label": "Age",
                        "hideFunction": False,
                        "fixedBars": 6,
                        "offset": 0,
                        "showEmptyIntervals": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "Age",
                        "originalType": "floating"
                    }
                ],
                "comparative": []
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": 100,
            "offset": 0,
            "visualization": "Histogram"
        }

        result = json.loads(Provider(self.df_ttn, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TTN_NONE_IN_EQUALS_FILTER)

    def test_visualize_with_none_in_not_equals_filter(self):
        config = {
            "config": {
                "filters": [
                    {
                        "path": "Age",
                        "label": "Age",
                        "enabled": True,
                        "operation": "NOT EQUAL",
                        "value": [
                            None
                        ]
                    }
                ],
                "groups": [],
                "metrics": [
                    {
                        "name": "Age",
                        "func": "histogram",
                        "customLabel": False,
                        "label": "Age",
                        "hideFunction": False,
                        "fixedBars": 6,
                        "offset": 0,
                        "showEmptyIntervals": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "Age",
                        "originalType": "floating"
                    }
                ],
                "comparative": []
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": 100,
            "offset": 0,
            "visualization": "Histogram"
        }

        result = json.loads(Provider(self.df_ttn, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TTN_NONE_IN_NOT_EQUALS_FILTER)

    def test_visualize_with_none_in_in_filter(self):
        config = {
            "config": {
                "filters": [
                    {
                        "path": "Cabin",
                        "label": "Cabin",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            None
                        ]
                    }
                ],
                "groups": [
                    {
                        "name": "Cabin",
                        "label": "Cabin",
                        "sort": {
                            "name": "Age",
                            "func": "sum",
                            "customLabel": False,
                            "label": "Age",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "Age",
                            "originalType": "floating"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "Cabin",
                        "originalType": "string"
                    }
                ],
                "metrics": [
                    {
                        "name": "Age",
                        "func": "sum",
                        "customLabel": False,
                        "label": "Age",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "Age",
                        "originalType": "floating"
                    }
                ],
                "comparative": []
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars"
        }

        result = json.loads(Provider(self.df_ttn, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TTN_NONE_IN_IN_FILTER)

    def test_visualize_with_none_in_not_in_filter(self):
        config = {
            "config": {
                "filters": [
                    {
                        "path": "Cabin",
                        "label": "Cabin",
                        "enabled": True,
                        "operation": "NOT IN",
                        "value": [
                            None
                        ]
                    }
                ],
                "groups": [
                    {
                        "name": "Cabin",
                        "label": "Cabin",
                        "sort": {
                            "name": "Age",
                            "func": "sum",
                            "customLabel": False,
                            "label": "Age",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "Age",
                            "originalType": "floating"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "Cabin",
                        "originalType": "string"
                    }
                ],
                "metrics": [
                    {
                        "name": "Age",
                        "func": "sum",
                        "customLabel": False,
                        "label": "Age",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "Age",
                        "originalType": "floating"
                    }
                ],
                "comparative": []
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars"
        }

        result = json.loads(Provider(self.df_ttn, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TTN_NONE_IN_NOT_IN_FILTER)

    def test_run_raw_query_with_date_filter(self):
        config = {
            "columnFilters": [
                {
                    "field": "incident_number",
                    "component": "slicer"
                },
                {
                    "field": "date_of_call",
                    "component": "datePicker",
                    "props": {
                        "func": "DAY"
                    }
                },
                {
                    "field": "timestamp_of_call",
                    "component": "datePicker",
                    "props": {
                        "func": "DAY"
                    }
                }
            ],
            "sizeColumnsToFit": True,
            "columnsWidth": [
                {
                    "incident_number": 100
                },
                {
                    "date_of_call": 176
                },
                {
                    "cal_year": 100
                },
                {
                    "time_of_call": 100
                },
                {
                    "hour_of_call": 100
                },
                {
                    "timestamp_of_call": 100
                },
                {
                    "incident_group": 100
                },
                {
                    "stop_code_description": 100
                },
                {
                    "special_service_type": 100
                },
                {
                    "property_category": 100
                },
                {
                    "property_type": 100
                },
                {
                    "address_qualifier": 100
                },
                {
                    "postcode_full": 100
                },
                {
                    "postcode_district": 100
                },
                {
                    "borough_code": 100
                },
                {
                    "borough_name": 100
                },
                {
                    "proper_case": 100
                },
                {
                    "ward_code": 100
                },
                {
                    "ward_name": 100
                },
                {
                    "ward_name_new": 100
                },
                {
                    "easting_m": 100
                },
                {
                    "northing_m": 100
                },
                {
                    "easting_rounded": 100
                },
                {
                    "northing_rounded": 100
                },
                {
                    "frs": 100
                },
                {
                    "incident_station_ground": 100
                },
                {
                    "first_pump_arriving_attendance_time": 100
                },
                {
                    "first_pump_arriving_deployed_from_station": 100
                },
                {
                    "second_pump_arriving_attendance_time": 100
                },
                {
                    "second_pump_arriving_deployed_from_station": 100
                },
                {
                    "num_stations_with_pumps_attending": 100
                },
                {
                    "num_pumps_attending": 100
                },
                {
                    "total_cf_count": 100
                }
            ],
            "sort": [
                {
                    "incident_number": "asc"
                }
            ],
            "timezone": {
                "display": "America/Guayaquil"
            },
            "config": {
                "filters": [
                    {
                        "path": "date_of_call",
                        "label": "date_of_call",
                        "enabled": True,
                        "operation": "BETWEEN",
                        "value": [
                            "2017-02-22 00:00:00.000",
                            "2017-02-22 23:59:59.999"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "origin": {
                            "name": "date_of_call",
                            "label": "date_of_call",
                            "type": "TIME",
                            "originName": "date_of_call",
                            "originalType": "date",
                            "timestampGranularity": "YEAR",
                            "originLabel": "date_of_call"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [],
                "metrics": [],
                "comparative": [],
                "fields": [
                    {
                        "name": "incident_number",
                        "label": "incident_number",
                        "groupName": False,
                        "limit": 100,
                        "is": "Field",
                        "type": "ATTRIBUTE",
                        "originName": "incident_number",
                        "originalType": "string",
                        "originLabel": "incident_number"
                    },
                    {
                        "name": "date_of_call",
                        "label": "date_of_call",
                        "groupName": False,
                        "limit": 100,
                        "is": "Field",
                        "tz": "America/Guayaquil",
                        "type": "TIME",
                        "originName": "date_of_call",
                        "originalType": "date",
                        "timestampGranularity": "YEAR",
                        "originLabel": "date_of_call"
                    },
                    {
                        "name": "timestamp_of_call",
                        "label": "timestamp_of_call EST",
                        "groupName": False,
                        "limit": 100,
                        "is": "Field",
                        "tz": "America/New_York",
                        "type": "TIME",
                        "originName": "timestamp_of_call",
                        "originalType": "datetime",
                        "timestampGranularity": "YEAR",
                        "originLabel": "timestamp_of_call"
                    }
                ],
                "exclude": [],
                "limit": 100
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": 100,
            "offset": 0,
            "rawQuery": True,
            "showRowNumber": False,
            "autoSizeColumns": False,
            "visualization": "Raw Data Table"
        }

        result = json.loads(Provider(self.df_lfb, config).run_raw_query()).get('data')
        self.assertDictEqual(result, prov_data.LFB_RUN_RAW_QUERY_WITH_DATE_FILTER)

    def test_slicer_with_text_filter_only(self):
        config = {
            "uid": "0575a12e-3394-4e7d-bd16-0497d45da57f",
            "providerName": "Pandas DataFrames",
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "name",
                        "label": "name",
                        "limit": 10000,
                        "sort": {
                            "dir": "asc",
                            "name": "name"
                        },
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "name",
                        "originalType": "string"
                    }
                ],
                "metrics": [
                    {
                        "name": "investor_count",
                        "func": "sum",
                        "customLabel": False,
                        "label": "investor_count",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "investor_count",
                        "originalType": "floating"
                    }
                ],
                "comparative": [],
                "slicerTextFilter": "Stev"
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "originalGroup": {
                "name": "name",
                "label": "",
                "limit": 10000
            },
            "visualization": "Slicer",
            "element": "visefbe8f8e-5eac-4d2d-9016-f1850706ec66",
            "source": {
                "name": "funding_rounds"
            },
            "color": {
                "_metric": None
            }
        }

        result = json.loads(Provider(self.df_ifr, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.IFR_SLICER_WITH_TEXT_FILTER)

    def test_slicer_with_text_filter_and_in_filters(self):
        config = {
            "uid": "0575a12e-3394-4e7d-bd16-0497d45da57f",
            "providerName": "Pandas DataFrames",
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [
                    {
                        "path": "name",
                        "label": "name",
                        "enabled": True,
                        "operation": "IN",
                        "value": [
                            "Angel Round - !Creatice"
                        ],
                        "relative": False,
                        "presetValue": False,
                        "isTextFilter": False,
                        "id": "26ff2525-b252-45d9-b878-7d25242cadf5",
                        "sender": {
                            "type": "Slicer",
                            "id": "visefbe8f8e-5eac-4d2d-9016-f1850706ec66"
                        },
                        "origin": {
                            "name": "name",
                            "label": "name",
                            "limit": 10000,
                            "sort": {
                                "dir": "asc",
                                "name": "name"
                            },
                            "is": "Attribute",
                            "type": "ATTRIBUTE",
                            "originName": "name",
                            "originalType": "string"
                        }
                    }
                ],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "name",
                        "label": "name",
                        "limit": 10000,
                        "sort": {
                            "dir": "asc",
                            "name": "name"
                        },
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "name",
                        "originalType": "string"
                    }
                ],
                "metrics": [
                    {
                        "name": "investor_count",
                        "func": "sum",
                        "customLabel": False,
                        "label": "investor_count",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "investor_count",
                        "originalType": "floating"
                    }
                ],
                "comparative": [],
                "slicerTextFilter": "Stev"
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "originalGroup": {
                "name": "name",
                "label": "",
                "limit": 10000
            },
            "visualization": "Slicer",
            "element": "visefbe8f8e-5eac-4d2d-9016-f1850706ec66",
            "source": {
                "name": "funding_rounds"
            },
            "color": {
                "_metric": None
            }
        }

        result = json.loads(Provider(self.df_ifr, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.IFR_SLICER_WITH_TEXT_FILTER)

    def test_rdt_kpi_column_stats(self):
        config = {
            "uid": "0c65698e-8ba1-4bb6-a402-44b728350084",
            "providerName": "Pandas DataFrames",
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [],
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
                "comparative": []
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "element": "6b1bd997-3008-4943-a802-0ab8b6222875",
            "source": {
                "name": "healthy_lifestyle_cities"
            },
            "color": {
                "_metric": None
            }
        }

        result = json.loads(Provider(self.df_hlc, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.HLC_RDT_KPI_COLUMN_STAT)

    def test_rdt_kpi_unique_column_stats(self):
        config = {
            "uid": "3e03a8b1-89d3-493e-8b0c-fafb77b139b0",
            "providerName": "Pandas DataFrames",
            "_parentId": "visualization",
            "_isChild": True,
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [],
                "metrics": [
                    {
                        "name": "City",
                        "func": "unique",
                        "customLabel": False,
                        "label": "City",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "ATTRIBUTE",
                        "originName": "City",
                        "originalType": "string"
                    }
                ],
                "comparative": []
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "element": "6d989af2-fab8-410b-a522-46b5ad822b1b",
            "source": {
                "name": "healthy_lifestyle_cities"
            },
            "color": {
                "_metric": None
            }
        }

        result = json.loads(Provider(self.df_hlc, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.HLC_RDT_KPI_COLUMN_STAT_2)

    def test_data_breaches_single_group_with_1st_source(self):
        config = {
            "uid": "ce2f21c3-5199-4e61-859a-155bdfd914d8",
            "providerName": "Pandas DataFrames",
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "1st source",
                        "label": "1st source",
                        "sort": {
                            "name": "Records Lost",
                            "func": "sum",
                            "customLabel": False,
                            "label": "Records Lost",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "Records Lost",
                            "originalType": "floating"
                        },
                        "limit": 100,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "1st source",
                        "originalType": "string"
                    }
                ],
                "metrics": [
                    {
                        "name": "Records Lost",
                        "func": "sum",
                        "customLabel": False,
                        "label": "Records Lost",
                        "hideFunction": False,
                        "is": "Metric",
                        "type": "NUMBER",
                        "originName": "Records Lost",
                        "originalType": "floating"
                    }
                ],
                "comparative": []
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Bars",
            "element": "visualization",
            "source": {
                "name": "dataBreaches"
            },
            "color": {
                "_metric": None
            }
        }

        result = json.loads(Provider(self.df_dbr, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.DBR_BREACHES_SINGLE_GROUP_WITH_1ST_SOURCE)

    def test_data_ticket_sales_row_venuename_col_eventname(self):
        config = {
            "uid": "471562dc-e8bc-462f-8846-791f69e712de",
            "providerName": "Aktiun Pandas",
            "showValues": True,
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "venuename",
                        "label": "venuename",
                        "sort": {
                            "name": "commission",
                            "func": "sum",
                            "customLabel": False,
                            "label": "commission",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "asc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "commission",
                            "originalType": "float64"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "venuename",
                        "originalType": "string"
                    }
                ],
                "colgroups": [
                    {
                        "name": "eventname",
                        "label": "eventname",
                        "sort": {
                            "name": "commission",
                            "func": "sum",
                            "customLabel": False,
                            "label": "commission",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "commission",
                            "originalType": "float64"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "eventname",
                        "originalType": "string"
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
                        "type": "NUMBER",
                        "originName": "commission",
                        "originalType": "float64"
                    }
                ],
                "comparative": []
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Heat Map",
            "element": "visualization23",
            "source": {
                "name": "ticket_sales"
            },
            "color": {
                "_metric": {
                    "name": "catid.1",
                    "func": "sum",
                    "customLabel": False,
                    "label": "catid.1",
                    "hideFunction": False,
                    "is": "Metric",
                    "type": "INTEGER",
                    "originName": "catid.1",
                    "originalType": "int64"
                }
            }
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_row_venuename_col_eventname)

    def test_data_ticket_sales_column_starttime_row_venuename(self):
        config = {
            "uid": "84981ec9-f3b8-4789-ac12-f9748fd3bfcc",
            "providerName": "Aktiun Pandas",
            "showValues": True,
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "venuename",
                        "label": "venuename",
                        "sort": {
                            "name": "commission",
                            "func": "sum",
                            "customLabel": False,
                            "label": "commission",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "asc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "commission",
                            "originalType": "float64"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "venuename",
                        "originalType": "string"
                    }
                ],
                "colgroups": [
                    {
                        "name": "starttime",
                        "label": "starttime",
                        "func": "MONTH",
                        "sort": {
                            "dir": "asc",
                            "name": "starttime"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "TIME",
                        "originName": "starttime",
                        "originalType": "datetime",
                        "timestampGranularity": "YEAR"
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
                        "type": "NUMBER",
                        "originName": "commission",
                        "originalType": "float64"
                    }
                ],
                "comparative": []
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Heat Map",
            "element": "visualization26",
            "source": {
                "name": "ticket_sales"
            },
            "color": {
                "_metric": {
                    "name": "commission",
                    "func": "sum",
                    "customLabel": False,
                    "label": "commission",
                    "hideFunction": False,
                    "is": "Metric",
                    "type": "NUMBER",
                    "originName": "commission",
                    "originalType": "float64"
                }
            }
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_column_starttime_row_venuename)

    def test_data_ticket_sales_column_venuename_row_starttime(self):
        config = {
            "uid": "96d57891-fa53-4458-abcd-c4abe59d90fe",
            "providerName": "Aktiun Pandas",
            "showValues": True,
            "aqlId": "__DEFAULT__",
            "timezone": {},
            "config": {
                "filters": [],
                "staticFilters": [],
                "clientFilters": [],
                "textFilter": "",
                "staticTextFilter": "",
                "groups": [
                    {
                        "name": "starttime",
                        "label": "starttime",
                        "func": "MONTH",
                        "sort": {
                            "name": "commission",
                            "func": "sum",
                            "customLabel": False,
                            "label": "commission",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "desc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "commission",
                            "originalType": "float64"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "TIME",
                        "originName": "starttime",
                        "originalType": "datetime",
                        "timestampGranularity": "YEAR"
                    }
                ],
                "colgroups": [
                    {
                        "name": "venuename",
                        "label": "venuename",
                        "sort": {
                            "name": "commission",
                            "func": "sum",
                            "customLabel": False,
                            "label": "commission",
                            "hideFunction": False,
                            "metricFunc": "sum",
                            "dir": "asc",
                            "is": "Metric",
                            "type": "NUMBER",
                            "originName": "commission",
                            "originalType": "float64"
                        },
                        "limit": 10,
                        "is": "Attribute",
                        "type": "ATTRIBUTE",
                        "originName": "venuename",
                        "originalType": "string"
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
                        "type": "NUMBER",
                        "originName": "commission",
                        "originalType": "float64"
                    }
                ],
                "comparative": []
            },
            "volumeMetric": {
                "label": "Transactions",
                "func": "",
                "type": "INTEGER",
                "name": "count"
            },
            "hasDerivedFields": False,
            "aggregate": False,
            "limit": None,
            "offset": 0,
            "visualization": "Heat Map",
            "element": "visualization32",
            "source": {
                "name": "ticket_sales"
            },
            "color": {
                "_metric": {
                    "name": "commission",
                    "func": "sum",
                    "customLabel": False,
                    "label": "commission",
                    "hideFunction": False,
                    "is": "Metric",
                    "type": "NUMBER",
                    "originName": "commission",
                    "originalType": "float64"
                }
            }
        }

        result = json.loads(Provider(self.df, config).visualize()).get('data')
        self.assertDictEqual(result, prov_data.TS_column_venuename_row_starttime)
    # endregion

    # region NEGATIVE TESTS
    def test_should_return_granularity_missing_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["groups"] = [{
            "name": "saletime",
            "label": "saletime",
            "sort": {
                "name": "eventname",
                "func": "unique",
                "dir": "asc"
            },
            "limit": 5
        }]
        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The group 'saletime' represents a date or datetime field. Please provide the 'granularity' prop.{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_granularity_invalid_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["groups"] = [{
            "name": "saletime",
            "label": "saletime",
            "granularity": "MILLISECOND",
            "sort": {
                "name": "eventname",
                "func": "unique",
                "dir": "asc"
            },
            "limit": 5
        }]
        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}Invalid group granularity definition (MILLISECOND). Use one of these: ['SECOND', 'MINUTE', 'HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_instance_dataframe_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.
        prov = Provider({}, prov_data.JSON_CONFIG)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The first parameter of the provider() function must be an instance of: pandas.core.frame.DataFrame{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_filter_operation_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["filters"] = [{
            "path": "community_areas",
            "operation": 35,
            "value": [
                "75"
            ]
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = "The json config is invalid, please check the following errors:Invalid property 'config → filters → 0': " \
              "{'path': 'community_areas', 'operation': 35, 'value': ['75']} is not valid under any of the given schemas. " \
              "35 is not of type 'string'"
        captured_msg = captured_output.getvalue().replace("\n", '') \
            .replace('[41m', '') \
            .replace('[0m', '') \
            .replace('[1m', '') \
            .replace('[32m', '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_filter_operation_invalid_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["filters"] = [{
            "path": "community_areas",
            "operation": "INOUT",
            "value": [
                "75"
            ]
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}Invalid filter operation INOUT. Use one of these: ['LE', 'GE', 'LT', 'GT', 'GE,LT', 'GT,LE', 'GT,LT', 'EQUAL', 'NOT EQUAL', 'IN', 'NOT IN', 'TS', 'NOT TS', 'BETWEEN']{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_metric_interval_float_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": "yti",
            "fixedBars": 20,
            "offset": 5
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The interval must be a positive decimal.{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_metric_interval_zero_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": -1,
            "fixedBars": 20,
            "offset": 5
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The interval must be a positive decimal.{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_metric_interval_offset_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": 4,
            "fixedBars": 20,
            "offset": 5
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The offset must be less than the interval.{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_fixed_bars_float_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": 10,
            "fixedBars": "ftf",
            "offset": 5
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The fixedBars must be a positive decimal.{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_fixed_bars_zero_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": 10,
            "fixedBars": -1,
            "offset": 5
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The fixedBars must be a positive decimal.{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_offset_float_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": 10,
            "fixedBars": 10,
            "offset": "err"
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The offset must be a positive decimal.{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_offset_interval_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "histogram",
            "interval": 10,
            "fixedBars": 10,
            "offset": 11
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The offset must be less than the interval.{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_invalid_metric_func_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["metrics"] = [{
            "name": "pricepaid",
            "func": "SUMM"
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}Invalid function 'summ' for metric pricepaid. Use one of these: ['max', 'min', 'sum', 'avg', 'distinct', 'unique', 'percentiles', 'histogram', 'count']{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)

    def test_should_return_invalid_metric_name_exception(self):
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # Redirect stdout.

        config = copy.deepcopy(prov_data.JSON_CONFIG)
        config["config"]["metrics"] = [{
            "name": "pricepaid_price",
            "func": "SUM"
        }]

        prov = Provider(self.df, config)

        sys.stdout = sys.__stdout__  # Reset redirect.
        msg = f"{Style.BRIGHT}{Fore.RED}The metric 'pricepaid_price' does not belong to any columns in the dataframe.{Style.RESET_ALL}"
        captured_msg = captured_output.getvalue().replace("\n", '')
        self.assertEqual(captured_msg, msg)
    # endregion


if __name__ == '__main__':
    unittest.main()
