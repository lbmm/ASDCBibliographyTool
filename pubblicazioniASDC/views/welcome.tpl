% include header_template.tpl css_array=[], js_array=[], username=username

<div id="Content">
<h1>ASDC Publications</h1>

% if defined('msg'):
<p> {{!msg}} </p>
%end
% if defined('errors'):
<p class="error">{{!errors or ''}}</p>
%end

</div>

% include user_menu.tpl username=username
