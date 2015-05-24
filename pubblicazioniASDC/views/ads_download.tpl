% include header_template.tpl js_array=["/js/double_calendar.js", "/js/asdc_authors_toggle.js"], css_array=[], username=username


% if is_refeered :
%    title = "refeered publications"
% else:
%    title = "non-refeered publications"
% end
<div id="Content">
<h1>ADS Download </h1>
  <h2><i>{{title}}</i></h2>

    <form method="post" action="/ads_download">
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

        <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>

        <tr>
        <td >
           ASDC Authors
          </td>
          <td class="click">
            <i> select authors (double click) </i>
          <div class="hidden">
           <select name="asdc_authors" size="{{len(asdc_authors)}}" multiple>
               %for auth in asdc_authors:
                 <option value="{{auth['username']}}">{{auth['name'] + " " + auth['lastname']}}  </option>
               % end
            </select>
          </div>
         </td>
         </tr>

        <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>


      </table>

      <input type="hidden" name="is_refeered" value="{{is_refeered}}">

      <input type="submit">
    </form>


% include admin_menu.tpl
