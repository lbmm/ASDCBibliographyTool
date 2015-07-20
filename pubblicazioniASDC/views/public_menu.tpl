%import constants

<div id="Menu">
<ul id="menu">


    <li>
        <a href="#">Refereed</a>
        <ul>
           % for y in reversed(constants.years):
          <li><a href="/public_publications?year={{y}}">{{y}}</a></li>
           %end 
        </ul>
      </li>
      <li>
        <a href="#">Non-refereed</a>
        <ul>
           % for y in reversed(constants.years):
          <li><a href="/public_publications?year={{y}}&is_refeered=false">{{y}}</a></li>
           %end
        </ul>
      </li>



  <li>
    <a href="#">Search</a>
    <ul>
      <li><a href="/search_by_biblicode">Bibiographic code</a></li>
      <li><a href="/search_by_DOI">DOI</a></li>
      <li><a href="/search_by_author">Author</a></li>
      <li><a href="/search_by_mission">Mission</a></li>
      <li><a href="/search_by_journal">Journal</a></li>
    </ul>
  </li>

  <li><a href="#">Statistics</a>
  <ul>
      <li><a href="/metrics_ASDC">ASDC</a></li>
      <li><a href="/metrics_journal">Journal</a></li>
      <li><a href="/metrics_missions">Missions</a></li>
      <li><a href="/metrics_authors">Author</a></li>
    </ul>
  </li>

  <li><a href="/ASDC_authors_timeline">ASDC collaborators</a></li>
  <li><a href="/ASDC_missions_timeline">ASDC Missions</a></li>

<li><a href="/login">Login</a></li>
</ul>

</div>


</body>
</html>
