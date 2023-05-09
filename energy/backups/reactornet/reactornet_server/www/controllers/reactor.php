<?php

$query = "SELECT * FROM status WHERE key LIKE 'reactor_%'";

if(isset($_REQUEST["sort"])) $query .= sprintf(" ORDER BY %s", $_REQUEST["sort"]);

Common::renderView("table", ["source" => "reactor", "data" => pg_fetch_all(pg_query($db, $query))]);

?>
