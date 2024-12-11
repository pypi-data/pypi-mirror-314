import math
import re
import numpy as np
import pandas as pd
from pandas.api import types
from distutils import util
from pandas.errors import ParserError
from pandasql import sqldf
import copy
import pygeohash as pgh
import json
from jsonschema import Draft7Validator
from colorama import Fore, Style, Back
from .filter import Filter
from .field import Field
from .metric import Metric
from .compare_metric import CompareMetric
from .attribute import Attribute
from .row import Row
from .column import Column
from .resources.constants import Constants as cnts
from .resources.commons import Commons as cmms
import tzlocal
from decimal import Decimal, getcontext


def unique(x):
    return x.nunique()


def count(x):
    return len(x)


def quantile_0(x):
    return x.quantile(0)


def quantile_25(x):
    return x.quantile(.25)


def quantile_50(x):
    return x.quantile(.50)


def quantile_75(x):
    return x.quantile(.75)


def quantile_100(x):
    return x.quantile(1)


def transform_columns(columns):
    """
    Transforms tuples columns into string name
    E.g. ('commission', 'Concerts', 'Pop') into 'commission::Concerts::Pop'
    :param columns:
    :return:
    """
    new_columns = []
    for c in columns:
        if isinstance(c, tuple):
            new_columns.append('::'.join(filter(None, c)))
        else:
            new_columns.append(c)

    for i in range(len(new_columns)):
        c = re.sub(r'\s*(::size)$', '::count', new_columns[i])
        c = re.sub(r'\s*(::nunique)$', '::unique', c)
        new_columns[i] = c
    return new_columns


def get_pivot_columns(pivot):
    column_groups = []
    for c in pivot.columns:
        group = c.split("::")
        # Removing metric from first pos
        group = group[1:] if len(group) > 1 else group

        if group[-1] != '$total':  # Excluding the total columns
            if group not in column_groups:
                column_groups.append(group)

    return column_groups


def get_group_value(g):
    return None if str(g) in ['None', 'nan'] else str(g)


def convert_to_datetime_efficiently(df, datetime_col):
    unique_dates = pd.unique(df[datetime_col])
    m = dict(zip(unique_dates, pd.to_datetime(unique_dates, infer_datetime_format=True, utc=True)))
    df[datetime_col] = df[datetime_col].map(m)


def replace_agg(string):
    replaced = re.sub(r'\s*(_size)$', '_count', string)
    replaced = re.sub(r'\s*(_nunique)$', '_unique', replaced)
    return replaced


def sanitize(string):
    sanitized = re.sub(r'[\.\,\;\:\'\"\s\%\(\)\[\]\{\}\|\/\*\+\-\=\$\@\!\#\^\&]*', '', string)
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '_')
    sanitized = replace_agg(sanitized)
    if sanitized[0].isdigit():
        sanitized = f'cf_{sanitized}'
    return sanitized


def add_one_at_last_digit(input_string):
    dec = Decimal(input_string)
    getcontext().prec = len(dec.as_tuple().digits)
    return dec.next_plus()


def translate_nullable_value(value):
    if str(value) in ['None', 'nan']:
        return None
    else:
        return value


