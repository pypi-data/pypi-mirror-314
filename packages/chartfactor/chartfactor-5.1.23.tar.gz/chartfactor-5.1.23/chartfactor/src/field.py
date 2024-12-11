import json


class Field(object):
    """
    The field object is used when we need to obtain raw data or display a Raw Data Table.

    Definition example:

    >>> field = Field('venue_state','Venue State')
    """

    def __init__(self, name, label=''):
        self.__name = name
        self.__label = label
        self.__group_name = None
        self.__field_type = None
        self.__original_type = None
        self.__tz = 'local'

    @property
    def name(self):
        return self.__name

    @property
    def get_label(self):
        return self.__label

    @property
    def get_group_name(self):
        return self.__group_name

    @property
    def field_type(self):
        return self.__field_type

    @field_type.setter
    def field_type(self, field_type):
        self.__field_type = field_type

    @property
    def original_type(self):
        return self.__original_type

    @original_type.setter
    def original_type(self, original_type):
        self.__original_type = original_type

    @property
    def tz(self):
        return self.__tz

    @tz.setter
    def tz(self, tz):
        self.__tz = tz

    def __repr__(self):
        attrs = self.__get_val__()
        return json.dumps(attrs)

    def __get_val__(self):
        return {
            'name': self.__name,
            'label': self.__label,
            'type': self.__field_type,
            'originalType': self.__original_type,
            'tz': self.__tz
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

    def group(self, group_name):
        """
        It defines the group in which the field will be under.
        
        :param group_name:
        :return: self
        """
        self.__group_name = group_name
        return self
