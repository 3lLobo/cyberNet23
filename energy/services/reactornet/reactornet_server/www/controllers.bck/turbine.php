<?php

$query = "SELECT * FROM status WHERE key LIKE 'turbine_%'";

if(isset($_REQUEST["sort"])) $query .= sprintf(" ORDER BY %s", $_REQUEST["sort"]);

Common::renderView("table", ["source" => "turbine", "data" => pg_fetch_all(pg_query($db, $query))]);

?>
