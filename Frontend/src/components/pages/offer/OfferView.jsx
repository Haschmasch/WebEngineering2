import React, {useEffect, useState} from 'react';
import {useNavigate, useParams} from "react-router-dom";
import {deleteOffer, getOffer, getOfferImagesName, updateOffer} from "../../../fetchoperations/OffersOperations";
import Button from "@mui/material/Button";
import {addChat, getChatsByUser} from "../../../fetchoperations/ChatsOperations";
import Slideshow from "./slideshow/Slideshow";
import {getUser_id, isLoggedIn} from "../../utils/StorageInterface";
import {FormLabel, Input, MenuItem} from "@mui/material";
import Swal from "sweetalert2";
import TextField from "@mui/material/TextField";
import "./OfferView.css"
import DeleteIcon from "@mui/icons-material/Delete";
import Box from "@mui/material/Box";

export default function OfferView() {
    const {offer_id} = useParams();
    const [offer, setOffer] = useState(undefined)
    const [imageNames, setImageNames] = useState([]);
    const [editable, setEditable] = useState(false);
    const [title, setTitle] = useState("");
    const [category_id, setCategory_id] = useState(1);
    const [subcategory_id, setSubcategory_id] = useState(1);
    const [price, setPrice] = useState(1);
    const [currency, setCurrency] = useState("€");
    const [postcode, setPostcode] = useState();
    const [city, setCity] = useState("");
    const [address, setAddress] = useState("");
    const [description, setDescription] = useState("");
    const [short_description, setShort_description] = useState("");

    const navigate = useNavigate();

    const isOwner = offer?.user_id === getUser_id();

    useEffect(() => {
        getOffer(parseInt(offer_id)).then(offer => {
            setOffer(offer);
            setTitle(offer.title);
            setCategory_id(offer.category_id);
            setSubcategory_id(offer.subcategory_id);
            setPrice(offer.price);
            setCurrency(offer.currency);
            setPostcode(offer.postcode);
            setCity(offer.city);
            setAddress(offer.address);
            setDescription(offer.description);
            setShort_description(offer.short_description);
        })
        getOfferImagesName(parseInt(offer_id)).then(r => setImageNames(r));
    }, [offer_id])

    const currencies = [
        {
            value: '$',
            label: '$',
        },
        {
            value: '€',
            label: '€',
        },
        {
            value: '฿',
            label: '฿',
        },
        {
            value: '£',
            label: '£',
        },
    ];

    const createChat = async () => {

        getChatsByUser().then(chats => chats.some(chat => chat.offer_id === parseInt(offer_id) && chat.creator_id === getUser_id())).then(bool => {
            if (!bool) {
                addChat(offer_id).then(r => {
                    navigate(`/chats/${offer_id}/${r.id}`)
                }, (r) => {
                    console.log('Fehler beim Erstellen des Chats: ', r.detail);
                })
                return
            }
            getChatsByUser().then(chats => {
                return chats.filter(chat => chat.offer_id === parseInt(offer_id) && chat.creator_id === getUser_id())[0]
            }).then(r => {
                navigate(`/chats/${offer_id}/${r.id}`)
            })
        })
    };

    return (
        <div className="offer-view">
            {isOwner && (<Button onClick={() => setEditable(edit => !edit)}>Angebot bearbeiten</Button>)}
            {isOwner && editable ? (
                <>
                    <Input value={title} onChange={e => setTitle(e.target.value)}/>
                    <div className="offer-details">
                        <div className="offer-images">
                            <Slideshow offer={offer} imageNames={imageNames}/>
                        </div>
                        <Box sx={{display: "flex", flexDirection: "column"}}>
                            <div className="offer-info">
                                <FormLabel>Beschreibung:</FormLabel><br/>
                                <TextField
                                    style={{width: "300px"}}
                                    multiline
                                    placeholder="Beschreibung"
                                    name="description"
                                    value={description}
                                    minRows={4}
                                    maxRows={6}
                                    onChange={(e) => setDescription(e.target.value)}
                                    variant="outlined"
                                />
                                <div><FormLabel>Preis:</FormLabel><br/>
                                    <TextField style={{width: "300px"}} type="number" name="price"
                                               disabled={category_id === "3" || category_id === "5"}
                                               value={price} onChange={(e) => setPrice(e.target.value)}/>
                                    <TextField
                                        style={{width: "300px"}}
                                        id="outlined-select-currency"
                                        select
                                        defaultValue="€"
                                        value={currency}
                                        onChange={(e) => setCurrency(e.target.value)}
                                    >
                                        {currencies.map((option) => (
                                            <MenuItem key={option.value} value={option.value}>
                                                {option.label}
                                            </MenuItem>
                                        ))}
                                    </TextField>
                                </div>
                                <div>
                                    <FormLabel>Stadt:</FormLabel><br/>
                                    <TextField style={{width: "300px"}} type="text" name="postcode" value={postcode}
                                               onChange={(e) => setPostcode(e.target.value)}/>
                                    <TextField style={{width: "300px"}} type="text" name="city" value={city}
                                               onChange={(e) => setCity(e.target.value)}/>
                                </div>
                                <div>
                                    <FormLabel>Straße und Hausnummer:</FormLabel><br/>
                                    <TextField style={{width: "300px"}} type="text" name="address" value={address}
                                               onChange={(e) => setAddress(e.target.value)}/>
                                </div>
                            </div>
                            <Button sx={{display: "flex"}}
                                    onClick={() => {
                                        updateOffer(title, category_id, subcategory_id, price, currency, postcode, city, address, description, offer.primary_image, short_description, offer.id, offer.closed)
                                            .then(() => setEditable(false)).finally(() => getOffer(parseInt(offer_id)).then(offer => {
                                            setOffer(offer);
                                            setTitle(offer.title);
                                            setCategory_id(offer.category_id);
                                            setSubcategory_id(offer.subcategory_id);
                                            setPrice(offer.price);
                                            setCurrency(offer.currency);
                                            setPostcode(offer.postcode);
                                            setCity(offer.city);
                                            setAddress(offer.address);
                                            setDescription(offer.description);
                                            setShort_description(offer.short_description);
                                        }))
                                    }}>Änderung speichern</Button>
                            <Button variant="outlined" startIcon={<DeleteIcon/>} color="error"
                                    onClick={() => {
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
                                                const response = deleteOffer(offer_id);
                                                if (response) {
                                                    Swal.fire({
                                                        title: "Angebot gelöscht",
                                                        icon: "success",
                                                        html: "Ihr Angebot wurde erfolgreich gelöscht.",
                                                        showCloseButton: true,
                                                        focusConfirm: false,
                                                        confirmButtonText: "OK",
                                                        confirmButtonColor: "#0989ff",
                                                    }).then(function () {
                                                        window.location = "/userOffers";
                                                    });
                                                }
                                            }
                                        });
                                    }}>Angebot löschen</Button>
                        </Box>
                    </div>
                </>
            ) : (
                <>
                    <h1 className='offer-h1'>{offer?.title}</h1>
                    <div className="offer-details">
                        <div className="offer-images">
                            <Slideshow offer={offer} imageNames={imageNames}/>
                        </div>
                        <div className="offer-info">
                            <FormLabel className="offer-info-title">
                                Preis:
                            </FormLabel><br/>
                            {offer?.price} {offer?.currency}<br/><br/>

                            <FormLabel className="offer-info-title">
                                Standort:
                            </FormLabel><br/>
                            {offer?.city}<br/><br/>

                            <FormLabel className="offer-info-title">
                                Beschreibung:
                            </FormLabel><br/>
                            {offer?.description}<br/><br/>

                            {!isOwner && isLoggedIn() && (<Button
                                variant="outlined"
                                onClick={createChat}
                            >
                                Verkäufer kontaktieren
                            </Button>)}
                        </div>
                    </div>
                </>
            )}
        </div>
    );
};
