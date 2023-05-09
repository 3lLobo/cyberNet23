<?php

$filename = $_REQUEST["filename"] or die("Invalid argument specified");

$filename = sprintf("%s/%s", $cfg_download_dir, Common::safePath($filename));

if(!strlen($filename)) die("Invalid argument specified");

if(!file_exists($filename)) die("Invalid argument specified");

header("Content-Description: ReactorNet Export");

header("Content-Type: text/csv");

header('Content-Disposition: attachment; filename="export.csv"');

header("Cache-Control: no-cache no-store");

header(sprintf("Content-Length: %s", filesize($filename)));

readfile($filename);

?>
