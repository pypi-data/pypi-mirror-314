import json
import re
from .resources.constants import Constants as cnts
from .resources.commons import Commons as cmms


class CompareMetric(object):
    """
    This object can create different types of comparatives such as time periods, rates, and benchmarks.

    Definition examples:

    >>> benchmark = CompareMetric('price_paid', 'sum').benchmark("avg").using("event_name").label('benchmark')

    >>> rate = CompareMetric().rate().using('event_name').label('Rate')

    >>> bench_rate = CompareMetric().rate().using('like_musicals').label('Like Musicals rate').benchmark('avg').against('event_name').label('Avg event in the group')

    >>> time_comparative = CompareMetric('price_paid', 'sum').rate('growth')._with('-1 day').using('sale_time').label('Growth against yesterday')

    """
    def __init__(self, name='count', func=cnts.SUM):
        self.__name = name
        self.__label = None
        self.__filters = []
        self.__func = func
        self.__benchmark_label = None
        self.__use_name = name + '_compare'
        self.__rate = None
        self.__compare_type = 'time-offset'
        self.__using_filters = None
        self.__remove_after = []
        # Only for comparative
        self.__with = None
        self.__benchmark_function = None
        # Only for rateBenchmark: Filters to be removed
        self.__against = None
        self.__original_against  = None
        self.__hide_function = False
        self.__groups = []
        self.__type = None

    @property
    def name(self):
        return self.__name

    @property
    def get_label(self):
        return self.__label

    @property
    def get_benchmark_label(self):
        return self.__benchmark_label

    @property
    def get_benchmark_func(self):
        return self.__benchmark_function

    @property
    def get_with(self):
        return self.__with

    @property
    def get_using_filters(self):
        return self.__using_filters

    @property
    def get_rate(self):
        return self.__rate

    @property
    def get_against(self):
        return self.__original_against

    @property
    def get_hide_function(self):
        return self.__hide_function

    @property
    def get_func(self):
        return self.__func

    def __repr__(self):
        attr = self.__get_val__()
        return json.dumps(attr)

    def __get_val__(self):
        metric = {'name': self.__name, 'func': self.__func}
        if self.__name == "count":
            metric['func'] = ""
        return metric

    def label(self, label):
        if self.__compare_type != 'rate-benchmark':
            self.__label = label
            self.__use_name = re.sub(r"\s", '_', str(label).lower())
        else:
            self.__benchmark_label = label

        return self

    def _with(self, preset):
        preset = re.sub(r"\s", '|', str(preset).lower())
        match = re.match(r"-?\d(\d+)*\|(year|mon|day|week|hour|min|sec|frame)", preset)

        if match: self.__with = match[0]

        if not self.__with:
            self.__with = '-1|frame'

        return self

    def using(self, *filters):
        filters_list = list(filters)
        if len(filters_list) > 0 and isinstance(filters_list[0], list):
            self.__using_filters = filters_list[0]
        else:
            self.__using_filters = list(filters)
        return self

    def against(self, *filters):
        filters_list = list(filters)
        if len(filters_list) > 0 and isinstance(filters_list[0], list):
            against_filters = filters_list[0]
        else:
            against_filters = list(filters)

        self.__original_against = against_filters
        if self.__compare_type == 'benchmark':
            # It's the same as using()
            self.__using_filters = against_filters
            return self
        elif self.__compare_type == 'rate-benchmark':
            self.__against = against_filters
        else:
            raise Exception('Comparative method against() can be used only after benchmark()')
        return self

    def rate(self, type=''):
        self.__rate = type
        self.__compare_type = 'rate-raw' if type == 'raw' else 'rate-growth' if type == 'growth' else 'rate'
        self.__type = cnts.PERCENT
        return self

    def benchmark(self, func):
        if self.__compare_type == 'rate' and self.__using_filters:
            # The using is building a benchmark rate
            self.__compare_type = 'rate-benchmark'
            self.__type = cnts.PERCENT
            self.__benchmark_function = func
        else:
            self.__compare_type = 'benchmark'
            self.__benchmark_function = func
        return self

    def fromJSON(self, conf):
        keys = list(dict.fromkeys(conf))
        for k in keys:
            self[f'__{cmms.__to_snake_case__(k)}'] = conf[k]
        return self

    def hideFunction(self):
        self.__hide_function = True
        return self

    def func(self, func):
        self.__func = func
        return self
