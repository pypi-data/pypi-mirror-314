class GetVisualizationJsCodeData(object):
    def __init__(self):
        pass

    AREA_LINE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("catdesc")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("saletime")
	.limit(1000)
	.sort("asc", "saletime")
	.func("MONTH")
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(65)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Area Line")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", true)
	.element("visualization0")
	.execute();
"""
    STACKED_BAR_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
// Define attributes to group by
let group0 = cf.Attribute("city")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(35)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Bars")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", false)
	.set("serieLabel", {"show": true, "formatter": "BigNumber"})
	.element("visualization0")
	.execute();
"""
    BOX_PLOT_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "percentiles");
// Define attributes to group by
let group0 = cf.Attribute("catdesc")
	.limit(10)
	.sort("desc", "catdesc")
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(80)
	.left(100);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Box Plot")
	.set("grid", grid)
	.set("xAxis", {"nameGap": 40})
	.set("yAxis", {"nameGap": 80})
	.element("visualization0")
	.execute();
"""
    BARS_SERIE_LABEL = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("venuestate")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("venuecity")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(35)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Bars")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", false)
	.set("legend", "right")
	.set("serieLabel", {"show": true})
	.element("visualization0")
	.execute();
"""
    DEFAULT_GAUGE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
// Add metrics and groups to data source
let myData = source
	.metrics(metric0);

myData.graph("Gauge")
	.element("visualization0")
	.execute();
"""
    ADVANCE_GAUGE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "avg");
let metric1 = cf.Metric("pricepaid", "avg");
let metric2 = cf.Metric("count");
// Define Color Palette
let color = cf.Color()
	.palette("intense")
	.theme({"font": "white", "background": "#3e4953", "header": "#4e5861", "rowOdd": "#1b242c", "rowEven": "#38424a", "headerFont": "#52c7da"});
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1,metric2);

myData.graph("Gauge")
	.set("ranges", [[0, 200], [0, 800], [0, 1000]])
	.set("radius", ["80%", "40%", "80%"])
	.set("color", color)
	.set("angles", [[180, 0], [225, -45], [180, 0]])
	.set("rangeColors", [[[0.02, "lime"], [0.5, "#1e90ff"], [0.7, "#ff4500"], [0.8, "yellow"], [1, "orange"]], [[0.5, "red"], [1, "yellow"]], [[0.5, "black"], [1, "blue"]]])
	.set("layout", [["25%", "80%"], ["50%", "30%"], ["75%", "80%"]])
	.set("lineWidth", [5, 13, 20])
	.element("visualization0")
	.execute();
"""
    DEFAULT_KPI_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
// Add metrics and groups to data source
let myData = source
	.metrics(metric0);

myData.graph("KPI")
	.set("mainTextSize", 12)
	.set("secondaryTextSize", 12)
	.set("diffTextSize", 12)
	.set("labelTextSize", 8)
	.element("visualization0")
	.execute();
"""
    STACKED_BAR_4_SUBCATEGORIES_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("venuestate")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("catname")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(35)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Bars")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", false)
	.set("legend", "right")
	.set("serieLabel", {"show": true})
	.element("visualization0")
	.execute();
"""
    MULTIMETRIC_TREND_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
let metric1 = cf.Metric("qtysold", "sum");
let metric2 = cf.Metric("venueseats", "sum");
// Define attributes to group by
let group0 = cf.Attribute("saletime")
	.limit(1000)
	.sort("asc", "saletime")
	.func("DAY")
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(65)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1,metric2)
	.groupby(group0);

myData.graph("Multimetric Trend")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", true)
	.element("visualization0")
	.execute();
"""
    HORIZONTAL_STACKED_BARS_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("venuestate")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("venuecity")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(35)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Bars")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", false)
	.set("orientation", "horizontal")
	.set("yAxis", {"text": "out"})
	.set("serieLabel", {"show": true})
	.element("visualization0")
	.execute();
"""
    SCATTER_PLOT_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
let metric1 = cf.Metric("qtysold", "sum");
let metric2 = cf.Metric("venueseats", "sum");
// Define attributes to group by
let group0 = cf.Attribute("state")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1,metric2)
	.groupby(group0);

