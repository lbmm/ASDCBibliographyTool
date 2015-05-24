% include header_template.tpl css_array=[], js_array=['https://www.google.com/jsapi'], username=False

<script type="text/javascript">

      // histogramm visualization

      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart_histogram);


      function drawChart_histogram() {
        var data = google.visualization.arrayToDataTable([
          % refereed_tot = 0
          % not_refereed_tot=0
          ['Year', 'Refereed', 'Non-refereed']
           % for f in histogram_year:
          ,["{{f['year']}}", {{f['refeered']}}, {{f['not_refeered']}}]
          % refereed_tot = int(f['refeered']) + refereed_tot
          % not_refereed_tot =  int(f['not_refeered']) + not_refereed_tot
          %end
        ]);

        var options = {
          title: 'Publications',
          width: 850,
	  height: 300,
          chartArea: {left:50}, 
          hAxis: {title: 'Year', titleTextStyle: {color: 'red'}}
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() { 
        var selection = chart.getSelection();
        var sel = selection[0]
        var row = sel.row
        var column = sel.column
        var selected_year =  data.getFormattedValue(row, 0)
        var location = "/detail_by_year?year=" + selected_year;
        if ( column == 1){
          location +=  "&is_refeered=True"; 
           } else {
           location+=  "&is_refeered=False"; 
        }
      

        window.location = location;
        
         });


        }
        // end of histogram

</script>


<div id="Content">

<h1>ASDC publications overview</h1>

<table>
   <tr>
     <td colspan="2">
      <i>ASDC Refereed publications total : {{refereed_tot}}
     <br>
     ASDC Non-refereed publications total : {{not_refereed_tot}} </i>
     </td>
   </tr>
   <tr >
     <td> 
       <div id="chart_div" align="left" style="width: 900px; height: 400px;"></div>
     </td>
   </tr>
</table>

</div>

% include public_menu.tpl
