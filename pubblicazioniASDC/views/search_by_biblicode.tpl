%setdefault('username', False)
%setdefault('is_admin', False)

% include header_template.tpl js_array=[], css_array=[], username=username

<div id="Content">
<h1>Search by Bibliographic Code</h1>

    <form method="post" action="/search_by_biblicode">

      <table>

        <tr>
          <td >
            Bibliographic code
          </td>
          <td>
            <input type="text" name="biblicode" value="">
          </td>

        </tr>

        <tr>
          <td >
            Non-refeered publications
          </td>
          <td>
            <input type="checkbox" name="is_refeered" value="N">
          </td>

        </tr>

      </table>
      <p> <i>search does support Perl regular expressions </i></p>

      <button type="submit">search</button>
    </form>


% include common_footer.tpl  username=username, is_admin=is_admin

