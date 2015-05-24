% include header_template.tpl css_array=["/static/style.css"], js_array=[], username=username
<div class="container">

<h2> Publication detail {{publication['biblicode']}} </h2>


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


% include admin_menu.tpl