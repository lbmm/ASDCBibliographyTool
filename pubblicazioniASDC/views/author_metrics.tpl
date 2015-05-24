%setdefault('username', False)
%setdefault('is_admin', False)

% include header_template.tpl css_array=[], js_array=['https://www.google.com/jsapi',], username=username


<script type="text/javascript">


      //piece for the pie chart visualization
      google.load("visualization", "1", {packages:["corechart"]});
      google.load("visualization", "1", {packages:["timeline"]});
      google.setOnLoadCallback(drawChart_refeered);
      google.setOnLoadCallback(drawChart_not_refeered);
      % if histogram_year:
      google.setOnLoadCallback(drawChart_histogram);
      %end



      function drawChart_refeered() {

         var data = google.visualization.arrayToDataTable([
          ['year', 'how many articles published']
          % for f in refeered_count:
          ,["{{!f['author']}}", {{f['count']}}]
          %end

        ]);

        %title = 'ASDC Refeered Publications'

        var options = {
          title: '{{title}}',
          width: 500,
          height: 300,
          pieSliceText: 'value',
          is3D: true,
           }

        var chart = new google.visualization.PieChart(document.getElementById('piechart_refeered'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() {
        var selection = chart.getSelection();
        row = selection[0].row
        var selected =  data.getFormattedValue(row, 0)
        var year_selected = document.getElementById('year_selected').value
        var location = "/pub_closed/" + selected;
        if ( year_selected !== 'None' ){
           location  = "/detail_author_year?author=" + selected + "&year=" +year_selected; 
        }
        window.location = location;
         });
      }

       function drawChart_not_refeered() {

         var data = google.visualization.arrayToDataTable([
          ['Journal', 'how many articles published']
          % for f in not_refeered_count:
          ,["{{!f['author']}}", {{f['count']}}]
          %end

        ]);

        var options = {
          title: 'ASDC Non-refeered Publications',
          width: 500,
          height: 300,
          pieSliceText: 'value',
          is3D: true,

        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_not_refeered'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() {
        var selection = chart.getSelection();
        row = selection[0].row
        var selected =  data.getFormattedValue(row, 0)
        window.location = "/pub_closed/" + selected + "?is_refeered=False";
         });
      }
      // end of pie part visualization

      // histogramm visualization

      % refereed_tot=0
      % not_refereed_tot =0

      % if histogram_year:

      function drawChart_histogram() {
        var data = google.visualization.arrayToDataTable([
          ['Year', 'Refeered', 'Non-refeered']
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
        var author_selected = document.getElementById('author_selected').value
        var location = "";
         if ( author_selected !== 'None' ){
           location  = "/detail_author_year?author=" + author_selected + "&year=" + selected_year;
           
           if ( column == 1){
           location +=  "&is_refeered=True";
           } else {
           location+=  "&is_refeered=False"; 
          }
        } else{
          location="/detail_by_year?year=" + selected_year;
          if ( column == 1){
           location+= "&is_refeered=True";
           } else {
           location+=  "&is_refeered=False"; 
        }
      }

        window.location = location;
        
         });

        }
        // end of histogram
      %end

      //multi tab visualization
      $(function() {
         $( "#tabs" ).tabs();


         % if author:
           $( "#tabs" ).tabs({ active: 1});
         %end
      });
      // end of the multi tab visualization

  </script>

<div id="Content">
<h1>ASDC authors statistics</h1>


<div id="tabs" style="background: white">
  <ul>
    <li><a href="#tabs-2">Year details</a></li>
    <li><a href="#tabs-3">Authors details</a></li>
  </ul>




<div id="tabs-2">

<select onChange='window.location="metrics_authors?year=" + this.value;'>
    <option value="">--</option>
    % for y in years:
      % if str(y) == str(year):
        <option value="{{y}}" selected>{{y}}</option>
      %else:
        <option value="{{y}}">{{y}}</option>
      %end
    % end
</select>

<input id='year_selected'  value='{{year}}' type="hidden" year='{{year}}' />

<table  style="width: 900px; height: 300px;">
  <tr>
    <td >
       <div id="piechart_refeered"  align='left' style="width: 450px; height: 300px;"></div>
    </td>
    <td >
       <div id="piechart_not_refeered"  align='right' style="width: 450px; height: 300px;"></div>
    </td>
 </tr>
</table>
</div>

<div id="tabs-3">

<select onChange='window.location="metrics_authors?author=" + this.value;'>
    <option value="">--</option>
    % for a in authors:
      % if str(a) == str(author):
        <option value="{{a}}" selected>{{a}}</option>
      %else:
        <option value="{{a}}">{{a}}</option>
      %end
    % end
</select>

<input id='author_selected'  value='{{author}}' type="hidden" />

<table>
   <tr>
     <td colspan="2">
      ASDC Refereed total : {{refereed_tot}}
     <br>
     ASDC Non-refereed total : {{not_refereed_tot}}
     </td>
   </tr>
   % if not histogram_year:

   <tr>
     <td>
       No data to display
     </td>
   </tr>

   % else:
   <tr>
     <td>
       <div id="chart_div"></div> 
     </td>
   </tr>
   %end

</table>

</div>


</div>

% include common_footer.tpl  username=username, is_admin=is_admin
