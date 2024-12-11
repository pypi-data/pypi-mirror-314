import os
import json
import unittest
import pandas as pd
import sys

sys.path.append("..")
from chartfactor.src import CFToolkit
from chartfactor.src import Metric, Attribute, Grid, Color, Filter, CompareMetric, Row, Column, Legend, Field
from data.get_visualization_js_code_data import GetVisualizationJsCodeData as data


class TestGetVisualizationJsCode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = os.path.dirname(os.path.realpath(__file__)) + '/csv/ticket_sales.csv'
        path_ctt = os.path.dirname(os.path.realpath(__file__)) + '/csv/chicago_taxi_trips.csv'
        path_lfb = os.path.dirname(os.path.realpath(__file__)) + '/csv/london_fire_brigade.csv'

        cls.df = pd.read_csv(path)
        cls.df_lfb = pd.read_csv(path_lfb)
        df_ctt = pd.read_csv(path_ctt)
        # Adding the location field to be used in the Geo Map visualizations
        df_ctt['dropoff_location'] = df_ctt[['dropoff_latitude', 'dropoff_longitude']].apply(lambda x: [x.dropoff_latitude, x.dropoff_longitude], axis=1)
        cls.df_ctt = df_ctt

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_area_line(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric4 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group4 = Attribute("catdesc").limit(10).sort("desc", Metric("commission", "sum"))
        group42 = Attribute("saletime").func("MONTH").limit(1000).sort("asc", "saletime")
        # Add metrics and groups to data source
        myData4 = cf.groupby(group4, group42).metrics(metric4)
        # --- Define chart options and static filters ---
        # Define Grid
        grid4 = Grid().top(10).right(15).bottom(65).left(65)
        # Define Color Palette
        color4 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        myChart4 = myData4.graph("Area Line").set("grid", grid4).set("color", color4).set("dataZoom", True)
        code = myChart4.get_visualization_js_code()

        self.assertEqual(code, data.AREA_LINE_RESULT)

    def test_stacked_bar(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric5 = Metric("commission", "sum")
        # Define attributes to group by
        group5 = Attribute("city").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData5 = cf.groupby(group5).metrics(metric5)
        # --- Define chart options and static filters ---
        # Define Grid
        grid5 = Grid().top(10).right(15).bottom(35).left(65)
        # Define Color Palette
        color5 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        myChart5 = myData5.graph("Bars").set("grid", grid5).set("color", color5).set("dataZoom", False).set(
            "serieLabel", {
                "show": True,
                "formatter": "BigNumber"
            })

        code = myChart5.get_visualization_js_code()
        self.assertEqual(code, data.STACKED_BAR_RESULT)

    def test_box_plot(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Configuration for grid
        grid6 = Grid().left(100).right(15).bottom(80).top(10)
        yAxis6 = {'nameGap': 80}
        xAxis6 = {'nameGap': 40}
        # Define metrics
        metric6 = Metric("commission", "percentiles")
        # Define attributes to group by
        group6 = Attribute("catdesc").limit(10).sort("desc", "catdesc")
        # Add metrics and groups to data source
        myData6 = cf.groupby(group6).metrics(metric6)
        # Define chart options
        code = myData6.graph("Box Plot").set("grid", grid6).set("xAxis", xAxis6).set("yAxis", yAxis6).get_visualization_js_code()
        self.assertEqual(code, data.BOX_PLOT_RESULT)

    def test_bars_serie_label(self):
        cf = CFToolkit()
        cf.provider(self.df)
        #  Define metrics
        metric7 = Metric("commission", "sum").hideFunction()
        #  Define attributes to group by
        group7 = Attribute("venuestate").limit(10).sort("desc", Metric("commission", "sum"))
        group72 = Attribute("venuecity").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData7 = cf.groupby(group7, group72).metrics(metric7)
        #  --- Define chart options and static filters ---
        #  Define Grid
        grid7 = Grid().top(10).right(15).bottom(35).left(65)
        #  Define Color Palette
        color7 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData7.graph("Bars").set("grid", grid7).set("color", color7).set("dataZoom", False).set("legend", "right").set(
            "serieLabel", {
                "show": True
            }).get_visualization_js_code()
        self.assertEqual(code, data.BARS_SERIE_LABEL)

    def test_default_gauge(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric8 = Metric("commission", "sum")
        # Add metrics and groups to data source
        myData8 = cf.metrics(metric8)
        # Define chart options
        code = myData8.graph("Gauge").get_visualization_js_code()
        self.assertEqual(code, data.DEFAULT_GAUGE_RESULT)

    def test_advance_gauge(self):
        cf = CFToolkit()
        cf.provider(self.df)
        metrics81 = [
            Metric('commission', 'avg'),
            Metric('pricepaid', 'avg'),
            Metric('count')
        ]

        theme81 = {'font': 'white', 'background': '#3e4953', 'header': '#4e5861', 'rowOdd': '#1b242c',
                   'rowEven': '#38424a', 'headerFont': '#52c7da'}
        color81 = Color().theme(theme81).palette('intense')

        myData81 = cf.metrics(metrics81)
        # Define chart options
        code = myData81.graph("Gauge").set('ranges', [
            [0, 200],
            [0, 800],
            [0, 1000]
        ]).set('radius', ['80%', '40%', '80%']).set('color', color81).set('angles', [
            [180, 0],
            [225, -45],
            [180, 0]
        ]).set('rangeColors', [
            [[0.02, 'lime'], [0.5, '#1e90ff'], [0.7, '#ff4500'], [0.8, 'yellow'], [1, 'orange']],
            [[0.5, 'red'], [1, 'yellow']],
            [[0.5, 'black'], [1, 'blue']]
        ]).set('layout', [
            ['25%', '80%'],
            ['50%', '30%'],
            ['75%', '80%']
        ]).set('lineWidth', [5, 13, 20]).get_visualization_js_code()
        self.assertEqual(code, data.ADVANCE_GAUGE_RESULT)

    def test_default_kpi(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric9 = Metric("commission", "sum")
        #  Add metrics and groups to data source
        myData9 = cf.metrics(metric9)
        #  Define chart options
        code = myData9.graph("KPI").set("mainTextSize", 12).set("secondaryTextSize", 12).set("diffTextSize", 12).set(
            "labelTextSize", 8).get_visualization_js_code()
        self.assertEqual(code, data.DEFAULT_KPI_RESULT)

    def test_stacked_bars_with_4_subcategories(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric10 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group10 = Attribute("venuestate").limit(10).sort("desc", Metric("commission", "sum"))
        group102 = Attribute("catname").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData10 = cf.groupby(group10, group102).metrics(metric10)
        # --- Define chart options and static filters ---
        # Define Grid
        grid10 = Grid().top(10).right(15).bottom(35).left(65)
        # Define Color Palette
        color10 = Color().palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e"])
        code = myData10.graph("Bars").set("grid", grid10).set("color", color10).set("dataZoom", False).set("legend",
                                                                                                    "right").set(
            "serieLabel", {
                "show": True,
                #     "formatter": "BigNumber"
                #     "position": "insideTop",
                #     "align": 'right',
                #     "verticalAlign": 'middle'
            }).get_visualization_js_code()
        self.assertEqual(code, data.STACKED_BAR_4_SUBCATEGORIES_RESULT)

    def test_multimetric_trend(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metrics11 = [Metric("commission", "sum"), Metric("qtysold", "sum"), Metric("venueseats", "sum")]
        # Define attributes to group by
        group11 = Attribute("saletime").func("DAY").limit(1000).sort("asc", "saletime")
        # Add metrics and groups to data source
        myData11 = cf.groupby(group11).metrics(metrics11)
        # --- Define chart options and static filters ---
        # Define Grid
        grid11 = Grid().top(10).right(15).bottom(65).left(65)
        # Define Color Palette
        color11 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData11.graph("Multimetric Trend").set("grid", grid11).set("color", color11).set("dataZoom", True).get_visualization_js_code()
        self.assertEqual(code, data.MULTIMETRIC_TREND_RESULT)

    def test_horizontal_stacked_bars(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric12 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group12 = Attribute("venuestate").limit(10).sort("desc", Metric("commission", "sum"))
        group122 = Attribute("venuecity").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData12 = cf.groupby(group12, group122).metrics(metric12)
        # --- Define chart options and static filters ---
        # Define Grid
        grid12 = Grid().top(10).right(15).bottom(35).left(65)
        # Define Color Palette
        color12 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData12.graph("Bars").set("grid", grid12).set("color", color12).set("dataZoom", False).set("orientation",
                                                                                                    "horizontal").set(
            "yAxis", {"text": "out"}).set("serieLabel", {
            "show": True
        }).get_visualization_js_code()
        self.assertEqual(code, data.HORIZONTAL_STACKED_BARS_RESULT)

    def test_scatter_plot(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metrics14 = [
            Metric("commission", "sum"),
            Metric("qtysold", "sum"),
            Metric("venueseats", "sum")
        ]
        # Define attributes to group by
        group14 = Attribute("state").limit(10).sort("desc", metrics14[0])
        # Add metrics and groups to data source
        myData14 = cf.groupby(group14).metrics(metrics14)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color14 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData14.graph("Scatter Plot").set("color", color14).get_visualization_js_code()
        self.assertEqual(code, data.SCATTER_PLOT_RESULT)

    def test_tree_map_2d(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric16 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group16 = Attribute("catdesc").limit(10).sort("desc", Metric("commission", "sum"))
        group162 = Attribute("catgroup").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData16 = cf.groupby(group16, group162).metrics(metric16)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color16 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData16.graph("Tree Map 2D").set("color", color16).get_visualization_js_code()
        self.assertEqual(code, data.TREE_MAP_2D_RESULT)

    def test_clustered_bars(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric17 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group17 = Attribute("venuestate").limit(5).sort("desc", Metric("commission", "sum"))
        group172 = Attribute("venuecity").limit(2).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData17 = cf.groupby(group17, group172).metrics(metric17)
        # --- Define chart options and static filters ---
        # Define Grid
        grid17 = Grid().top(10).right(15).bottom(35).left(65)
        # Define Color Palette
        color17 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData17.graph("Bars").set("grid", grid17).set("color", color17).set("dataZoom", False).set("placement",
                                                                                                    "clustered").set(
            "serieLabel", {
                "show": True,
                "formatter": "BigNumber",
                #     "position": "insideTop"
            }).title('Clustered Bars').get_visualization_js_code()
        self.assertEqual(code, data.CLUSTERED_BARS_RESULT)

    def test_floating_bubbles(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metrics18 = [
            Metric("commission", "sum"),
            Metric("qtysold", "sum"),
            Metric("venueseats", "sum")
        ]
        # Define attributes to group by
        group18 = Attribute("firstname").limit(10).sort("desc", Metric("commission", "sum"))
        group182 = Attribute("catdesc").limit(10).sort("desc", Metric("qtysold", "sum"))

        # Add metrics and groups to data source
        myData18 = cf.groupby(group18, group182).metrics(metrics18)
        # Define chart options
        code = myData18.graph("Floating Bubbles").get_visualization_js_code()
        self.assertEqual(code, data.FLOATING_BUBBLES_RESULT)

    def test_geo_map_pivot_query(self):
        cf = CFToolkit()
        cf.provider(self.df_ctt)
        # Add Metrics
        metricCount = Metric()
        metricFare = Metric("fare", "sum")
        #  Add fields to data source.
        myData19 = cf.rows(Row('dropoff_latitude'), Row('dropoff_longitude'),
                                 Row('dropoff_community_area_desc')).metrics(metricCount, metricFare)
        # Define chart options
        code = myData19.graph("Geo Map").set("tileLayers", {
            'Base': "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            'attribution': 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        }).set("center", [41.82199022070215, -87.7687454223633]).set("zoom", 11).limit(200).get_visualization_js_code()
        self.assertEqual(code, data.GEO_MAP_PIVOT_QUERY_RESULT)

    def test_geo_map_geo_hash(self):
        cf = CFToolkit()
        cf.provider(self.df_ctt)
        # Define metrics
        metric20 = Metric("count")
        geohashIconCustomMarker = '''function(value){
          return `<img
                  class="icon-image"
                  style="width: 34px !important; height: 34px !important;"
                  src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAIAAACRXR/mAAAABmJLR0QA/wD/AP+gvaeTAAAE5klEQVRYhe2YW2xURRjH/9+cy+52r0CvFuhVKhYM8UGUQLzEoBLCg8TEaCQxRh+MMSY8+uCLifKivhj1TVATjTGNRg1GiSBRAyEiSImF0rvtblvavffcZj4fKt3tUtpuIUjC/l/OmTPz/87vzHwzc84hZsatJ/F/AyysClY5qmCVowpWOapglaMKVjm6HbCUx1aq9CLLK7X52cNyIunXi8IsL/0o//xEDhzj1DAA6H6xuk3r2K1t2Sdq74achDuBQCenD1PsSc7+RqHtYAdkLhL1unpLxc9aH221Dz7mnfkUuYQWq9GqG7VwhJOX3OMHrPfvcbpeYCvNyc/hDCN/El4C2Z8B5mTX4pFpxe9b8nyX/eUz8CwRXmWs79Bi1QAViDPT7vAFOT0u1rQbO8Ki+RVOf0fBB8Ae9HqAafU+zp+g4LYbiSX7jtgHH4fyjLV3Gus7QLRgM2+s3+nrpqBp7tpCPgaZMJthX6TGAzz1mah9Ff5NUBaEv8S4kkHkmSnni6ehPGNtu9F017WYAOgNLWZrJ+ds9/cegME27B6AOfE26atABicOQE5fbVwJlnv0Tc5PiqqIsa6jCFaxY6lciu0ZqMJ00xtatFiNGkmqRHquKbzLbPepoRcpuhtGw5VJWvQ8S0LI7q/cX95S8TPQ/dqGXcbDb8jTHwPQ17ZDCPYcLz4kpxMqM41CPpAIRbVVNXpdE/kCxroNMjnh9YybdZFCXGeQQg9ysgvyIFW/BF978U2XyC3v13ecw/sBkGGy6wIMzYB0IUTgvp3eSK871g8pr+knodeuM5o3WqePsnL8T90Lbd6IU3QP1e6HCJT6FsHi1PDMu+1E7Ou8X4RiKpe2u39n15mlJNOvculSjxAUNImgMhauBCZfFYjYypl7NotIUXaTBr0eZFD4EYrthV4zV7PYIMqebyEdrbFVBGPeaJ872jfLBIBdZ+58npTijIWQT9tQJyI+zrtqIqMu5yEVAMw4KMZiSUYD1b8Oo7EkzGJYbGcAQLHTf84b61+kZakxa8uehCSIuojWXms8FOWUpSay8BsA4CmVtUEQYT/nT/HAsxR5gmJ7i9NrYSxODan4Wc6OAfASg+BlbWRXRYGKp1U8LRqixrYWvSYEQF4Yd08NQTEAMjVt0x5j5wcUrCuxluaWSpxzv39N9h1ZCUdJ6IChtVaL1moRNNVoSsbT+sZ6CLK/OQtZuCnFmv3P/0Sr266JpQaPW4d2wcmKyBqjsVUEo+w5Kj3ljvSyYy0XR5BojOlt1Qj5eCwtR5Mqkfmve6pM49EO2Tshz8fnOeo2+1/+A6IwdAUstpLWex2cG9fvaDGbN83ubzI1KRPDMj3FdumKtwBPNCBa11CVqS7n1EiSs/bVbchvGDva3GMX2Zm3rJh7D+lbnpsrFgC9kx9yblyEomZLJwAwO71nvPHhJWnI1KgmTAGDbdf7axTeYonIluse76WGKA9OFV+Xf3+9MJbq/QGAXt80+yLg9HcvzaRpFKiCrql/kkvSF5F5PFK6D/L0QHGxgMWZMQAiEAag8hlvbABLSkrOZpYPVGQsXcPJHy0uFrZqijQCmE1tOTkK3NT/XmLt1uJiIeXVyAlODpE7DS/NZjW04E3FatpO4YYFsG4p3Q4fZDdOFaxyVMEqRxWsclTBKkcVrHJUwSpHtyjWv3ZmSTCYpkOiAAAAAElFTkSuQmCC"
                  />`;
        }
        '''
        # Add fields to data source.
        code = cf.graph('Geo Map').limit(10000).metrics(metric20).location('dropoff_location').precision(5).set(
            'precisionLevels', {
                'raw': {'zoom': 16, 'fields': ['dropoff_latitude', 'dropoff_longitude']},
                'levels': [
                    {'zoom': 6, 'precision': 4},
                    {'zoom': 10, 'precision': 5},
                    {'zoom': 13, 'precision': 8},
                    {'zoom': 15, 'precision': 11},
                ]
            }).set('geohashMarkerHtml', geohashIconCustomMarker).set('tileLayers', [{
            'Base': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            'attribution': 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
        }
        ]).set("center", [41.766190406938684, -87.73475646972658]).set("zoom", 10).get_visualization_js_code()
        self.assertEqual(code, data.GEO_MAP_GEO_HASH_RESULT)

    def test_nested_pie(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric21 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group21 = Attribute("catgroup").limit(10).sort("desc", Metric("commission", "sum"))
        group212 = Attribute("catdesc").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData21 = cf.groupby(group21, group212).metrics(metric21)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color21 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData21.graph("Nested Pie").set("color", color21).get_visualization_js_code()
        self.assertEqual(code, data.NESTED_PIE_RESULT)

    def test_multimetric_bars(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metrics22 = [
            Metric("commission", "sum"),
            Metric("qtysold", "sum"),
            Metric("venueseats", "sum")
        ]
        # Define attributes to group by
        group22 = Attribute("state").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData22 = cf.groupby(group22).metrics(metrics22)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color22 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData22.graph("Multimetric Bars").set("color", color22).set("placement", "stacked").set("dataZoom", False).get_visualization_js_code()
        self.assertEqual(code, data.MULTIMETRIC_BARS_RESULT)

    def test_sankey(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Configuration for grid
        grid23 = Grid().left(10).right(160).bottom(10).top(10)
        # Define metrics
        metric23 = Metric("commission", "sum")
        myData23 = cf.rows(Row("firstname"), Row("lastname")).metrics(metric23)
        # Define chart options
        code = myData23.graph("Sankey").set("grid", grid23).limit(50).get_visualization_js_code()
        self.assertEqual(code, data.SANKEY_RESULT)

    def test_donut(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric24 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group24 = Attribute("email").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData24 = cf.groupby(group24).metrics(metric24)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color24 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData24.graph("Donut").set("color", color24).get_visualization_js_code()
        self.assertEqual(code, data.DONUT_RESULT)

    def test_horizontal_clustered_bars(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric25 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group25 = Attribute("venuestate").limit(5).sort("desc", Metric("commission", "sum"))
        group252 = Attribute("venuecity").limit(2).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData25 = cf.groupby(group25, group252).metrics(metric25)
        # --- Define chart options and static filters ---
        # Define Grid
        grid25 = Grid().top(10).right(15).bottom(35).left(65)
        # Define Color Palette
        color25 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData25.graph("Bars").set("grid", grid25).set("color", color25).set("dataZoom", False).set("placement",
                                                                                                    "clustered").set(
            "orientation", "horizontal").set("yAxis", {"text": "out"}).set("serieLabel", {
            "show": True,
            "formatter": "BigNumber",
            #     "position": "insideTop"
        }).get_visualization_js_code()
        self.assertEqual(code, data.HORIZONTAL_CLUSTERED_BARS)

    def test_disk(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric26 = Metric("easting_m", "sum").hideFunction()
        # Define attributes to group by
        group26 = Attribute("hour_of_call").limit(24).sort("asc", "hour_of_call")
        # Add metrics and groups to data source
        myData26 = cf.groupby(group26).metrics(metric26)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color26 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData26.graph("Disk").set("color", color26).get_visualization_js_code()
        self.assertEqual(code, data.DISK_RESULT)

    def test_histogram(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric27 = Metric("commission", "histogram")
        # Add metrics and groups to data source
        myData27 = cf.metrics(metric27)
        # Define chart options
        code = myData27.graph("Histogram").set("serieLabel", True).get_visualization_js_code()
        self.assertEqual(code, data.HISTOGRAM_RESULT)

    def test_word_cloud(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric28 = Metric("commission", "sum")
        # Define attributes to group by
        group28 = Attribute("state").limit(30).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData28 = cf.groupby(group28).metrics(metric28)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color28 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData28.graph("Word Cloud").set("color", color28).get_visualization_js_code()
        self.assertEqual(code, data.WORD_CLOUD_RESULT)

    def test_pie(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric29 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group29 = Attribute("email").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData29 = cf.groupby(group29).metrics(metric29)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color29 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData29.graph("Pie").set("color", color29).title('Pie Default').get_visualization_js_code()
        self.assertEqual(code, data.PIE_RESULT)

    def test_multimetric_stacked_bars(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metrics33 = [
            Metric("commission", "sum").hideFunction(),
            Metric("pricepaid", "sum").hideFunction()
        ]
        # Define attributes to group by
        group33 = Attribute("eventname").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData33 = cf.groupby(group33).metrics(metrics33)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color33 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData33.graph("Multimetric Bars").set("color", color33).set("placement", "stacked").set("dataZoom", False).set(
            "serieLabel", {
                "show": True
            }).get_visualization_js_code()
        self.assertEqual(code, data.MULTIMETRIC_STACKED_BARS_RESULT)

    def test_tree_map(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric34 = Metric("commission", "sum")
        # Define attributes to group by
        group34 = Attribute("eventname").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData34 = cf.groupby(group34).metrics(metric34)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color34 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData34.graph("Tree Map").set("color", color34).set("serieLabel", {
            "show": True,
            "position": "insideTopLeft",
            'padding': 10
        }).get_visualization_js_code()
        self.assertEqual(code, data.TREE_MAP_RESULT)

    def test_bars_and_ine(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric37 = Metric("commission", "sum")
        metric372 = Metric("qtysold", "sum")
        # Define attributes to group by
        group37 = Attribute("saletime").func("DAY").limit(1000).sort("asc", "saletime")
        # Add metrics and groups to data source
        myData37 = cf.groupby(group37).metrics(metric37, metric372)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color37 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData37.graph("Bars and Line").set("color", color37).get_visualization_js_code()
        self.assertEqual(code, data.BARS_AND_LINES_RESULT)

    def test_pie_metric_value_true(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric38 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group38 = Attribute("catname").limit(10).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData38 = cf.groupby(group38).metrics(metric38)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color38 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData38.graph("Pie").set("color", color38).set("labelPosition", "inside").set("metricValue", True).get_visualization_js_code()
        self.assertEqual(code, data.PIE_METRIC_VALUE_RESULT)

    def test_multimetric_area_line(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metrics40 = [
            Metric("commission", "sum"),
            Metric("qtysold", "sum"),
            Metric("venueseats", "sum")
        ]
        # Define attributes to group by
        group40 = Attribute("saletime").func("DAY").limit(1000).sort("asc", "saletime")
        # Add metrics and groups to data source
        myData40 = cf.groupby(group40).metrics(metrics40)
        # --- Define chart options and static filters ---
        # Define Grid
        grid40 = Grid().top(10).right(15).bottom(65).left(65)
        # Define Color Palette
        color40 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData40.graph("Multimetric Area Line").set("grid", grid40).set("color", color40).set("dataZoom", True).get_visualization_js_code()
        self.assertEqual(code, data.MULTIMETRIC_AREA_LINE_RESULT)

    def test_packed_bubbles(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric41 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group41 = Attribute("eventname").limit(50).sort("desc", Metric("commission", "sum"))
        # Add metrics and groups to data source
        myData41 = cf.groupby(group41).metrics(metric41)
        # --- Define chart options and static filters ---
        # Define Color Palette
        color41 = Color().metric().palette(["#0095b7", "#a0b774", "#f4c658"])
        color41.range([
            {'min': 0, 'max': 30000, 'color': 'red'},
            {'min': 30000, 'max': 80000, 'color': 'gray'},
            {'min': 80000, 'max': 200000, 'color': 'blue'}
        ])

        code = myData41.graph("Packed Bubbles").set("color", color41).get_visualization_js_code()
        self.assertEqual(code, data.PACKED_BUBBLES_RESULT)

    def test_heat_map(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Configuration for grid
        grid42 = Grid().left(10).right(10).bottom(10).top(10)
        # Define metrics
        metric42 = Metric("commission", "sum").hideFunction()
        # Define attributes to group by
        group42 = Attribute("catdesc").limit(10).sort("desc", metric42)
        group422 = Attribute("catgroup").limit(10).sort("desc", metric42)
        # Add metrics and groups to data source
        myData42 = cf.groupby(group42, group422).metrics(metric42)
        # Define chart options
        color42 = Color().metric(metric42)
        code = myData42.graph("Heat Map").set("grid", grid42).set("color", color42).set("showValues", True).get_visualization_js_code()
        self.assertEqual(code, data.HEAT_MAP_RESULT)

    def test_vector_map(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric43 = Metric("commission", "sum")
        # Define attributes to group by
        group43 = Attribute("catdesc").limit(10).sort("desc", metric43)
        # Add metrics and groups to data source
        myData43 = cf.groupby(group43).metrics(metric43)
        # Define chart options
        color43 = Color().metric(metric43)
        code = myData43.graph("Vector Map").set("shape", "world").set("min", 0).set("zoom", 1.030328968347247).set("center", [
            14.531024917022904, 24.607267038606977]).set("color", color43).get_visualization_js_code()
        self.assertEqual(code, data.VECTOR_MAP_RESULT)

    def test_tree(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Add Metrics
        metric44 = Metric("pricepaid", "sum").hideFunction()
        # Add fields to data source.
        myData44 = cf.rows(Row("catdesc")).metrics(metric44)
        # Define chart options
        # Define Grid
        grid44 = Grid().top("5%").left("15%").bottom("5%").right("40%")
        code = myData44.graph("Tree").limit(1000).set("grid", grid44).get_visualization_js_code()
        self.assertEqual(code, data.TREE_RESULT)

    def test_range_filter(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metrics45 = [
            Metric("commission"),
            Metric("qtysold"),
            Metric("venueseats"),
        ]
        # Add metrics and groups to data source
        myData45 = cf.metrics(metrics45)
        # Define chart options
        code = myData45.graph("Range Filter").get_visualization_js_code()
        self.assertEqual(code, data.RANGE_FILTER_RESULT)

    def test_radar(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric460 = Metric("commission", "sum")
        metric461 = Metric("qtysold", "sum")
        metric462 = Metric("venueseats", "sum")
        # Define attributes to group by
        group46 = Attribute("catdesc").limit(10).sort("desc", metric460)
        # Add metrics and groups to data source
        myData46 = cf.groupby(group46).metrics(metric460, metric461, metric462)
        # Define chart options
        code = myData46.graph("Radar").get_visualization_js_code()
        self.assertEqual(code, data.RADAR_RESULT)

    def test_time_range_picker(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define the time field to be used
        field47 = Attribute("saletime").func("YEAR")
        myData47 = cf.timeField(field47)
        # Define chart options
        code = myData47.graph("Time Range Picker").get_visualization_js_code()
        self.assertEqual(code, data.TIME_RANGE_PICKER)

    def test_trend(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric48 = Metric("commission", "sum")
        # Define attributes to group by
        group481 = Attribute("catdesc").limit(10).sort("desc", Metric("commission", "sum"))
        group482 = Attribute("saletime").func("DAY").limit(1000).sort("asc", "saletime")
        # Add metrics and groups to data source
        myData48 = cf.groupby(group481, group482).metrics(metric48)
        # --- Define chart options and static filters ---
        # Define Grid
        grid48 = Grid().top(10).right(15).bottom(65).left(65)
        # Define Color Palette
        color48 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        code = myData48.graph("Trend").set("grid", grid48).set("color", color48).set("dataZoom", True).get_visualization_js_code()
        self.assertEqual(code, data.TREND_RESULT)

    def test_sunburst(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Add Metrics
        metric50 = Metric("count")
        # Add fields to data source
        myData50 = cf.rows(Row("catdesc")).metrics(metric50)
        # Define chart options
        code = myData50.graph("Sunburst").limit(1000).get_visualization_js_code()
        self.assertEqual(code, data.SUNBURST_RESULT)

    def test_multigroup_trend(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Configuration for grid
        grid51 = Grid().left(65).right(15).bottom(65).top(10)
        # Add Metrics
        metric51 = Metric("commission", "avg")
        # Add fields to data source.
        myData51 = cf.rows(Row("saletime").func("MONTH"), Row("catdesc")).metrics(metric51)
        # Define chart options
        code = myData51.graph("Multigroup Trend").set("grid", grid51).limit(10000).get_visualization_js_code()
        self.assertEqual(code, data.MULTIGROUP_TREND)

    def test_row_data_table_stats(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Declare your fields (do not remove this comment line)
        fields52 = [
            Field('salesid', 'salesid'),
            Field('listid', 'listid'),
            Field('sellerid', 'sellerid'),
            Field('buyerid', 'buyerid'),
            Field('eventid', 'eventid'),
            Field('dateid', 'dateid'),
            Field('qtysold', 'qtysold'),
            Field('pricepaid', 'pricepaid'),
            Field('commission', 'commission'),
            Field('saletime', 'saletime'),
            Field('eventid.1', 'eventid.1'),
            Field('venueid', 'venueid'),
            Field('catid', 'catid'),
            Field('dateid.1', 'dateid.1'),
            Field('eventname', 'eventname'),
            Field('starttime', 'starttime'),
            Field('catid.1', 'catid.1'),
            Field('catgroup', 'catgroup'),
            Field('catname', 'catname'),
            Field('catdesc', 'catdesc'),
            Field('venueid.1', 'venueid.1'),
            Field('venuename', 'venuename'),
            Field('venuecity', 'venuecity'),
            Field('venuestate', 'venuestate'),
            Field('venueseats', 'venueseats'),
            Field('userid', 'userid'),
            Field('username', 'username'),
            Field('firstname', 'firstname'),
            Field('lastname', 'lastname'),
            Field('city', 'city'),
            Field('state', 'state'),
            Field('email', 'email'),
            Field('phone', 'phone'),
            Field('likesports', 'likesports'),
            Field('liketheatre', 'liketheatre'),
            Field('likeconcerts', 'likeconcerts'),
            Field('likejazz', 'likejazz'),
            Field('likeclassical', 'likeclassical'),
            Field('likeopera', 'likeopera'),
            Field('likerock', 'likerock'),
            Field('likevegas', 'likevegas'),
            Field('likebroadway', 'likebroadway'),
            Field('likemusicals', 'likemusicals'),
            Field('saletime_utc', 'saletime_utc'),
            Field('saletime_min_7', 'saletime_min_7'),
            Field('saletime_plus_8', 'saletime_plus_8'),
        ]
        myData52 = cf.fields(fields52)
        color52 = Color().theme({
            "headerStyle": "background: #009688; color: #fff; font-size: 16px;",
            "headerIconStyle": "color: #fff; font-size: 16px;",
            "rowOddStyle": "background: #fff; color: #000;",
            "rowEvenStyle": "background: #e0f2f1; color: #000;",
            "headerResizeLineStyle": "border-right-color: #fff; border-right-width: 1px;",
            "headerHorizontalLineStyle": "border-bottom-color: #fff; border-bottom-width: 1px;",
            "tpButtonActive": "color: #fff; background: #009688;",
            "cellMoving": "color: black; background: #80cbc4;",
        })
        histogramColor = Color()
        histogramColor.theme({'background': '#e0f2f1'})
        # --- Define chart options and static filters ---
        code = myData52.graph("Raw Data Table").set('color', color52).set("columnFilters", [
            {'field': "salesid", 'component': "slicer"},
            {'field': "listid", 'component': "slicer"},
            {'field': "sellerid", 'component': "slicer"},
            {'field': "buyerid", 'component': "slicer"},
            {'field': "eventid", 'component': "slicer"},
            {'field': "dateid", 'component': "slicer"},
            {'field': "qtysold", 'component': "slicer"},
            {'field': "pricepaid", 'component': "range"},
            {'field': "commission", 'component': "range"},
            {'field': "saletime", 'component': "datePicker", 'props': {'func': 'DAY'}},
            {'field': "eventid.1", 'component': "slicer"},
            {'field': "venueid", 'component': "slicer"},
            {'field': "catid", 'component': "slicer"},
            {'field': "dateid.1", 'component': "slicer"},
            {'field': "eventname", 'component': "slicer"},
            {'field': "starttime", 'component': "datePicker", 'props': {'func': 'DAY'}},
            {'field': "catid.1", 'component': "slicer"},
            {'field': "catgroup", 'component': "slicer"},
            {'field': "catname", 'component': "slicer"},
            {'field': "catdesc", 'component': "slicer"},
            {'field': "venueid.1", 'component': "range"},
            {'field': "venuename", 'component': "slicer"},
            {'field': "venuecity", 'component': "slicer"},
            {'field': "venuestate", 'component': "slicer"},
            {'field': "venueseats", 'component': "range"},
            {'field': "userid", 'component': "slicer"},
            {'field': "username", 'component': "slicer"},
            {'field': "firstname", 'component': "slicer"},
            {'field': "lastname", 'component': "slicer"},
            {'field': "city", 'component': "slicer"},
            {'field': "state", 'component': "slicer"},
            {'field': "email", 'component': "slicer"},
            {'field': "phone", 'component': "slicer"},
            {'field': "likesports", 'component': "slicer"},
            {'field': "liketheatre", 'component': "slicer"},
            {'field': "likeconcerts", 'component': "slicer"},
            {'field': "likejazz", 'component': "slicer"},
            {'field': "likeclassical", 'component': "slicer"},
            {'field': "likeopera", 'component': "slicer"},
            {'field': "likerock", 'component': "slicer"},
            {'field': "likevegas", 'component': "slicer"},
            {'field': "likebroadway", 'component': "slicer"},
            {'field': "likemusicals", 'component': "slicer"},
            {'field': "saletime_utc", 'component': "datePicker", 'props': {'func': 'DAY'}},
            {'field': "saletime_min_7", 'component': "datePicker", 'props': {'func': 'DAY'}},
            {'field': "saletime_plus_8", 'component': "datePicker", 'props': {'func': 'DAY'}},
        ]).set("showRowNumber", True).set("autoSizeColumns", True).limit(100).set("columnStats", {
            'enabled': True,
            'height': 70,
            'widgetProps': [
                {'field': 'salesid', 'props': {'color': histogramColor}},
                {'field': 'listid', 'props': {'color': histogramColor}},
                {'field': 'sellerid', 'props': {'color': histogramColor}},
                {'field': 'buyerid', 'props': {'color': histogramColor}},
                {'field': 'eventid', 'props': {'color': histogramColor}},
                {'field': 'dateid', 'props': {'color': histogramColor}},
                {'field': 'qtysold', 'props': {'color': histogramColor}},
                {'field': 'pricepaid', 'props': {'color': histogramColor}},
                {'field': 'commission', 'props': {'color': histogramColor}},
                {'field': 'saletime', 'props': {'color': histogramColor}},
                {'field': 'eventid.1', 'props': {'color': histogramColor}},
                {'field': 'venueid', 'props': {'color': histogramColor}},
                {'field': 'catid', 'props': {'color': histogramColor}},
                {'field': 'dateid.1', 'props': {'color': histogramColor}},
                {'field': 'eventname', 'props': {'color': histogramColor}},
                {'field': 'starttime', 'props': {'color': histogramColor}},
                {'field': 'catid.1', 'props': {'color': histogramColor}},
                {'field': 'catgroup', 'props': {'color': histogramColor}},
                {'field': 'catname', 'props': {'color': histogramColor}},
                {'field': 'catdesc', 'props': {'color': histogramColor}},
                {'field': 'venueid.1', 'props': {'color': histogramColor}},
                {'field': 'venuename', 'props': {'color': histogramColor}},
                {'field': 'venuecity', 'props': {'color': histogramColor}},
                {'field': 'venuestate', 'props': {'color': histogramColor}},
                {'field': 'venueseats', 'props': {'color': histogramColor}},
                {'field': 'userid', 'props': {'color': histogramColor}},
                {'field': 'username', 'props': {'color': histogramColor}},
                {'field': 'firstname', 'props': {'color': histogramColor}},
                {'field': 'lastname', 'props': {'color': histogramColor}},
                {'field': 'city', 'props': {'color': histogramColor}},
                {'field': 'state', 'props': {'color': histogramColor}},
                {'field': 'email', 'props': {'color': histogramColor}},
                {'field': 'phone', 'props': {'color': histogramColor}},
                {'field': 'likesports', 'props': {'color': histogramColor}},
                {'field': 'liketheatre', 'props': {'color': histogramColor}},
                {'field': 'likeconcerts', 'props': {'color': histogramColor}},
                {'field': 'likejazz', 'props': {'color': histogramColor}},
                {'field': 'likeclassical', 'props': {'color': histogramColor}},
                {'field': 'likeopera', 'props': {'color': histogramColor}},
                {'field': 'likerock', 'props': {'color': histogramColor}},
                {'field': 'likevegas', 'props': {'color': histogramColor}},
                {'field': 'likebroadway', 'props': {'color': histogramColor}},
                {'field': 'likemusicals', 'props': {'color': histogramColor}},
                {'field': 'saletime_utc', 'props': {'color': histogramColor}},
                {'field': 'saletime_min_7', 'props': {'color': histogramColor}},
                {'field': 'saletime_plus_8', 'props': {'color': histogramColor}}
            ]}).get_visualization_js_code()
        self.assertEqual(code, data.ROW_DATA_TABLE_STATS)

    def test_pivot_table(self):
        cf = CFToolkit()
        cf.provider(self.df)
        # Define metrics
        metric55 = Metric("count")
        metric552 = Metric("commission", "avg")
        metric553 = Metric("qtysold", "sum")
        # Add fields to data source
        myData55 = cf.rows("venuestate", "venuecity", "venuename").columns('catgroup', 'catname').metrics(
            metric55, metric552, metric553)
        # --- Define chart options and static filters ---
        code = myData55.graph("Pivot Table").limit(1000).set("autoSizeColumns", True).title(
            'Pivot Table Rows - Columns - Metrics').get_visualization_js_code()
        self.assertEqual(code, data.PIVOT_TABLE_RESULT)

    def test_comparative_kpi(self):
        cf = CFToolkit()
        cf.provider(self.df)
        filter62 = Filter('catname').label('Catname').operation('IN').value(["Plays"])
        filter621 = Filter('likemusicals').label('Likemusicals').operation('IN').value(["TRUE"])
        filter622 = Filter('eventname').label('Eventname').operation('IN').value(["All My Sons"])
        filter623 = Filter('saletime').label('Saletime').operation('BETWEEN').value(
            ["2008-04-01 00:00:00.000", "2008-07-31 23:59:59.999"])
        filter624 = Filter('catgroup').label('Catgroup').operation('IN').value(["Shows"])
        metric62 = Metric()
        rate62 = CompareMetric().rate().using('eventname').label('Rate')
        # Add metrics and groups to data source
        myData62 = cf.metrics(metric62, rate62)
        myData62.filter(filter62)
        myData62.filter(filter621)
        myData62.filter(filter622)
        myData62.filter(filter623)
        myData62.filter(filter624)
        code = myData62.graph("KPI").set("mainTextSize", 10).set("secondaryTextSize", 10).set("spacing", 10).set(
            "labelTextSize", 5).set("diff", False).get_visualization_js_code()
        self.assertEqual(code, data.COMPARATIVE_KPI)

    def test_multimetric_bars_comparative(self):
        cf = CFToolkit()
        cf.provider(self.df)
        filter63 = Filter('catname').label('Catname').operation('IN').value(["Plays"])
        filter631 = Filter('likemusicals').label('Likemusicals').operation('IN').value(["TRUE"])
        filter632 = Filter('eventname').label('Eventname').operation('IN').value(["All My Sons"])
        filter633 = Filter('saletime').label('Saletime').operation('BETWEEN').value(
            ["2008-04-01 00:00:00.000", "2008-07-31 23:59:59.999"])
        filter634 = Filter('catgroup').label('Catgroup').operation('IN').value(["Shows"])
        metric63 = Metric()
        benchrate63 = CompareMetric().rate().using('likemusicals').label('Like Musicals rate').benchmark('avg').against(
            'eventname').label('Avg event in the group')
        # Define attributes to group by
        group63 = Attribute("catgroup").limit(10).sort("desc", metric63)
        # Add metrics and groups to data source
        myData63 = cf.groupby(group63).metrics(benchrate63)
        # Define Grid
        grid63 = Grid().top(10).right(15).bottom(35).left(65)
        # Define Color Palette
        color63 = Color().palette(["#4b9864", "#007896"])

        myData63.filter(filter63)
        myData63.filter(filter631)
        myData63.filter(filter632)
        myData63.filter(filter633)
        myData63.filter(filter634)

        code = myData63.graph("Multimetric Bars").set("grid", grid63).set('placement', 'clustered').set("color", color63).set(
            "dataZoom", False).get_visualization_js_code()
        self.assertEqual(code, data.MULTIMETRIC_BARS_COMPARATIVE_RESULT)

    def test_multimetric_bars_comparative2(self):
        cf = CFToolkit()
        cf.provider(self.df)
        filter64 = Filter('likemusicals').label('likemusicals').operation('IN').value(["TRUE"])
        filter642 = Filter('eventname').label('eventname').operation('IN').value(
            ["A Doll's House", "A Bronx Tale", "At The Gates", "A Streetcar Named Desire"])
        filter643 = Filter('saletime').label('saletime').operation('BETWEEN').value(
            ["2008-02-23 00:00:00.000", "2008-02-23 23:59:59.999"])
        # Define metrics
        metric64 = Metric()
        benchrate64 = CompareMetric().rate().using('likemusicals').label('Like Musicals rate').benchmark('avg').against(
            'eventname').label('Avg event in the group')
        # Define attributes to group by
        group64 = Attribute("catgroup").limit(10).sort("desc", metric64)
        # Add metrics and groups to data source
        myData64 = cf.groupby(group64).metrics(benchrate64)
        # Define chart options
        # Define Grid
        grid64 = Grid().top(10).right(15).bottom(35).left(65)
        # Define Color Palette
        color64 = Color().palette(["#4b9864", "#007896"])

        myData64.filter(filter64)
        myData64.filter(filter642)
        myData64.filter(filter643)

        code = myData64.graph("Multimetric Bars").set("grid", grid64).set('placement', 'clustered').set("color", color64).set(
            "dataZoom", False).onlyWithFilters({
            'filter': 'likemusicals',  # required
            'andFilters': [{'filter': 'eventname'}]
        }).get_visualization_js_code()
        self.assertEqual(code, data.MULTIMETRIC_BARS_COMPARATIVE_RESULT2)

    def test_bars_with_metadata(self):
        cf = CFToolkit()
        cf.provider(self.df)
        filter67 = Filter('saletime').label('Sale Time').operation('BETWEEN').value(
            ["2008-01-01 01:00:00.000", "2008-01-31 23:59:59.999"])
        # Define metrics
        metric67 = Metric("commission", "sum")
        rate67 = CompareMetric("commission", "sum").rate().using('catname', 'state_str').label('Rate')
        # Define attributes to group by
        group67 = Attribute("cat_str").limit(10).sort("desc", "cat_str")
        group672 = Attribute("state_str").limit(100).sort("desc", "state_str")
        # Add metrics and groups to data source
        myData67 = cf.groupby(group67, group672).metrics(metric67, rate67)
        myData67.metadata(data.METADATA_STANDARD)
        # Define chart options
        # Define Grid
        grid67 = Grid().top(10).right(15).bottom(35).left(65)
        # Define Color Palette
        color67 = Color().palette(
            ["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b",
             "#ff6b30", "#e94d29", "#005b76"])
        myData67.filter(filter67)
        code = myData67.graph("Bars").set("grid", grid67).set("color", color67).set("placement", "stacked").set("dataZoom", False).get_visualization_js_code()
        self.assertEqual(code, data.BARS_WITH_METADATA)
