% include header_template.tpl css_array=["/static/table.css","/static/style.css"], js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/missions_list.js"], username=username

	<div class="container">
	 <form id="form" method="post" action="/close_missions_validity">
		<div style="text-align:right; padding-bottom:1em;">
			<button type="submit">Close</button>
		</div>

		<table class="table" id="missions">
			<thead>
				<tr>
					<th>Name</th>
					<th>start date</th>
					<th>end date</th>
					<th>Close mission validity</th>
					<th>Remove</th>
				</tr>
			</thead>

			<tbody>

			% for m in missions:
				<tr id="{{m['name']}}">
					<td class="hidden-phone">{{m['name']}}</td>
					<td class="hidden-phone">{{m['start_date']}}</td>
					<td class="editable hidden-phone">
					%if m['end_date']=='February 2020':
					   valid
					% else:
					   {{m['end_date']}}
					%end
					</td>
					% if m['end_date']=='February 2020':
				    <td class="center"><input type="checkbox" name="mission" value="{{m['name']}}" ></td>
				    % else:
				    <td class="center"></td>
				    %end
					<td><a href="javascript:;" id="delete-{{m['name']}}" class="delete no-underline">x</a></td>
				</tr>
			% end
	          </tbody>
		</table>

	 </form>


	</div>

% include admin_menu.tpl


