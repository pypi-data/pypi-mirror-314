import json
from .resources.constants import Constants as cnts
from .metric import Metric


class Attribute(object):
    """
    This is the object that the .groupby() function expects as parameters.
    It represents the field used to aggregate a query.

    Definition example:

    >>> attr_1 = cf.Attribute("timestamp_of_call").func("DAY").limit(1000).sort("asc", "timestamp_of_call")
    >>> attr_2 = cf.Attribute("event_name", "Event name").limit(20).sort("desc", metricObject)

    The Attribute constructor takes the name of the field existing in the data engine and the custom label which the default value is the name value.

    """

    def __init__(self, name, label=''):
        self.__name = name
        self.__label = label
        self.__limit = 100
        self.__granularity = None
        self.__time_zone = None
        self.__sort = {'name': '', 'func': cnts.SUM, 'dir': cnts.ASC}
        self.__has_sort = False
        self.__is_sort_by_metric = False
        self.__group_type = None
        self.__original_type = None

    @property
    def get_name(self):
        return self.__name

    @property
    def get_label(self):
        return self.__label

    @property
    def get_limit(self):
        return self.__limit

    @property
    def get_sort(self):
        return self.__sort

    @property
    def has_sort(self):
        return self.__has_sort

    @property
    def is_sort_by_metric(self):
        return self.__is_sort_by_metric

    @property
    def get_granularity(self):
        return self.__granularity

    @property
    def get_tz(self):
        return self.__time_zone

    @property
    def group_type(self):
        return self.__group_type

    @group_type.setter
    def group_type(self, group_type):
        self.__group_type = group_type

    @property
    def original_type(self):
        return self.__original_type

    @original_type.setter
    def original_type(self, original_type):
        self.__original_type = original_type

    def __repr__(self):
        attrs = self.__get_val__()
        return json.dumps(attrs)

    def __get_val__(self):
        return {
            'name': self.__name,
            'label': self.__label,
            'limit': self.__limit,
            'sort': self.__sort
        }

    def label(self, label):
        """
        label() sets the custom label to be displayed.
        :param label:
        :return:
        """
        self.__label = label
        return self

    def limit(self, limit):
        """
        limit() sets the max number of results to be retrieved for that attribute.

        :param limit:
        :return:
        """
        if not isinstance(limit, int):
            raise Exception('The value for the limit must be integer')
        self.__limit = limit
        return self

    def sort(self, dir, metric):
        """
        sort() takes two parameters, the first one is the sort order ('asc' or 'desc'), and the second is based on what
        is going to be sorted. It can be a Metric object or the string with the name of the same field, which will mean
        then that is going to be alphabetically sorted (or reverse alphabetically if is 'desc').
        
        :param dir:
        :param metric:
        :return:
        """
        func = ''
        if isinstance(metric, Metric):
            self.__is_sort_by_metric = True
            name = metric.__get_val__()['name']
            func = metric.__get_val__()['func']
        elif isinstance(metric, str):
            name = metric
        else:
            raise Exception("The second parameter of the sort() function must be string or an instance of Metric() object")

        if str.upper(dir) not in [cnts.ASC, cnts.DESC]:
            raise Exception(f"Invalid sort direction '{dir}'. Use one of these: %s" % [cnts.ASC, cnts.DESC])

        self.__sort = {'name': name, 'func': func, 'dir': str.upper(dir)}
        self.__has_sort = True

        return self

    def func(self, granularity):
        """
        func() only applies to time attributes and it defines granularity of the data.
        The possible values are SECOND, MINUTE, HOUR, DAY, WEEK, MONTH and YEAR. If the data is in date format for example,
        we can not tell the object to use SECOND or MINUTE. This will be possible only data is in datetime format.
        If the data represents monthly events for example, there is no point in using DAY but MONTH or YEAR.
        
        :param granularity:
        :return:
        """
        self.__granularity = granularity
        return self

    def tz(self, tz):
        self.__time_zone = tz
        return self
