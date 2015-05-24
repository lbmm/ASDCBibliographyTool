% include header_template.tpl js_array=["/js/double_calendar.js"], css_array=[], username=username

<div id="Content">
<h1>Close publication period</h1>

    <form method="post" action="/close_publications_period">
      <table>

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

      <input type="hidden" name="is_refeered" value="{{is_refeered}}" >

      <input type="submit">
    </form>


% include admin_menu.tpl