myData.graph("Scatter Plot")
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    TREE_MAP_2D_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("catdesc")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("catgroup")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Tree Map 2D")
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    CLUSTERED_BARS_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("venuestate")
	.limit(5)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("venuecity")
	.limit(2)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(35)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Bars")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", false)
	.set("placement", "clustered")
	.set("serieLabel", {"show": true, "formatter": "BigNumber"})
	.element("visualization0")
	.execute();
"""
    FLOATING_BUBBLES_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
let metric1 = cf.Metric("qtysold", "sum");
let metric2 = cf.Metric("venueseats", "sum");
// Define attributes to group by
let group0 = cf.Attribute("firstname")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("catdesc")
	.limit(10)
	.sort("desc", cf.Metric("qtysold", "sum" ))
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1,metric2)
	.groupby(group0,group1);

myData.graph("Floating Bubbles")
	.element("visualization0")
	.execute();
"""
    GEO_MAP_PIVOT_QUERY_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("count");
let metric1 = cf.Metric("fare", "sum");
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1)
	.rows(
		cf.Row("dropoff_latitude"),
		cf.Row("dropoff_longitude"),
		cf.Row("dropoff_community_area_desc")
	);

myData.graph("Geo Map")
	.limit(200)
	.set("tileLayers", {"Base": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", "attribution": "Map data &copy; <a href=\\"https://www.openstreetmap.org/\\">OpenStreetMap</a> contributors, <a href=\\"https://creativecommons.org/licenses/by-sa/2.0/\\">CC-BY-SA</a>"})
	.set("center", [41.82199022070215, -87.7687454223633])
	.set("zoom", 11)
	.element("visualization0")
	.execute();
"""
    GEO_MAP_GEO_HASH_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("count");
// Add metrics and groups to data source
let myData = source
	.metrics(metric0);

myData.graph("Geo Map")
	.limit(10000)
	.location("dropoff_location")
	.precision(5)
	.set("precisionLevels", {"raw": {"zoom": 16, "fields": ["dropoff_latitude", "dropoff_longitude"]}, "levels": [{"zoom": 6, "precision": 4}, {"zoom": 10, "precision": 5}, {"zoom": 13, "precision": 8}, {"zoom": 15, "precision": 11}]})
	.set("geohashMarkerHtml", function(value){
          return `<img
                  class="icon-image"
                  style="width: 34px !important; height: 34px !important;"
                  src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAIAAACRXR/mAAAABmJLR0QA/wD/AP+gvaeTAAAE5klEQVRYhe2YW2xURRjH/9+cy+52r0CvFuhVKhYM8UGUQLzEoBLCg8TEaCQxRh+MMSY8+uCLifKivhj1TVATjTGNRg1GiSBRAyEiSImF0rvtblvavffcZj4fKt3tUtpuIUjC/l/OmTPz/87vzHwzc84hZsatJ/F/AyysClY5qmCVowpWOapglaMKVjm6HbCUx1aq9CLLK7X52cNyIunXi8IsL/0o//xEDhzj1DAA6H6xuk3r2K1t2Sdq74achDuBQCenD1PsSc7+RqHtYAdkLhL1unpLxc9aH221Dz7mnfkUuYQWq9GqG7VwhJOX3OMHrPfvcbpeYCvNyc/hDCN/El4C2Z8B5mTX4pFpxe9b8nyX/eUz8CwRXmWs79Bi1QAViDPT7vAFOT0u1rQbO8Ki+RVOf0fBB8Ae9HqAafU+zp+g4LYbiSX7jtgHH4fyjLV3Gus7QLRgM2+s3+nrpqBp7tpCPgaZMJthX6TGAzz1mah9Ff5NUBaEv8S4kkHkmSnni6ehPGNtu9F017WYAOgNLWZrJ+ds9/cegME27B6AOfE26atABicOQE5fbVwJlnv0Tc5PiqqIsa6jCFaxY6lciu0ZqMJ00xtatFiNGkmqRHquKbzLbPepoRcpuhtGw5VJWvQ8S0LI7q/cX95S8TPQ/dqGXcbDb8jTHwPQ17ZDCPYcLz4kpxMqM41CPpAIRbVVNXpdE/kCxroNMjnh9YybdZFCXGeQQg9ysgvyIFW/BF978U2XyC3v13ecw/sBkGGy6wIMzYB0IUTgvp3eSK871g8pr+knodeuM5o3WqePsnL8T90Lbd6IU3QP1e6HCJT6FsHi1PDMu+1E7Ou8X4RiKpe2u39n15mlJNOvculSjxAUNImgMhauBCZfFYjYypl7NotIUXaTBr0eZFD4EYrthV4zV7PYIMqebyEdrbFVBGPeaJ872jfLBIBdZ+58npTijIWQT9tQJyI+zrtqIqMu5yEVAMw4KMZiSUYD1b8Oo7EkzGJYbGcAQLHTf84b61+kZakxa8uehCSIuojWXms8FOWUpSay8BsA4CmVtUEQYT/nT/HAsxR5gmJ7i9NrYSxODan4Wc6OAfASg+BlbWRXRYGKp1U8LRqixrYWvSYEQF4Yd08NQTEAMjVt0x5j5wcUrCuxluaWSpxzv39N9h1ZCUdJ6IChtVaL1moRNNVoSsbT+sZ6CLK/OQtZuCnFmv3P/0Sr266JpQaPW4d2wcmKyBqjsVUEo+w5Kj3ljvSyYy0XR5BojOlt1Qj5eCwtR5Mqkfmve6pM49EO2Tshz8fnOeo2+1/+A6IwdAUstpLWex2cG9fvaDGbN83ubzI1KRPDMj3FdumKtwBPNCBa11CVqS7n1EiSs/bVbchvGDva3GMX2Zm3rJh7D+lbnpsrFgC9kx9yblyEomZLJwAwO71nvPHhJWnI1KgmTAGDbdf7axTeYonIluse76WGKA9OFV+Xf3+9MJbq/QGAXt80+yLg9HcvzaRpFKiCrql/kkvSF5F5PFK6D/L0QHGxgMWZMQAiEAag8hlvbABLSkrOZpYPVGQsXcPJHy0uFrZqijQCmE1tOTkK3NT/XmLt1uJiIeXVyAlODpE7DS/NZjW04E3FatpO4YYFsG4p3Q4fZDdOFaxyVMEqRxWsclTBKkcVrHJUwSpHtyjWv3ZmSTCYpkOiAAAAAElFTkSuQmCC"
                  />`;
        }
        )
	.set("tileLayers", [{"Base": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", "attribution": "Map data &copy; <a href=\\"https://www.openstreetmap.org/\\">OpenStreetMap</a> contributors, <a href=\\"https://creativecommons.org/licenses/by-sa/2.0/\\">CC-BY-SA</a>"}])
	.set("center", [41.766190406938684, -87.73475646972658])
	.set("zoom", 10)
	.element("visualization0")
	.execute();
"""
    NESTED_PIE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("catgroup")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("catdesc")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Nested Pie")
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    MULTIMETRIC_BARS_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
let metric1 = cf.Metric("qtysold", "sum");
let metric2 = cf.Metric("venueseats", "sum");
// Define attributes to group by
let group0 = cf.Attribute("state")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1,metric2)
	.groupby(group0);

myData.graph("Multimetric Bars")
	.set("color", color)
	.set("placement", "stacked")
	.set("dataZoom", false)
	.element("visualization0")
	.execute();
"""
    SANKEY_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(160)
	.bottom(10)
	.left(10);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.rows(
		cf.Row("firstname"),
		cf.Row("lastname")
	);

myData.graph("Sankey")
	.limit(50)
	.set("grid", grid)
	.element("visualization0")
	.execute();
"""
    DONUT_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("email")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Donut")
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    HORIZONTAL_CLUSTERED_BARS = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("venuestate")
	.limit(5)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("venuecity")
	.limit(2)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(35)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Bars")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", false)
	.set("placement", "clustered")
	.set("orientation", "horizontal")
	.set("yAxis", {"text": "out"})
	.set("serieLabel", {"show": true, "formatter": "BigNumber"})
	.element("visualization0")
	.execute();
