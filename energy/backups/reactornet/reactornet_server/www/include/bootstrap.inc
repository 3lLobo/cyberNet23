<?php
header("Cache-Control: no-cache no-store");
if(isset($_SESSION["profile"])) RequestProfiler::getInstance()->startProfiling();
$db = pg_connect($cfg_secure["database"]) or die("Could not connect to database");
?>
