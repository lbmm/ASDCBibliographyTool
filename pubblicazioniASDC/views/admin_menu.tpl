
<div id="Menu">
<ul id="menu">
<li>
    <a href="#">Missions</a>
    <ul>
      <li><a href="/add_mission">Add Mission</a></li>
      <li><a href="/list_missions">List Missions</a></li>
      <li><a href="/list_valide_missions">List valide missions</a></li>
    </ul>
  </li>
  <li>
    <a href="#">Users</a>
    <ul>
      <li><a href="/add_user">Add User</a></li>
      <li>
          <a href="#">Users Roles</a>
           <ul>
             <li><a href="/add_role">Add role</a></li>
             <li><a href="/list_roles">List roles</a></li>
           </ul>
       </li>
      <li><a href="/list_users">List users</a></li>
      <li><a href="/list_valide_users">List valide users</a></li>
    </ul>
  </li>
  <li>
  <a href="#">Ads download</a>
  <ul>
    <li><a href="/ads_download">Refeered</a></li>
    <li><a href="/ads_download?is_refeered=False">Non-refeered</a></li>
  </ul>
  </li>
  <li>
    <a href="#">Publications</a>
    <ul>
    <li>
        <a href="#">Refeered</a>
        <ul>
          <li><a href="/list_open_publications">List open publications</a></li>
          <li>
            <a href="#">confirmed publications</a>
           <ul>
             <li><a href="/list_valide_publications">List confirmed publications</a></li>
             <li><a href="/modify_valid_publication">Modify confirmed publications</a></li>
           </ul>
          </li>
          <li><a href="/close_publications_period">Close a period</a></li>
        </ul>
      </li>
      <li>
        <a href="#">Non-refeered</a>
        <ul>
          <li><a href="/list_open_publications?is_refeered=False">List open publications</a></li>

          <li>
            <a href="#">confirmed publications</a>
           <ul>
             <li><a href="/list_valide_publications?is_refeered=False">List confirmed publications</a></li>
             <li><a href="/modify_valid_publication?is_refeered=False">Modify confirmed publications</a></li>
           </ul>
          </li>

          <li><a href="/close_publications_period?is_refeered=False">Close a period</a></li>
        </ul>
      </li>
    </ul>
  </li>
  <li>
    <a href="#">User publications</a>
    <ul>
      <li><a href="/validate_users_publications">Validate users publications</a></li>
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
      <li><a href="/metrics_ASDC">ASDC </a></li>
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
