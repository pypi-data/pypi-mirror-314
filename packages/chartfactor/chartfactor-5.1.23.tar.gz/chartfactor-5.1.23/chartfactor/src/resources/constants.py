class Constants(object):
    MAX = 'max'
    MIN = 'min'
    SUM = 'sum'
    AVG = 'avg'
    DISTINCT = 'distinct'
    UNIQUE = 'unique'
    PERCENTILES = 'percentiles'
    PERCENT = 'PERCENT'
    HISTOGRAM = 'histogram'
    COUNT = 'count'
    FUNCTIONS = [MAX, MIN, SUM, AVG, DISTINCT, UNIQUE, PERCENTILES, HISTOGRAM, COUNT]
    FUNCTIONS_TRANSLATED = {
        "max": "max",
        "min": "min",
        "sum": "sum",
        "avg": "mean",
        "distinct": "unique",
        "unique": "unique",
        "count": "count",
        "percentiles": "percentiles",
        "histogram": "histogram"
    }
    META_TYPES = {
        "b": "ATTRIBUTE",
        "i": "INTEGER",
        "u": "INTEGER",
        "f": "NUMBER",
        "c": "NUMBER",
        "m": "TIME",
        "M": "TIME",
        "O": "ATTRIBUTE",
        "S": "ATTRIBUTE",
        "U": "ATTRIBUTE",
        "V": "ATTRIBUTE"
    }
    ASC = 'ASC'
    DESC = 'DESC'
    LE = "LE"
    GE = "GE"
    LT = "LT"
    GT = "GT"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT EQUAL"
    IN = "IN"
    NOT_IN = "NOT IN"
    TS = "TS"
    NOT_TS = "NOT TS"
    BETWEEN = "BETWEEN"
    GE_LT = "GE,LT"
    GT_LE = "GT,LE"
    GT_LT = "GT,LT"
    FILTER_OPERATIONS = [LE, GE, LT, GT, GE_LT, GT_LE, GT_LT, EQUAL, NOT_EQUAL, IN, NOT_IN, TS, NOT_TS, BETWEEN]
    SORT_DIRECTIONS = [ASC, DESC]
    TIME_GRANULARITY = ["SECOND", "MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "YEAR"]
    # To see more info about the granularity offset aliases visit:
    # https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases
    GRANULARITY_TRANSLATED = {
        "YEAR": "Y",
        "MONTH": "M",
        "WEEK": "W",
        "DAY": "D",
        "HOUR": "H",
        "MINUTE": "T",
        "SECOND": "S",
        "MILLISECOND": "L"
    }
    THEMES = {
        'default': 'intense',
        'skins': {
            'dark': {
                'name': 'dark',
                'font': 'white',
                'background': '#404040',

                'header': '#616161',
                'rowOdd': '#302f2f',
                'rowEven': '#403e3e'
            },
            'light': {  # This is the default skin
                'name': 'light',
                'font': 'black',
                'background': 'white'
            }
        },
        'definition': {
            'neonGreen': ['#00ffff', '#52f0fd', '#6fe0fc', '#83d2fa', '#54cee1', '#00c8cb', '#00bec0', '#00b4b5',
                          '#00a9ab', '#009fa0', '#009595', '#008b8b'],
            'pastel': ['#a7efe9', '#a1ebe3', '#ace4d5', '#e1d3b5', '#f0caa9', '#f7c1a1', '#fab99b', '#fbb296',
                       '#fbac91'],
            'eclipse': ['#f6efb4', '#dbe6b6', '#c2deb8', '#a9d4bb', '#91c9be', '#7abec1', '#66b3c5', '#52a5ca',
                        '#4398d0', '#378ad8', '#3379e4'],
            'candy': ['#ffb6b9', '#fdc0c0', '#fac8c5', '#f4ceca', '#edd3cd', '#e4d6cf', '#d9d7d0', '#cdd8d1', '#bfd7d0',
                      '#b0d4ce', '#9fd1cb', '#8dccc8', '#78c7c4', '#61c0bf'],
            'nightly': ['#11cbd7', '#64d6dc', '#8cdedf', '#a9e3e0', '#c2e4dd', '#d6dfd6', '#e7d4ca', '#f4c2b8',
                        '#fda79f', '#ff817f', '#fa4659'],
            'macarons': ['#2ec7c9', '#b6a2de', '#5ab1ef', '#ffb980', '#d87a80', '#8d98b3', '#e5cf0d', '#97b552',
                         '#95706d', '#dc69aa', '#07a2a4', '#9a7fd1', '#588dd5', '#f5994e', '#c05050', '#59678c',
                         '#c9ab00', '#7eb00a', '#6f5553', '#c14089'],
            'vintage': ['#d87c7c', '#919e8b', '#d7ab82', '#6e7074', '#61a0a8', '#efa18d', '#787464', '#cc7e63',
                        '#724e58', '#4b565b'],
            'roma': ['#E01F54', '#001852', '#f5e8c8', '#b8d2c7', '#c6b38e', '#a4d8c2', '#f3d999', '#d3758f', '#dcc392',
                     '#2e4783', '#82b6e9', '#ff6347', '#a092f1', '#0a915d', '#eaf889', '#6699FF', '#ff6666', '#3cb371',
                     '#d5b158', '#38b6b6'],
            'green': ['#00ff7f', '#2bdb77', '#32bd6c', '#2fa35c', '#288c47', '#1c772c', '#006400'],
            'intense': ['#0095b7', '#a0b774', '#f4c658', '#fe8b3e', '#cf2f23', '#756c56', '#007896', '#47a694',
                        '#f9a94b', '#ff6b30', '#e94d29', '#005b76'],
            'zoomdata': ['#ffc65f', '#9eb778', '#0096b6'],
            'purple': ['#6495ed', '#6297dc', '#6097ce', '#5e93c2', '#5d8db9', '#5c84b2', '#5c78ad', '#5c6aaa',
                       '#5a58aa', '#5742ac', '#4f25af']
        }
    }
    JSON_CONFIG_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "$id": "http://example.com/example.json",
        "type": "object",
        "title": "The root schema",
        "description": "The root schema comprises the entire JSON document.",
        "default": {},
        "examples": [
            {
                "config": {
                    "location": "dropoff_location",
                    "precision": 3,
                    "filters": [
                        {
                            "path": "community_areas",
                            "operation": "IN",
                            "value": [
                                "75"
                            ]
                        }
                    ],
                    "groups": [
                        {
                            "name": "community_areas",
                            "label": "community_areas",
                            "granularity": "YEAR",
                            "tz": "America/Guayaquil",
                            "sort": {
                                "name": "extras",
                                "func": "sum",
                                "dir": "desc"
                            },
                            "limit": 10
                        }
                    ],
                    "metrics": [
                        {
                            "name": "metric",
                            "func": "sum"
                        }
                    ],
                    "fields": [
                        {
                            "name": "community_areas",
                            "label": "community_areas"
                        }
                    ],
                    "exclude": [
                        "dropoff_census_tract"
                    ]
                },
                "columns": [
                    {
                        "name": "community_areas",
                        "label": "community_areas"
                    }
                ],
                "rows": [
                    {
                        "name": "community_areas",
                        "label": "community_areas"
                    }
                ],
                "sortModel": [
                    {
                        "colId": "catname",
                        "sort": "asc"
                    }
                ],
                "rawQuery": False,
                "timeRangeVisual": False,
                "aggregate": True,
                "limit": 0,
                "offset": 0,
                "visualization": "Box Plot"
            }
        ],
        "required": [
            "config"
        ],
        "properties": {
            "config": {
                "$id": "#/properties/config",
                "type": "object",
                "title": "The config schema",
                "description": "An explanation about the purpose of this instance.",
                "default": {},
                "examples": [
                    {
                        "location": "dropoff_location",
                        "precision": 3,
                        "filters": [
                            {
                                "path": "community_areas",
                                "operation": "IN",
                                "value": [
                                    "75"
                                ]
                            }
                        ],
                        "groups": [
                            {
                                "name": "community_areas",
                                "label": "community_areas",
                                "granularity": "YEAR",
                                "tz": "America/Guayaquil",
                                "sort": {
                                    "name": "extras",
                                    "func": "sum",
                                    "dir": "desc"
                                },
                                "limit": 10
                            }
                        ],
                        "metrics": [
                            {
                                "name": "metric",
                                "func": "sum"
                            }
                        ],
                        "fields": [
                            {
                                "name": "community_areas",
                                "label": "community_areas"
                            }
                        ],
                        "exclude": [
                            "dropoff_census_tract"
                        ]
                    }
                ],
                "required": [
                    "filters",
                    "groups",
                    "metrics"
                ],
                "properties": {
                    "location": {
                        "$id": "#/properties/config/properties/location",
                        "type": "string",
                        "title": "The location schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": "",
                        "examples": [
                            "dropoff_location"
                        ]
                    },
                    "precision": {
                        "$id": "#/properties/config/properties/precision",
                        "type": "integer",
                        "title": "The precision schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": 0,
                        "examples": [
                            3
                        ]
                    },
                    "filters": {
                        "$id": "#/properties/config/properties/filters",
                        "type": "array",
                        "title": "The filters schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": [],
                        "examples": [
                            [
                                {
                                    "path": "community_areas",
                                    "operation": "IN",
                                    "value": [
                                        "75"
                                    ]
                                }
                            ]
                        ],
                        "additionalItems": True,
                        "items": {
                            "$id": "#/properties/config/properties/filters/items",
                            "anyOf": [
                                {
                                    "$id": "#/properties/config/properties/filters/items/anyOf/0",
                                    "type": "object",
                                    "title": "The first anyOf schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": {},
                                    "examples": [
                                        {
                                            "path": "community_areas",
                                            "operation": "IN",
                                            "value": [
                                                "75"
                                            ]
                                        }
                                    ],
                                    "required": [
                                        "path",
                                        "operation",
                                        "value"
                                    ],
                                    "properties": {
                                        "path": {
                                            "$id": "#/properties/config/properties/filters/items/anyOf/0/properties/path",
                                            "type": "string",
                                            "title": "The path schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "community_areas"
                                            ]
                                        },
                                        "operation": {
                                            "$id": "#/properties/config/properties/filters/items/anyOf/0/properties/operation",
                                            "type": "string",
                                            "title": "The operation schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "IN"
                                            ]
                                        },
                                        "value": {
                                            "$id": "#/properties/config/properties/filters/items/anyOf/0/properties/value",
                                            "type": "array",
                                            "title": "The value schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": [],
                                            "examples": [
                                                [
                                                    "75"
                                                ]
                                            ],
                                            "additionalItems": True,
                                            "items": {
                                                "$id": "#/properties/config/properties/filters/items/anyOf/0/properties/value/items",
                                                "anyOf": [
                                                    {
                                                        "$id": "#/properties/config/properties/filters/items/anyOf/0/properties/value/items/anyOf/0",
                                                        "default": "",
                                                        "description": "An explanation about the purpose of this instance.",
                                                        "examples": [
                                                            "75"
                                                        ],
                                                        "title": "The first anyOf schema",
                                                        "type": [
                                                            "string",
                                                            "boolean",
                                                            "number",
                                                            "integer",
                                                            "null"
                                                        ]
                                                    }
                                                ]
                                            }
                                        }
                                    },
                                    "additionalProperties": True
                                }
                            ]
                        }
                    },
                    "groups": {
                        "$id": "#/properties/config/properties/groups",
                        "type": "array",
                        "title": "The groups schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": [],
                        "examples": [
                            [
                                {
                                    "name": "community_areas",
                                    "label": "community_areas",
                                    "granularity": "YEAR",
                                    "tz": "America/Guayaquil",
                                    "sort": {
                                        "name": "extras",
                                        "func": "sum",
                                        "dir": "desc"
                                    },
                                    "limit": 10
                                }
                            ]
                        ],
                        "additionalItems": True,
                        "items": {
                            "$id": "#/properties/config/properties/groups/items",
                            "anyOf": [
                                {
                                    "$id": "#/properties/config/properties/groups/items/anyOf/0",
                                    "type": "object",
                                    "title": "The first anyOf schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": {},
                                    "examples": [
                                        {
                                            "name": "community_areas",
                                            "label": "community_areas",
                                            "granularity": "YEAR",
                                            "tz": "America/Guayaquil",
                                            "sort": {
                                                "name": "extras",
                                                "func": "sum",
                                                "dir": "desc"
                                            },
                                            "limit": 10
                                        }
                                    ],
                                    "required": [
                                        "name",
                                        "sort"
                                    ],
                                    "properties": {
                                        "name": {
                                            "$id": "#/properties/config/properties/groups/items/anyOf/0/properties/name",
                                            "type": "string",
                                            "title": "The name schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "community_areas"
                                            ]
                                        },
                                        "label": {
                                            "$id": "#/properties/config/properties/groups/items/anyOf/0/properties/label",
                                            "type": "string",
                                            "title": "The label schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "community_areas"
                                            ]
                                        },
                                        "granularity": {
                                            "$id": "#/properties/config/properties/groups/items/anyOf/0/properties/granularity",
                                            "type": "string",
                                            "title": "The granularity schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "YEAR"
                                            ]
                                        },
                                        "tz": {
                                            "$id": "#/properties/config/properties/groups/items/anyOf/0/properties/tz",
                                            "type": "string",
                                            "title": "The tz schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "America/Guayaquil"
                                            ]
                                        },
                                        "sort": {
                                            "$id": "#/properties/config/properties/groups/items/anyOf/0/properties/sort",
                                            "type": "object",
                                            "title": "The sort schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": {},
                                            "examples": [
                                                {
                                                    "name": "extras",
                                                    "func": "sum",
                                                    "dir": "desc"
                                                }
                                            ],
                                            "required": [
                                                "name",
                                                "dir"
                                            ],
                                            "properties": {
                                                "name": {
                                                    "$id": "#/properties/config/properties/groups/items/anyOf/0/properties/sort/properties/name",
                                                    "type": "string",
                                                    "title": "The name schema",
                                                    "description": "An explanation about the purpose of this instance.",
                                                    "default": "",
                                                    "examples": [
                                                        "extras"
                                                    ]
                                                },
                                                "func": {
                                                    "$id": "#/properties/config/properties/groups/items/anyOf/0/properties/sort/properties/func",
                                                    "type": "string",
                                                    "title": "The func schema",
                                                    "description": "An explanation about the purpose of this instance.",
                                                    "default": "",
                                                    "examples": [
                                                        "sum"
                                                    ]
                                                },
                                                "dir": {
                                                    "$id": "#/properties/config/properties/groups/items/anyOf/0/properties/sort/properties/dir",
                                                    "type": "string",
                                                    "title": "The dir schema",
                                                    "description": "An explanation about the purpose of this instance.",
                                                    "default": "",
                                                    "examples": [
                                                        "desc"
                                                    ]
                                                }
                                            },
                                            "additionalProperties": True
                                        },
                                        "limit": {
                                            "$id": "#/properties/config/properties/groups/items/anyOf/0/properties/limit",
                                            "type": [
                                                "integer",
                                                "null"
                                            ],
                                            "title": "The limit schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": 0,
                                            "examples": [
                                                10
                                            ]
                                        }
                                    },
                                    "additionalProperties": True
                                }
                            ]
                        }
                    },
                    "metrics": {
                        "$id": "#/properties/config/properties/metrics",
                        "type": "array",
                        "title": "The metrics schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": [],
                        "examples": [
                            [
                                {
                                    "name": "metric",
                                    "func": "sum"
                                }
                            ]
                        ],
                        "additionalItems": True,
                        "items": {
                            "$id": "#/properties/config/properties/metrics/items",
                            "anyOf": [
                                {
                                    "$id": "#/properties/config/properties/metrics/items/anyOf/0",
                                    "type": "object",
                                    "title": "The first anyOf schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": {},
                                    "examples": [
                                        {
                                            "name": "metric",
                                            "func": "sum"
                                        }
                                    ],
                                    "required": [
                                        "name",
                                        "func"
                                    ],
                                    "properties": {
                                        "name": {
                                            "$id": "#/properties/config/properties/metrics/items/anyOf/0/properties/name",
                                            "type": "string",
                                            "title": "The name schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "metric"
                                            ]
                                        },
                                        "func": {
                                            "$id": "#/properties/config/properties/metrics/items/anyOf/0/properties/func",
                                            "type": "string",
                                            "title": "The func schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "sum"
                                            ]
                                        }
                                    },
                                    "additionalProperties": True
                                }
                            ]
                        }
                    },
                    "fields": {
                        "$id": "#/properties/config/properties/fields",
                        "type": "array",
                        "title": "The fields schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": [],
                        "examples": [
                            [
                                {
                                    "name": "community_areas",
                                    "label": "community_areas"
                                }
                            ]
                        ],
                        "additionalItems": True,
                        "items": {
                            "$id": "#/properties/config/properties/fields/items",
                            "anyOf": [
                                {
                                    "$id": "#/properties/config/properties/fields/items/anyOf/0",
                                    "type": "object",
                                    "title": "The first anyOf schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": {},
                                    "examples": [
                                        {
                                            "name": "community_areas",
                                            "label": "community_areas"
                                        }
                                    ],
                                    "required": [
                                        "name"
                                    ],
                                    "properties": {
                                        "name": {
                                            "$id": "#/properties/config/properties/fields/items/anyOf/0/properties/name",
                                            "type": "string",
                                            "title": "The name schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "community_areas"
                                            ]
                                        },
                                        "label": {
                                            "$id": "#/properties/config/properties/fields/items/anyOf/0/properties/label",
                                            "type": "string",
                                            "title": "The label schema",
                                            "description": "An explanation about the purpose of this instance.",
                                            "default": "",
                                            "examples": [
                                                "community_areas"
                                            ]
                                        }
                                    },
                                    "additionalProperties": True
                                }
                            ]
                        }
                    },
                    "exclude": {
                        "$id": "#/properties/config/properties/exclude",
                        "type": "array",
                        "title": "The exclude schema",
                        "description": "An explanation about the purpose of this instance.",
                        "default": [],
                        "examples": [
                            [
                                "dropoff_census_tract"
                            ]
                        ],
                        "additionalItems": True,
                        "items": {
                            "$id": "#/properties/config/properties/exclude/items",
                            "anyOf": [
                                {
                                    "$id": "#/properties/config/properties/exclude/items/anyOf/0",
                                    "type": "string",
                                    "title": "The first anyOf schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": "",
                                    "examples": [
                                        "dropoff_census_tract"
                                    ]
                                }
                            ]
                        }
                    }
                },
                "additionalProperties": True
            },
            "columns": {
                "$id": "#/properties/columns",
                "type": "array",
                "title": "The columns schema",
                "description": "An explanation about the purpose of this instance.",
                "default": [],
                "examples": [
                    [
                        {
                            "name": "community_areas",
                            "label": "community_areas"
                        }
                    ]
                ],
                "additionalItems": True,
                "items": {
                    "$id": "#/properties/columns/items",
                    "anyOf": [
                        {
                            "$id": "#/properties/columns/items/anyOf/0",
                            "type": "object",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": {},
                            "examples": [
                                {
                                    "name": "community_areas",
                                    "label": "community_areas"
                                }
                            ],
                            "required": [
                                "name"
                            ],
                            "properties": {
                                "name": {
                                    "$id": "#/properties/columns/items/anyOf/0/properties/name",
                                    "type": "string",
                                    "title": "The name schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": "",
                                    "examples": [
                                        "community_areas"
                                    ]
                                },
                                "label": {
                                    "$id": "#/properties/columns/items/anyOf/0/properties/label",
                                    "type": "string",
                                    "title": "The label schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": "",
                                    "examples": [
                                        "community_areas"
                                    ]
                                }
                            },
                            "additionalProperties": True
                        }
                    ]
                }
            },
            "rows": {
                "$id": "#/properties/rows",
                "type": "array",
                "title": "The rows schema",
                "description": "An explanation about the purpose of this instance.",
                "default": [],
                "examples": [
                    [
                        {
                            "name": "community_areas",
                            "label": "community_areas"
                        }
                    ]
                ],
                "additionalItems": True,
                "items": {
                    "$id": "#/properties/rows/items",
                    "anyOf": [
                        {
                            "$id": "#/properties/rows/items/anyOf/0",
                            "type": "object",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": {},
                            "examples": [
                                {
                                    "name": "community_areas",
                                    "label": "community_areas"
                                }
                            ],
                            "required": [
                                "name"
                            ],
                            "properties": {
                                "name": {
                                    "$id": "#/properties/rows/items/anyOf/0/properties/name",
                                    "type": "string",
                                    "title": "The name schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": "",
                                    "examples": [
                                        "community_areas"
                                    ]
                                },
                                "label": {
                                    "$id": "#/properties/rows/items/anyOf/0/properties/label",
                                    "type": "string",
                                    "title": "The label schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": "",
                                    "examples": [
                                        "community_areas"
                                    ]
                                }
                            },
                            "additionalProperties": True
                        }
                    ]
                }
            },
            "sortModel": {
                "$id": "#/properties/sortModel",
                "type": "array",
                "title": "The sortModel schema",
                "description": "An explanation about the purpose of this instance.",
                "default": [],
                "examples": [
                    [
                        {
                            "colId": "catname",
                            "sort": "asc"
                        }
                    ]
                ],
                "additionalItems": True,
                "items": {
                    "$id": "#/properties/sortModel/items",
                    "anyOf": [
                        {
                            "$id": "#/properties/sortModel/items/anyOf/0",
                            "type": "object",
                            "title": "The first anyOf schema",
                            "description": "An explanation about the purpose of this instance.",
                            "default": {},
                            "examples": [
                                {
                                    "colId": "catname",
                                    "sort": "asc"
                                }
                            ],
                            "required": [
                                "colId",
                                "sort"
                            ],
                            "properties": {
                                "colId": {
                                    "$id": "#/properties/sortModel/items/anyOf/0/properties/colId",
                                    "type": "string",
                                    "title": "The colId schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": "",
                                    "examples": [
                                        "catname"
                                    ]
                                },
                                "sort": {
                                    "$id": "#/properties/sortModel/items/anyOf/0/properties/sort",
                                    "type": "string",
                                    "title": "The sort schema",
                                    "description": "An explanation about the purpose of this instance.",
                                    "default": "",
                                    "examples": [
                                        "asc"
                                    ]
                                }
                            },
                            "additionalProperties": True
                        }
                    ]
                }
            },
            "rawQuery": {
                "$id": "#/properties/rawQuery",
                "type": "boolean",
                "title": "The rawQuery schema",
                "description": "An explanation about the purpose of this instance.",
                "default": False,
                "examples": [
                    False
                ]
            },
            "timeRangeVisual": {
                "$id": "#/properties/timeRangeVisual",
                "type": "boolean",
                "title": "The timeRangeVisual schema",
                "description": "An explanation about the purpose of this instance.",
                "default": False,
                "examples": [
                    False
                ]
            },
            "aggregate": {
                "$id": "#/properties/aggregate",
                "type": "boolean",
                "title": "The aggregate schema",
                "description": "An explanation about the purpose of this instance.",
                "default": False,
                "examples": [
                    True
                ]
            },
            "limit": {
                "$id": "#/properties/limit",
                "type": [
                    "integer",
                    "null"
                ],
                "title": "The limit schema",
                "description": "An explanation about the purpose of this instance.",
                "default": 0,
                "examples": [
                    0
                ]
            },
            "offset": {
                "$id": "#/properties/offset",
                "type": "integer",
                "title": "The offset schema",
                "description": "An explanation about the purpose of this instance.",
                "default": 0,
                "examples": [
                    0
                ]
            },
            "visualization": {
                "$id": "#/properties/visualization",
                "type": "string",
                "title": "The visualization schema",
                "description": "An explanation about the purpose of this instance.",
                "default": "",
                "examples": [
                    "Box Plot"
                ]
            }
        },
        "additionalProperties": True
    }

