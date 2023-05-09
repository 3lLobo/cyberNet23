<?php /* views/home.php */ ?>
<HTML>
<HEAD><TITLE>REACTORNET</TITLE></HEAD>
<BODY>
<?php Common::renderView("header") ?>
<UL>
    <LI><A HREF="/?page=reactor">Reactor Status</A></LI>
    <LI><A HREF="/?page=turbine">Turbine Status</A></LI>
    <LI><A HREF="/?page=radiation">Radiation Monitoring</A></LI>
    <LI><A HREF="/?page=search">Status Search</A></LI>
    <?php if(isset($_SESSION["profile"])): ?>
        <LI><A HREF="/?page=profile&operation=disable">Disable Profiling</A></LI>
    <?php else: ?>
        <LI><A HREF="/?page=profile&operation=enable">Enable Profiling</A></LI>
    <?php endif ?>
    <LI><A HREF="/?page=emergency">Emergency</A></LI>
    <?php if(isset($_SESSION["operator"])): ?>
        <LI><A HREF="/?page=logout">Logout</A></LI>
    <?php endif ?>
</UL>
</BODY>
</HTML>
