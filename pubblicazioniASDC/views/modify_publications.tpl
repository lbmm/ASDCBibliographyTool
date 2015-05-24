% include header_template.tpl js_array=["/js/double_calendar.js"], css_array=[], username=username

<div id="Content">

% if is_refeered:
%    title = "refereed"
% else:
%     title= "non-refereed"
%end

<h1>Modify {{title}} valid publications</h1>

    <form method="post" action="/modify_valid_publication">
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
