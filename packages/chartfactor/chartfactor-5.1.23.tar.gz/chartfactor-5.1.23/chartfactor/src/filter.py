import json
from .resources.constants import Constants as cnts


class Filter(object):
    """
    The Filter object allows to build filters to narrow our queries.

    Definition example:

    >>> filter = Filter('venue_state').operation('IN').value(['CA','FL'])

    See https://chartfactor.com/doc/latest/objects/filter/ for more information.
    """

    def __init__(self, path):
        self.__path = path
        self.__label = path
        self.__operation = 'IN'
        self.__value = []
        self.__relative = False
        self.__is_text_filter = False

    def __repr__(self):
        attrs = self.__get_val__()
        return json.dumps(attrs)

    def __get_val__(self):
        return {
            'path': self.__path,
            'operation': self.__operation,
            'value': self.__value
        }

    @property
    def get_path(self):
        return self.__path

    @property
    def get_label(self):
        return self.__label

    @property
    def get_operation(self):
        return self.__operation

    @property
    def get_value(self):
        return self.__value

    @property
    def get_relative(self):
        return self.__relative

    @property
    def is_text_filter(self):
        return self.__is_text_filter

    def __translate_operation__(self, op):
        op = op.replace('<=', 'LE')
        op = op.replace('>=', 'GE')
        op = op.replace('<', 'LT')
        op = op.replace('>', 'GT')
        op = op.replace('!=', 'NOT EQUAL')
        op = op.replace('<>', 'NOT EQUAL')
        op = op.replace('=', 'EQUAL')
        op = op.replace('EQUALS', 'EQUAL')
        op = op.replace('NOT EQUALS', 'NOT EQUAL')
        return op

    def label(self, label):
        """
        label() sets the custom label to be displayed.
        
        :param label:
        :return: self
        """
        self.__label = label
        return self

    def operation(self, op):
        """
        It defines the filter operation to be used.
        Possible operation are [LE, GE, LT, GT, GE_LT, GT_LE, GT_LT, EQUAL, NOT_EQUAL, IN, NOT_IN, TS, NOT_TS, BETWEEN].
        
        :param op:
        :return: self
        """
        if not isinstance(op, str):
            raise Exception('The value for the operation must be string')

        op = op.upper()
        op = self.__translate_operation__(op)

        if op not in cnts.FILTER_OPERATIONS:
            raise Exception(f'Invalid filter operation {op}. Use one of these: %s' % cnts.FILTER_OPERATIONS)

        self.__operation = op
        return self

    def value(self, *args):
        """
        It defines the value of the filter, could be a single value or an array.
        
        :param args:
        :return: self
        """
        if args and isinstance(args[0], list):
            self.__value = args[0]
        else:
            self.__value = list(args)
        return self

    def isRelative(self):
        """
        See https://chartfactor.com/doc/latest/objects/filter/#relative-filters for more information.
        :return:
        """
        self.__relative = True
        return self

    def isTextFilter(self):
        self.__is_text_filter = True
        return self
