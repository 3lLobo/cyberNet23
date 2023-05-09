<?php

if(isset($_REQUEST["password"])) {

    if(!strcmp($cfg_secure["operator_password"], $_REQUEST["password"])) {

        $_SESSION["operator"] = true;
    
        header("Location: /?page=emergency");

    } else $_REQUEST["failure"] = true;
}

Common::renderView("login", $_REQUEST);

?>
