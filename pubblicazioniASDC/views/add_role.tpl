% include header_template.tpl js_array=[""], css_array=[], username=username

<div id="Content">
<h1>Add new User Role</h1>

    <form method="post" action="/add_role">
      <table>
        <tr>
          <td >
            Role
          </td>
          <td>
            <input type="text" name="role" value="{{role}}">
          </td>
          <td class="error">
            {{error['name_error']}}
          </td>
        </tr>
        <tr>
      </table>

      <input type="submit" value="add role">
    </form>


% include admin_menu.tpl
