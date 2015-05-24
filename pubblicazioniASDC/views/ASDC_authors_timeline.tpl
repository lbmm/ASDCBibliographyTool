%setdefault('username', False)
%setdefault('is_admin', False)

% include header_template.tpl css_array=[], js_array=['https://www.google.com/jsapi',], username=username


<script type="text/javascript">


      //piece for the pie chart visualization
      google.load("visualization", "1", {packages:["timeline"]});

      google.setOnLoadCallback(drawHeaderTimeLine);
      google.setOnLoadCallback(drawTimeLine);

      // Header Timeline Chart

      function drawHeaderTimeLine() {
        var container = document.getElementById('header_authors_timeline');
        var chart = new google.visualization.Timeline(container);
        var dataTable = new google.visualization.DataTable();
        dataTable.addColumn({ type: 'string', id: 'Term' });
        dataTable.addColumn({ type: 'string', id: 'count' });
        dataTable.addColumn({ type: 'date', id: 'Start' });
        dataTable.addColumn({ type: 'date', id: 'End' });
        dataTable.addRows([
        % i = 0
        % for k in header_authors.keys():
        % i=i+1
        % if i == 1:
           [ 'ASDC active authors', '{{header_authors[k]}}', new Date( 'January 01, {{k}}'), new Date('December 31, {{k}}') ]
        %else:
           ,[ 'ASDC active authors', '{{header_authors[k]}}', new Date('January 01, {{k}}'), new Date('December 31, {{k}}') ]
        %end

        %end
         ]);

        var options = {
        timeline: { groupByRowLabel: true }, 
        width: 850,
        height: 100 
        };

        chart.draw(dataTable, options);
}

      // Timeline Chart

      function drawTimeLine() {
        var container = document.getElementById('authors_timeline');
        var chart = new google.visualization.Timeline(container);
        var dataTable = new google.visualization.DataTable();
        dataTable.addColumn({ type: 'string', id: 'username' });
        dataTable.addColumn({ type: 'string', id: 'Name' });
        dataTable.addColumn({ type: 'date', id: 'Start' });
        dataTable.addColumn({ type: 'date', id: 'End' });
        dataTable.addRows([
        % colors = []
        % for j in range(0,len(complete_authors)):
        % end_date = complete_authors[j]["end_date"]
        %  if end_date=='February 20, 2020':
        %     end_date = today
        %  end
        % if complete_authors[j]['role'] == 'SeniorScientist':
        %    colors.append("#C4C45D")
        % elif complete_authors[j]['role'] == 'Scientist':
        %    colors.append("#55AA55")
        % else:
        %    colors.append("#33CC33")
        %end
        % if j == 0:
           ["{{complete_authors[j]["name"]}}  {{!complete_authors[j]["lastname"]}}", "{{complete_authors[j]["username"]}}" , new Date('{{complete_authors[j]["start_date"]}}'), new Date('{{end_date}}') ]
        %else:
           ,["{{complete_authors[j]["name"]}} {{!complete_authors[j]["lastname"]}}", "{{complete_authors[j]["username"]}}" ,new Date('{{complete_authors[j]["start_date"]}}'), new Date('{{end_date}}') ]
        %end

        %end
         ]);

        var options = {
        width: 850,
        timeline: { groupByRowLabel: false, showBarLabels: false },
        % height = 10*len(complete_authors)
        height: {{height}},
        colors: {{!colors}}
        };


        chart.draw(dataTable, options);

        google.visualization.events.addListener(chart, 'select', clickHandler);

        function clickHandler(){
        var selection = chart.getSelection();
        var location = "/metrics_authors?author=";
        for (var i = 0; i < selection.length; i++) {
           var item = selection[i];
           location +=  dataTable.getFormattedValue(item.row, 1);
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
<h1>ASDC Authors Overview</h1>


<div id="tabs" style="background: white">
  <ul>
    <li><a href="#tabs-1">Active Status</a></li>
  </ul>

<div id="tabs-1">
   <div id="header_authors_timeline"></div>
   <div align="left">
          <font color="#C4C45D"> Senior-Scientist  </font>
          <font color="#55AA55"> Scientist </font>
          <font color="#33CC33"> Software Eng </font>
   </div>
   <div id="authors_timeline"></div>

</div>


</div>

% include common_footer.tpl  username=username, is_admin=is_admin