class Provider(object):
    """
    Sets the query's parameters defined in the json config.
    Can execute queries to the pandas dataframe object passed in the config.dataFrame property key.
    """

    def __init__(self, dataframe=None, json_config=None):
        self.__data = dataframe
        self.__config = json_config
        self.__filters = []
        self.__client_filters = []
        self.__static_filters = []
        self.__groups = []
        self.__col_groups = []
        self.__metrics = []
        self.__original_metrics = []
        self.__comparative_metrics = []
        self.__fields = []
        self.__exclude = []
        self.__rows = []
        self.__columns = []
        self.__limit = 0
        self.__offset = 0
        self.__visualization = ''
        self.__raw_query = False
        self.__aggregate = False
        self.__time_range_visual = False
        self.__benchmark_query = False
        self.__location = None
        self.__precision = None
        self.__sort_model = []
        self.__time_zone = None
        self.__has_comparative = None
        self.__time_field = None
        self.__only_with_filters = None
        self.__error = True
        self.__process_json_config__()
        # Apply defined filters to the current dataframe
        self.__data = self.__apply_filters__(self.__data)

    def __repr__(self):
        try:
            self_config = self.__get_self_config__()
            return json.dumps(self_config)
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')
        finally:
            return ''

    def __get_self_config__(self):
        filters = []
        groups = []
        fields = []

        [filters.append(json.loads(repr(f))) for f in self.__filters]
        [groups.append(json.loads(repr(g))) for g in self.__groups]
        [fields.append(json.loads(repr(f))) for f in self.__fields]

        self_config = {
            'filters': filters,
            'groups': groups,
            'fields': fields,
            'exclude': self.__exclude,
            'limit': self.__limit,
            'offset': self.__offset
        }

        return self_config

    def __clear_attrs__(self):
        self.__filters = []
        self.__client_filters = []
        self.__static_filters = []
        self.__groups = []
        self.__fields = []
        self.__exclude = []
        self.__limit = 0
        self.__error = True

    # region Getters
    @property
    def get_error(self):
        return self.__error

    @property
    def get_groups(self):
        return self.__groups

    @property
    def get_colgroups(self):
        return self.__col_groups

    @property
    def get_metrics(self):
        return self.__metrics

    @property
    def get_comparative_metrics(self):
        return self.__comparative_metrics

    @property
    def get_filters(self):
        return self.__filters

    @property
    def get_client_filters(self):
        return self.__client_filters

    @property
    def get_static_filters(self):
        return self.__static_filters

    @property
    def get_rows(self):
        return self.__rows

    @property
    def get_columns(self):
        return self.__columns

    @property
    def get_fields(self):
        return self.__fields

    @property
    def get_exclude(self):
        return self.__exclude

    @property
    def get_chart(self):
        return self.__visualization

    @property
    def get_time_field(self):
        return self.__time_field

    @property
    def get_limit(self):
        return self.__limit

    @property
    def get_location(self):
        return self.__location

    @property
    def get_precision(self):
        return self.__precision\

    @property
    def get_only_with_filters(self):
        return self.__only_with_filters

    # endregion

    # region Json config validations
    def __validate_json_config__(self):
        if self.__config is None:
            print('The provider needs a json config parameter, please provide a valid one')
            self.__clear_attrs__()
            return False
        else:
            validator = Draft7Validator(cnts.JSON_CONFIG_SCHEMA)
            errors = sorted(validator.iter_errors(self.__config), key=lambda e: e.path)
            if len(errors) > 0:
                print(f'{Back.RED}The json config is invalid, please check the following errors:{Style.RESET_ALL}')
                for error in errors:
                    if len(error.path) > 0:
                        error_msg = f"Invalid property {Style.BRIGHT}{Fore.GREEN}'{' → '.join(map(str, error.path))}'{Style.RESET_ALL}: {error.message}."
                        for sub_error in sorted(error.context, key=lambda e: e.schema_path):
                            error_msg = error_msg + ' ' + sub_error.message
                        print(error_msg)
                    else:
                        print(error.message)
                self.__clear_attrs__()
                return False
            else:
                return True

    def __process_json_config__(self):
        try:
            if isinstance(self.__data, pd.core.frame.DataFrame):
                self.__metadata = json.loads(self.get_data_source('name'))
                if self.__config and self.__validate_json_config__():
                    json_string = json.dumps(self.__config)
                    json_data = json.loads(json_string)

                    # Process the filters
                    filters = cmms.__deep_get__(json_data, 'config.filters') or []
                    for ft in filters:
                        new_filter = Filter(ft.get('path')).operation(ft.get('operation')).value(ft.get('value'))
                        self.__filters.append(new_filter)

                    # Process the metrics
                    metrics = cmms.__deep_get__(json_data, 'config.metrics') or []
                    for m in metrics:
                        metric_name = m.get('name')
                        metric_func = str.lower(m.get('func'))

                        if metric_name == 'count':
                            metric_name = 'total_cf_count'
                            metric_func = 'count'

                        interval = m.get('interval') or None
                        fb = m.get('fixedBars') or 8
                        sei = m.get('showEmptyIntervals') or False
                        offset = m.get('offset') or 0

                        added_metric = self.__add_new_metric__(metric_name, metric_func)
                        try:
                            if interval is not None:
                                float(interval)
                        except Exception:
                            raise Exception('The interval must be a positive decimal.')

                        if interval is not None:
                            added_metric.interval(interval)

                        try:
                            if fb != 8:
                                float(fb)
                        except Exception:
                            raise Exception('The fixedBars must be a positive decimal.')

                        if fb != 8:
                            added_metric.fixedBars(fb)

                        if sei:
                            added_metric.showEmptyIntervals(sei)

                        try:
                            if offset > 0:
                                float(offset)
                        except Exception:
                            raise Exception('The offset must be a positive decimal.')

                        if offset > 0:
                            added_metric.offset(offset)

                        self.__original_metrics.append(copy.deepcopy(added_metric))

                    # Process the groups
                    groups = cmms.__deep_get__(json_data, 'config.groups') or []
                    self.__groups = self.__get_groups__(groups, json_data)

                    # Process the colgroups
                    col_groups = cmms.__deep_get__(json_data, 'config.colgroups') or []
                    self.__col_groups = self.__get_groups__(col_groups, json_data)

                    # Process the fields
                    fields = cmms.__deep_get__(json_data, 'config.fields') or []
                    for fl in fields:
                        label = fl.get('label') if fl.get('label') is not None else fl.get('name')
                        new_field = Field(fl.get('name')).label(label)
                        new_field.field_type = fl.get('type')
                        new_field.original_type = fl.get('originalType')
                        new_field.tz = fl.get('tz', 'UTC')
                        if new_field.tz.lower() == 'local':
                            new_field.tz = tzlocal.get_localzone().zone
                        self.__fields.append(new_field)

                    self.__exclude = cmms.__deep_get__(json_data, 'config.exclude')

                    # Process the rows
                    rows = json_data.get('rows', [])
                    for r in rows:
                        label = r.get('label') if r.get('label') is not None else r.get('name')
                        func = r.get('func', r.get("timestampGranularity"))
                        new_row = Row(r.get('name')).label(label).func(func)
                        self.__rows.append(new_row)

                    # Process the columns
                    columns = json_data.get('columns', [])
                    for c in columns:
                        label = c.get('label') if c.get('label') is not None else c.get('name')
                        new_column = Column(c.get('name')).label(label)
                        self.__columns.append(new_column)

                    # Process the columns
                    sort_model = json_data.get('sortModel', [])
                    for s in sort_model:
                        col_id = s.get('colId')
                        sort = s.get('sort')
                        self.__sort_model.append({
                            "col": col_id,
                            "sort": sort
                        })

                    try:
                        limit = json_data.get('limit', 100)
                        self.__limit = int(limit)
                    except Exception:
                        self.__limit = 0

                    try:
                        offset = json_data.get('offset', 0)
                        self.__offset = int(offset)
                    except Exception:
                        self.__offset = 0

                    self.__raw_query = json_data.get('rawQuery', False)
                    self.__time_range_visual = json_data.get('timeRangeVisual', False)
                    # Inserting the time field in the first groups position to execute the time range query
                    if self.__time_range_visual:
                        tf = cmms.__deep_get__(json_data, 'config.timefield')
                        if tf:
                            label = tf.get('label') if tf.get('label') is not None else tf.get('name')
                            new_group = Attribute(tf.get('name')).label(label)

                            granularity = tf.get('func')
                            time_zone = tf.get('tz', cmms.__deep_get__(json_data, 'timezone.display')) or 'UTC'

                            if granularity is None:
                                raise Exception(
                                    f"The time field '{tf.get('name')}' represents a date or datetime field. "
                                    f"Please provide the 'granularity' prop.")
                            else:
                                if granularity not in cnts.TIME_GRANULARITY:
                                    raise Exception(
                                        f'Invalid time field granularity definition ({granularity}). Use one of these: %s' % cnts.TIME_GRANULARITY)

                                new_group.func(granularity)
                                new_group.tz(time_zone)

                            self.__groups.insert(0, new_group)

                    # Process the comparative metrics
                    comparative_metrics = cmms.__deep_get__(json_data, 'config.comparative') or []
                    for cm in comparative_metrics:
                        metric_name = cm.get('name')
                        metric_func = str.lower(cm.get('func'))
                        if metric_func == "derived":
                            metric_name = cm.get('dependencies')[0].get('name')
                            metric_func = cm.get('dependencies')[0].get('func')

                        if metric_name == 'count':
                            metric_name = 'total_cf_count'
                            metric_func = 'count'

                        added_metric = self.__add_new_comparative_metric__(metric_name, metric_func)

                        label = cm.get('label')
                        __with = cm.get('with')
                        using_filters = cm.get('usingFilters', [])
                        against = cm.get('against', [])
                        compare_type = cm.get('compareType')
                        rate_type = 'raw' if compare_type == 'rate-raw' else 'growth' if compare_type == 'rate-growth' else ''
                        benchmark = cm.get('benchmarkFunction')

                        if label:
                            added_metric.label(label)

                        if __with:
                            added_metric._with(__with)

                        if len(using_filters) > 1:
                            added_metric.using(using_filters)

                        if len(against) > 1:
                            added_metric.against(against)

                        added_metric.rate(rate_type)
                        added_metric.benchmark(benchmark)

                        self.__comparative_metrics.append(added_metric)

                    self.__benchmark_query = json_data.get('benchmarkQuery', False)
                    self.__aggregate = json_data.get('aggregate', False)
                    self.__location = cmms.__deep_get__(json_data, 'config.location')
                    self.__precision = cmms.__deep_get__(json_data, 'config.precision')
                    self.__visualization = json_data.get('visualization', '')
                    self.__time_zone = cmms.__deep_get__(json_data, 'timezone.display') or 'UTC'
                    if self.__time_zone.lower() == 'local':
                        self.__time_zone = tzlocal.get_localzone().zone
                    self.__has_comparative = json_data.get('hasComparative')
                    self.__slicerTextFilter = cmms.__deep_get__(json_data, 'config.slicerTextFilter')
                    if self.__slicerTextFilter:
                        slicer_group = self.__groups[0].get_name
                        slicer_text_filter = Filter(slicer_group).operation(cnts.TS).value(self.__slicerTextFilter)
                        self.__filters.append(slicer_text_filter)
                        for f in self.__filters:
                            if f.get_path == slicer_group and f.get_operation == cnts.IN:
                                f.operation(cnts.NOT_IN)
                    self.__error = False
                else:
                    self.__error = True
            else:
                raise Exception(
                    'The first parameter of the provider() function must be an instance of: pandas.core.frame.DataFrame')

        except AttributeError as a:
            print(f'{Style.BRIGHT}{Fore.RED}{a}{Style.RESET_ALL}')
        except ValueError as v:
            print(f'{Style.BRIGHT}{Fore.RED}{v}{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')

    # endregion

    def __get_groups__(self, groups, json_data):
        try:
            groups_list = []
            for g in groups:
                limit = g.get('limit') or 100
                label = g.get('label') if g.get('label') is not None else g.get('name')

                metric_name = cmms.__deep_get__(g, 'sort.name')
                metric_func = cmms.__deep_get__(g, 'sort.metricFunc')
                if metric_func is None or metric_func == '':
                    metric_func = cmms.__deep_get__(g, 'sort.func')
                metric_func = str.lower(metric_func or 'sum')

                if metric_name == g.get('name'):
                    metric_func = cnts.DISTINCT
                else:
                    if metric_name == 'count':
                        metric_name = g.get('name')
                        metric_func = cnts.COUNT

                sort_dir = cmms.__deep_get__(g, 'sort.dir')

                new_metric = self.__add_new_metric__(metric_name, metric_func)
                new_group = Attribute(g.get('name')).label(label).sort(sort_dir, new_metric).limit(limit)

                granularity = g.get('granularity', g.get('func'))
                time_zone = g.get('tz', cmms.__deep_get__(json_data, 'timezone.display')) or 'UTC'
                if time_zone.lower() == 'local':
                    time_zone = tzlocal.get_localzone().zone

                if self.__is_date_field__(g.get('name')):
                    if granularity is None:
                        raise Exception(
                            f"The group '{g.get('name')}' represents a date or datetime field. "
                            f"Please provide the 'granularity' prop.")
                    else:
                        if granularity not in cnts.TIME_GRANULARITY:
                            raise Exception(
                                f'Invalid group granularity definition ({granularity}). Use one of these: %s' % cnts.TIME_GRANULARITY)

                        new_group.func(granularity)
                        new_group.tz(time_zone)

                groups_list.append(new_group)

            return groups_list
        except Exception as e:
            raise Exception(e)

    # region Metric internal functions
    def __is_metric_field__(self, name):
        if self.__field_exists_in_df__(name):
            try:
                numeric_type = pd.to_numeric(self.__data[name]).dtype
                if numeric_type in [np.int64, np.float64]:
                    return True
            except (ParserError, ValueError, TypeError):
                return False

    def __field_exists_in_df__(self, name):
        if name not in self.__data.columns:
            raise Exception(f"The metric '{name}' does not belong to any columns in the dataframe.")
        return True

    def __metric_exists__(self, name, func):
        for m in self.__metrics:
            if m.name == name and m.func == func:
                return True
        return False

    def __original_metric_exists__(self, name, func):
        for m in self.__original_metrics:
            if m.name == name and m.func == func:
                return True
        return False

    def __comparative_metric_exists__(self, name, func):
        for m in self.__comparative_metrics:
            if m.name == name and m.func == func:
                return True
        return False

    def __add_new_metric__(self, name, func):
        try:
            if name != 'total_cf_count':
                if self.__field_exists_in_df__(name):
                    if func not in cnts.FUNCTIONS:
                        raise Exception(
                            f"Invalid function '{func}' for metric {name}. Use one of these: %s" % cnts.FUNCTIONS)
                    func = cnts.FUNCTIONS_TRANSLATED.get(func)

            new_metric = Metric(name, func)
            if not self.__metric_exists__(name, func):
                self.__metrics.append(new_metric)
            return new_metric
        except Exception as e:
            raise Exception(e)

    def __add_new_comparative_metric__(self, name, func):
        try:
            if name != 'total_cf_count':
                # if self.__field_exists_in_df__(name):
                if func not in cnts.FUNCTIONS:
                    raise Exception(
                        f"Invalid function '{func}' for metric {name}. Use one of these: %s" % cnts.FUNCTIONS)
                func = cnts.FUNCTIONS_TRANSLATED.get(func)

            new_metric = CompareMetric(name, func)
            if not self.__comparative_metric_exists__(name, func):
                self.__comparative_metrics.append(new_metric)
            return new_metric
        except Exception as e:
            raise Exception(e)

    # endregion

    # region Helper functions
    def is_field_type(self, name, type):
        object_fields = self.__metadata.get('objectFields')
        if object_fields:
            return any(f for f in object_fields if f.get('name') == name and f.get('type') == type)
        return False

    def get_original_type(self, name):
        object_fields = self.__metadata.get('objectFields')
        if object_fields:
            field = list(filter(lambda f: f.get('name') == name, object_fields))
            return field[0]['originalType']
        return None

    def get_time_fields(self):
        object_fields = self.__metadata.get('objectFields')
        if object_fields:
            fields = list(filter(lambda f: f.get('type') == 'TIME', object_fields))
            return fields
        return None

    def get_chartfactor_type(self, name):
        object_fields = self.__metadata.get('objectFields')
        if object_fields:
            field = list(filter(lambda f: f.get('name') == name, object_fields))
            return field[0]['type']
        return None

    def __is_date_field__(self, name):
        try:
            return self.is_field_type(name, 'TIME')
        except (ParserError, ValueError):
            return False

    def __apply_filters__(self, data):
        """
        Applies the current filters defined in the json config to the current DataFrame
        :param data: current pandas DataFrame defined in the provider
        :return: the DataFrame already filtered
        """
        if len(self.__filters) > 0:
            for f in self.__filters:
                if f.get_path in data.columns:
                    try:
                        cf_type = self.get_chartfactor_type(f.get_path)
                        original_type = self.get_original_type(f.get_path)
                        # Convert into boolean values
                        converted_values = []
                        for v in f.get_value:
                            try:
                                if cf_type == 'ATTRIBUTE' and v.lower() in ('true', 'false'):
                                    v = bool(util.strtobool(v))
                                elif cf_type == 'INTEGER':
                                    v = int(float(v))
                                elif cf_type == 'NUMBER':
                                    v = float(v)
                            except:
                                pass

                            try:
                                if original_type == 'date':
                                    v = pd.Timestamp(v).date()
                            except:
                                pass
                            converted_values.append(v)

                        f.value(converted_values)

                        if f.get_operation == cnts.LE:
                            data = data.loc[data[f.get_path] <= f.get_value[0]].reset_index(drop=True)
                        elif f.get_operation == cnts.GE:
                            data = data.loc[data[f.get_path] >= f.get_value[0]].reset_index(drop=True)
                        elif f.get_operation == cnts.BETWEEN:
                            between = (data[f.get_path] >= f.get_value[0]) & (data[f.get_path] <= f.get_value[1])
                            data = data.loc[between].reset_index(drop=True)
                        elif f.get_operation == cnts.GE_LT:
                            mask = (data[f.get_path] >= f.get_value[0]) & (data[f.get_path] < f.get_value[1])
                            data = data.loc[mask].reset_index(drop=True)
                        elif f.get_operation == cnts.GT_LE:
                            mask = (data[f.get_path] > f.get_value[0]) & (data[f.get_path] <= f.get_value[1])
                            data = data.loc[mask].reset_index(drop=True)
                        elif f.get_operation == cnts.GT_LT:
                            mask = (data[f.get_path] > f.get_value[0]) & (data[f.get_path] < f.get_value[1])
                            data = data.loc[mask].reset_index(drop=True)
                        elif f.get_operation == cnts.LT:
                            data = data.loc[data[f.get_path] < f.get_value[0]].reset_index(drop=True)
                        elif f.get_operation == cnts.GT:
                            data = data.loc[data[f.get_path] > f.get_value[0]].reset_index(drop=True)
                        elif f.get_operation == cnts.EQUAL:
                            data = data.loc[data[f.get_path] == f.get_value[0] if f.get_value[0] is not None else data[f.get_path].isnull()].reset_index(drop=True)
                        elif f.get_operation == cnts.NOT_EQUAL:
                            data = data.loc[data[f.get_path] != f.get_value[0] if f.get_value[0] is not None else data[f.get_path].notnull()].reset_index(drop=True)
                        elif f.get_operation == cnts.IN:
                            mask = data[f.get_path].isin(f.get_value)
                            if None in f.get_value:
                                mask = (data[f.get_path].isin(f.get_value) | data[f.get_path].isnull())
                            data = data.loc[mask].reset_index(drop=True)
                        elif f.get_operation == cnts.NOT_IN:
                            mask = ~data[f.get_path].isin(f.get_value)
                            if None in f.get_value:
                                mask = (~data[f.get_path].isin(f.get_value) & data[f.get_path].notnull())
                            data = data.loc[mask].reset_index(drop=True)
                        elif f.get_operation in [cnts.TS, cnts.NOT_TS]:
                            flag = True if f.get_operation == cnts.TS else False
                            data = data.loc[data[f.get_path].astype(str).str.contains(
                                '|'.join(map(re.escape, list(map(str,f.get_value))))) == flag].reset_index(drop=True)
                        else:
                            raise Exception(
                                f'Invalid filter operation {f.get_operation}. Use one of these: %s' % cnts.FILTER_OPERATIONS)
                    except Exception as e:
                        raise Exception(f'Error trying to apply filter to {f.get_path} column. {e}')
        return data

    def __is_type__(self, type):
        if len(self.__metrics) > 0:
            metric = self.__metrics[0]
        else:
            metric = Metric('', '')

        if type == 'histogram':
            return self.__visualization == 'Histogram' or metric.func == 'histogram'
        elif type == 'boxplot':
            return self.__visualization == 'Box Plot' or metric.func == 'percentiles'
        elif type == 'time_range':
            return self.__time_range_visual
        elif type == 'benchmark':
            return self.__benchmark_query
        elif type == 'raw_query':
            return self.__raw_query
        elif type == 'geo_clusters':
            return self.__location and self.__precision
        elif type == 'pivot':
            return self.__aggregate and len(self.__rows) > 0
        elif type == 'colgroups':
            return len(self.__groups) > 0 and len(self.__col_groups) > 0
        else:
            return False

    # endregion

    def get_config(self):
        """
        Prints the current configuration and the DataFrame
        :param self:
        :return:
        """
        try:
            if not self.__error:
                self_config = self.__get_self_config__()
                print('Config:')
                print('=========\n')
                print(json.dumps(self_config, indent=4, sort_keys=True))
                print('\n')
                print('DataFrame:')
                print('========= \n')
                print(self.__data)
            else:
                print(
                    f'{Style.BRIGHT}{Fore.RED}Either the dataframe or the json config is invalid. '
                    f'The get_config function can not be performed.{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')

    def run_count_query(self):
        """
        Execute the total count to the given DataFrame
        :param self:
        :return: a dict object that contains the count results
        """
        response = [{'group': [], 'current': {'count': 0}}]
        try:
            response = [{
                'group': [],
                'current': {
                    'count': len(self.__data.index)
                }
            }]
            return json.dumps(response)
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')
            return json.dumps(response)

    def run_raw_query(self):
        """
        Execute the row query into the given DataSource
        :param self:
        :return: a dict object that contains the raw query results
        """
        try:
            response = {'data': []}
            if not self.__error:
                size = len(self.__data.index)
                if size > 0:
                    if len(self.__sort_model) > 0:
                        sort_col = []
                        sort_dir = []
                        for s in self.__sort_model:
                            sort_col.append(s.get("col"))
                            direction = True if s.get("sort") == cnts.ASC.lower() else False
                            sort_dir.append(direction)
                        data = self.__data.sort_values(sort_col, ascending=sort_dir).reset_index(drop=True)

                        # Applying the offset and limit to the dataframe
                        data = data.iloc[self.__offset:(self.__limit if self.__limit > 0 else None)]\
                            .copy().reset_index(drop=True)
                    else:
                        # Applying the offset and limit to the dataframe
                        data = self.__data.iloc[self.__offset:].head(self.__limit if self.__limit > 0 else None)\
                            .copy().reset_index(drop=True)

                    if len(self.__fields) > 0:
                        fields = []
                        [fields.append(f.name) for f in self.__fields]
                        data = data.loc[:, data.columns.isin(fields)].reset_index(drop=True)

                    if len(self.__exclude) > 0:
                        data = data.loc[:, ~data.columns.isin(self.__exclude)].reset_index(drop=True)

                    for f in self.__fields:
                        if f.field_type == 'TIME' and f.name in data.columns and self.get_original_type(f.name) == 'datetime':
                            data[f.name] = pd.to_datetime(data[f.name], infer_datetime_format=True, utc=True)
                            if f.tz != 'UTC':
                                data[f.name] = data[f.name].dt.tz_convert(f.tz)
                            data[f.name] = data[f.name].dt.tz_localize(None)  # Removing time offset
                else:
                    response = {"data": []}
                    return json.dumps({'data': response})

                data.insert(0, 'rn', np.arange(1, data.shape[0] + 1))  # Inserting the row number column
                data = data.where(data.notnull(), None)
                time_fields_type = {}
                for f in self.get_time_fields():
                    if f.get('name') in data.columns:
                        time_fields_type[f.get('name')] = str
                if time_fields_type != {}:
                    result = data.astype(time_fields_type).to_json(orient="records")  # Convert datetime fields to str
                else:
                    result = data.to_json(orient="records")
                parsed = json.loads(result)
                response = {'data': parsed}
                return json.dumps({'data': response})
            else:
                print(
                    f'{Style.BRIGHT}{Fore.RED}Either the dataframe or the json config is invalid. '
                    f'The raw query can not be performed.{Style.RESET_ALL}')
                return json.dumps({'data': response})

        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')

    # region Visualize

    def __process_metrics_totals__(self):
        try:
            if len(self.__metrics) > 0:
                columns = []
                metrics = {}
                for m in self.__metrics:
                    columns.append(m.name)
                    if m.name in metrics:
                        metrics[m.name].append(m.func)
                    else:
                        metrics[m.name] = ['nunique'] if m.func == cnts.UNIQUE else ['size'] if m.func == cnts.COUNT else [
                            m.func]

                if 'total_cf_count' not in metrics:
                    self.__metrics.append(Metric('total_cf_count', 'count'))
                    metrics['total_cf_count'] = ['size']

                # Taking only the columns that will be used
                metrics_df = self.__data.loc[:, self.__data.columns.isin(columns)].reset_index(drop=True)
                metrics_df['total_cf_count'] = 1  # Column to calculate the count in queries

                metrics_totals = metrics_df.agg(metrics).copy()
                size = 0

                response = {
                    'data': [],
                    "visualization": self.__visualization
                }

                current_metrics = {}
                for index, row in metrics_totals.iterrows():
                    for m in self.__metrics:
                        if m.name == 'total_cf_count' and not pd.isna(row[m.name]):
                            size = int(row[m.name])
                        else:
                            if not pd.isna(row[m.name]):
                                if m.name not in current_metrics:
                                    current_metrics[m.name] = {}
                                metric_func = index.replace('mean', 'avg').replace('nunique', 'unique')
                                metric_value = translate_nullable_value(row[m.name])
                                if metric_value is not None:
                                    metric_value = round(float(row[m.name]), 2)
                                current_metrics[m.name][metric_func] = metric_value

                response.get('data').append({
                    'group': [],
                    'current': {
                        'count': size,
                        'metrics': current_metrics
                    }
                })

                return json.dumps({'data': response})

            else:
                raise Exception('Provide a metric to be able to run the query.')
        except Exception as e:
            raise Exception(e)

    def __process_single_group__(self):
        try:
            g = self.__groups[0]
            limit = g.get_limit
            asc = True if g.get_sort.get('dir') == cnts.ASC else False
            sort_name = g.get_sort.get('name')
            sort_func = g.get_sort.get('func')
            granularity_g = cnts.GRANULARITY_TRANSLATED.get(g.get_granularity)
            tz_g = g.get_tz
            columns = [g.get_name]

            self.__metrics = list(filter(lambda m: m.name != 'total_cf_count', self.__metrics))

            metrics = {}
            for m in self.__metrics:
                columns.append(m.name)
                if m.name in metrics:
                    metrics[m.name].append(m.func)
                else:
                    metrics[m.name] = ['nunique'] if m.func == cnts.UNIQUE else ['size'] if m.func == cnts.COUNT else [
                        m.func]

            # Adding total count
            if g.get_name in metrics:
                if 'size' not in metrics[g.get_name]:
                    metrics[g.get_name].append('size')
            else:
                metrics[g.get_name] = ['size']

            # Taking only the columns that will be used
            group_df = self.__data.loc[:, self.__data.columns.isin(columns)].reset_index(drop=True)
            group_df['total_cf_count'] = 1  # Column to calculate the count in queries

            # Converting group column to the specified granularity
            if g.get_granularity:
                convert_to_datetime_efficiently(group_df, g.get_name)
                if tz_g != 'UTC':
                    group_df[g.get_name] = group_df[g.get_name].dt.tz_convert(tz_g)
                group_df[g.get_name] = group_df[g.get_name].dt.tz_localize(None)  # Removing time offset
                group_df[g.get_name] = group_df[g.get_name].dt.to_period(granularity_g).dt.to_timestamp()

            original_type = self.get_original_type(g.get_name)
            is_tuple = isinstance(group_df[g.get_name][0], tuple)
            is_list = isinstance(group_df[g.get_name][0], list)

            if original_type == 'mixed' and (is_tuple or is_list):
                group_df = group_df.explode(g.get_name).reset_index(drop=True)

            group = group_df.groupby(g.get_name, dropna=False).agg(metrics).copy().reset_index()
            group.columns = [sanitize('_'.join(filter(None, x))) for x in group.columns]  # Renaming columns

            cf_type = self.get_chartfactor_type(g.get_name)
            if (cf_type != 'ATTRIBUTE' and g.get_name == sort_name) or \
                    (cf_type == 'ATTRIBUTE' and sort_func == cnts.UNIQUE):
                group = group.sort_values([sanitize(g.get_name)], ascending=[asc]).iloc[:limit].reset_index(drop=True)
            else:
                group = group.sort_values([f'{sanitize(sort_name)}_{sort_func}'], ascending=[asc]).iloc[:limit].reset_index(drop=True)

            if self.__visualization == 'Disk':
                group = group.sort_values([sanitize(sort_name)], ascending=[True]).reset_index(drop=True)

            response = {
                'data': [],
                "visualization": self.__visualization
            }

            for row in group.itertuples():
                row = row._asdict()
                current_metrics = {}
                for m in self.__metrics:
                    if m.func != cnts.COUNT:
                        if m.name not in current_metrics:
                            current_metrics[m.name] = {}

                        metric_value = translate_nullable_value(row[f'{sanitize(m.name)}_{m.func}'])
                        if metric_value is not None:
                            metric_value = round(float(row[f'{sanitize(m.name)}_{m.func}']), 2)
                        current_metrics[m.name][m.func.replace('mean', 'avg')] = metric_value

                row_value = translate_nullable_value(row[sanitize(g.get_name)])
                if row_value is not None:
                    row_value = row[sanitize(g.get_name)]
                    # Converting to string the fields to avoid json serialize exception
                    cf_type = self.get_chartfactor_type(g.get_name)
                    if cf_type not in ['INTEGER', 'NUMBER']:
                        row_value = str(row_value)

                response.get('data').append({
                    'group': [row_value],
                    'current': {
                        'count': int(row[f'{sanitize(g.get_name)}_count']),
                        'metrics': current_metrics
                    }
                })

            return json.dumps({'data': response})

        except Exception as e:
            raise Exception(e)

    def __process_two_groups__(self):
        try:
            g1 = self.__groups[0]
            limit_g1 = g1.get_limit
            sort_dir_g1 = g1.get_sort.get('dir')
            asc_g1 = True if sort_dir_g1 == cnts.ASC else False
            sort_name_g1 = g1.get_sort.get('name')
            sort_func_g1 = g1.get_sort.get('func')
            granularity_g1 = cnts.GRANULARITY_TRANSLATED.get(g1.get_granularity)
            tz_g1 = g1.get_tz

            g2 = self.__groups[1]
            limit_g2 = g2.get_limit
            sort_dir_g2 = g2.get_sort.get('dir')
            asc_g2 = True if sort_dir_g2 == cnts.ASC else False
            sort_name_g2 = g2.get_sort.get('name')
            sort_func_g2 = g2.get_sort.get('func')
            granularity_g2 = cnts.GRANULARITY_TRANSLATED.get(g2.get_granularity)
            tz_g2 = g2.get_tz

            columns = [g1.get_name, g2.get_name]

            metrics = {}
            for m in self.__metrics:
                columns.append(m.name)
                if m.name in metrics:
                    metrics[m.name].append(m.func)
                else:
                    metrics[m.name] = ['nunique'] if m.func == cnts.UNIQUE else ['size'] if m.func == cnts.COUNT else [
                        m.func]

            # Adding total count
            if g1.get_name in metrics:
                if 'size' not in metrics[g1.get_name]:
                    metrics[g1.get_name].append('size')
            else:
                metrics[g1.get_name] = ['size']

            groups_df = self.__data.loc[:, self.__data.columns.isin(columns)].reset_index(drop=True)
            groups_df['total_cf_count'] = 1  # Column to calculate the count in queries

            # Converting g1 column to the specified granularity
            if g1.get_granularity:
                convert_to_datetime_efficiently(groups_df, g1.get_name)
                if tz_g1 != 'UTC':
                    groups_df[g1.get_name] = groups_df[g1.get_name].dt.tz_convert(tz_g1)
                groups_df[g1.get_name] = groups_df[g1.get_name].dt.tz_localize(None)  # Removing time offset
                groups_df[g1.get_name] = groups_df[g1.get_name].dt.to_period(granularity_g1).dt.to_timestamp()

            # Converting g1 column to the specified granularity
            if g2.get_granularity:
                convert_to_datetime_efficiently(groups_df, g2.get_name)
                if tz_g2 != 'UTC':
                    groups_df[g2.get_name] = groups_df[g2.get_name].dt.tz_convert(tz_g2)
                groups_df[g2.get_name] = groups_df[g2.get_name].dt.tz_localize(None)  # Removing time offset
                groups_df[g2.get_name] = groups_df[g2.get_name].dt.to_period(granularity_g2).dt.to_timestamp()

            group_by_array = [g1.get_name, g2.get_name] if g1.get_name != g2.get_name else [g1.get_name]
            sub_query1 = groups_df.groupby(group_by_array, dropna=False).agg(metrics).copy().reset_index()
            sub_query1.columns = [sanitize('_'.join(filter(None, x))) for x in sub_query1.columns]
            sub_query1 = sub_query1.sort_values([f'{sanitize(sort_name_g2)}_{sort_func_g2}'], ascending=[asc_g2]).reset_index()

            agg_sub_query2 = {sort_name_g1: [sort_func_g1]}
            sub_query2 = groups_df.groupby([g1.get_name], dropna=False).agg(agg_sub_query2).copy().reset_index()
            sub_query2.columns = [sanitize('_'.join(filter(None, x))) for x in sub_query2.columns]
            sort_by = f'{sanitize(sort_name_g1)}_{sort_func_g1}'
            if sort_name_g1 == g1.get_name:
                sort_by = sanitize(sort_name_g1)
                if sort_func_g1 == 'count':
                    sort_by += '_count'
            sub_query2 = sub_query2.sort_values([sort_by], ascending=[asc_g1]).iloc[
                         :limit_g1].reset_index(drop=True)

            metrics_select = ""
            for m in self.__metrics:
                metrics_select += f"sq1.{sanitize(str(m.name))}_{m.func},\n"

            if sort_name_g1 == g1.get_name and sort_func_g1 != 'count':
                first_sort = sanitize(str(sort_name_g1))
            else:
                first_sort = f"{sanitize(str(sort_name_g1))}_{sort_func_g1}"

            if sort_name_g2 == g2.get_name and sort_func_g2 != 'count':
                second_sort = sanitize(str(sort_name_g2))
            else:
                second_sort = f"{sanitize(str(sort_name_g2))}_{sort_func_g2}"

            final_query = f"""
            SELECT * FROM (
                SELECT sq1.{sanitize(g1.get_name)},
                       sq1.{sanitize(g2.get_name)},
                       {metrics_select}
                       sq1.{sanitize(g1.get_name)}_count as count,
                       ROW_NUMBER() OVER (PARTITION BY sq1.{sanitize(g1.get_name)} ORDER BY sq1.{second_sort} {sort_dir_g2}) as rank
                FROM sub_query1 as sq1 join sub_query2 as sq2
                ON sq1.{sanitize(g1.get_name)} = sq2.{sanitize(g1.get_name)}
                ORDER BY sq2.{first_sort} {sort_dir_g1}, sq1.{second_sort} {sort_dir_g2}
            ) WHERE rank <= {limit_g2}
            """

            groups = sqldf(final_query, locals())

            response = {
                'data': [],
                "visualization": self.__visualization
            }

            for row in groups.itertuples():
                row = row._asdict()
                current_metrics = {}
                for m in self.__metrics:
                    if m.name not in current_metrics:
                        current_metrics[m.name] = {}
                    current_metrics[m.name][m.func.replace('mean', 'avg')] = round(
                        float(row[f"{sanitize(str(m.name))}_{m.func}"]), 2)

                    group1 = None if str(row[sanitize(g1.get_name)]) in ['None', 'nan'] else str(row[sanitize(g1.get_name)])
                    group2 = None if str(row[sanitize(g2.get_name)]) in ['None', 'nan'] else str(row[sanitize(g2.get_name)])

                response.get('data').append({
                    'group': [group1, group2],
                    'current': {
                        'count': int(row['count']),
                        'metrics': current_metrics
                    }
                })

            return json.dumps({'data': response})
        except Exception as e:
            raise Exception(e)

    def __process_colgroups__(self):
        row_group = self.__groups[0]
        limit_row_group = row_group.get_limit
        sort_dir_row_group = row_group.get_sort.get('dir')
        asc_row_group = True if sort_dir_row_group == cnts.ASC else False
        sort_name_row_group = row_group.get_sort.get('name')
        sort_func_row_group = row_group.get_sort.get('func')
        granularity_row_group = cnts.GRANULARITY_TRANSLATED.get(row_group.get_granularity)
        tz_row_group = row_group.get_tz

        col_group = self.__col_groups[0]
        limit_col_group = col_group.get_limit
        sort_dir_col_group = col_group.get_sort.get('dir')
        asc_col_group = True if sort_dir_col_group == cnts.ASC else False
        sort_name_col_group = col_group.get_sort.get('name')
        sort_func_col_group = col_group.get_sort.get('func')
        granularity_col_group = cnts.GRANULARITY_TRANSLATED.get(col_group.get_granularity)
        tz_col_group = col_group.get_tz

        columns = [row_group.get_name, col_group.get_name]

        metrics = {}
        metrics_sql_agg_sub2 = []
        for m in self.__metrics:
            columns.append(m.name)

            # Adding all sql codes for metrics e.g: "sum(commission) as commission_sum"
            if m.func != 'unique':
                metric_sql_agg = f'{m.func}({sanitize(str(m.name))}) AS {sanitize(str(m.name))}_{m.func}'
                if metric_sql_agg not in metrics_sql_agg_sub2:
                    metrics_sql_agg_sub2.append(metric_sql_agg)

            if m.name in metrics:
                metrics[m.name].append(m.func)
            else:
                metrics[m.name] = ['nunique'] if m.func == cnts.UNIQUE else ['size'] if m.func == cnts.COUNT else [
                    m.func]

        # Adding total count
        if row_group.get_name in metrics:
            if 'size' not in metrics[row_group.get_name]:
                metrics[row_group.get_name].append('size')
        else:
            metrics[row_group.get_name] = ['size']

        groups_df = self.__data.loc[:, self.__data.columns.isin(columns)].reset_index(drop=True)
        groups_df['total_cf_count'] = 1  # Column to calculate the count in queries

        # Converting row_group column to the specified granularity
        if row_group.get_granularity:
            convert_to_datetime_efficiently(groups_df, row_group.get_name)
            if tz_row_group != 'UTC':
                groups_df[row_group.get_name] = groups_df[row_group.get_name].dt.tz_convert(tz_row_group)
            groups_df[row_group.get_name] = groups_df[row_group.get_name].dt.tz_localize(None)  # Removing time offset
            groups_df[row_group.get_name] = groups_df[row_group.get_name].dt.to_period(granularity_row_group).dt.to_timestamp()

        # Converting col_group column to the specified granularity
        if col_group.get_granularity:
            convert_to_datetime_efficiently(groups_df, col_group.get_name)
            if tz_col_group != 'UTC':
                groups_df[col_group.get_name] = groups_df[col_group.get_name].dt.tz_convert(tz_col_group)
            groups_df[col_group.get_name] = groups_df[col_group.get_name].dt.tz_localize(None)  # Removing time offset
            groups_df[col_group.get_name] = groups_df[col_group.get_name].dt.to_period(granularity_col_group).dt.to_timestamp()

        row_group_query = groups_df.groupby([row_group.get_name], dropna=False).agg(metrics).copy().reset_index()
        row_group_query.columns = [sanitize('_'.join(filter(None, x))) for x in row_group_query.columns]
        row_group_sort_by = f'{sanitize(sort_name_row_group)}_{sort_func_row_group}'
        if sort_name_row_group == row_group.get_name:
            row_group_sort_by = sanitize(sort_name_row_group)
            if sort_func_row_group == 'count':
                row_group_sort_by += '_count'
        row_group_query = row_group_query.sort_values([row_group_sort_by], ascending=[asc_row_group]).iloc[:limit_row_group].reset_index(drop=True).reset_index()

        col_group_query = groups_df.groupby([col_group.get_name], dropna=False).agg(metrics).copy().reset_index()
        col_group_query.columns = [sanitize('_'.join(filter(None, x))) for x in col_group_query.columns]
        col_group_sort_by = f'{sanitize(sort_name_col_group)}_{sort_func_col_group}'
        if sort_name_col_group == col_group.get_name:
            col_group_sort_by = sanitize(sort_name_col_group)
            if sort_func_col_group == 'count':
                col_group_sort_by += '_count'
        col_group_query = col_group_query.sort_values([col_group_sort_by], ascending=[asc_col_group]).iloc[:limit_col_group].reset_index(drop=True).reset_index()

        groups_df.columns = [sanitize(x) for x in groups_df.columns]

        final_metrics_select = []
        cross_row_metrics_select = []
        for m in self.__metrics:
            if m.func != 'unique':
                final_metric_select = f"_sub2.{sanitize(str(m.name))}_{m.func}"
                cross_metric_select = f"_main.{sanitize(str(m.name))}_{m.func}"

                if final_metric_select not in final_metrics_select:
                    final_metrics_select.append(final_metric_select)
                if cross_metric_select not in cross_row_metrics_select:
                    cross_row_metrics_select.append(cross_metric_select)

        final_query = f"""
        SELECT _sub1.{row_group.get_name}, _sub1.{col_group.get_name}, {', '.join(final_metrics_select)}, count
        FROM
        (
            SELECT _crossRow.{row_group.get_name}, _crossCol.{col_group.get_name}, _crossRow.{row_group_sort_by}, rank
            FROM (
                SELECT _main.{row_group.get_name}, {', '.join(cross_row_metrics_select)}
                    FROM row_group_query _main
                ) _crossRow
               CROSS JOIN (
                    SELECT *, ROW_NUMBER() OVER(ORDER BY {col_group_sort_by} {sort_dir_col_group}) AS rank
                    FROM col_group_query
                    ORDER BY rank ASC
               ) _crossCol
            GROUP BY _crossRow.{row_group.get_name}, _crossCol.{col_group.get_name}, _crossRow.{row_group_sort_by}, rank
        ) _sub1
        LEFT JOIN
        (
            SELECT _main.{row_group.get_name}, _main.{col_group.get_name}, _colGroupSub.rank, {', '.join(cross_row_metrics_select)}, count
            FROM
            (
                SELECT *, ROW_NUMBER() OVER(ORDER BY {col_group_sort_by} {sort_dir_col_group}) AS rank
                FROM col_group_query
            ) _colGroupSub
            LEFT JOIN
            (
                SELECT _main.{row_group.get_name}, _main.{col_group.get_name}, {', '.join(metrics_sql_agg_sub2)}, COUNT(*) AS count
                FROM groups_df as _main
                GROUP BY _main.{row_group.get_name}, _main.{col_group.get_name}
            ) _main
            on _colGroupSub.{col_group.get_name} = _main.{col_group.get_name}
            GROUP BY _main.{row_group.get_name}, _main.{col_group.get_name}, _colGroupSub.rank, {', '.join(cross_row_metrics_select)}, count
        ) _sub2
        ON coalesce(_sub1.{row_group.get_name}, '&&null&&') = coalesce(_sub2.{row_group.get_name}, '&&null&&') and
        coalesce(_sub1.{col_group.get_name}, '&&null&&') = coalesce(_sub2.{col_group.get_name}, '&&null&&')
        ORDER BY _sub1.{row_group_sort_by} {sort_dir_row_group}, _sub1.rank ASC
        """

        groups = sqldf(final_query, locals())

        response = {
            'data': [],
            "visualization": self.__visualization
        }

        for row in groups.itertuples():
            row = row._asdict()
            current_metrics = {}
            for m in self.__metrics:
                if m.func != 'unique':
                    if m.name not in current_metrics:
                        current_metrics[m.name] = {}
                    if math.isnan(row[f"{sanitize(str(m.name))}_{m.func}"]):
                        current_metrics[m.name][m.func.replace('mean', 'avg')] = None
                    else:
                        current_metrics[m.name][m.func.replace('mean', 'avg')] = round(
                            float(row[f"{sanitize(str(m.name))}_{m.func}"]), 2)

                group1 = None if str(row[sanitize(row_group.get_name)]) in ['None', 'nan'] else str(row[sanitize(row_group.get_name)])
                group2 = None if str(row[sanitize(col_group.get_name)]) in ['None', 'nan'] else str(row[sanitize(col_group.get_name)])

            response.get('data').append({
                'group': [group1, group2],
                'current': {
                    'count': None if math.isnan(row['count']) else int(row['count']),
                    'metrics': current_metrics
                }
            })

        return json.dumps({'data': response})

    def __process_boxplot__(self):
        try:
            if len(self.__metrics) > 0:
                m = self.__metrics[0]
                merge = None
                response_name = 'default'
                response = {
                    'data': [],
                    "visualization": self.__visualization
                }

                if len(self.__groups) > 0:
                    g = self.__groups[0]
                    response_name = g.get_name
                    limit = g.get_limit
                    asc = True if g.get_sort.get('dir') == cnts.ASC else False

                    group1 = self.__data.groupby([g.get_name]).agg({m.name: [quantile_0]}).reset_index()
                    group1.columns = [sanitize('_'.join(filter(None, x))) for x in group1.columns]

                    group2 = self.__data.groupby([g.get_name]).agg({m.name: [quantile_25]}).reset_index()
                    group2.columns = [sanitize('_'.join(filter(None, x))) for x in group2.columns]

                    group3 = self.__data.groupby([g.get_name]).agg({m.name: [quantile_50]}).reset_index()
                    group3.columns = [sanitize('_'.join(filter(None, x))) for x in group3.columns]

                    group4 = self.__data.groupby([g.get_name]).agg({m.name: [quantile_75]}).reset_index()
                    group4.columns = [sanitize('_'.join(filter(None, x))) for x in group4.columns]

                    group5 = self.__data.groupby([g.get_name]).agg({m.name: [quantile_100]}).reset_index()
                    group5.columns = [sanitize('_'.join(filter(None, x))) for x in group5.columns]

                    merge = pd.merge(group1, group2, on=sanitize(g.get_name))
                    merge = pd.merge(merge, group3, on=sanitize(g.get_name))
                    merge = pd.merge(merge, group4, on=sanitize(g.get_name))
                    merge = pd.merge(merge, group5, on=sanitize(g.get_name))
                    merge = merge.sort_values([sanitize(g.get_name)], ascending=[asc]).iloc[:limit].reset_index(drop=True)

                    for row in merge.itertuples():
                        row = row._asdict()
                        current_metrics = {}
                        for met in self.__metrics:
                            if met.name == m.name:
                                if met.name not in current_metrics:
                                    current_metrics[met.name] = {}

                                q_0 = round(float(row[f'{sanitize(m.name)}_quantile_0']), 2)
                                q_25 = round(float(row[f'{sanitize(m.name)}_quantile_25']), 2)
                                q_50 = round(float(row[f'{sanitize(m.name)}_quantile_50']), 2)
                                q_75 = round(float(row[f'{sanitize(m.name)}_quantile_75']), 2)
                                q_100 = round(float(row[f'{sanitize(m.name)}_quantile_100']), 2)

                                current_metrics[met.name]['percentile0'] = q_0 if not np.isnan(q_0) else None
                                current_metrics[met.name]['percentile25'] = q_25 if not np.isnan(q_25) else None
                                current_metrics[met.name]['percentile50'] = q_50 if not np.isnan(q_50) else None
                                current_metrics[met.name]['percentile75'] = q_75 if not np.isnan(q_75) else None
                                current_metrics[met.name]['percentile100'] = q_100 if not np.isnan(q_100) else None

                        response.get('data').append({
                            'group': [str(row[sanitize(response_name)])],
                            'current': {
                                'metrics': current_metrics
                            }
                        })
                    return json.dumps({'data': response})
                else:
                    group1 = self.__data.agg({m.name: [quantile_0]}).reset_index()
                    group1.columns = [sanitize('_'.join(filter(None, x))) for x in group1.columns]

                    group2 = self.__data.agg({m.name: [quantile_25]}).reset_index()
                    group2.columns = [sanitize('_'.join(filter(None, x))) for x in group2.columns]

                    group3 = self.__data.agg({m.name: [quantile_50]}).reset_index()
                    group3.columns = [sanitize('_'.join(filter(None, x))) for x in group3.columns]

                    group4 = self.__data.agg({m.name: [quantile_75]}).reset_index()
                    group4.columns = [sanitize('_'.join(filter(None, x))) for x in group4.columns]

                    group5 = self.__data.agg({m.name: [quantile_100]}).reset_index()
                    group5.columns = [sanitize('_'.join(filter(None, x))) for x in group5.columns]

                    q_0 = round(float(group1.get(sanitize('_'.join(filter(None, m.name))))[0]), 2)
                    q_25 = round(float(group2.get(sanitize('_'.join(filter(None, m.name))))[0]), 2)
                    q_50 = round(float(group3.get(sanitize('_'.join(filter(None, m.name))))[0]), 2)
                    q_75 = round(float(group4.get(sanitize('_'.join(filter(None, m.name))))[0]), 2)
                    q_100 = round(float(group5.get(sanitize('_'.join(filter(None, m.name))))[0]), 2)

                    current_metrics = {}
                    current_metrics[m.name] = {}

                    current_metrics[m.name]['percentile0'] = q_0 if not np.isnan(q_0) else None
                    current_metrics[m.name]['percentile25'] = q_25 if not np.isnan(q_25) else None
                    current_metrics[m.name]['percentile50'] = q_50 if not np.isnan(q_50) else None
                    current_metrics[m.name]['percentile75'] = q_75 if not np.isnan(q_75) else None
                    current_metrics[m.name]['percentile100'] = q_100 if not np.isnan(q_100) else None

                    response.get('data').append({
                        'group': [m.name],
                        'current': {
                            'metrics': current_metrics
                        }
                    })
                    return json.dumps({'data': response})
            else:
                raise Exception('Provide a metric to be able to run the boxplot query.')
        except Exception as e:
            raise Exception(e)

    def __process_time_range__(self):
        try:
            if len(self.__groups) > 0:
                g = self.__groups[0]
                if self.__is_date_field__(g.get_name):
                    granularity = cnts.GRANULARITY_TRANSLATED.get(g.get_granularity)
                    tz = g.get_tz

                    # Taking only the column that will be used
                    df = self.__data.loc[:, self.__data.columns == g.get_name].reset_index(drop=True)
                    if self.get_original_type(g.get_name) == 'date':
                        convert_to_datetime_efficiently(df, g.get_name)

                    dt_min = df[g.get_name].min()
                    dt_max = df[g.get_name].max()

                    if tz != 'UTC':
                        if dt_min.tzinfo is None:
                            dt_min = dt_min.tz_localize('UTC').tz_convert(tz)
                            dt_max = dt_max.tz_localize('UTC').tz_convert(tz)
                        else:
                            dt_min = dt_min.tz_convert(tz)
                            dt_max = dt_max.tz_convert(tz)

                    dt_min = dt_min.to_period(granularity).to_timestamp()
                    dt_max = dt_max.to_period(granularity).to_timestamp()

                    response = {
                        "data": [
                            {
                                "min": str(dt_min),
                                "max": str(dt_max)
                            }
                        ],
                        "visualization": self.__visualization
                    }

                    return json.dumps({'data': response})
                else:
                    raise Exception(
                        'Provide a time field in the first group definition to be able to run the Time Range query.')
            else:
                raise Exception('Provide a group to be able to run the Time Range query.')
        except Exception as e:
            raise Exception(e)

    def __process_histogram__(self):
        try:
            if len(self.__metrics) > 0:
                m = self.__metrics[0]

                # Getting only the metric column
                metric_df = self.__data.loc[:, self.__data.columns.isin([m.name])].reset_index(drop=True)
                metric_df['total_cf_count'] = 1  # Column to calculate the count in queries
                # metric_df = metric_df.dropna(how='all')

                # Calculating interval if None
                is_calculated_interval = False
                if m.get_interval is None:
                    min_val = float(metric_df[m.name].min())
                    max_val = float(metric_df[m.name].max())
                    fb = m.get_fixed_bars
                    interval_per_bars = (max_val - min_val) / (fb + 1)
                    if interval_per_bars == 0:
                        m.interval(1)
                    else:
                        m.interval(interval_per_bars)
                    is_calculated_interval = True

                # Do not apply offset if metric interval was calculated
                if is_calculated_interval:
                    m.offset(0)

                offset = m.get_offset
                interval = m.get_interval

                # Adding the groups intervals into the group column
                metric_df['group'] = np.floor((metric_df[m.name] - offset) / interval) * interval + offset
                group = metric_df.groupby('group', dropna=False).agg({m.name: ['size']}).reset_index()
                group.columns = [sanitize('_'.join(filter(None, x))) for x in group.columns]
                if self.__limit > 0:
                    limited_group = group.iloc[:self.__limit]
                else:
                    limited_group = group.iloc[:100]

                response = {
                    'data': [],
                    "visualization": self.__visualization
                }

                for row in limited_group.itertuples():
                    row = row._asdict()
                    index = row['Index']
                    g1 = row['group']
                    if index + 1 in group.index:
                        g2 = group.iloc[[index + 1]]['group'].values[0]
                    else:
                        g2 = g1 + m.get_interval

                    g1 = float(g1) if str(g1) != 'nan' else None
                    g2 = float(g2) if str(g2) != 'nan' else None

                    if g1 is not None and g2 is None:
                        g2 = g1 + m.get_interval

                    if g1 is None and g2 is None:
                        response.get('data').insert(0, {
                            'group': [[g1, g2]],
                            'current': {
                                'count': round(float(row[f"{sanitize(m.name)}_count"]), 2)
                            }
                        })
                    else:
                        response.get('data').append({
                            'group': [[g1, g2]],
                            'current': {
                                'count': round(float(row[f"{sanitize(m.name)}_count"]), 2)
                            }
                        })

                return json.dumps({'data': response})

            else:
                raise Exception('Provide a metric to be able to run the Histogram query.')
        except Exception as e:
            raise Exception(e)

    def __process_pivot__(self):
        try:
            if self.__visualization == 'Pivot Table':
                self.__original_metrics = list(filter(lambda m: m.name != 'total_cf_count', self.__original_metrics))
                columns = []
                r = []
                c = []
                v = []
                agg = {}
                [r.append(row.name) for row in self.__rows]
                [c.append(col.name) for col in self.__columns]
                [v.append(met.name) for met in self.__original_metrics]

                # Removing duplicates
                r = list(dict.fromkeys(r))
                c = list(dict.fromkeys(c))
                v = list(dict.fromkeys(v))
                if 'total_cf_count' not in v:
                    v.append('total_cf_count')

                for m in self.__original_metrics:
                    agg[m.name] = unique if m.func == cnts.UNIQUE else m.func

                agg['total_cf_count'] = count

                columns.extend(r)
                columns.extend(c)
                columns.extend(v)
                # Taking only the columns that will be used
                group_df = self.__data.loc[:, self.__data.columns.isin(columns)].reset_index(drop=True)
                group_df['total_cf_count'] = 1  # Column to calculate the count in queries

                for x in self.__rows:
                    if x.get_func and self.__is_date_field__(x.name):
                        granularity = cnts.GRANULARITY_TRANSLATED.get(x.get_func)
                        convert_to_datetime_efficiently(group_df, x.name)
                        if self.__time_zone != 'UTC':
                            group_df[x.name] = group_df[x.name].dt.tz_convert(self.__time_zone)
                        group_df[x.name] = group_df[x.name].dt.tz_localize(None)  # Removing time offset
                        group_df[x.name] = group_df[x.name].dt.to_period(granularity).dt.to_timestamp()

                group_df[r] = group_df[r].fillna('None')
                pivot = pd.pivot_table(group_df, values=v, index=r, columns=c, aggfunc=agg,
                                       fill_value=0, margins=True, margins_name='$total')
                pivot.columns = transform_columns(pivot.columns)

                response = {
                    'data': [],
                    "visualization": self.__visualization
                }

                col_count = len(self.__columns)

                # Adding group's values
                if col_count > 0:
                    column_groups = get_pivot_columns(pivot)

                    for c in column_groups:
                        for index, row in pivot.iterrows():
                            group = []

                            if isinstance(index, tuple):
                                group.extend(index)
                                group = list(map(lambda el: str(el), group))
                            else:
                                group.append(str(index))

                            group.extend(c)

                            if group[0] != "$total":  # $total belongs to the last row, will be processed bellow
                                metrics = {}
                                for m in self.__original_metrics:
                                    column_name = m.name + '::' + '::'.join(c)
                                    cell_value = float(row[column_name])
                                    if cell_value > 0:
                                        metrics[m.name] = {}
                                        metrics[m.name][m.func.replace('mean', 'avg')] = float(row[column_name])
                                if bool(metrics):
                                    group = list(map(lambda g: get_group_value(g), group))
                                    response.get('data').append({
                                        'group': copy.deepcopy(group),
                                        'current': {
                                            'count': int(row['total_cf_count::$total']),
                                            'metrics': copy.deepcopy(metrics)
                                        }
                                    })

                # Adding group's totals
                for index, row in pivot.iterrows():
                    group = []

                    if isinstance(index, tuple):
                        group.extend(index)
                        group = list(map(lambda el: str(el), group))
                    else:
                        group.append(str(index))

                    if group[0] != "$total":
                        # Append $total to group only if columns were set
                        if col_count > 0: group.append('$total')

                        metrics = {}
                        for m in self.__original_metrics:
                            metrics[m.name] = {}
                            column_name = f'{m.name}::$total' if col_count > 0 else m.name
                            metrics[m.name][m.func.replace('mean', 'avg')] = float(row[column_name])

                        size = int(row['total_cf_count::$total']) if col_count > 0 else int(row['total_cf_count'])
                        group = list(map(lambda g: get_group_value(g), group))
                        response.get('data').append({
                            'group': group,
                            'current': {
                                'count': size,
                                'metrics': metrics
                            }
                        })
                    else:
                        if col_count > 0:
                            column_groups = get_pivot_columns(pivot)
                            for c in column_groups:
                                group.clear()
                                group.extend(c)
                                metrics = {}
                                for m in self.__original_metrics:
                                    column_name = m.name + '::' + '::'.join(c)
                                    metrics[m.name] = {}
                                    metrics[m.name][m.func.replace('mean', 'avg')] = float(row[column_name])

                                group.append('$columnTotal')
                                group = list(map(lambda g: get_group_value(g), group))
                                response.get('data').append({
                                    'group': copy.deepcopy(group),
                                    'current': {
                                        'count': int(row[f"total_cf_count::{'::'.join(c)}"]),
                                        'metrics': copy.deepcopy(metrics)
                                    }
                                })

                            # Adding the absolute total just once
                            absolute_total_metrics = {}
                            for m in self.__original_metrics:
                                absolute_total_metrics[m.name] = {}
                                absolute_total_metrics[m.name][m.func.replace('mean', 'avg')] = float(
                                    row[f'{m.name}::$total'])
                            response.get('data').append({
                                'group': ["$absoluteTotal"],
                                'current': {
                                    'count': int(row['total_cf_count::$total']),
                                    'metrics': absolute_total_metrics
                                }
                            })
                        else:
                            metrics = {}
                            for m in self.__original_metrics:
                                column_name = m.name
                                cell_value = float(row[column_name])
                                if cell_value > 0:
                                    metrics[m.name] = {}
                                    metrics[m.name][m.func.replace('mean', 'avg')] = float(row[column_name])

                            response.get('data').append({
                                'group': ["$columnTotal"],
                                'current': {
                                    'count': int(row['total_cf_count']),
                                    'metrics': metrics
                                }
                            })
                            response.get('data').append({
                                'group': ["$absoluteTotal"],
                                'current': {
                                    'count': int(row['total_cf_count']),
                                    'metrics': metrics
                                }
                            })

                return json.dumps({'data': response})
            else:
                r = []
                [r.append(row.name) for row in self.__rows]

                self.__metrics = list(filter(lambda m: m.name != 'total_cf_count', self.__metrics))

                columns = copy.deepcopy(r)
                metrics = {}
                for m in self.__metrics:
                    columns.append(m.name)
                    if m.name in metrics:
                        metrics[m.name].append(m.func)
                    else:
                        metrics[m.name] = ['nunique'] if m.func == cnts.UNIQUE else ['size'] if m.func == cnts.COUNT else [
                            m.func]

                # Adding total count
                if r[0] in metrics:
                    if 'size' not in metrics[r[0]]:
                        metrics[r[0]].append('size')
                else:
                    metrics[r[0]] = ['size']

                # Taking only the columns that will be used
                group_df = self.__data.loc[:, self.__data.columns.isin(columns)].reset_index(drop=True)
                group_df['total_cf_count'] = 1  # Column to calculate the count in queries

                for row in self.__rows:
                    if self.__is_date_field__(row.name) and row.get_func is not None:
                        granularity = cnts.GRANULARITY_TRANSLATED.get(row.get_func)
                        convert_to_datetime_efficiently(group_df, row.name)
                        if self.__time_zone != 'UTC':
                            group_df[row.name] = group_df[row.name].dt.tz_convert(self.__time_zone)
                        group_df[row.name] = group_df[row.name].dt.tz_localize(None)  # Removing time offset
                        group_df[row.name] = group_df[row.name].dt.to_period(granularity).dt.to_timestamp()

                group = group_df.groupby(r, dropna=False).agg(metrics)
                if self.__limit > 0:
                    group = group.iloc[:self.__limit]
                else:
                    group = group.iloc[:100]

                group.columns = [sanitize('_'.join(filter(None, x))) for x in group.columns]

                response = {
                    'data': [],
                    "visualization": self.__visualization
                }

                for index, row in group.iterrows():
                    current_metrics = {}
                    for m in self.__metrics:
                        if m.name not in current_metrics:
                            current_metrics[m.name] = {}
                        current_metrics[m.name][m.func.replace('mean', 'avg')] = float(
                            round(row[f'{m.name}_{m.func}'], 2))

                    group_list = list(map(lambda el: str(el), list(index))) if isinstance(index, tuple) else [
                        str(index)]
                    group_list = list(map(lambda g: get_group_value(g), group_list))
                    response.get('data').append({
                        'group': group_list,
                        'current': {
                            'count': int(row[f'{r[0]}_count']),
                            'metrics': current_metrics
                        }
                    })

                return json.dumps({'data': response})

        except Exception as e:
            raise Exception(e)

    def __add_geohash_column__(self, locations):
        try:
            geo_hash_array = []
            for location in locations:
                if isinstance(location, list) or isinstance(location, tuple):
                    lat = float(location[0])
                    lon = float(location[1])
                else:
                    raise Exception()

                if isinstance(lat, float) and isinstance(lon, float):
                    geo_hash_array.append(pgh.encode(lat, lon, precision=self.__precision))
            return np.append([], geo_hash_array)
        except Exception:
            raise Exception("The location field specified must satisfy the following criteria: array -> [lat, lon] or "
                            "tuple -> (lat, lon)")

    def __process_geo_cluster__(self):
        try:
            if isinstance(self.__precision, int):
                if isinstance(self.__location, str):
                    agg = {}
                    columns = [self.__location]
                    for m in self.__original_metrics:
                        columns.append(m.name)
                        agg[m.name] = ['nunique'] if m.func == cnts.UNIQUE else ['size'] if m.func == cnts.COUNT else [
                            m.func]

                    # Taking only the columns that will be used
                    geo_df = self.__data.loc[:, self.__data.columns.isin(columns)].reset_index(drop=True)
                    geo_df['total_cf_count'] = 1  # Column to calculate the count in queries

                    geo_df[self.__location] = geo_df[self.__location].transform(tuple)
                    unique_locations = geo_df[self.__location].unique()
                    m = dict(zip(unique_locations, self.__add_geohash_column__(unique_locations)))
                    geo_df['$geohash'] = geo_df[self.__location].map(m)

                    # Adding total count
                    agg['$geohash'] = ['size']

                    group = geo_df.groupby('$geohash', dropna=False).agg(agg)
                    group.columns = transform_columns(group.columns)
                    group = group.sort_values(['$geohash::count'], ascending=[False])

                    response = {
                        'data': [],
                        "visualization": self.__visualization
                    }

                    for index, row in group.iterrows():
                        new_response = {
                            'geohash': index,
                            'count': int(row['$geohash::count'])
                        }

                        for m in self.__original_metrics:
                            column_name = f"{m.name}::{m.func}"
                            new_response[m.name + '+' + m.func.replace('mean', 'avg')] = float(row[column_name])

                        response.get('data').append(new_response)

                    return json.dumps({'data': response})
                else:
                    raise Exception('To execute geo cluster query the location must be a string value.')
            else:
                raise Exception('To execute geo cluster query the precision must be an integer value.')
        except Exception as e:
            raise Exception(e)

    def __process_multi_groups__(self):
        try:
            group_by = []
            if len(self.__groups) > 0:
                [group_by.append(x.get_name) for x in self.__groups]
            else:
                group_by.append('total_cf_count')

            columns = copy.deepcopy(group_by)
            metrics = {}
            for m in self.__original_metrics:
                columns.append(m.name)
                if m.name in metrics:
                    metrics[m.name].append(m.func)
                else:
                    metrics[m.name] = ['nunique'] if m.func == cnts.UNIQUE else [m.func]

            # Adding total count
            metrics['total_cf_count'] = ['size']

            groups_df = self.__data.loc[:, self.__data.columns.isin(columns)].reset_index(drop=True)
            groups_df['total_cf_count'] = 1  # Column to calculate the count in queries

            for g in self.__groups:
                if g.get_granularity and self.__is_date_field__(g.get_name):
                    granularity = cnts.GRANULARITY_TRANSLATED.get(g.get_granularity)
                    convert_to_datetime_efficiently(groups_df, g.get_name)
                    if self.__time_zone != 'UTC':
                        groups_df[g.get_name] = groups_df[g.get_name].dt.tz_convert(self.__time_zone)
                    groups_df[g.get_name] = groups_df[g.get_name].dt.tz_localize(None)  # Removing time offset
                    groups_df[g.get_name] = groups_df[g.get_name].dt.to_period(granularity).dt.to_timestamp()

            groups_df[group_by] = groups_df[group_by].where(groups_df[group_by].notnull(), None)
            groups = groups_df.groupby(group_by, dropna=False).agg(metrics)
            groups.columns = transform_columns(groups.columns)  # Renaming columns

            if self.__visualization != 'Pivot Table':
                if self.__limit > 0:
                    groups = groups.iloc[:self.__limit]

            response = {
                'data': [],
                "visualization": self.__visualization
            }

            for index, row in groups.iterrows():
                group = []

                if groups.index.name != 'total_cf_count':
                    if isinstance(index, tuple):
                        group.extend(index)
                        group = list(map(lambda el: str(el), group))
                    else:
                        group.append(str(index))

                group = list(map(lambda g: get_group_value(g), group))

                metrics = {}
                self.__original_metrics = list(filter(lambda m: m.name != 'total_cf_count', self.__original_metrics))
                for m in self.__original_metrics:
                    column_name = m.name + '::' + m.func
                    cell_value = float(row[column_name])
                    if cell_value > 0:
                        metrics[m.name] = {}
                        metrics[m.name][m.func.replace('mean', 'avg')] = float(row[column_name])

                response.get('data').append({
                    'group': copy.deepcopy(group),
                    'current': {
                        'count': int(row['total_cf_count::count']),
                        'metrics': copy.deepcopy(metrics)
                    }
                })

            return json.dumps({'data': response})

        except Exception as e:
            raise Exception(e)

    def visualize(self):
        try:
            if not self.__error:
                response = {"data": [], "visualization": self.__visualization}
                size = len(self.__data.index)
                if size > 0:
                    if self.__is_type__('boxplot'):
                        return self.__process_boxplot__()
                    elif self.__is_type__('time_range'):
                        return self.__process_time_range__()
                    elif self.__is_type__('histogram'):
                        return self.__process_histogram__()
                    elif self.__is_type__('benchmark'):
                        return self.__process_multi_groups__()
                    elif self.__is_type__('geo_clusters'):
                        return self.__process_geo_cluster__()
                    elif self.__is_type__('pivot'):
                        return self.__process_pivot__()
                    elif self.__is_type__('raw_query'):
                        return json.dumps({'data': response})
                    elif self.__is_type__('colgroups'):
                        return self.__process_colgroups__()
                    elif len(self.__groups) == 0 and len(self.__metrics) > 0:
                        return self.__process_metrics_totals__()
                    elif len(self.__groups) == 1:
                        return self.__process_single_group__()
                    elif len(self.__groups) == 2:
                        return self.__process_two_groups__()
                    else:
                        return json.dumps({'data': response})
                else:
                    return json.dumps({'data': response})
            else:
                print(
                    f'{Style.BRIGHT}{Fore.RED}Either the dataframe or the json config is invalid. '
                    f'The visualize query can not be performed.{Style.RESET_ALL}')
        except Exception as e:
            print(f'{Style.BRIGHT}{Fore.RED}{e}{Style.RESET_ALL}')

    # endregion

    def get_data_source(self, df_name):
        try:
            metadata_info = {
                "id": df_name,
                "name": df_name,
                "reference": df_name,
                "objectFields": [],
                "providerType": "pandas-dataframe"
            }
            object_fields = []
            columns = self.__data.columns

            for column in columns:
                dtype = self.__data.dtypes[column]
                sample = self.__data[column].iloc[:1000]
                try:
                    original_type = dtype.name if dtype.name != 'object' else types.infer_dtype(sample)
                except TypeError as e:
                    original_type = 'unknown'

                current_type = "ATTRIBUTE"

                if original_type == 'date':
                    current_type = "TIME"
                elif original_type in ['timedelta64', 'timedelta', 'time'] or \
                        types.is_timedelta64_dtype(dtype) or \
                        types.is_timedelta64_ns_dtype(dtype):
                    current_type = "ATTRIBUTE"
                elif original_type == 'datetime' or types.is_datetime64_any_dtype(dtype):
                    current_type = "TIME"
                    original_type = 'datetime'
                elif types.is_numeric_dtype(dtype):
                    if types.is_integer_dtype(dtype):
                        current_type = "INTEGER"
                    elif types.is_float_dtype(dtype):
                        current_type = "NUMBER"

                new_object = {
                    "name": column,
                    "label": column,
                    "type": current_type,
                    "originName": column,
                    "originalType": original_type
                }

                if current_type in ["INTEGER", "NUMBER"]:
                    new_object["func"] = "SUM"
                elif current_type == "TIME":
                    new_object["timestampGranularity"] = "YEAR"

                object_fields.append(new_object)

            metadata_info["objectFields"] = object_fields
            return json.dumps(metadata_info)
        except Exception as e:
            raise Exception(e)

    # region Standalone app definitions
    def filters(self, args):
        for f in args:
            if not isinstance(f, Filter):
                print('filters function parameters must be an instance of a Filter object')
                self.__error = True
                return self
            self.__filters.append(f)
        self.__error = False
        return self

    def filter(self, filter_obj):
        if not isinstance(filter_obj, Filter):
            print('filter function parameter must be an instance of a Filter object')
            self.__error = True
            return self
        self.__filters.append(filter_obj)
        self.__error = False
        return self

    def clientFilters(self, args):
        for f in args:
            if not isinstance(f, Filter):
                print('clientFilters function parameters must be an instance of a Filter object')
                self.__error = True
                return self
            self.__client_filters.append(f)
        self.__error = False
        return self

    def clientFilter(self, filter_obj):
        if not isinstance(filter_obj, Filter):
            print('clientFilter function parameter must be an instance of a Filter object')
            self.__error = True
            return self
        self.__client_filters.append(filter_obj)
        self.__error = False
        return self

    def staticFilters(self, args):
        for f in args:
            if not isinstance(f, Filter):
                print('staticFilters function parameters must be an instance of a Filter object')
                self.__error = True
                return self
            self.__static_filters.append(f)
        self.__error = False
        return self

    def metrics(self, args):
        for m in args:
            if isinstance(m, Metric):
                self.__metrics.append(m)
            elif isinstance(m, CompareMetric):
                self.__comparative_metrics.append(m)
            else:
                print('metrics function parameters must be an instance of a Metric or CompareMetric objects')
                self.__error = True
                return self
        self.__error = False
        return self

    def groupby(self, args):
        for g in args:
            if not isinstance(g, Attribute):
                print('groupby function parameters must be an instance of a Attribute object')
                self.__error = True
                return self
            self.__groups.append(g)
        self.__error = False
        return self

    def colgroupby(self, args):
        for g in args:
            if not isinstance(g, Attribute):
                print('colgroupby function parameters must be an instance of a Attribute object')
                self.__error = True
                return self
            self.__col_groups.append(g)
        self.__error = False
        return self

    def rows(self, args):
        for r in args:
            if isinstance(r, Row):
                self.__rows.append(r)
            elif isinstance(r, str):
                self.__rows.append(Row(r))
            else:
                print('rows function parameters must be an instance of a Row or String object')
                self.__error = True
                return self
        self.__error = False
        return self

    def columns(self, args):
        for c in args:
            if isinstance(c, Column):
                self.__columns.append(c)
            elif isinstance(c, str):
                self.__columns.append(Column(c))
            else:
                print('columns function parameters must be an instance of a Column or String object')
                self.__error = True
                return self
        self.__error = False
        return self

    def fields(self, args):
        for f in args:
            if isinstance(f, Field):
                self.__fields.append(f)
            elif isinstance(f, str):
                self.__fields.append(Field(f))
            else:
                print('fields function parameters must be an instance of a Field or String object')
                self.__error = True
                return self
        self.__error = False
        return self

    def exclude(self, args):
        for f in args:
            if not isinstance(f, str):
                print('exclude function parameters must be a string object')
                self.__error = True
                return self
            self.__exclude.append(f)
        self.__error = False
        return self

    def limit(self, limit):
        self.__limit = limit
        self.__error = False
        return self

    def location(self, location_field):
        self.__location = location_field
        self.__error = False
        return self

    def precision(self, precision):
        self.__precision = precision
        self.__error = False
        return self

    def timeField(self, time_field):
        if not isinstance(time_field, Attribute):
            print('timeField function parameter must be an instance of a Attribute object')
            self.__error = True
            return self
        self.__time_field = time_field
        self.__error = False
        return self

    def onlyWithFilters(self, obj):
        self.__only_with_filters = obj
        self.__error = False
        return self

    # endregion
