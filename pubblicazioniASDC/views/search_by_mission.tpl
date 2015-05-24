%setdefault('username', False)
%setdefault('is_admin', False)

% include header_template.tpl js_array=["/js/double_calendar.js"], css_array=[], username=username

<div id="Content">
<h1>Search by Mission</h1>

    <form method="post" action="/search_by_mission">
      <table>
        <tr>
          <td >
            Mission
          </td>
          <td>
            <input type="text" name="mission" value="{{mission}}">
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
        <tr>
          <td >
            Non-refereed publications
          </td>
          <td>
            <input type="checkbox" name="is_refeered" value="N">
          </td>

        </tr>
      </table>

      <button type="submit">search</button>
    </form>

    <p>  <i>search does support Perl regular expressions and it is case not sensitive </i> </p>


% include common_footer.tpl  username=username, is_admin=is_admin

