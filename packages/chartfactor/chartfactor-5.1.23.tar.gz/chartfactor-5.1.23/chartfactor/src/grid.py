import json


class Grid(object):
    """
    This is the object that creates a Grid definition.

    Definition example to set a grid with top 10px, bottom 15px, left 20px and right 10px:

    >>> grid = Grid().top('10px').bottom('15px').left('20px').right('10px')
    """

    def __init__(self):
        self.__top = None
        self.__bottom = None
        self.__left = None
        self.__right = None
        self.__width = None
        self.__height = None
        self.__border_color = None
        self.__background_color = None

    @property
    def get_top(self):
        return self.__top

    @property
    def get_bottom(self):
        return self.__bottom

    @property
    def get_left(self):
        return self.__left

    @property
    def get_right(self):
        return self.__right

    @property
    def get_width(self):
        return self.__width

    @property
    def get_height(self):
        return self.__height

    @property
    def get_border_color(self):
        return self.__border_color

    @property
    def get_background_color(self):
        return self.__background_color

    def __repr__(self):
        attrs = self.__get_val__()
        return json.dumps(attrs)

    def __get_val__(self):
        return {
            'position': self.__top,
            'bottom': self.__bottom,
            'left': self.__left,
            'right': self.__right,
            'width': self.__width,
            'height': self.__height,
            'borderColor': self.__border_color,
            'backgroundColor': self.__background_color
        }

    def top(self, top):
        self.__top = top
        return self

    def bottom(self, bottom):
        self.__bottom = bottom
        return self

    def left(self, left):
        self.__left = left
        return self

    def right(self, right):
        self.__right = right
        return self

    def width(self, width):
        self.__width = width
        return self

    def height(self, height):
        self.__height = height
        return self

    def borderColor(self, border_color):
        self.__border_color = border_color
        return self

    def backgroundColor(self, background_color):
        self.__background_color = background_color
        return self

    def dimensions(self, conf):
        self.__top = conf.get('top')
        self.__bottom = conf.get('bottom')
        self.__left = conf.get('left')
        self.__right = conf.get('right')
        return self