"""
    DISK_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("easting_m", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("hour_of_call")
	.limit(24)
	.sort("asc", "hour_of_call")
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Disk")
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    HISTOGRAM_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "histogram");
// Add metrics and groups to data source
let myData = source
	.metrics(metric0);

myData.graph("Histogram")
	.set("serieLabel", true)
	.element("visualization0")
	.execute();
"""
    WORD_CLOUD_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
// Define attributes to group by
let group0 = cf.Attribute("state")
	.limit(30)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Word Cloud")
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    PIE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("email")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Pie")
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    MULTIMETRIC_STACKED_BARS_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
let metric1 = cf.Metric("pricepaid", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("eventname")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1)
	.groupby(group0);

myData.graph("Multimetric Bars")
	.set("color", color)
	.set("placement", "stacked")
	.set("dataZoom", false)
	.set("serieLabel", {"show": true})
	.element("visualization0")
	.execute();
"""
    TREE_MAP_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
// Define attributes to group by
let group0 = cf.Attribute("eventname")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Tree Map")
	.set("color", color)
	.set("serieLabel", {"show": true, "position": "insideTopLeft", "padding": 10})
	.element("visualization0")
	.execute();
"""
    BARS_AND_LINES_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
let metric1 = cf.Metric("qtysold", "sum");
// Define attributes to group by
let group0 = cf.Attribute("saletime")
	.limit(1000)
	.sort("asc", "saletime")
	.func("DAY")
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1)
	.groupby(group0);

