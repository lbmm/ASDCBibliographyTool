% include header_template.tpl css_array=["/static/table.css","/static/style.css"], js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/publications_list_table_to_validate.js"], username=username

	<div class="container">

	<form id="form" method="post" action="/invalidate_publications">
		<div style="text-align:right; padding-bottom:1em;">
			<button type="submit">Update</button>
		</div>

       </br></br>

        <p> <i>Retrieved {{len(publications)}} publications: </i></p>

		<table class="table" id="publications">
			<thead>
				<tr>
					<th>Bibliographic code</th>
					<th>Title </th>
					<th>Pub date</th>
					<th>ASDC Authors</th>
					<th>Missions</th>
					<th>Refereed</th>
					<th>Not Valide</th>
				</tr>
			</thead>

			<tbody>

			% for p in publications:


				<tr id="{{p['biblicode'].replace(".","")}}">
					<td class="hidden-phone"><a href="/publication/{{p['biblicode']}}" target="_blank">{{p['biblicode']}}</a></td>
					<td class="hidden-phone" style="width:150px">{{!p['title']}}</td>
					<td class="hidden-phone"><i>{{p['pub_date']}}</i></td>
					<td class="hidden-phone" nowrap>
					%for auth in  p['asdc_auth']:
					{{auth['author']}}
					<br>
					%end
					</td>
					<td id="mission-{{p['biblicode']}}" class="editable_mission">
					% for m in p['mission']:
					    {{m}} <br>
					% end
					</td>

					</td>
					<td class="hidden-phone">{{p['is_refeered']}}</td>
					<td class="center"><input type="checkbox" name="biblicode" value="{{p['biblicode']}}" ></td>
				</tr>
			% end
	          </tbody>
		</table>

    </form>
	</div>

% include user_menu.tpl username=username
