<?php

require_once "include/common.inc";

require_once "include/config.inc";

require_once "include/bootstrap.inc";

if(isset($_REQUEST["page"]) &&

        is_string($_REQUEST["page"]) &&

        Common::checkPageValidity($_REQUEST["page"])) {

   Common::runPage($_REQUEST["page"]); 

} else Common::runPage("home");

?>
