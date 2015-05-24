%setdefault('username', False)
%setdefault('is_admin', False)


% include header_template.tpl css_array=["/static/style.css"], js_array=[], username=username

<script>
  $(function() {
    $( "#tabs" ).tabs();
  });
  </script>

<div class="container">

<h2> Publication detail {{publication['biblicode']}} </h2>


<div id="tabs" style="background: white">
  <ul>
    <li><a href="#tabs-1">Publication</a></li>
    <li><a href="#tabs-2">Metrics</a></li>
  </ul>
  <div id="tabs-1">
    <p>
    <a href="{{publication['URL']}}">{{!publication['title']}} </a>
     <br>
    {{!publication['authors']}}
    <br>
    <i>{{publication['pub_date']}}</i>
    <br>
    Origin: {{publication['Origin']}}
    <br>
    DOI: {{publication['DOI']}}
    <br>
    <br>

    <p>
   {{!publication['Abstract']}}
    </p>

    <strong>keywords</strong> : {{!publication['Keywords']}}

    </p>
  </div>
  <div id="tabs-2">
    <p>  <img src="/static/images/metric_example.png" alt="metric example" width='600px' height='400px' align='center' > </p>
  </div>
</div>

</div>


% include common_footer.tpl  username=username, is_admin=is_admin