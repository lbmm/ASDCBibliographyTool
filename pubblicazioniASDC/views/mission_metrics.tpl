%setdefault('username', False)
%setdefault('is_admin', False)

% include header_template.tpl css_array=[], js_array=['https://www.google.com/jsapi',], username=username


<script type="text/javascript">


      //piece for the pie chart visualization
      google.load("visualization", "1", {packages:["corechart"]});
      google.load("visualization", "1", {packages:["timeline"]});

      google.setOnLoadCallback(drawChart_refeered);
      google.setOnLoadCallback(drawChart_not_refeered);
      google.setOnLoadCallback(drawChart_author_per_mission_refeered);
      google.setOnLoadCallback(drawChart_author_per_mission_not_refeered);




      function drawChart_refeered() {

         var data = google.visualization.arrayToDataTable([
          ['Journal', 'how many articles published']
          %refereed_missions_year_tot=0
          % for f in refeered_count:
          ,["{{!f['mission']}}", {{f['count']}}]
          %refereed_missions_year_tot= int(f['count']) +refereed_missions_year_tot
          %end

        ]);

        var options = {
          title: 'ASDC Refereed Publications',
          width: 450,
          height: 300,
          pieSliceText: 'value',
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_refeered'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() {
        var selection = chart.getSelection();
        row = selection[0].row
        var selected =  data.getFormattedValue(row, 0)
        var year_selected = document.getElementById('year_selected').value
        var location = "missions_publications_detail?is_refeered=True&mission=" + selected ;
        if ( year_selected !== 'None' ){
           location  = location + "&year=" + year_selected; 
        } 
        window.location = location; 
         });
      }

       function drawChart_not_refeered() {

         var data = google.visualization.arrayToDataTable([
          ['Journal', 'how many articles published']
          % not_refereed_missions_year_tot=0
          % for f in not_refeered_count:
          ,["{{!f['mission']}}", {{f['count']}}]
          % not_refereed_missions_year_tot= int(f['count']) + not_refereed_missions_year_tot
          %end

        ]);

        var options = {
          title: 'ASDC Non-refereed Publications',
          width: 450,
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
        var year_selected = document.getElementById('year_selected').value
        var location = "missions_publications_detail?is_refeered=False&mission=" + selected ;
        if ( year_selected !== 'None' ){
           location  = location + "&year=" + year_selected;
        }
        window.location = location;
         });
      }

      function drawChart_author_per_mission_refeered() {

         var data = google.visualization.arrayToDataTable([
          ['Author', 'how many articles published']
          % for f in author_per_mission['refeered']:
          ,["{{!f['author']}}", {{f['count']}}]
          %end

        ]);

        var options = {
          title: 'ASDC Refereed Publications',
          width: 450,
          height: 300,
          pieSliceText: 'value',
          is3D: true,
         };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_author_mission_refeered'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() {
        var selection = chart.getSelection();
        row = selection[0].row
        var selected =  data.getFormattedValue(row, 0)
        var mission_selected = document.getElementById('mission_selected').value
        var location = "missions_author_publications_detail?is_refeered=True&author=" + selected + "&mission=" + mission_selected ;
        window.location = location; 
         });

      }

      function drawChart_author_per_mission_not_refeered() {

         var data = google.visualization.arrayToDataTable([
          ['Author', 'how many articles published']

          % for f in author_per_mission['not_refeered']:
          ,["{{!f['author']}}", {{f['count']}}]
          %end

        ]);

        var options = {
          title: 'ASDC Non-refereed Publications',
          width: 450,
          height: 300,
          pieSliceText: 'value',
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_author_mission_not_refeered'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() {
        var selection = chart.getSelection();
        row = selection[0].row
        var selected =  data.getFormattedValue(row, 0)
        var mission_selected = document.getElementById('mission_selected').value
        var location = "missions_author_publications_detail?is_refeered=False&author=" + selected + "&mission=" + mission_selected ;
        window.location = location; 
         });

        }

      // end of pie part visualization


      //multi tab visualization
      $(function() {
         $( "#tabs" ).tabs();


         % if mission:
           $( "#tabs" ).tabs({ active: 1 });
         %end
      });
      // end of the multi tab visualization

  </script>

<div id="Content">
<h1>Missions Statistics</h1>


<div id="tabs" style="background: white">
  <ul>
    <li><a href="#tabs-1">Year detail</a></li>
    <li><a href="#tabs-2">Mission detail</a></li>
  </ul>



<div id="tabs-1">

<select onChange='window.location="metrics_missions?year=" + this.value;'> 
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

<table width="95%">
<tr>
     <td colspan="2">
      <i>Refereed total : {{refereed_missions_year_tot}}
     <br>
     Non-refereed total : {{not_refereed_missions_year_tot}}</i>
     </td>
  </tr>
  <tr>
    <td>
       <div id="piechart_refeered" align='left' style="width: 400px; height: 300px;"></div>
    </td>
    <td>
       <div id="piechart_not_refeered" align='right'></div>
    </td>
 </tr>
</table>
</div>

<div id="tabs-2">

 <select onChange='window.location="metrics_missions?mission=" + this.value;'> 
    <option value="">--</option>
    % for m in missions_list:
      % if m['name'] == mission:
        <option value="{{m['name']}}" selected>{{m['name']}}</option>
      %else:
        <option value="{{m['name']}}">{{m['name']}}</option>
      %end
    % end
</select>
<input id='mission_selected'  value='{{mission}}' type="hidden"  />

<table width="95%">
% if mission:
  <tr>
     <td colspan="2">
      <i>Refereed total : {{tot_missions[mission]['refereed']}}
     <br>
     Non-refereed total : {{tot_missions[mission]['not_refereed']}}</i>
     </td>
  </tr>
  %end
  <tr>
    <td>
       <div id="piechart_author_mission_refeered" align='left' style="width: 400px; height: 300px;"></div>
    </td>
    <td>
       <div id="piechart_author_mission_not_refeered" align='right' style="width: 400px; height: 300px;"></div>
    </td>
 </tr>
</table>

</div>

</div>


</div>

% include common_footer.tpl  username=username, is_admin=is_admin
