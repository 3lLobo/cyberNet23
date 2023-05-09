<?php /* views/header.php */ ?>
<TABLE WIDTH=100% ALIGN=CENTER>
    <TR>
        <TD></TD>
        <TD ALIGN=CENTER>
            <PRE>
   ________  ____ ______/ /_____  _________  ___  / /_
  / ___/ _ \/ __ `/ ___/ __/ __ \/ ___/ __ \/ _ \/ __/
 / /  /  __/ /_/ / /__/ /_/ /_/ / /  / / / /  __/ /_  
/_/   \___/\__,_/\___/\__/\____/_/  /_/ /_/\___/\__/  
            </PRE>
        </TD>
        <TD></TD>
    </TR>
    <?php if(isset($_SESSION["profile"])): ?>
    <TR>
        <TD></TD>
        <TD ALIGN=CENTER>
            <p><?= RequestProfiler::getInstance() ?></p>
        </TD>
        <TD></TD>
    </TR>
    <?php endif ?>
</TABLE>
