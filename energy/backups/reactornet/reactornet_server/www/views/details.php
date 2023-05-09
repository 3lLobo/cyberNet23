<?php /* views/details.php */ ?>
<HTML>
<HEAD><TITLE>REACTORNET</TITLE></HEAD>
<BODY>
<?php Common::renderView("header"); ?>
<UL>
    <LI><A HREF="/?page=<?= urlencode($source) ?>">&lt; Back</A></LI>
</UL>
<TABLE BORDER=1 CELLSPACING=1 WIDTH=100% ALIGN=CENTER>
<THEAD>
<TR>
    <TH ALIGN=CENTER><?= htmlspecialchars($key) ?></TH>
</TR>
</THEAD>
<TBODY>
<TR>
    <TD ALIGN=CENTER><?= $data[0]["details"] ?></TD>
</TR>
</TBODY>
</TABLE>
</BODY>

