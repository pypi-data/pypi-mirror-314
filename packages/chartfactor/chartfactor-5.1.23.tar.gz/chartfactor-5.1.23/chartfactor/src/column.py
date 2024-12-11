import json


class Column(object):
    """
    This is the object that creates a Column definition

    Definition example:

    >>> column = cf.Column('venues_tate', 'Venue State')
    """

    def __init__(self, name, label=''):
        self.__name = name
        self.__label = label
        self.__func = None

    @property
    def name(self):
        return self.__name

    @property
    def get_label(self):
        return self.__label

    @property
    def get_func(self):
        return self.__func

    def __repr__(self):
        attrs = self.__get_val__()
        return json.dumps(attrs)

    def __get_val__(self):
        return {
            'name': self.__name,
            'label': self.__label
        }

    def label(self, label):
        """
        label() sets the custom label to be displayed.
        
        :param label:
        :return: self
        """
        if not isinstance(label, str):
            raise Exception('The value for the label must be string')
        self.__label = label
        return self

    def func(self, func):
        self.__func = func
        return self
