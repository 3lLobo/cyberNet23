<?php

if(!isset($_SESSION["operator"])) header("Location: /?page=login");

$result = pg_fetch_all(pg_query($db, "SELECT value FROM status WHERE key = 'emergency_scram_code'"));

Common::renderView("emergency", ["SCRAM" => $result[0]["value"]]);

?>
