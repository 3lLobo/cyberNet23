<?php

$query = "SELECT * FROM status WHERE key LIKE 'radiation_%'";

if(isset($_REQUEST["sort"])) $query .= sprintf(" ORDER BY %s", $_REQUEST["sort"]);

Common::renderView("table", ["source" => "radiation", "data" => pg_fetch_all(pg_query($db, $query))]);

?>
