<?php

if(!isset($_REQUEST["key"])) die("Invalid argument specified");

if(intval($_REQUEST["key"])) {

    $query = "SELECT details FROM status WHERE id = " . $_REQUEST["key"];

} else $query = sprintf("SELECT details FROM status WHERE key = '%s'", $_REQUEST["key"]);

Common::renderView("details", [

        "source" => isset($_REQUEST["source"]) ? $_REQUEST["source"] : "home",

        "data" => pg_fetch_all(pg_query($db, $query)) ]);
?>
