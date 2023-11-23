import React, {useState} from "react";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Link from "@mui/material/Link";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import {createTheme, ThemeProvider} from "@mui/material/styles";
import Swal from "sweetalert2";

import {checkUsernameAvailability, registerUser, userLogin,} from "../../../fetchoperations/UsersOperation";
import {storeCredentials} from "../../utils/StorageInterface";

function Copyright(props) {
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

const defaultTheme = createTheme();

export default function SignUp() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [phonenumber, setPhonenumber] = useState("");

    const submitRegistration = async () => {
        const isUsernameAvailable = await checkUsernameAvailability(name);

        if (isUsernameAvailable) {
            await registerUser(name, email, password, phonenumber)
                .then(() => userLogin(name, password))
                .then((storage) =>
                    storeCredentials(storage)
                );

            Swal.fire({
                title: "Erfolgreiche Registrierung",
                icon: "success",
                html:
                    "Sie haben sich mit folgenden Informationen registriert:<br><br>" +
                    `<b>Benutzername: </b> ${name}<br>` +
                    `<b>E-Mail: </b> ${email}<br>` +
                    `<b>Telefonnummer: </b> ${phonenumber}<br>`,
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText: "OK",
                confirmButtonColor: "#0989ff",
            }).then(function () {
                window.location = "/";
            });
        } else {
            await Swal.fire({
                title: "<b>Benutzername bereits vergeben</b>",
                icon: "error",
                html: "Der Benutzername ist bereits vergeben. Bitte wählen Sie einen anderen.",
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText: "OK",
                confirmButtonColor: "#0989ff",
            });
        }
    };

    function isEmailValid(email) {
        const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
        return emailRegex.test(email);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!isEmailValid(email)) {
            Swal.fire({
                title: "Ungültiges E-Mail-Format",
                icon: "info",
                html: "Bitte geben Sie eine gültige E-Mail-Adresse ein.",
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText: "OK",
                confirmButtonColor: "#0989ff",
            });
        } else if (password.length > 5) {
            submitRegistration();
        } else {
            Swal.fire({
                title: `Registrierung fehlgeschlagen `,
                icon: "info",
                html: "Das Passwort sollte länger als 5 Zeichen sein!",
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText: "OK",
                confirmButtonColor: "#0989ff",
            });
        }
    };

    return (
        <ThemeProvider theme={defaultTheme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline/>
                <Box
                    sx={{
                        marginTop: 8,
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                    }}
                >
                    <Avatar sx={{m: 1, bgcolor: "#0989ff"}}>
                        <LockOutlinedIcon/>
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Registrieren
                    </Typography>
                    <Box
                        component="form"
                        noValidate
                        onSubmit={handleSubmit}
                        sx={{mt: 3}}
                    >
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <TextField
                                    autoComplete="given-name"
                                    name="name"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    required
                                    fullWidth
                                    id="name"
                                    label="Benutzername"
                                    autoFocus
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    id="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    label="E-Mail Adresse"
                                    name="email"
                                    autoComplete="email"
                                    type={"email"}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    id="phonenumber"
                                    value={phonenumber}
                                    onChange={(e) => setPhonenumber(e.target.value)}
                                    label="Telefonnummer"
                                    name="phonenumber"
                                    autoComplete="phonenumber"
                                    type="phonenumber"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    required
                                    fullWidth
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    name="password"
                                    label="Passwort"
                                    type="password"
                                    id="password"
                                    autoComplete="new-password"
                                />
                            </Grid>
                        </Grid>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{mt: 3, mb: 2}}
                        >
                            Registrieren
                        </Button>
                        <Grid container justifyContent="flex-end">
                            <Grid item>
                                <Link
                                    href="../signin"
                                    variant="body2"
                                    sx={{
                                        "&:hover": {color: "darkgrey", transition: "0.8s"},
                                        textDecoration: "none",
                                    }}
                                >
                                    Bereits registriert? Anmelden
                                </Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
                <Copyright sx={{mt: 5}}/>
            </Container>
        </ThemeProvider>
    );
}
