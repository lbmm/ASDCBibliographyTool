%setdefault('username', False)

% include header_template.tpl css_array=["/static/style.css"], js_array=["/js/jquery.pages.js","/js/list_publications.js"], username=username
	<div class="container">
	    <h1> List of ASDC publications </h1>

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
			<input type="checkbox" name="biblicode" class="selectedId" value="{{p['biblicode']}}" >
			<a href="{{p['URL']}}">{{p['biblicode']}}</a>
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


% include  public_menu