myData.graph("Bars and Line")
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    PIE_METRIC_VALUE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("catname")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Pie")
	.set("color", color)
	.set("labelPosition", "inside")
	.set("metricValue", true)
	.element("visualization0")
	.execute();
"""
    MULTIMETRIC_AREA_LINE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
let metric1 = cf.Metric("qtysold", "sum");
let metric2 = cf.Metric("venueseats", "sum");
// Define attributes to group by
let group0 = cf.Attribute("saletime")
	.limit(1000)
	.sort("asc", "saletime")
	.func("DAY")
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(65)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1,metric2)
	.groupby(group0);

myData.graph("Multimetric Area Line")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", true)
	.element("visualization0")
	.execute();
"""
    PACKED_BUBBLES_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("eventname")
	.limit(50)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658"])
	.range([{"min": 0, "max": 30000, "color": "red"}, {"min": 30000, "max": 80000, "color": "gray"}, {"min": 80000, "max": 200000, "color": "blue"}]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Packed Bubbles")
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    HEAT_MAP_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum")
	.hideFunction();
// Define attributes to group by
let group0 = cf.Attribute("catdesc")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("catgroup")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(10)
	.bottom(10)
	.left(10);
let metricColor = cf.Metric("commission", "sum");
// Define Color Palette
let color = cf.Color()
	.metric(metricColor);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Heat Map")
	.set("grid", grid)
	.set("color", color)
	.set("showValues", true)
	.element("visualization0")
	.execute();
"""
    VECTOR_MAP_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
// Define attributes to group by
let group0 = cf.Attribute("catdesc")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let metricColor = cf.Metric("commission", "sum");
// Define Color Palette
let color = cf.Color()
	.metric(metricColor);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0);

myData.graph("Vector Map")
	.set("shape", "world")
	.set("min", 0)
	.set("zoom", 1.030328968347247)
	.set("center", [14.531024917022904, 24.607267038606977])
	.set("color", color)
	.element("visualization0")
	.execute();
"""
    TREE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("pricepaid", "sum")
	.hideFunction();
// Define Grid
let grid = cf.Grid()
	.top("5%")
	.right("40%")
	.bottom("5%")
	.left("15%");
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.rows(
		cf.Row("catdesc")
	);

myData.graph("Tree")
	.limit(1000)
	.set("grid", grid)
	.element("visualization0")
	.execute();
"""
    RANGE_FILTER_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
let metric1 = cf.Metric("qtysold", "sum");
let metric2 = cf.Metric("venueseats", "sum");
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1,metric2);

myData.graph("Range Filter")
	.element("visualization0")
	.execute();
"""
    RADAR_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
let metric1 = cf.Metric("qtysold", "sum");
let metric2 = cf.Metric("venueseats", "sum");
// Define attributes to group by
let group0 = cf.Attribute("catdesc")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1,metric2)
	.groupby(group0);

myData.graph("Radar")
	.element("visualization0")
	.execute();
"""
    TIME_RANGE_PICKER = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Add metrics and groups to data source
let myData = source
	.metrics();

myData.graph("Time Range Picker")
	.timeField(cf.Attribute("saletime")
	.limit(100)
	.func("YEAR"))
	.element("visualization0")
	.execute();
"""
    TREND_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "sum");
// Define attributes to group by
let group0 = cf.Attribute("catdesc")
	.limit(10)
	.sort("desc", cf.Metric("commission", "sum" ))
let group1 = cf.Attribute("saletime")
	.limit(1000)
	.sort("asc", "saletime")
	.func("DAY")
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(65)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.groupby(group0,group1);

