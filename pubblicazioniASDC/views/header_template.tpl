<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
<title>ASDC publications </title>

<!-- different css for the pages-->

% for css in css_array:
<link href="{{css}}" media="screen" rel="stylesheet" type="text/css" />
% end 

<link rel="stylesheet" href="/static/jquery-ui-1.10.4.custom.css">
<style href="/static/page_layout.css" type="text/css" media="all">@import "/static/page_layout.css";</style>

<script src="/js/jquery-ui-1.10.4.custom/js/jquery-1.10.2.js"></script>
<script src="/js/jquery-ui-1.10.4.custom/js/jquery-ui-1.10.4.custom.min.js"></script>

% for js in js_array:
<script type="text/javascript" src="{{js}}"></script>
%end 

<script>
$(function() {
    $( "#menu" ).menu();
  });
  </script>

<style>
.ui-menu { width: 150px; }
</style>


</head>
<body>



<div id="Header">

% if username:

<table width=95%>
<tr>

  <td align="left">
      <a href="/user_info">Welcome {{username}}</a>
   </td>
   <td>
   <table align="right">
   <tr>



   <td align="right" >
     <a href="/static/manual.pdf">Download PDF Manual</a>
   </td>
   <td align="right">
     <a href="mailto:publications@asdc.asi.it" target="_top"><img src="/static/images/email.png" width="20" height="20"></a>
 </td>
 </tr>
 </table>
 </td>
 </tr>
 </table>
% else:

<table align="right">
   <tr>
   <td align="right" >
     <a href="/static/manual.pdf">Download PDF Manual  </a>
   </td>
   <td align="right">
     <a href="mailto:publications@asdc.asi.it" target="_top"><img src="/static/images/email.png" width="20" height="20"></a>
    </td>
    </tr>
 </table>

%end
   <br/>
</div>


