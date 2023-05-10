express = require("express");
jwt = require("jsonwebtoken");


token = jwt.sign({ username: "admin" }, "TBDTBDTBDTBDTBDTBDTBDTBDTBDTBDTBD", {expiresIn: 172800,});
print(token)