myData.graph("Trend")
	.set("grid", grid)
	.set("color", color)
	.set("dataZoom", true)
	.element("visualization0")
	.execute();
"""
    SUNBURST_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("count");
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.rows(
		cf.Row("catdesc")
	);

myData.graph("Sunburst")
	.limit(1000)
	.element("visualization0")
	.execute();
"""
    MULTIGROUP_TREND = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("commission", "avg");
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(65)
	.left(65);
// Add metrics and groups to data source
let myData = source
	.metrics(metric0)
	.rows(
		cf.Row("saletime").func("MONTH"),
		cf.Row("catdesc")
	);

myData.graph("Multigroup Trend")
	.limit(10000)
	.set("grid", grid)
	.element("visualization0")
	.execute();
"""
    ROW_DATA_TABLE_STATS = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define Color Palette
let color = cf.Color()
	.theme({"headerStyle": "background: #009688; color: #fff; font-size: 16px;", "headerIconStyle": "color: #fff; font-size: 16px;", "rowOddStyle": "background: #fff; color: #000;", "rowEvenStyle": "background: #e0f2f1; color: #000;", "headerResizeLineStyle": "border-right-color: #fff; border-right-width: 1px;", "headerHorizontalLineStyle": "border-bottom-color: #fff; border-bottom-width: 1px;", "tpButtonActive": "color: #fff; background: #009688;", "cellMoving": "color: black; background: #80cbc4;"});
// Add metrics and groups to data source
let myData = source
	.metrics()
	.fields(...[
cf.Field("salesid", "salesid"),
cf.Field("listid", "listid"),
cf.Field("sellerid", "sellerid"),
cf.Field("buyerid", "buyerid"),
cf.Field("eventid", "eventid"),
cf.Field("dateid", "dateid"),
cf.Field("qtysold", "qtysold"),
cf.Field("pricepaid", "pricepaid"),
cf.Field("commission", "commission"),
cf.Field("saletime", "saletime"),
cf.Field("eventid.1", "eventid.1"),
cf.Field("venueid", "venueid"),
cf.Field("catid", "catid"),
cf.Field("dateid.1", "dateid.1"),
cf.Field("eventname", "eventname"),
cf.Field("starttime", "starttime"),
cf.Field("catid.1", "catid.1"),
cf.Field("catgroup", "catgroup"),
cf.Field("catname", "catname"),
cf.Field("catdesc", "catdesc"),
cf.Field("venueid.1", "venueid.1"),
cf.Field("venuename", "venuename"),
cf.Field("venuecity", "venuecity"),
cf.Field("venuestate", "venuestate"),
cf.Field("venueseats", "venueseats"),
cf.Field("userid", "userid"),
cf.Field("username", "username"),
cf.Field("firstname", "firstname"),
cf.Field("lastname", "lastname"),
cf.Field("city", "city"),
cf.Field("state", "state"),
cf.Field("email", "email"),
cf.Field("phone", "phone"),
cf.Field("likesports", "likesports"),
cf.Field("liketheatre", "liketheatre"),
cf.Field("likeconcerts", "likeconcerts"),
cf.Field("likejazz", "likejazz"),
cf.Field("likeclassical", "likeclassical"),
cf.Field("likeopera", "likeopera"),
cf.Field("likerock", "likerock"),
cf.Field("likevegas", "likevegas"),
cf.Field("likebroadway", "likebroadway"),
cf.Field("likemusicals", "likemusicals"),
cf.Field("saletime_utc", "saletime_utc"),
cf.Field("saletime_min_7", "saletime_min_7"),
cf.Field("saletime_plus_8", "saletime_plus_8")]);

myData.graph("Raw Data Table")
	.limit(100)
	.set("color", color)
	.set("columnFilters", [{"field": "salesid", "component": "slicer"}, {"field": "listid", "component": "slicer"}, {"field": "sellerid", "component": "slicer"}, {"field": "buyerid", "component": "slicer"}, {"field": "eventid", "component": "slicer"}, {"field": "dateid", "component": "slicer"}, {"field": "qtysold", "component": "slicer"}, {"field": "pricepaid", "component": "range"}, {"field": "commission", "component": "range"}, {"field": "saletime", "component": "datePicker", "props": {"func": "DAY"}}, {"field": "eventid.1", "component": "slicer"}, {"field": "venueid", "component": "slicer"}, {"field": "catid", "component": "slicer"}, {"field": "dateid.1", "component": "slicer"}, {"field": "eventname", "component": "slicer"}, {"field": "starttime", "component": "datePicker", "props": {"func": "DAY"}}, {"field": "catid.1", "component": "slicer"}, {"field": "catgroup", "component": "slicer"}, {"field": "catname", "component": "slicer"}, {"field": "catdesc", "component": "slicer"}, {"field": "venueid.1", "component": "range"}, {"field": "venuename", "component": "slicer"}, {"field": "venuecity", "component": "slicer"}, {"field": "venuestate", "component": "slicer"}, {"field": "venueseats", "component": "range"}, {"field": "userid", "component": "slicer"}, {"field": "username", "component": "slicer"}, {"field": "firstname", "component": "slicer"}, {"field": "lastname", "component": "slicer"}, {"field": "city", "component": "slicer"}, {"field": "state", "component": "slicer"}, {"field": "email", "component": "slicer"}, {"field": "phone", "component": "slicer"}, {"field": "likesports", "component": "slicer"}, {"field": "liketheatre", "component": "slicer"}, {"field": "likeconcerts", "component": "slicer"}, {"field": "likejazz", "component": "slicer"}, {"field": "likeclassical", "component": "slicer"}, {"field": "likeopera", "component": "slicer"}, {"field": "likerock", "component": "slicer"}, {"field": "likevegas", "component": "slicer"}, {"field": "likebroadway", "component": "slicer"}, {"field": "likemusicals", "component": "slicer"}, {"field": "saletime_utc", "component": "datePicker", "props": {"func": "DAY"}}, {"field": "saletime_min_7", "component": "datePicker", "props": {"func": "DAY"}}, {"field": "saletime_plus_8", "component": "datePicker", "props": {"func": "DAY"}}])
	.set("showRowNumber", true)
	.set("autoSizeColumns", true)
	.set("columnStats", {"enabled": true, "height": 70, "widgetProps": [{"field": "salesid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "listid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "sellerid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "buyerid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "eventid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "dateid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "qtysold", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "pricepaid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "commission", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "saletime", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "eventid.1", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "venueid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "catid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "dateid.1", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "eventname", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "starttime", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "catid.1", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "catgroup", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "catname", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "catdesc", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "venueid.1", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "venuename", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "venuecity", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "venuestate", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "venueseats", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "userid", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "username", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "firstname", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "lastname", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "city", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "state", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "email", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "phone", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "likesports", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "liketheatre", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "likeconcerts", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "likejazz", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "likeclassical", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "likeopera", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "likerock", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "likevegas", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "likebroadway", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "likemusicals", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "saletime_utc", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "saletime_min_7", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}, {"field": "saletime_plus_8", "props": {"color": cf.Color().theme({"background": "#e0f2f1"})}}]})
	.element("visualization0")
	.execute();
"""
    PIVOT_TABLE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define metrics
