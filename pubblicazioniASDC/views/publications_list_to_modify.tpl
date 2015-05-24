% include header_template.tpl css_array=["/static/table.css","/static/style.css"], js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/publications_valide_to_modify.js"], username=username



	<div class="container">

	% if is_refeered:
	%    title = "refereed"
	% else:
	%     title= "non-refereed"
	%end

        <h1>Modify confirmed {{title}} publications</h1>

        <p> <i>Retrieved {{len(publications)}} publications: </i></p>

		<table class="table" id="publications">
			<thead>
				<tr>
					<th>Bibliographic code</th>
					<th>Title </th>
					<th>Pub date</th>
					<th>ASDC Authors</th>
					<th>Missions</th>
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
					<td class="editable_authors" id="author-{{p['biblicode']}}" nowrap>
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
					<td><a href="javascript:;" id="delete-{{biblicode_id}}-{{p['biblicode'].replace("&","!")}}" class="delete no-underline">x</a></td>
				</tr>
			% end
	          </tbody>
		</table>


	</div>

% include admin_menu.tpl
