<?php

$query = "SELECT * FROM status WHERE key LIKE 'radiation_%'";

if(isset($_REQUEST["sort"])) {
    $query .= " ORDER BY $1";
    pg_prepare($db, "search_query", $query);    

    Common::renderView("table", ["source" => "radiation", "data" => pg_fetch_all(pg_execute($db, "search_query", array($_REQUEST["sort"])))]);
} else {
    Common::renderView("table", ["source" => "radiation", "data" => pg_fetch_all(pg_query($db, $query))]);
}
?>
