% include header_template.tpl css_array=[], js_array=[], username=username

<div id="Content">
<h1>User functions</h1>
<p> {{!msg}} </p>

<p class="error">{{!errors or ''}}</p>


</div>

% include user_menu.tpl username=username
