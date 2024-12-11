import json
from .resources.constants import Constants as cnts


class Metric(object):
    """
    The Metric object represents the measure object.
    One or more Metric objects can be passed as parameters to the .metrics() function.

    Definition example:

    >>> # The count metric
    >>> metric_0 = cf.Metric()
    >>> # Commission sum
    >>> metric_1 = cf.Metric("commission", "sum").hideFunction()
    >>> # Price paid sum
    >>> metric_2 = cf.Metric("price_paid", "sum").hideFunction()
    >>> # Define an attribute to group by
    >>> group = cf.Attribute("event_name").limit(10) .sort("desc", metric_1);
    >>> cf.source("data_frame_name").graph("Chart Name").groupby(group).metrics(metric_0, metric_1, metric_2).execute()

    """
    def __init__(self, name='count', func=cnts.SUM):
        self.__name = name
        self.__func = func
        self.__interval = None
        self.__fixed_bars = 8
        self.__has_fixed_bars = False
        self.__show_empty_intervals = False
        self.__has_show_empty_intervals = False
        self.__offset = 0
        self.__hide_function = False
        self.__is_sort_metric = False

    @property
    def name(self):
        return self.__name

    @property
    def func(self):
        return self.__func

    @property
    def get_interval(self):
        return self.__interval

    @property
    def get_fixed_bars(self):
        return self.__fixed_bars

    @property
    def has_fixed_bars(self):
        return self.__has_fixed_bars

    @property
    def get_show_empty_intervals(self):
        return self.__show_empty_intervals

    @property
    def has_show_empty_intervals(self):
        return self.__has_show_empty_intervals

    @property
    def get_offset(self):
        return self.__offset

    @property
    def get_hide_function(self):
        return self.__hide_function

    @property
    def is_sort_metric(self):
        return self.__is_sort_metric

    def __repr__(self):
        attr = self.__get_val__()
        return json.dumps(attr)

    def __get_val__(self):
        metric = {'name': self.__name, 'func': self.__func, "isSortMetric": self.__is_sort_metric}
        if self.__name == "count":
            metric['func'] = ""
        return metric

    def interval(self, interval):
        """
        It defines the interval to be used by each bar of the histogram. It must be a positive decimal.
        For example an interval of 10 will create bars from 0-10, 10-20, 20-30,... etc.
        If some intervals are skipped, it means that they have zero transactions (count).
        
        :param interval:
        :return: self
        """
        if interval < 0:
            raise Exception('The interval must be a positive decimal.')
        if interval < self.__offset:
            raise Exception('The interval must be greater than the offset.')
        self.__interval = interval
        return self

    def fixedBars(self, fixed_bars):
        """
        It will try to display a fixed number of bars. It must be a positive decimal.
        If the bars rendered are less than the amount specified, then it means that there are some bars with zero transactions (count)
        See https://chartfactor.com/doc/latest/visualizations/histogram/#metric-parameters for more info.
        
        :param fixed_bars:
        :return: self
        """
        if fixed_bars < 0:
            raise Exception('The fixedBars must be a positive decimal.')
        self.__fixed_bars = fixed_bars
        self.__has_fixed_bars = True
        return self

    def showEmptyIntervals(self, show):
        """
        It allows to display all bars/buckets even if they have no transactions. Its default value is false.
        
        :param show:
        :return: self
        """
        self.__show_empty_intervals = show
        self.__has_show_empty_intervals = True
        return self

    def offset(self, offset):
        """
        The buckets can be shifted by using this option. It must be a decimal greater than or equal to 0 and less than interval.
        For example, if there are 10 documents with values ranging from 5 to 14, using interval 10 will result in two buckets, [0, 5), [5, 15).
        If an additional offset 5 is used, there will be only one single bucket [5, 15) containing all the 10 documents.
        
        :param offset:
        :return: self
        """
        if offset < 0:
            raise Exception('The offset must be a positive decimal.')
        if self.__interval is not None and offset > self.__interval:
            raise Exception('The offset must be less than the interval.')
        self.__offset = offset
        return self

    def hideFunction(self):
        """
        It allows to only render the metric label and hide the aggregation function.
        
        :return: self
        """
        self.__hide_function = True
        return self

    def isSortMetric(self):
        self.__is_sort_metric = True
        return self
