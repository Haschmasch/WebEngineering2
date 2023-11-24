/* Userprofile Page.
Contains Usersettings, all Offers created by an individual user and all chats the User has */

import React, {useEffect, useState} from "react";
import "./UserProfile.css";
import Button from "@mui/material/Button";
import Swal from "sweetalert2";
import {deleteUser, getUser, updateUser} from "../../../fetchoperations/UsersOperation";
import {FormLabel, Input} from "@mui/material";
import {getUser_id} from "../../utils/StorageInterface";
import DeleteIcon from "@mui/icons-material/Delete";
import UserOffers from "./UserOffers";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";

const handleSubmit = async (e) => {
    e.preventDefault();
    Swal.fire({
        title: "Sind Sie sicher?",
        text: "Ihre Daten werden gelöscht und können nicht wiederhergestellt werden!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Bestätigen",
        cancelButtonText: "Abbrechen",
    }).then((result) => {
        if (result.isConfirmed) {
            deleteUser().then(() => {
                Swal.fire({
                    title: "Konto gelöscht",
                    icon: "success",
                    html: "Ihr Konto wurde erfolgreich gelöscht.",
                    showCloseButton: true,
                    focusConfirm: false,
                    confirmButtonText: "OK",
                    confirmButtonColor: "#0989ff",
                }).then(function () {
                    window.location = "/";
                });
            })
        }
    });
};

export default function UserProfile() {
    const [email, setEmail] = useState("")
    const [phoneNumber, setPhoneNumber] = useState("")
    const [timeCreated, setTimeCreated] = useState("")
    const [editable, setEditable] = useState(false);

    useEffect(() => {
        getUser(getUser_id()).then(r => {
                setEmail(r.email);
                setPhoneNumber(r.phone_number);
                setTimeCreated(r.time_created);
            }
        )
    }, []);

    return (
        <>
            <div className="section">
                <Box sx={{width: '100%', height: '100%'}}>
                    <Grid container gap={{xs: 1}} columnSpacing={{xs: 1, sm: 2, md: 3}}>
                        <Grid item xs={3}>
                            <h1 id="profile-title">Dein Profil</h1>
                            <Box className="UserProfilBox" sx={{maxWidth: "100%"}}>
                                <Button name={'edit'} onClick={() => setEditable(edit => !edit)}>
                                    Profilinformationen bearbeiten
                                </Button>
                                <FormLabel style={{padding: "10px"}}>Email:</FormLabel>
                                <Input value={email} disabled={!editable} style={{paddingLeft: "20px"}}
                                       onChange={e => setEmail(e.target.value)}/>
                                <FormLabel style={{padding: "10px"}}>Telefonnummer:</FormLabel>
                                <Input value={phoneNumber} disabled={!editable} style={{paddingLeft: "20px"}}
                                       onChange={e => setPhoneNumber(e.target.value)}/>

                                {editable && (<Button name={'confirm'} onClick={() => {
                                        setEditable(false)
                                        getUser(getUser_id()).then(r => updateUser(r.name, email, phoneNumber, timeCreated)).then(r => {
                                            setEmail(r.email);
                                            setPhoneNumber(r.phone_number);
                                        })
                                    }}>
                                        Änderungen bestätigen
                                    </Button>
                                )}
                                <br/>
                                <Button
                                    variant="contained"
                                    color="error"
                                    startIcon={<DeleteIcon/>}
                                    onClick={handleSubmit}
                                    style={{margin: "20px"}}
                                >
                                    Konto löschen
                                </Button>
                            </Box>
                        </Grid>
                        <Grid item xs={8}>
                            <h1 id="profile-title">Deine Angebote</h1>
                            <UserOffers/>
                        </Grid>
                    </Grid>
                </Box>
            </div>
        </>
    );
}


