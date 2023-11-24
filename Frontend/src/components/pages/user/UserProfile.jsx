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
import UserChats from "./UserChats";

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
            <h1>Dein Profil</h1>
            <Box className="UserProfilBox">
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
            <hr/>
            <h1>Deine Angebote</h1>
            <UserOffers/>
            <h1>Offene Chats</h1>
            <UserChats/>
        </>
    );
}


