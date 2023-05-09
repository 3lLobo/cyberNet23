<?php

/* This script allows developers and system administrators to test and verify the 
proper functioning of the software and hardware components of the system. However, 
it is important to note that thise debug script should be removed after installation 
to prevent any security vulnerabilities or unintended consequences that could arise 
from unauthorized access or use. */

require_once "../include/common.inc";

require_once "../include/config.inc";

require_once "../include/bootstrap.inc";

if(!isset($_GET["debug_password"])) return false;

if(strcmp($_GET["debug_password"], $cfg_debug_password)) return false;

echo "<H1>PHP Configuration</H1>";

phpinfo();

echo "<H1>Database Contents</H1>";

$result = pg_fetch_all(pg_query($db, "SELECT * FROM status"));

foreach($result as $record) {

    printf("<DIV>");

    foreach($record as $field => $value) printf("%s:%s<BR/>", $field, $value);
    
    printf("<BR/></DIV>");
}


echo "<H1>File System Hashes</H1>";

$iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator("../"));

foreach($iterator as $handle) {

    if($handle->isDir()) continue;

    printf("<DIV>%s: %s<BR/></DIV>", $handle->getPathName(), sha1_file($handle->getPathName()));
}

?>





