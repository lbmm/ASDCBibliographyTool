<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
<title>ASDC publications </title>
<style href="/static/page_layout.css" type="text/css" media="all">@import "/static/page_layout.css";</style>
</head>
<body>


</head>

<body>

%setdefault('error', '')
%setdefault('username', '')


<div id="Header"><a>ASDC Publications utilities </a></p> </div>
 <div id="Content">
    <h1>Forgot Password</h1>
    Enter the username you submitted at registration. <br>
    Your password will be e-mailed to you immediately
    <br>
    <form method="post" action="/recover_password">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="{{username}}">
          </td>
          </tr>
          <tr>
          <td class="error">
          {{error}}
          </td>
        </tr>


      <tr>
      <td>
      <input type="submit" value="recover password">
      </td>

      </table>
 </form>
  </body>
</div>

</html>
