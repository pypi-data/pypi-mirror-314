import json
import re
from .legend import Legend
from .grid import Grid
from .markline import MarkLine
from .color import Color
from random import randint

eol = '\n'
tab = '\t'
COMMENT_GROUPS = '// Define attributes to group by'
COMMENT_TIME = '// Define the time field to be used'
COMMENT_METRICS = '// Define metrics'
COMMENT_FILTERS = '// Define filters'
COMMENT_DATA = '// Add metrics and groups to data source'
COMMENT_CHART = '// --- Define chart options and static filters ---'
COMMENT_LEGEND = '// Define Legend'
COMMENT_GRID = '// Define Grid'
COMMENT_COLOR = '// Define Color Palette'
COMMENT_MARKLINE = '// Define MarkLine'
LEGEND_EXCLUDED_CHARTS = ['Disk', 'Box Plot', 'Sankey']
ZOOM_SUPPORT_LIST = ['Trend', 'Area Line', 'Bars', 'Multimetric Bars', 'Multimetric Trend', 'Multimetric Area Line', 'Stacked Bars', 'Clustered Bars']

class CodeGenerator(object):

    def __init__(self, cf):
        self.__cf = cf
        self.__current_filter_number = 0
        self.__current_group_number = 0

    def __get_header_code(self):
        declaration_code = '/* Configuration code for this widget */' + eol
        declaration_code += 'let provider = cf.provider("Aktiun Pandas");' + eol
        declaration_code += 'let source = provider.source("' + self.__cf.get_source + '");' + eol

        return declaration_code

    def get_time_fields(self, prov):
        metadata = json.loads(prov.get_data_source('name'))
        object_fields = metadata.get('objectFields')
        if object_fields:
            return [f for f in object_fields if f.get('type') == 'TIME']
        else:
            return []

    def get_integer_metrics(self, prov, metrics):
        integer_metrics = []
        for m in metrics:
            if prov.is_field_type(m.name, 'INTEGER'):
                integer_metrics.append(m)
        return integer_metrics

    def can_generate_code(self, chart):
        prov = self.__cf.get_provider
        attrs = prov.get_groups
        metrics = prov.get_metrics
        times = self.get_time_fields(prov)
        integer_metrics = self.get_integer_metrics(prov, metrics)

        if chart in ['Bars', 'Pie', 'Donut', 'Disk', 'Raw Data Table', 'Data List']:
            return True
        elif chart in ['Pivot Table','Geo Map','Vector Map','KPI','Histogram','Word Cloud','Packed Bubbles','Gauge','Tree Map','Floating Bubbles','Group Legend','Slicer','Dropdown']:
            return len(attrs) > 0
        elif chart == 'Text Search':
            return False # Only elasticsearch
        elif chart in ['Tree Map 2D','Nested Pie','Stacked Bars','Heat Map','Sunburst','Tree', 'Sankey']:
            return len(attrs) > 1
        elif chart in ['Time Range Filter', 'Time Range Picker', 'Time Slider']:
            return len(times) > 0 and len(attrs) > 0
        elif chart == 'Box Plot':
            return (len(times) > 0 or len(integer_metrics) > 0 or len(attrs) > 0) and len([m for m in prov.get_metrics if m.name != 'count']) > 0
        elif chart == 'Scatter Plot':
            return len(attrs) > 0 and len(metrics) > 1
        elif chart in ['Multimetric Bars', 'Multimetric Floating Bubbles']:
            return len(attrs) > 0
        elif chart == 'Bars and Line':
            return len(attrs) > 0 and len(metrics) > 1
        elif chart == 'Multigroup Trend':
            return len(times) > 0
        elif chart in ['Trend', 'Area Line']:
            return (len(times) > 0 or len(integer_metrics) > 0) and len(attrs) > 0
        elif chart in ['Multimetric Trend', 'Multimetric Area Line']:
            return len(times) > 0 or len(integer_metrics) > 0 or len(attrs) > 0
        elif chart == 'Range Filter':
            return len(metrics) >= 1
        elif chart == 'Radar':
            return len(attrs) > 0 and len(metrics) > 1
        elif chart in ['Custom Chart', 'Field Selector']:
            return True
        else:
            return False

    def __generate_extra_argument_code(self, chart):
        try:
            declaration_extra = ''
            set_statement = ''
            options = self.__cf.get_options
            if bool(options) > 0:
                for k in options:
                    o = options[k]
                    if k == 'legend':
                        if isinstance(o, Legend):
                            l_position = o.get_position
                            l_width = o.get_width
                            if isinstance(o.get_height, dict):
                                l_height = str(o.get_height.get('value', '95%'))
                                l_height += o.get_height.get('unit', '')
                            else:
                                l_height = o.get_height
                            l_height = l_height if re.match(r"/[0-9]/", str(l_height)) else f'{l_height}'
                            l_sort = o.get_sort

                            legend_declaration = f'{COMMENT_LEGEND}{eol}let legend = cf.Legend()'
                            legend_position = f'{eol}{tab}.position("{l_position}")'
                            legend_width = f'{eol}{tab}.width("{l_width}")'
                            legend_height = f'{eol}{tab}.height("{l_height}")'
                            legend_sort = f'{eol}{tab}.sort("{l_sort}")'

                            declaration_extra += legend_declaration + legend_position + legend_width + legend_height + legend_sort
                            set_statement += f'{eol}{tab}.set("legend", legend)'
                        elif isinstance(o, str):
                            set_statement += f'{eol}{tab}.set("legend", "{o}")'
                        elif isinstance(o, bool):
                            set_statement += f'{eol}{tab}.set("legend", {json.dumps(o)})'
                        else:
                            raise Exception('The value for the legend must be an instance of Legend object')
                    elif k == 'grid':
                        if isinstance(o, Grid):
                            g_top = o.get_top or 0
                            if not str(g_top).isnumeric():
                                g_top = f'"{g_top}"'

                            g_right = o.get_right or 0
                            if not str(g_right).isnumeric():
                                g_right = f'"{g_right}"'

                            g_bottom = o.get_bottom or 0
                            if not str(g_bottom).isnumeric():
                                g_bottom = f'"{g_bottom}"'

                            g_left = o.get_left or 0
                            if not str(g_left).isnumeric():
                                g_left = f'"{g_left}"'

                            declaration_extra += f'{COMMENT_GRID}{eol}let grid = cf.Grid(){eol}{tab}.top({g_top}){eol}{tab}.right({g_right}){eol}{tab}.bottom({g_bottom}){eol}{tab}.left({g_left});{eol}'
                            set_statement += f'{eol}{tab}.set("grid", grid)'
                        else:
                            raise Exception('The value for the grid must be an instance of Grid object')
                    elif k == 'markline':
                        if isinstance(o, MarkLine):
                            if isinstance(o.get_data, list) and len(o.get_data) > 0:
                                ml_data = json.dumps(o.get_data)
                                ml_color = o.get_color
                                ml_style = o.get_style

                                declaration_extra += f'{COMMENT_MARKLINE}{eol}let lines = cf.MarkLine(){eol}{tab}.data({ml_data}){eol}{tab}.color("{ml_color}"){eol}{tab}.style("{ml_style}");{eol}'
                                set_statement += f'{eol}{tab}.set("markline", lines)'
                            else:
                                raise Exception('Provide a valid Markline data array using the .data() function')
                        else:
                            raise Exception('The value for markline must be an instance of MarkLine object')
                    elif k == 'color':
                        if isinstance(o, Color):
                            if o.get_metric is not None:
                                cm_func = o.get_metric.func
                                cm_name = o.get_metric.name
                                func_declaration = f', "{cm_func}"' if cm_func and cm_func != 'derived' else ''
                                declaration_extra += f'let metricColor = cf.Metric("{cm_name}"{func_declaration});{eol}'

                            palette_call = f'{eol}{tab}.palette({json.dumps(o.get_palette)})' if o.get_palette is not None else ''
                            metric_call = f'{eol}{tab}.metric(metricColor)' if o.get_metric is not None else ''
                            range_call = f'{eol}{tab}.range({json.dumps(o.get_range)})' if o.get_range is not None else ''
                            match_call = f'{eol}{tab}.match({json.dumps(o.get_match)})' if o.get_match is not None else ''
                            theme_call = f'{eol}{tab}.theme({json.dumps(o.get_theme)})' if o.get_theme is not None else ''
                            auto_range_call = f'{eol}{tab}.autoRange({json.dumps(o.get_auto_range_options)})' if o.get_auto_range_options is not None else ''

                            declaration_extra += f'{COMMENT_COLOR}{eol}let color = cf.Color(){palette_call}{metric_call}{range_call}{theme_call}{auto_range_call}{match_call};{eol}'
                            set_statement += f'{eol}{tab}.set("color", color)'
                        else:
                            raise Exception('The value for color must be an instance of Color object')
                    elif k == 'geohashMarkerHtml':
                        set_statement += f'{eol}{tab}.set("geohashMarkerHtml", {o})'
                    elif k == 'markerHtml':
                        set_statement += f'{eol}{tab}.set("markerHtml", {o})'
                    elif k == 'columnStats':
                        # Processing the Color object specified in the 'widgetProps' -> 'props' -> 'color' property
                        default = lambda o: o.toJs() if isinstance(o, Color) else o
                        o = json.dumps(o, default=default)
                        o = re.sub(r"\"__cf.", 'cf.', o)
                        o = re.sub(r"\)__\"", ')', o)
                        o = re.sub(r"\\", '', o)
                        set_statement += f'{eol}{tab}.set("columnStats", {o})'
                    elif k == 'dataZoom':
                        if chart in ZOOM_SUPPORT_LIST:
                            set_statement += f'{eol}{tab}.set("dataZoom", {json.dumps(o)})'
                    elif k == 'orientation':
                        set_statement += f'{eol}{tab}.set("orientation", {json.dumps(o)})'
                    elif k == 'placement':
                        set_statement += f'{eol}{tab}.set("placement", {json.dumps(o)})'
                    elif k == 'axisLabels':
                        set_statement += f'{eol}{tab}.set("axisLabels", {json.dumps(o)})'
                    elif k == 'xAxis':
                        set_statement += f'{eol}{tab}.set("xAxis", {json.dumps(o)})'
                    elif k == 'yAxis':
                        set_statement += f'{eol}{tab}.set("yAxis", {json.dumps(o)})'
                    else:
                        set_statement += f'{eol}{tab}.set("{k}", {json.dumps(o)})'

                return [declaration_extra, set_statement]
            else:
                return ['', '']
        except Exception as e:
            raise Exception(e)

    def __generate_filters_code(self, filters):
        filters_code = ''
        filters_names = ''

        if len(filters) > 0:
            filters_code += COMMENT_FILTERS + eol            
            for f in filters:
                fn = self.__current_filter_number
                if f.get_relative:
                    filters_code += f'let filter{fn} = cf.Filter("{f.get_path}"){eol}{tab}.value("{f.get_value}").isRelative();'
                else:
                    is_text_filter = f'{eol}{tab}.isTextFilter()' if f.is_text_filter else ''
                    filters_code += f'let filter{fn} = cf.Filter("{f.get_path}"){eol}{tab}.label("{f.get_label}"){eol}{tab}.operation("{f.get_operation}"){eol}{tab}.value({json.dumps(f.get_value)}){is_text_filter};' + eol
                filters_names += f'filter{fn},'
                self.__current_filter_number += 1
        return [filters_code, filters_names]

    def __generate_metrics_code(self, metrics):
        metrics_code = ''
        metrics_names = ''

        if len(metrics) > 0:
            metrics_code += COMMENT_METRICS + eol
            mn = 0
            for m in metrics:
                if m.name != 'count':
                    # Calls
                    i_call = f'{eol}{tab}.interval({m.get_interval})' if m.get_interval is not None else ''
                    fb_call = f'{eol}{tab}.fixedBars({m.get_fixed_bars})' if m.has_fixed_bars else ''
                    sei_call = f'{eol}{tab}.showEmptyIntervals({json.dumps(m.get_show_empty_intervals)})' if m.has_show_empty_intervals else ''
                    o_call = f'{eol}{tab}.offset({m.get_offset})' if m.get_offset > 0 else ''
                    hide_metrics_call = f'{eol}{tab}.hideFunction()' if m.get_hide_function else ''

                    metrics_code += f'let metric{mn} = cf.Metric("{m.name}", "{str.lower(m.func)}"){i_call}{fb_call}{sei_call}{o_call}{hide_metrics_call};' + eol
                else:
                    metrics_code += f'let metric{mn} = cf.Metric("count");' + eol

                metrics_names += f'metric{mn},'
                mn += 1

        return [metrics_code, metrics_names]

    def __generate_comparative_metrics_code(self, comparative_metrics):
        metrics_code = ''
        metrics_names = ''
        mn = 0
        for m in comparative_metrics:
            hide_metrics_call = f'{eol}{tab}.hideFunction()' if m.get_hide_function else ''

            if m.name != 'count':
                metrics_code += f'let cMetric{mn} = cf.CompareMetric("{m.name}", "{str.lower(m.get_func)}"){hide_metrics_call}'
            else:
                metrics_code += f'let cMetric{mn} = cf.CompareMetric(){hide_metrics_call}'

            rate_call = f'{eol}{tab}.rate(' + (f'"{m.get_rate}"' if m.get_rate != '' else '') + ')' if m.get_rate is not None else ''
            with_call = f'{eol}{tab}.with("{m.get_with}")' if m.get_with is not None else ''

            if m.get_using_filters is not None:
                u_filters = ''
                for uf in m.get_using_filters:
                    u_filters += f'"{uf}",'
                using_call = f'{eol}{tab}.using({u_filters[:-1]})'
            else:
                using_call = ''

            label_call = f'{eol}{tab}.label("{m.get_label}")' if m.get_label is not None else ''
            benchmark_call = f'{eol}{tab}.benchmark("{str.lower(m.get_benchmark_func)}")' if m.get_benchmark_func is not None else ''

            if m.get_against is not None:
                a_filters = ''
                for af in m.get_against:
                    a_filters += f'"{af}",'
                against_call = f'{eol}{tab}.against({a_filters[:-1]})'
            else:
                against_call = ''

            benchmark_label_call = f'{eol}{tab}.label("{m.get_benchmark_label}")' if m.get_benchmark_label is not None else ''

            metrics_code += rate_call
            metrics_code += with_call
            metrics_code += using_call
            metrics_code += label_call
            metrics_code += benchmark_call
            metrics_code += against_call
            metrics_code += benchmark_label_call
            metrics_code += ';' + eol

            metrics_names += f'cMetric{mn},'
            mn += 1
        return [metrics_code, metrics_names]

    def __generate_attributes_code(self, attributes):
        attributes_code = ''
        attributes_names = ''

        if len(attributes) > 0:
            attributes_code += COMMENT_GROUPS + eol
            for a in attributes:
                gn = self.__current_group_number
                # Calls
                lbl_call = f'{eol}{tab}.label({a.get_label})' if a.get_label != '' else ''
                l_call = f'{eol}{tab}.limit({a.get_limit})' if a.get_limit is not None else ''

                s_call = ''
                if a.has_sort:
                    dir = a.get_sort.get('dir')
                    name = a.get_sort.get('name')
                    func = a.get_sort.get('func')
                    if a.is_sort_by_metric:
                        sort_by = f'cf.Metric("{name}", "{func}" )' if name != 'count' else 'cf.Metric()'
                    else:
                        sort_by = f'"{name}"'
                    s_call = f'{eol}{tab}.sort("{str.lower(dir)}", {sort_by})' if a.get_limit is not None else ''

                f_call = f'{eol}{tab}.func("{a.get_granularity}")' if a.get_granularity is not None else ''

                attributes_code += f'let group{gn} = cf.Attribute("{a.get_name}"){lbl_call}{l_call}{s_call}{f_call}' + eol
                attributes_names += f'group{gn},'
                self.__current_group_number += 1

        return [attributes_code, attributes_names]

    def __generate_rows_code(self, rows):
        full_rows_code = ''
        rows_code = []

        for r in rows:
            name = r.name
            label = f', "{r.get_label}"' if r.get_label != '' else ''
            func = f'.func("{r.get_func}")' if r.get_func is not None else ''
            rows_code.append(f'{tab}{tab}cf.Row("{name}"{label}){func}')

        if len(rows_code) > 0:
            full_rows_code = eol + tab + '.rows(\n{}\n\t)'.format(',\n'.join(rows_code))
        return full_rows_code

    def __generate_columns_code(self, columns):
        full_columns_code = ''
        columns_code = []

        for c in columns:
            name = c.name
            label = f', "{c.get_label}"' if c.get_label != '' else ''
            func = f'.func("{c.get_func}")' if c.get_func is not None else ''
            columns_code.append(f'{tab}{tab}cf.Column("{name}"{label}){func}')

        if len(columns_code) > 0:
            full_columns_code = eol + tab + '.columns(\n{}\n\t)'.format(',\n'.join(columns_code))
        return full_columns_code

    def __generate_fields_code(self, fields):
        full_fields_code = ''
        fields_code = []

        for f in fields:
            name = f.name
            label = f', "{f.get_label}"' if f.get_label != '' else ''
            group = f'.group("{f.get_group_name}")' if f.get_group_name is not None else ''
            fields_code.append(f'cf.Field("{name}"{label}){group}')

        if len(fields_code) > 0:
            full_fields_code = eol + tab + '.fields(...[\n{}])'.format(',\n'.join(fields_code))
        return full_fields_code

    def __generate_exclude_code(self, exclude):
        exclude_code = ''
        excludes = ''
        if len(exclude) > 0:
            for e in exclude:
                excludes += f'"{e}",'
            exclude_code = f"{eol}{tab}.exclude({excludes[:-1]})"
        return exclude_code

    def __generate_limit_code(self, limit):
        limit_code = ''
        if limit > 0:
            limit_code = f'{eol}{tab}.limit({limit})'
        return limit_code

    def __generate_location_code(self, location):
        location_code = ''
        if location is not None:
            location_code = f'{eol}{tab}.location("{location}")'
        return location_code

    def __generate_precision_code(self, precision):
        precision_code = ''
        if precision is not None:
            precision_code = f'{eol}{tab}.precision({precision})'
        return precision_code

    def __generate_time_field_code(self, tf):
        time_field_code = ''
        if tf is not None:
            lbl_call = f'{eol}{tab}.label("{tf.get_label}")' if tf.get_label != '' else ''
            l_call = f'{eol}{tab}.limit({tf.get_limit})' if tf.get_limit is not None else ''

            s_call = ''
            if tf.has_sort:
                dir =tf.get_sort.get('dir')
                name = tf.get_sort.get('name')
                func = tf.get_sort.get('func')
                if tf.is_sort_by_metric:
                    sort_by = f'cf.Metric("{name}", "{func}" )' if name != 'count' else 'cf.Metric()'
                else:
                    sort_by = f'"{name}"'
                s_call = f'{eol}{tab}.sort("{str.lower(dir)}", {sort_by})' if tf.get_limit is not None else ''

            f_call = f'{eol}{tab}.func("{tf.get_granularity}")' if tf.get_granularity is not None else ''
            time_field_code = f'{eol}{tab}.timeField(cf.Attribute("{tf.get_name}"){lbl_call}{l_call}{s_call}{f_call})'
        return time_field_code

    def __generate_only_with_filters_code(self, obj):
        only_with_filters_code = ''
        if obj is not None:
            only_with_filters_code = f'{tab}.onlyWithFilters({json.dumps(obj)})' + eol
        return only_with_filters_code

    def generate_code(self, chart, pn):
        try:
            prov = self.__cf.get_provider
            filters = prov.get_filters
            client_filters = prov.get_client_filters
            static_filters = prov.get_static_filters
            metrics = prov.get_metrics
            comparative_metrics = prov.get_comparative_metrics
            groups = prov.get_groups
            colgroups = prov.get_colgroups
            rows = prov.get_rows
            columns = prov.get_columns
            fields = prov.get_fields
            exclude = prov.get_exclude
            limit = prov.get_limit
            location = prov.get_location
            precision = prov.get_precision
            time_field = prov.get_time_field
            only_with_filters = prov.get_only_with_filters

            code = self.__get_header_code()
            extra_arguments = self.__generate_extra_argument_code(chart)
            declaration_extra = extra_arguments[0]
            set_statement = extra_arguments[1]

            # Filters
            filters_code = self.__generate_filters_code(filters)
            code += filters_code[0]
            filters_call = f'{eol}{tab}.filters({filters_code[1][:-1]})' if filters_code[1] != '' else ''
            # Client filters
            client_filters_code = self.__generate_filters_code(client_filters)
            code += client_filters_code[0]
            client_filters_call = f'{eol}{tab}.clientFilters({client_filters_code[1][:-1]})' if client_filters_code[1] != '' else ''
            # Static filters
            static_filters_code = self.__generate_filters_code(static_filters)
            code += static_filters_code[0]
            static_filters_call = f'{eol}{tab}.staticFilters({static_filters_code[1][:-1]})' if static_filters_code[1] != '' else ''
            # Metrics and Comparative Metrics
            metrics_code = self.__generate_metrics_code(metrics)
            code += metrics_code[0]

            comp_metrics_code = self.__generate_comparative_metrics_code(comparative_metrics)
            code += comp_metrics_code[0]

            metrics_name = metrics_code[1] if metrics_code[1] != '' else ''
            metrics_name += comp_metrics_code[1] if comp_metrics_code[1] != '' else ''

            metrics_call = f'{eol}{tab}.metrics({metrics_name[:-1]})'

            # Attribute
            groups_code = self.__generate_attributes_code(groups)
            code += groups_code[0]
            groups_call = f'{eol}{tab}.groupby({groups_code[1][:-1]})' if groups_code[1] != '' else ''
            # colgroupby
            colgroups_code = self.__generate_attributes_code(colgroups)
            code += colgroups_code[0]
            colgroups_call = f'{eol}{tab}.colgroupby({colgroups_code[1][:-1]})' if colgroups_code[1] != '' else ''
            # Rows
            rows_code = self.__generate_rows_code(rows)
            # Columns
            columns_code = self.__generate_columns_code(columns)
            # Fields
            fields_code = self.__generate_fields_code(fields)
            # Exclude
            exclude_code = self.__generate_exclude_code(exclude)
            # Limit
            limit_code = self.__generate_limit_code(limit)
            # Location
            location_code = self.__generate_location_code(location)
            # Precision
            precision_code = self.__generate_precision_code(precision)
            # Time field
            time_field_code = self.__generate_time_field_code(time_field)
            # Only with filters
            only_with_filters_code = self.__generate_only_with_filters_code(only_with_filters)

            code += declaration_extra
            code += COMMENT_DATA + eol
            code += f'let myData = source{filters_call}{client_filters_call}{static_filters_call}{metrics_call}{groups_call}{colgroups_call}{rows_code}{columns_code}{fields_code}{exclude_code};' + eol + eol
            code += f'myData.graph("{chart}")'
            code += limit_code + location_code + precision_code + time_field_code
            code += set_statement + eol
            code += only_with_filters_code
            code += tab + f'.element("visualization{pn}")' + eol
            code += tab + '.execute();' + eol
            return code
        except Exception as e:
            raise Exception(e)
