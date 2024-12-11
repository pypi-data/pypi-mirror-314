from functools import reduce
import re


class Commons(object):
    """
    Contains all the commons functions to be used in the Api
    """

    def __deep_get__(dictionary, keys, default=None):
        """
        Gets the values from the dict, while the next prop is a dict, given the path in the keys object
        :param keys: the path to the property e.g. 'config.filers'
        :param default: default value if the property can not be found from the given path
        :return: the value of the property
        """
        return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."),
                      dictionary)

    def __to_snake_case__(self, string):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()

    def __get_anonymous_object__(self):
        """
        Define an instance of type Object which contains the given arguments inside
        :return: new anonymous object instance
        """
        Anonymous = lambda **kwargs: type("Object", (), kwargs)()
        return Anonymous
