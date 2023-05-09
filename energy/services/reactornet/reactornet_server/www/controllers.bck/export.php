<?php

$data = $_REQUEST["data"] or die("Invalid argument specified");

$data = unserialize(base64_decode($data));

if(!is_array($data)) die("Invalid value ($data) specified");

$name = isset($_REQUEST["name"]) ? $_REQUEST["name"] : "export";

$filename = sprintf("%s-%s", uniqid(rand()), $name);

if(!($handle = fopen(sprintf("%s/%s", $cfg_download_dir, $filename), "w"))) die("Unexpected failure");

foreach($data as $record) fputcsv($handle, $record);

fclose($handle);

header(sprintf("Location: /?page=download&filename=%s", urlencode($filename)));

?>
