<?php

$result = [];

if(isset($_REQUEST["query"])) {

    // FIX-3019: Make sure to not disclose sensitive data

    $banned_word_list = ["emergency", "scram", "code", "password", "admin"];

    if(strlen(trim($_REQUEST["query"])) < $cfg_min_search_length) goto render_result;

    foreach($banned_word_list as $word) if(stripos($_REQUEST["query"], $word) !== false) goto render_result;
        
    $result = pg_fetch_all(pg_query($db, 

        sprintf("SELECT * FROM status WHERE key LIKE '%%%s%%' OR value LIKE '%%%s%%'", 

        $_REQUEST["query"], $_REQUEST["query"])));
}

render_result:

Common::renderView("search", ["data" => $result]);

?>
