try:
    from importlib.metadata import version
except ImportError:
    # Try backport to PY<37 `importlib_resources`.
    from importlib_metadata import version

version = version('chartfactor')


class HtmlTemplate(object):

    def __init__(self):
        self.google_font_1 = '<link href="https://fonts.gstatic.com" rel="preconnect" />'
        self.google_font_2 = '<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Nunito:300,300i,400,400i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet" />'
        self.bootstrap = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" />'
        self.iframe = """
            <iframe id={} name={} width=100% height={} frameborder=0 allow="clipboard-write *;" srcdoc='
                <!DOCTYPE html>
                <html lang="en">
                  <head>
                    <title>Charfactor visualization</title>
                    <meta charset="utf-8" />
            
                    <!-- Google Fonts -->
                    {}
                    {}
            
                    <!-- Bootstrap -->
                    {}
                    
                    <style type="text/css" media="screen">
                      {}
                    </style>
                    
                    <!-- CFT -->
                    <script src="https://chartfactor.com/cf/cft/""" + version + """/cftoolkit.min.js"></script>       
                    <script src="https://chartfactor.com/cf/cft/""" + version + """/cft-geo-charts.min.js"></script>       
                    <script src="https://chartfactor.com/cf/cft/""" + version + """/cft-pandas-dataframe-provider.min.js"></script>
                    <script src="https://chartfactor.com/cf/cft/""" + version + """/cft-standard-charts.min.js"></script>
                    <script src="https://chartfactor.com/cf/cft/""" + version + """/cft-tables-charts.min.js"></script>
                    <script src="https://chartfactor.com/cf/cft/""" + version + """/cft-interactive-charts.min.js"></script>
                  </head>
            
                  <body>
                    <main id="main" class="main">
                      <section class="section">
                        <div class="row" style="margin: 0px !important;">
                          <div class="col-12">
                            <div class="cf-card">
                              <div class="cf-card-body">
                                <h5 class="cf-card-title">{}</h5>
                                <div id="visualization{}" class="vis-container"></div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </section>
                    </main>                                
                  </body>
                  
                  <!-- Provider definitions -->
                  <script type="text/javascript">
                    // Metadata definitions
                    {} 
                    var _META_INFO_ = typeof(_META_) !== "undefined" ? _META_ : {{}}                
                    var AKT_PANDAS = {{
                        name: "Aktiun Pandas",
                        provider: "pandas-dataframe",
                        metadata: _META_INFO_
                    }};
                  </script>   
                  
                  <!-- Visualization definitions -->    
                  <script type="text/javascript">
                    var $ = cf.getDependency("jquery");
                    
                    cf.setProviders([
                      AKT_PANDAS
                    ]);
                    
                    var renderVisualization = () => {{
                        {}
                    }}                    
                    
                    $(document).ready(function() {{
                        renderVisualization();
                    }});
                  </script>                 
                   
                </html>
            '</iframe>
        """
