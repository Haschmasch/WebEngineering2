/* Copyright field that is being used in the Login, Registration and Footer,
Usage of MUI Library*/
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";
import React from "react";

export default function Copyright(props) {
    return (
        <Typography
            variant="body2"
            color="text.secondary"
            align="center"
            {...props}
        >
            {"Copyright © "}
            <Link color="inherit" href="/">
                GenuineGoods
            </Link>{" "}
            {new Date().getFullYear()}
            {"."}
        </Typography>
    );
}