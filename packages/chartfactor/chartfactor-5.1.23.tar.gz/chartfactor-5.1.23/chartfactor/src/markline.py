import json


class MarkLine(object):
    """
    This is the object that creates a MarkLine definition.

    Definition example:

    >>> mark_lines = cf.MarkLine().data([
    >>>     {'name':'Min', 'type':'min'},
    >>>     {'name':'Max', 'type':'max'},
    >>>     {'name':'Average', 'type':'average'},
    >>>     {'name':'Value', 'yAxis':100000}
    >>> ])

    # ...
    >>> .set('markline', mark_lines)
    # ...

    """

    def __init__(self):
        self.__color = '#000'
        self.__style = 'solid'
        self.__data = []

    @property
    def get_color(self):
        return self.__color

    @property
    def get_style(self):
        return self.__style

    @property
    def get_data(self):
        return self.__data

    def __repr__(self):
        attrs = self.__get_val__()
        return json.dumps(attrs)

    def __get_val__(self):
        return {
            'color': self.__color,
            'style': self.__style,
            'data': self.__data
        }

    def color(self, color):
        self.__color = color
        return self

    def style(self, style):
        self.__style = style
        return self

    def data(self, data):
        self.__data = data
        return self
