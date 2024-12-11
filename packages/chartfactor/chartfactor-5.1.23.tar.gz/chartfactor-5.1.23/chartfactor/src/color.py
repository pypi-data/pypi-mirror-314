import json
from .resources.constants import Constants as cnts
from .resources.commons import Commons as cmms
from .metric import Metric

eol = '\n'
tab = '\t'


class Color(object):
    """
    This is the object that creates a Color definition.

    Definition example to set a color configuration using theme 'intense' and coloring by metric value:

    >>> color = Color().theme('intense').metric(metric_0)
    """

    def __init__(self):
        self.__metric = None
        self.__skin = None
        self.__palette = None
        self.__range = None
        self.__match = None
        self.__auto_range_options = None

    @property
    def get_theme(self):
        return self.__skin

    @property
    def get_metric(self):
        return self.__metric

    @property
    def get_palette(self):
        return self.__palette

    @property
    def get_range(self):
        return self.__range

    @property
    def get_match(self):
        return self.__match

    @property
    def get_auto_range_options(self):
        return self.__auto_range_options

    def theme(self, skin):
        self.__skin = skin
        return self

    def metric(self, metric=None):
        """
        The color object accepts a metric object. Use this feature when you have ordered data.
        :param metric:

        :return: self
        """
        if metric is not None and not isinstance(metric, Metric):
            raise Exception('The metric function parameter must be an instance of Metric object')
        self.__metric = metric
        return self

    def palette(self, palette):
        """
        Palettes are the set of colors used to display data in a visual.
        ChartFactor includes a set of predefined palettes for the color object.
        These are: intense (default), green, macarons, purple, roma, and vintage.

        Usage:
        .palette(['#fdd49e', '#fdbb84', '#fc8d59', '#ef6548', '#d7301f', '#b30000', '#7f0000'])
        :param palette:
        
        :return: self
        """
        self.__palette = palette
        return self

    def range(self, color_range):
        """
        The range method of the Color object allows you to specify a range in the form of a list of objects that contain
        the minimum (min), maximum (max) and color (color) of each range.

        Usage:
        .range([
            {'min': 0, 'max': 30000, 'color': 'red'},
            {'min': 30000, 'max': 80000, 'color': 'gray'},
            {'min': 80000, 'max': 200000, 'color': 'blue'}
        ])
        :param color_range:
        :return:
        """
        self.__range = color_range
        return self

    def match(self, match_object):
        """
        The match method of the Color object allows you to specify a color by attribute values.

        Usage:
        .match({
            'Mamma Mia!': 'red',
            'Macbeth': 'blue',
            'Jersey Boys': 'purple'
        })
        :param match_object: color by attribute values
        :return:
        """
        self.__match = match_object
        return self

    def autoRange(self, options):
        """
        It enables automatic color range calculation rather than specifying color ranges manually.

        Usage:
        .autoRange({ dynamic: false })

        Note: To enable the recalculation of ranges while adding and removing filters to the visualization pass the object { dynamic: true } as parameter.

        :param options:
        :return: self
        """
        self.__auto_range_options = options
        return self

    def toJs(self):
        metric_call = ''
        if self.__metric is not None:
            cm_func = self.__metric.func
            cm_name = self.__metric.name
            func_declaration = f', "{cm_func}"' if cm_func and cm_func != 'derived' else ''
            metric_call = f'.metric(cf.Metric("{cm_name}"{func_declaration}))' if self.__metric is not None else ''

        palette_call = f'.palette({json.dumps(self.__palette)})' if self.__palette is not None else ''
        range_call = f'.range({json.dumps(self.__range)})' if self.__range is not None else ''
        match_call = f'.match({json.dumps(self.__match)})' if self.__match is not None else ''
        theme_call = f'.theme({json.dumps(self.__skin)})' if self.__skin is not None else ''
        auto_range_call = f'.autoRange({json.dumps(self.__auto_range_options)})' if self.__auto_range_options is not None else ''

        return f'__cf.Color(){palette_call}{metric_call}{range_call}{theme_call}{auto_range_call}{match_call}__'
