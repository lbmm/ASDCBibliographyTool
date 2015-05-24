% include header_template.tpl css_array=["/static/table.css","/static/style.css"], js_array=["/js/jquery.dataTables.js","/js/jquery.blockUI.js","/js/roles_list.js"], username=username

	<div class="container">

		<table class="table" id="roles">
			<thead>
				<tr>
					<th>Role</th>
					<th>Remove</th>
				</tr>
			</thead>

			<tbody>

			% for r in roles:
				<tr id="{{r['role']}}">
					<td class="hidden-phone">{{r['role']}}</td>
					<td align="center"><a href="javascript:;" id="delete-{{r['role']}}" class="delete no-underline">x</a></td>
				</tr>
			% end
	          </tbody>
		</table>


	</div>

% include admin_menu.tpl


