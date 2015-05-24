% include header_template.tpl css_array=["/static/table.css","/static/style.css"],js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/users_list.js"], username=username

	<div class="container">

    <form id="form" method="post" action="/close_users_validity">
		<div style="text-align:right; padding-bottom:1em;">
			<button type="submit">Close</button>
		</div>
         
		<table class="table" id="users">
			<thead>
				<tr>
					<th>username</th>
					<th>Name</th>
					<th>Lastname</th>
					<th>email</th>
					<th>role</th>
					<th>Missions</th>
					<th>start_date</th>
					<th>end_date</th>
					<th>Close user validity</th>
					<th>Remove</th>
				</tr>
			</thead>

			<tbody>

			% for u in users:

				<tr id="{{u['username']}}">
					<td class="hidden-phone">{{u['username']}}</td>
					<td class="hidden-phone">{{u['name']}}</td>
					<td class="hidden-phone">{{u['lastname']}}</td>
					<td id="mail-{{u['username']}}" class="editable_email">{{u['email']}}</td>
					<td id="role-{{u['username']}}" class="editable_role">{{u['role']}}</td>
					<td id="mission-{{u['username']}}" class="editable_mission">
					% for m in u['missions']:
					    {{m}} <br>
					% end
					</td>
					<td class="hidden-phone">{{u['start_date']}}</td>
					<td >
					%if u['end_date']=='February 2020':
					   valid
					% else:
					   {{u['end_date']}}
					%end
					</td>
					% if u['end_date']=='February 2020':
				    <td class="center"><input type="checkbox" name="username" value="{{u['username']}}" ></td>
				    % else:
				    <td class="center"></td>
				    %end
					<td><a href="javascript:;" id="delete-{{u['username']}}" class="delete no-underline">x</a></td>
				</tr>
			% end
	          </tbody>
		</table>

    </form>
	</div>

% include admin_menu.tpl


