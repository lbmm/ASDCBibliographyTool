% include header_template.tpl css_array=[], js_array=[], username=username

<div id="Content">
<h1>Admin functions</h1>
<p> {{!msg}} </p>

<p class="error">{{!errors or ''}}</p>

<br>

</div>

% include admin_menu.tpl
