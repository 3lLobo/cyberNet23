<?php

class Common {

    public static function checkPageValidity($page, $allow_list = []) {

        if(str_ends_with($page, ".php")) $page = substr($page, 0, -4);

        if(!strlen($page)) return false;

        if(!count($allow_list)) $allow_list = ["home", "login", "search",

            "reactor", "turbine", "radiation", "emergency",

            "details", "export", "download", "logout", "profile"];

        if(in_array($page, $allow_list)) return true;

        $new_page = mb_substr($page, 0, mb_strpos($page . "?", "?"));

        if(in_array($new_page, $allow_list)) return true;

        $new_page = urldecode($new_page);

        $new_page = mb_substr($new_page, 0, mb_strpos($new_page . "?", "?"));

        return in_array($new_page, $allow_list);
    }

    public static function renderView($view, $data = []) { 

        if(!str_ends_with($view, ".php")) $view = "$view.php";

        extract(array_merge($GLOBALS, $_REQUEST, $data), EXTR_REFS); 

        require "$cfg_view_dir/$view"; 

        return true; 
    }

    public static function runPage($controller, $data = []) {

        if(!str_ends_with($controller, ".php")) $controller = "$controller.php";

        extract(array_merge($GLOBALS, $_REQUEST, $data), EXTR_REFS); 

        require "$cfg_controller_dir/$controller"; 

        return true; 
    }

    public static function safePath($filename) {

        if(!strlen($filename)) return false;
        
        return str_replace("..", ".", $filename);
    }

    public static function loadJSON($filename) {

        $contents = file_get_contents($filename);
        
        return json_decode($contents, true);
    }
}

class RequestProfiler { 

    private $start_time = false;

    private $start_load = false;

    private $load_command = "/usr/bin/uptime";

    public static $instance = null;

    public static function getInstance() {

        if(!isset(self::$instance)) self::$instance = new RequestProfiler();

        return self::$instance;
    }

    public function startProfiling() {

        $this->start_time = microtime(true);

        $this->start_load = $this->getCurrentLoad();

        if(isset($_REQUEST["profile_debug"])) {

            printf("<-- %s -->\n", $this->getCurrentStatus());

            register_shutdown_function(function($self) {

                printf("<-- %s -->\n", $self->getCurrentStatus());

            }, $this);
        }

        return true;
    }

    private function getCurrentLoad() {

        $load_output = [];

        if(!exec("/usr/bin/uptime", $load_output)) return false;

        $load_output = implode($load_output);

        $load_output = explode("load average: ", $load_output)[1];

        $load_output = explode(",", $load_output)[0];

        $load_output = str_replace(" ", "", $load_output);

        return $load_output;
    }

    public function getCurrentStatus() {

        $current_time = microtime(true);

        $current_load = $this->getCurrentLoad();

        return sprintf("duration=%fs start_load=%s current_load=%s",

            $current_time - $this->start_time,

            $this->start_load, $current_load);
    }

    public function __toString() { return $this->getCurrentStatus(); } 
}
?>
