
<div id="Menu">
<ul id="menu">

<li>
    <a href="#">Publications</a>
    <ul>
      <li>
        <a href="#">Refereed</a>
        <ul>
          <li><a href="/pub_to_validate/{{username}}">List open publications</a></li>
          <li><a href="/pub_closed/{{username}}">List confirmed publications</a></li>
          <li><a href="/validate_publications">Validate publications</a></li>
        </ul>
      </li>
      <li>
      <a href="#">Non-refereed</a>
        <ul>
          <li><a href="/pub_to_validate/{{username}}?is_refeered=False">List open publications</a></li>
          <li><a href="/pub_closed/{{username}}?is_refeered=False">List confirmed publications</a></li>
          <li><a href="/validate_publications?is_refeered=False">Validate publications</a></li>
        </ul>
      </li>
     </ul>
    </li>
  <li>
    <a href="#">Add publication</a>
    <ul>
      <li><a href="/add_publication">Add publication</a></li>
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

  <li><a href="/logout">logout</a></li>

</ul>

</div>


</body>
</html>
