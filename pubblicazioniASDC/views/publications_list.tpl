%setdefault('username', False)
%setdefault('is_admin', False)
%setdefault('errors_utf8', [])

% include header_template.tpl css_array=["/static/style.css"], js_array=["/js/jquery.pages.js","/js/list_publications.js"], username=username
	<div class="container">
	    <h1> List of ASDC publications </h1>

	     %if errors_utf8:
          <p class="error">
        % for err in errors_utf8:
           {{err}} <br>
        % end
        </p>
        %end

        <br>

        list search: <input type="text" />

	    <form  method="post" action="/export_as_pdf">
	    <div style="text-align:right; padding-bottom:1em;">
			<button type="export" id="exportPDF" disabled>Export as Pdf</button>
		</div>



        </br></br>

        <p> <i>Retrieved {{len(publications)}} publications: </i></p>

        <input type="checkbox" id="selectall"> Select all</input>


        <ul id="listPublications">
        % for p in publications:


			<li>
			<input type="checkbox" class="selectedId" name="biblicode" value="{{p['biblicode']}}" >
			<a href="/publication/{{p['biblicode']}}">{{p['biblicode']}}</a>
			<br>
			<strong>{{!p['title']}}</strong>
			<br>
			{{!p['authors']}}
			<br>
			<i>{{p['pub_date']}}</i>
            <br>
			</li>


		% end

		</ul>

		<div class="holder"></div>

	</div>


% include common_footer.tpl  username=username, is_admin=is_admin
