% include header_template.tpl js_array=["/js/double_calendar.js"], css_array=[], username=username

<div id="Content">
<h1>Add new user</h1>

    <form method="post" action="/add_user">
      <table>
        <tr>
          <td >
            Username
          </td>
          <td>
            <input type="text" name="username" value="{{username_to_add}}">
          </td>
          <td class="error">
	    {{errors['username_error']}}
            
          </td>
        </tr>


         <tr>
          <td >
            Name
          </td>
          <td>
            <input type="text" name="name" value="{{name}}">
          </td>
        </tr>

        <tr>
          <td >
            Lastname
          </td>
          <td>
            <input type="text" name="lastname" value="{{lastname}}">
          </td>

        </tr>

        <tr>
          <td >
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
	    {{errors['password_error']}}
            
          </td>
        </tr>

        <tr>
          <td >
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
	    {{errors['verify_error']}}
            
          </td>
        </tr>

        <tr>
          <td >
            Email 
          </td>
          <td>
            <input type="text" name="email" value="{{email}}">
          </td>
          <td class="error">
	    {{errors['email_error']}}
            
          </td>
        </tr>
        <tr>
           <td > Role </td>
           <td>
            <select name="role">
               %for r in roles:
                 %if r == role_selected:
                 <option value="{{r['role']}}" selected>{{r['role']}} </option>
                 % else:
                 <option value="{{r['role']}}">{{r['role']}} </option>
                 %end
               % end
            </select>
          </td>
        </tr>
        <tr>
           <td > Mission </td>
           <td>
            <select name="missions" size="{{len(missions)}}" multiple>
               %for m in missions:
                 <option value="{{m['name']}}">{{m['name']}} </option>
               % end 
            </select> 
          </td>
        </tr>
        <tr>
          <td >
            start date
          </td>
          <td>
            <input type="text" name="start_date" id="datepicker" value="{{start_date}}">
          </td>
           <td class="error">
            {{errors['start_date_error']}}
          </td>
        </tr>

        <tr>
          <td >
            end date
          </td>
          <td>
            <input type="text" name="end_date" id="datepicker1" value="{{end_date}}">
          </td>
           <td class="error">
            {{errors['end_date_error']}}
          </td>
        </tr>

      </table>

      <input type="submit">
    </form>


% include admin_menu.tpl