let metric0 = cf.Metric("count");
let metric1 = cf.Metric("commission", "avg");
let metric2 = cf.Metric("qtysold", "sum");
// Add metrics and groups to data source
let myData = source
	.metrics(metric0,metric1,metric2)
	.rows(
		cf.Row("venuestate"),
		cf.Row("venuecity"),
		cf.Row("venuename")
	)
	.columns(
		cf.Column("catgroup"),
		cf.Column("catname")
	);

myData.graph("Pivot Table")
	.limit(1000)
	.set("autoSizeColumns", true)
	.element("visualization0")
	.execute();
"""
    COMPARATIVE_KPI = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define filters
let filter0 = cf.Filter("catname")
	.label("Catname")
	.operation("IN")
	.value(["Plays"]);
let filter1 = cf.Filter("likemusicals")
	.label("Likemusicals")
	.operation("IN")
	.value(["TRUE"]);
let filter2 = cf.Filter("eventname")
	.label("Eventname")
	.operation("IN")
	.value(["All My Sons"]);
let filter3 = cf.Filter("saletime")
	.label("Saletime")
	.operation("BETWEEN")
	.value(["2008-04-01 00:00:00.000", "2008-07-31 23:59:59.999"]);
let filter4 = cf.Filter("catgroup")
	.label("Catgroup")
	.operation("IN")
	.value(["Shows"]);
// Define metrics
let metric0 = cf.Metric("count");
let cMetric0 = cf.CompareMetric()
	.rate()
	.using("eventname")
	.label("Rate");
// Add metrics and groups to data source
let myData = source
	.filters(filter0,filter1,filter2,filter3,filter4)
	.metrics(metric0,cMetric0);

myData.graph("KPI")
	.set("mainTextSize", 10)
	.set("secondaryTextSize", 10)
	.set("spacing", 10)
	.set("labelTextSize", 5)
	.set("diff", false)
	.element("visualization0")
	.execute();
"""
    MULTIMETRIC_BARS_COMPARATIVE_RESULT = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define filters
