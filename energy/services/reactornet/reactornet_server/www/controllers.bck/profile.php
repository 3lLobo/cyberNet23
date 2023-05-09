<?php

if(isset($_REQUEST["operation"]) && 
        
        $_REQUEST["operation"] == "enable") {

    $_SESSION["profile"] = true;

} else $_SESSION["profile"] = null;

header("Location: /");

?>
