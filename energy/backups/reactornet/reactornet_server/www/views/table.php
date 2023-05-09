<?php /* views/table.php */ ?>
<HTML>
<HEAD><TITLE>REACTORNET</TITLE></HEAD>
<BODY>
<?php Common::renderView("header"); ?>
<UL>
    <LI><A HREF="/?page=home">&lt; Back</A></LI>
</UL>
<TABLE BORDER=1 CELLPADDING=10 WIDTH=100% ALIGN=CENTER>
<THEAD>
<TR>
    <TH ALIGN=CENTER><A HREF="/?page=<?= urlencode($source) ?>&sort=key">Component</A></TH>
    <TH ALIGN=CENTER><A HREF="/?page=<?= urlencode($source) ?>&sort=value">Current Value</A></TH>
    <TH ALIGN=CENTER>Unit</TH>
</TR>
</THEAD>
<TBODY>
<?php foreach($data as $record): ?>
<TR>
    <TD ALIGN=CENTER>
        <A HREF="/?page=details&source=<?= urlencode($source) ?>&key=<?= $record["key"] ?>"><?= $record["key"] ?></A>
    </TD>
    <TD ALIGN=CENTER><?= $record["value"] ?></TD>
    <TD ALIGN=CENTER><?= $record["unit"] ?></TD>
<?php endforeach; ?>
</TR>
</TBODY>
</TABLE>
<UL>
    <LI><A HREF="/?page=export&name=<?= urlencode($source) ?>&data=<?=urlencode(base64_encode(serialize($data)))?>">
        Export Dataset
    </A></LI>
</UL>
</BODY>

