% include header_template.tpl css_array=["/static/table.css","/static/style.css"],js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/user_info.js"], username=username

	<div class="container">

    <h3>You can update your email information and Missions affiliation double clicking the cell.</h3>
	<br>
	<br>

		<table class="table" id="users">
			<thead>
				<tr>
					<th>username</th>
					<th>Name</th>
					<th>Lastname</th>
					<th>Role</th>
					<th>email</th>
					<th>Missions</th>
					<th>start_date</th>
					<th>end_date</th>

				</tr>
			</thead>

			<tbody>
				<tr id="{{user['username']}}">
					<td class="hidden-phone">{{user['username']}}</td>
					<td class="hidden-phone">{{user['name']}}</td>
					<td class="hidden-phone">{{user['lastname']}}</td>
					<td class="hidden-phone">{{user['role']}}</td>
					<td id="mail-{{user['username']}}"class="editable_email">{{user['email']}}</td>


					<td id="mission-{{user['username']}}" class="editable_mission">
					% for m in user['missions']:
					    {{m}} <br>
					% end
					</td>


					<td class="hidden-phone">{{user['start_date']}}</td>
					<td >
					%if user['end_date']=='02/20/2020':
					   valid
					% else:
					   {{user['end_date']}}
					%end
					</td>
					</tr>
	          </tbody>
		</table>



	</div>

% include user_menu.tpl username=username