let filter0 = cf.Filter("catname")
	.label("Catname")
	.operation("IN")
	.value(["Plays"]);
let filter1 = cf.Filter("likemusicals")
	.label("Likemusicals")
	.operation("IN")
	.value(["TRUE"]);
let filter2 = cf.Filter("eventname")
	.label("Eventname")
	.operation("IN")
	.value(["All My Sons"]);
let filter3 = cf.Filter("saletime")
	.label("Saletime")
	.operation("BETWEEN")
	.value(["2008-04-01 00:00:00.000", "2008-07-31 23:59:59.999"]);
let filter4 = cf.Filter("catgroup")
	.label("Catgroup")
	.operation("IN")
	.value(["Shows"]);
let cMetric0 = cf.CompareMetric()
	.rate()
	.using("likemusicals")
	.label("Like Musicals rate")
	.benchmark("avg")
	.against("eventname")
	.label("Avg event in the group");
// Define attributes to group by
let group0 = cf.Attribute("catgroup")
	.limit(10)
	.sort("desc", cf.Metric())
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(35)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#4b9864", "#007896"]);
// Add metrics and groups to data source
let myData = source
	.filters(filter0,filter1,filter2,filter3,filter4)
	.metrics(cMetric0)
	.groupby(group0);

myData.graph("Multimetric Bars")
	.set("grid", grid)
	.set("placement", "clustered")
	.set("color", color)
	.set("dataZoom", false)
	.element("visualization0")
	.execute();
