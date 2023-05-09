<?php

if(!isset($_REQUEST["key"])) die("Invalid argument specified");

if(intval($_REQUEST["key"])) {
    $query = pg_prepare($db, "search_query", "SELECT details FROM status WHERE id = $1");
} else {

$query = pg_prepare($db, "search_query", "SELECT details FROM status WHERE key = $1");
}
//$query = sprintf("SELECT details FROM status WHERE key = '%s'", $_REQUEST["key"])   

//$query = "SELECT details FROM status WHERE id = " . $_REQUEST["key"];


Common::renderView("details", [

        "source" => isset($_REQUEST["source"]) ? $_REQUEST["source"] : "home",

        "data" => pg_fetch_all(pg_execute($db, "search_query", array($_REQUEST["key"]))) ]);
?>
