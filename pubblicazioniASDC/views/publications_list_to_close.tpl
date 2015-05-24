% include header_template.tpl css_array=["/static/table.css","/static/style.css"], js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/publications_list_table.js"], username=username

	<div class="container">

	<form id="form" method="post" action="/close_publications">
		<div style="text-align:right; padding-bottom:1em;">
			<button type="submit">Close</button>
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
					<th>Valide</th>
					<th>Remove</th>
				</tr>
			</thead>

			<tbody>

			% for p in publications:

			% biblicode_id = (p['biblicode'].replace(".","")).replace("&","")


				<tr id="{{biblicode_id}}">
					<td class="hidden-phone"><a href="/publication/{{p['biblicode']}}" target="_blank">{{p['biblicode']}}</a></td>
					<td class="hidden-phone" style="width:150px">{{!p['title']}}</td>
					<td class="hidden-phone"><i>{{p['pub_date']}}</i></td>
					<td class="hidden-phone" nowrap>
					%for auth in  p['asdc_auth']:
					{{auth['author']}} : {{auth['validate'] or 'No'}}
					<br>
					%end
					</td>
					<td id="mission-{{p['biblicode']}}" class="editable_mission">
					% for m in p['mission']:
					    {{m}} <br>
					% end
					</td>
					<td class="hidden-phone">{{p['is_refeered']}}</td>
					<td class="center"><input type="checkbox" name="biblicode" value="{{p['biblicode']}}" ></td>
					<td><a href="javascript:;" id="delete-{{biblicode_id}}-{{p['biblicode'].replace("&","!")}}" class="delete no-underline">x</a></td>
				</tr>
			% end
	          </tbody>
		</table>

    </form>
	</div>

% include admin_menu.tpl
