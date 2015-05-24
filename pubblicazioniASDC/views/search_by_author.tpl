%setdefault(username, False)
%setdefault(is_admin, False)

% include header_template.tpl js_array=["/js/double_calendar.js"], css_array=[], username=username

<div id="Content">
<h1>Search by ASDC Author</h1>

    <form method="post" action="/search_by_author">
      <table>
        <tr>
          <td >
            Author
          </td>
          <td>
            <input type="text" name="author" value="{{author}}">
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


% include common_footer.tpl  username=username, is_admin=is_admin
