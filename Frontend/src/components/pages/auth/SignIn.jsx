/* Sign In page */

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

import {userLogin} from "../../../fetchoperations/UsersOperation";
import {storeCredentials} from "../../utils/StorageInterface";
import Copyright from "../../utils/Copyright";

const defaultTheme = createTheme();

export default function SignIn() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await userLogin(username, password);

        storeCredentials(response).then(() => {
            Swal.fire({
                title: "<b>Willkommen zurück!</b>",
                icon: "success",
                html: "Sie sind erfolgreich eingeloggt.",
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText: "Weiter",
                confirmButtonColor: "#456385",
            }).then(function () {
                window.location = "/";
            });
        }, () => {
        });
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
                    <Avatar sx={{m: 1, bgcolor: "#456385"}}>
                        <LockOutlinedIcon/>
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Anmelden
                    </Typography>
                    <Box
                        component="form"
                        onSubmit={handleSubmit}
                        noValidate
                        sx={{mt: 1}}
                    >
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="UnameOrEmail"
                            label="Benutzername oder E-Mail Adresse"
                            name="UnameOrEmail"
                            type="UnameOrEmail"
                            autoComplete="UnameOrEmail"
                            onChange={(e) => setUsername(e.target.value)}
                            autoFocus
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Passwort"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{mt: 3, mb: 2, bgcolor: "#456385"}}
                        >
                            Anmelden
                        </Button>
                        <Grid container>
                            <Grid item>
                                <Link
                                    href="../signup"
                                    variant="body2"
                                    sx={{
                                        "&:hover": {color: "darkgrey", transition: "0.8s"},
                                        textDecoration: "none",
                                    }}
                                >
                                    {"Noch keinen Account? Jetzt registrieren!"}
                                </Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
                <Copyright sx={{mt: 8, mb: 4}}/>
            </Container>
        </ThemeProvider>
    );
}

