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

%setdefault('username', '')
%setdefault('login_error', '')


<div id="Header"><a>ASDC Publications utilities </a></p> </div>
 <div id="Content">
    <h1>Login</h1>
    <form method="post" action="/login">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="{{username}}">
          </td>
          <td class="error">
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
	    {{login_error}}
            
          </td>
        </tr>


      <tr>
      <td>
      <input type="submit" value="login">
      </td>
      </form>
      <form action="/forgot_password" method="post">
      <td>
      <input type="submit" value="reset password">
      </td>
      </tr>
      </table>

  </body>
</div>

</html>
