<?php /* views/search.php */ ?>
<HTML>
<HEAD><TITLE>REACTORNET</TITLE></HEAD>
<BODY>
<?php Common::renderView("header"); ?>
<TABLE WIDTH=100% ALIGN=CENTER>
<TBODY>
<TR>
	<TD ALIGN=CENTER VALIGN=TOP CELLSPACING=5 CELLPADDING=5>
        <A HREF="/?page=home">&lt; Back</a>
        <BR/><BR/>
        <FORM METHOD="POST" ACTION="/?page=search">
            <LABEL>KEYWORDS:</LABEL>
            <INPUT TYPE="text" NAME="query" VALUE="<?=isset($query) ? htmlspecialchars($query) : ""?>"/>
            <BR/><BR/>
            <INPUT TYPE="submit" VALUE="SEARCH"/>
        </FORM>
	</TD>	
</TR>
<?php if(count($data)): ?>
    <TR><TD>&nbsp;</TD></TR>
    <TR>
        <TD>
            <TABLE BORDER=1 CELLPADDING=10 WIDTH=100% ALIGN=CENTER>
            <THEAD>
            <TR>
                <TH ALIGN=CENTER>Component</TH>
                <TH ALIGN=CENTER>Current Value</TH>
                <TH ALIGN=CENTER>Unit</TH>
                <TH ALIGN=CENTER>Description</TH>
            </TR>
            </THEAD>
            <TBODY>
            <?php foreach($data as $record): ?>
            <TR>
                <TD ALIGN=CENTER><?= $record["key"] ?></TD>
                <TD ALIGN=CENTER><?= $record["value"] ?></TD>
                <TD ALIGN=CENTER><?= $record["unit"] ?></TD>
                <TD ALIGN=CENTER><?= $record["details"] ?></TD>
            </TR>
            <?php endforeach ?>
            </TBODY>
            </TABLE>
        </TD>
    </TR>
<?php endif ?>
</TBODY>
</TABLE>
</BODY>

