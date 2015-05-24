% include header_template.tpl js_array=["/js/double_calendar.js"], css_array=[], username=username

<div id="Content">
<h1>Add new Mission</h1>

    <form method="post" action="/add_mission">
      <table>
        <tr>
          <td >
            Mission
          </td>
          <td>
            <input type="text" name="mission" value="{{mission}}">
          </td>
          <td class="error">
            {{error['name_error']}}
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
            {{error['start_date_error']}}
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
            {{error['end_date_error']}}
          </td>
        </tr>

      </table>

      <input type="submit">
    </form>


% include admin_menu.tpl
