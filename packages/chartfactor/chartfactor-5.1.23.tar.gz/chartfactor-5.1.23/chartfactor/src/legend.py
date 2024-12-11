import json


class Legend(object):
    """
    This is the object that creates a Legend definition.

    Definition example:

    >>> legend = Legend().position('right').width(150)
    """

    def __init__(self, position='vertical', width=150, height='95%', sort='none'):
        self.__position = position
        self.__width = width
        self.__height = height
        self.__sort = sort

    @property
    def get_position(self):
        return self.__position

    @property
    def get_width(self):
        return self.__width

    @property
    def get_height(self):
        return self.__height

    @property
    def get_sort(self):
        return self.__sort

    def __repr__(self):
        attrs = self.__get_val__()
        return json.dumps(attrs)

    def __get_val__(self):
        return {
            'position': self.__position,
            'width': self.__width,
            'height': self.__height,
            'sort': self.__sort
        }

    def position(self, position):
        self.__position = position
        return self

    def width(self, width):
        self.__width = width
        return self

    def height(self, height):
        self.__height = height
        return self

    def sort(self, sort):
        self.__sort = sort
        return self
