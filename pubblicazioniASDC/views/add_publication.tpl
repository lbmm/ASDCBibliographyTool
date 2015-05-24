% include header_template.tpl js_array=["/js/double_calendar.js", "/js/asdc_authors_toggle.js"], css_array=[], username=username

<div id="Content">
<h1>Add publication</h1>


    <form method="post" action="/add_publication">
      <table>
      <tr>
        <td class="error" colspan="2">
	    {{errors['general']}}
          </td>
        </tr>
        <tr>
          <td >
            Biblicode 
          </td>
          <td>
            <input type="text" name="biblicode" value="{{publication['biblicode']}}">
          </td>
          <td class="error">
	    {{errors['biblicode']}}
          </td>
        </tr>
       <tr>
          <td >
            DOI 
          </td>
          <td>
            <input type="text" name="DOI" value="{{publication['DOI']}}">
          </td>
        </tr>
       <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>

         <tr>
          <td >
           Title 
          </td>
          <td>
            <textarea rows="1" cols="50" name="title" > {{publication['title']}}
            </textarea>
           </td>
          <td class="error">
            {{errors['title']}}
         </td>
        </tr>
        <tr>
          <td >
           Authors 
          </td>
          <td>
            <textarea rows="1" cols="50" name="authors"> {{publication['authors']}}
            </textarea>
          </td>
         <td class="error">
            {{errors['authors']}}
         </td>
         </tr>
         <tr>
         <td >
           ASDC Authors
          </td>
          <td class="click">
          select authors:
          <div class="hidden">
           <select name="asdc_authors" size="{{len(asdc_authors)}}" multiple>
               %for auth in asdc_authors:
                 <option value="{{auth['username']+ "_" + auth['pub_name']}}">{{auth['name'] + " " + auth['lastname']}}  </option>
               % end
            </select>
          </div>
         </td>
         <td class="error">
         {{errors['asdc_authors']}}
         </td>
         </tr>

        <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>


        <tr>
          <td >
            Publication Date
          </td>
          <td>
            <input type="text" name="pub_date" id="datepicker" value="{{publication['pub_date']}}">
          </td>
          <td class="error">
	    {{errors['start_date_error']}}
          </td>
        </tr>
        <tr>
          <td >
            Origin 
          </td>
          <td>
            <input type="text" name="origin"  value="{{publication['origin']}}">
          </td>
        </tr>

        <tr>
          <td >
            Journal 
          </td>
          <td>
            <input type="text" name="magazine"  value="{{publication['magazine']}}">
          </td>
          <td class="error">
	    {{errors['magazine_error']}}
          </td>
        </tr>

        <tr>
          <td >
            external URL 
          </td>
          <td>
            <textarea rows="1" cols="50" name="URL"> {{publication['URL']}}
            </textarea>
          </td>
          <td class="error">
	    {{errors['URL_error']}}
          </td>
        </tr>

        <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>


        <tr>
          <td >
            Abstract 
          </td>
          <td>
            <textarea rows="6" cols="50" name="abstract"> {{publication['abstract']}}
            </textarea>
          </td>
          </td>
        </tr>
        <tr>
          <td >
            keywords 
          </td>
          <td>
            <textarea rows="2" cols="50" name="keywords"> {{publication['keywords']}}
            </textarea>
          </td>
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
         <td colspan="2">
           <hr>
         </td>
       </tr>

        <tr>
          <td >
            Refereed publications
          </td>
          <td>
            <input type="checkbox" name="is_refeered" value="Y">
          </td>

        </tr>
      </table>

      <input type="submit">
    </form>

% include user_menu.tpl username=username
