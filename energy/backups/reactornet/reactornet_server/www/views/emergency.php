<?php /* views/login.php */ ?>
<HTML>
<HEAD><TITLE>REACTORNET</TITLE></HEAD>
<BODY>
<?php Common::renderView("header"); ?>
<TABLE WIDTH=100% ALIGN=CENTER>
<TBODY>
<TR>
    <TD ALIGN=LEFT VALIGN=TOP><?php Common::renderView("danger"); ?></TD>
    <TD>&nbsp;&nbsp;</TD>
	<TD ALIGN=CENTER VALIGN=TOP CELLSPACING=5 CELLPADDING=5>
        <A HREF="/?page=home">&lt; Back</a>
        <P>CURRENT SCRAM CODE:<BR/><BR/> <i><?= $SCRAM ?></I></P>
        <P>In the event of an emergency at the nuclear power plant, it may be necessary to initiate a SCRAM to rapidly shut 
        down the reactor and prevent further damage. The emergency procedure for using the SCRAM code is as follows:</P>
        <P>
        1. Immediately notify the control room of the emergency situation.<BR/><BR/>
        2. Access the Emergency menu using your authorized security credentials.<BR/><BR/>
        3. Communicate the SCRAM code to your supervisor.<BR/><BR/>
        4. <B>Run</B></BR>
        </P>
	</TD>	
    <TD>&nbsp;&nbsp;</TD>
    <TD ALIGN=RIGHT VALIGN=TOP><?php Common::renderView("danger"); ?></TD>
</TR>
</TBODY>
</TABLE>
</BODY>

