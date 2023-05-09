<?php /* views/login.php */ ?>
<HTML>
<HEAD><TITLE>REACTORNET</TITLE></HEAD>
<BODY>
<?php Common::renderView("header"); ?>
<TABLE WIDTH=100% ALIGN=CENTER>
<TBODY>
<TR>
    <TD ALIGN=LEFT><?php Common::renderView("danger"); ?></TD>
	<TD ALIGN=CENTER VALIGN=TOP CELLSPACING=5 CELLPADDING=5>
        <A HREF="/?page=home">&lt; Back</a>
        <H1>AUTHENTICATION REQUIRED</H1>
        <?php if(isset($failure)): ?><H2>ACCESS DENIED</H2><?php endif ?>
        <P>Access to the Emergency Settings menu is restricted to authorized personnel only. This screen contains sensitive and critical information related to the safety control systems used to rapidly shut down the nuclear reactor in case of an emergency or abnormal situation. </P>
        <FORM METHOD="POST" ACTION="/?page=login">
            <LABEL>OPERATOR PASSWORD:</LABEL>
            <INPUT TYPE="password" NAME="password"/>
            <BR/><BR/>
            <INPUT TYPE="submit"/>
        </FORM>
	</TD>	
    <TD ALIGN=RIGHT><?php Common::renderView("danger"); ?></TD>
</TR>
</TBODY>
</TABLE>
</BODY>

