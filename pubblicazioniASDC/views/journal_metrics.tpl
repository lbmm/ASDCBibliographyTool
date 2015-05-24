%setdefault('username', False)
%setdefault('is_admin', False)

% include header_template.tpl css_array=[], js_array=['https://www.google.com/jsapi',], username=username


<script type="text/javascript">


      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart_refeered);
      google.setOnLoadCallback(drawChart_not_refeered);

      function drawChart_refeered() {

         var data = google.visualization.arrayToDataTable([
          ['Journal', 'how many articles published']
          % refereed_journals_tot=0
          % for f in refeered_count:
          ,["{{!f['journal']}}", {{f['count']}}]
          % refereed_journals_tot= int(f['count']) +refereed_journals_tot
          %end

        ]);

        var options = {
          title: 'ASDC Refereed Publications',
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_refeered'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() {
        var selection = chart.getSelection();
        row = selection[0].row
        var selected =  data.getFormattedValue(row, 0)
        selected = selected.replace("&","!");
        var year_selected = document.getElementById('year_selected').value
        var location = "journals_publications_detail?is_refeered=True&journal=" + selected ;
        if ( year_selected !== 'None' ){
           location  = location + "&year=" + year_selected; 
        } 
        window.location = location;
            
      });
      }

       function drawChart_not_refeered() {

         var data = google.visualization.arrayToDataTable([
          ['Journal', 'how many articles published']
          % not_refereed_journals_tot=0
          % for f in not_refeered_count:
          ,["{{!f['journal']}}", {{f['count']}}]
          % not_refereed_journals_tot= int(f['count']) + not_refereed_journals_tot
          %end

        ]);

        var options = {
          title: 'ASDC Non-refereed Publications',
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_not_refeered'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() {
        var selection = chart.getSelection();
        row = selection[0].row
        var selected =  data.getFormattedValue(row, 0)
        selected = selected.replace("&","!");
        var year_selected = document.getElementById('year_selected').value
        var location = "journals_publications_detail?is_refeered=False&journal=" + selected ;
        if ( year_selected !== 'None' ){
           location  = location + "&year=" + year_selected;
        }
        window.location = location;

      });
      }

    </script>


<div id="Content">
<h1>Journal Statistics</h1>

<select onChange='window.location="metrics_journal?year=" + this.value;'>
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


<table >
<tr>
     <td colspan="2">
      <i>Refereed total : {{refereed_journals_tot}}
     <br>
     Non-refereed total : {{not_refereed_journals_tot}}</i>
     </td>
  </tr>
<tr>
 <td>
    <div id="piechart_refeered" align='left' style="width: 450px; height: 250px;"></div>
 </td>
 <td>

    <div id="piechart_not_refeered" align='right' style="width: 450px; height: 250px;"></div>
 </td>
 </tr>

</table>






</div>

% include common_footer.tpl  username=username, is_admin=is_admin
