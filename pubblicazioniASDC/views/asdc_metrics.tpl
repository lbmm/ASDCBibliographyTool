%setdefault('username', False)
%setdefault('is_admin', False)

% include header_template.tpl css_array=[], js_array=['https://www.google.com/jsapi',], username=username


<script type="text/javascript">


      google.load('visualization', '1.1', {'packages':['annotationchart']});
      google.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('date', 'Date');
        data.addColumn('number', 'Refereed');
        data.addColumn('string', 'Refereed title');
        data.addColumn('string', 'Refereed text');
        data.addColumn('number', 'Non-refereed');
        data.addColumn('string', 'Non-refereed title');
        data.addColumn('string', 'Non-refeered text');
        data.addRows([
           % for f in histogram_year:
           [new Date({{f['year']}}, {{f['month']}}, 01),
             % if 'refeered' in f:
              {{f['refeered']}},
             %else:
             0,
             %end
             undefined, undefined,
             %if 'not_refeered' in f:
               {{f['not_refeered']}},
             %else:
               0,
             %end
               undefined, undefined],
           % end
        ]);



        var chart = new google.visualization.AnnotationChart(document.getElementById('chart_div'));

        var options = {
          displayAnnotations: false,
          displayZoomButtons: false
        };

        chart.draw(data, options);
      }






  </script>



<div id="Content">
<h1>ASDC Statistics</h1>

 <div id='chart_div' style='width: 800px; height: 400px;'></div>

</div>

% include common_footer.tpl  username=username, is_admin=is_admin