"""
    MULTIMETRIC_BARS_COMPARATIVE_RESULT2 = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define filters
let filter0 = cf.Filter("likemusicals")
	.label("likemusicals")
	.operation("IN")
	.value(["TRUE"]);
let filter1 = cf.Filter("eventname")
	.label("eventname")
	.operation("IN")
	.value(["A Doll's House", "A Bronx Tale", "At The Gates", "A Streetcar Named Desire"]);
let filter2 = cf.Filter("saletime")
	.label("saletime")
	.operation("BETWEEN")
	.value(["2008-02-23 00:00:00.000", "2008-02-23 23:59:59.999"]);
let cMetric0 = cf.CompareMetric()
	.rate()
	.using("likemusicals")
	.label("Like Musicals rate")
	.benchmark("avg")
	.against("eventname")
	.label("Avg event in the group");
// Define attributes to group by
let group0 = cf.Attribute("catgroup")
	.limit(10)
	.sort("desc", cf.Metric())
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(35)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#4b9864", "#007896"]);
// Add metrics and groups to data source
let myData = source
	.filters(filter0,filter1,filter2)
	.metrics(cMetric0)
	.groupby(group0);

myData.graph("Multimetric Bars")
	.set("grid", grid)
	.set("placement", "clustered")
	.set("color", color)
	.set("dataZoom", false)
	.onlyWithFilters({"filter": "likemusicals", "andFilters": [{"filter": "eventname"}]})
	.element("visualization0")
	.execute();
"""
    BARS_WITH_METADATA = """/* Configuration code for this widget */
let provider = cf.provider("Aktiun Pandas");
let source = provider.source("");
// Define filters
let filter0 = cf.Filter("saletime")
	.label("Sale Time")
	.operation("BETWEEN")
	.value(["2008-01-01 01:00:00.000", "2008-01-31 23:59:59.999"]);
// Define metrics
let metric0 = cf.Metric("commission", "sum");
let cMetric0 = cf.CompareMetric("commission", "sum")
	.rate()
	.using("catname","state_str")
	.label("Rate");
// Define attributes to group by
let group0 = cf.Attribute("cat_str")
	.limit(10)
	.sort("desc", "cat_str")
let group1 = cf.Attribute("state_str")
	.limit(100)
	.sort("desc", "state_str")
// Define Grid
let grid = cf.Grid()
	.top(10)
	.right(15)
	.bottom(35)
	.left(65);
// Define Color Palette
let color = cf.Color()
	.palette(["#0095b7", "#a0b774", "#f4c658", "#fe8b3e", "#cf2f23", "#756c56", "#007896", "#47a694", "#f9a94b", "#ff6b30", "#e94d29", "#005b76"]);
// Add metrics and groups to data source
let myData = source
	.filters(filter0)
	.metrics(metric0,cMetric0)
	.groupby(group0,group1);

myData.graph("Bars")
	.set("grid", grid)
	.set("color", color)
	.set("placement", "stacked")
	.set("dataZoom", false)
	.element("visualization0")
	.execute();
"""

    METADATA_STANDARD = """
    let state = {
      'AL' : 'Alabama',
    	'AK' : 'Alaska',
    	'AZ' : 'Arizona',
    	'AR' : 'Arkansas',
    	'CA' : 'California',
    	'CO' : 'Colorado',
    	'CT' : 'Connecticut',
    	'DE' : 'Delaware',
    	'DC' : 'District of Columbia',
    	'FL' : 'Florida',
    	'GA' : 'Georgia',
    	'HI' : 'Hawaii',
    	'ID' : 'Idaho',
    	'IL' : 'Illinois',
    	'IN' : 'Indiana',
    	'IA' : 'Iowa',
    	'KS' : 'Kansas',
    	'KY' : 'Kentucky',
    	'LA' : 'Louisiana',
    	'ME' : 'Maine',
    	'MD' : 'Maryland',
    	'MA' : 'Massachusetts',
    	'MI' : 'Michigan',
    	'MN' : 'Minnesota',
    	'MS' : 'Mississippi',
    	'MO' : 'Missouri',
    	'MT' : 'Montana',
    	'NE' : 'Nebraska',
    	'NV' : 'Nevada',
    	'NH' : 'New Hampshire',
    	'NJ' : 'New Jersey',
    	'NM' : 'New Mexico',
    	'NY' : 'New York',
    	'NC' : 'North Carolina',
    	'ND' : 'North Dakota',
    	'OH' : 'Ohio',
    	'OK' : 'Oklahoma',
    	'OR' : 'Oregon',
    	'PA' : 'Pennsylvania',
    	'RI' : 'Rhode Island',
    	'SC' : 'South Carolina',
    	'SD' : 'South Dakota',
    	'TN' : 'Tennessee',
    	'TX' : 'Texas',
    	'UT' : 'Utah',
    	'VT' : 'Vermont',
    	'VA' : 'Virginia',
    	'WA' : 'Washington',
    	'WV' : 'West Virginia',
    	'WI' : 'Wisconsin',
    	'WY' : 'Wyoming'
    }

    let stateStr = {
      'name': 'state_str',
      'label': 'Venue State Name',
      'type': 'ATTRIBUTE',
      'dependencies': ['venuestate'],
      'reverse': (derived) => {
          let result = false;
          let index = Object.values(state).indexOf(derived)

          return Object.keys(state)[index];
      },
      'function': (venuestate) => {
            return state[venuestate] ? state[venuestate] : venuestate;
        }
    }

    let catStr = {
      'name': 'cat_str',
      'label': 'Category Str',
      'type': 'ATTRIBUTE',
      'dependencies': ['catname'],
      'reverse': (derived) => {
          return derived;
      },
      'function': (cat) => {
            return cat;
        }
    }
    let _META_ = {
        'ticket_sales': {    
            'fields': {
                'state_str': stateStr,
                'catgroup': {
                  label: 'Group'
                },
                'catname': {
                  label: 'Category Name'
                },
                'catdesc': {
                  'label': 'Category'
                },
                cat_str: catStr,
                'eventname': {
                  'label': 'Event'
                },
                'venuename': {
                  'label': 'Venue'
                },
                venuestate: {
                  label: 'Venue State'
                },
                'venuecity': {
                  label: 'Venue City'
                },
                'likerock': {
                  'label': "Likes Rock"
                },
                'saletime': {
                  'label': 'Sale Time'
                },
                'commission': {
                  'type': 'MONEY'
                },
                'pricepaid': {
                  'label': 'Price Paid',
                  'type': 'MONEY'
                },
                'qtysold': {
                  label: 'Quantity Sold'
                }
            }
        }
    }
    """




