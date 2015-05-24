%setdefault('username', False)
%setdefault('is_admin', False)

% include header_template.tpl css_array=[], js_array=['https://www.google.com/jsapi',], username=username


<script type="text/javascript">


      //piece for the pie chart visualization
      google.load("visualization", "1", {packages:["timeline"]});
      
      setTimeout(function() {google.setOnLoadCallback(drawTimeLine)},300);


      google.setOnLoadCallback(drawTimeLine);

      // Timeline Chart

      function drawTimeLine() {
        var container = document.getElementById('missions_timeline');
        var chart = new google.visualization.Timeline(container);
        var dataTable = new google.visualization.DataTable();
        dataTable.addColumn({ type: 'string', id: 'Name' });
        dataTable.addColumn({ type: 'date', id: 'Start' });
        dataTable.addColumn({ type: 'date', id: 'End' });
        dataTable.addRows([

        % for j in range(0,len(missions_list)):
        % i=j+1
        % end_date = missions_list[j]["end_date"]
        %  if end_date=='February 20, 2020':
        %     end_date = today
        %  end
        %  if missions_list[j]["name"] == "Other":
        %    continue
        %  end
        % if j == 0:
           [  '{{missions_list[j]["name"]}}', new Date('{{missions_list[j]["start_date"]}}'), new Date('{{end_date}}') ]
        %else:
           ,[  '{{missions_list[j]["name"]}}', new Date('{{missions_list[j]["start_date"]}}'), new Date('{{end_date}}') ]
        %end

        %end
         ]);

        var options = {
        width: 850,
        % height = 30*len(missions_list)
        height: {{height}}
        };

    chart.draw(dataTable, options);

    google.visualization.events.addListener(chart, 'select', clickHandler);

    function clickHandler(){
        var selection = chart.getSelection();
        var location = "/metrics_missions?mission=";
    for (var i = 0; i < selection.length; i++) {
         var item = selection[i];
         location +=  dataTable.getFormattedValue(item.row, 0);
         }
         window.location = location;

    }


 }
      //multi tab visualization
      $(function() {
         $( "#tabs" ).tabs();

      });
      // end of the multi tab visualization

  </script>

<div id="Content">
<h1>Missions Overview</h1>


<div id="tabs" style="background: white">
  <ul>
    <li><a href="#tabs-1">ASDC Missions TimeLine</a></li>
  </ul>

<div id="tabs-1">
   <div id="missions_timeline" align="center"></div>
</div>

</div>


</div>

% include common_footer.tpl  username=username, is_admin=is_admin
