import React, {useEffect, useState} from "react";

import "./AddOfferStyles.css"
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Select from '@mui/material/Select';
import Container from "@mui/material/Container";
import {createTheme, styled, ThemeProvider} from "@mui/material/styles";
import {FormLabel, MenuItem} from "@mui/material";
import Swal from "sweetalert2";

import {addOffer, createOfferImages} from "../../../fetchoperations/OffersOperations";
import {getCategories, getCategory} from "../../../fetchoperations/CategoriesOperations";
import CloudUploadIcon from '@mui/icons-material/CloudUpload';


const defaultTheme = createTheme();

export default function AddOffers() {
    const [title, setTitle] = useState("");
    const [category_id, setCategory_id] = useState('');
    const [subcategory_id, setSubcategory_id] = useState('');
    const [price, setPrice] = useState(1);
    const [currency, setCurrency] = useState("€");
    const [postcode, setPostcode] = useState("");
    const [city, setCity] = useState("");
    const [address, setAddress] = useState("");
    const [description, setDescription] = useState("");
    const [images, setImages] = useState([]);
    const [short_description, setShort_description] = useState("");
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [subcategories, setSubcategories] = useState([]);
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        getCategories().then((data) => {
            setCategories(data);
            setCategory_id(1)
        }).catch((error) => console.error(error));
    }, []);

    const VisuallyHiddenInput = styled('input')({
        clip: 'rect(0 0 0 0)',
        clipPath: 'inset(50%)',
        height: 1,
        overflow: 'hidden',
        position: 'absolute',
        bottom: 0,
        left: 0,
        whiteSpace: 'nowrap',
        width: 1,
    });

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

    useEffect(() => {
        const response = getCategory(category_id);
        if (response) {
            response.then((data) => {
                if (data?.related_subcategories?.length > 0) {
                    setSubcategories(data.related_subcategories);
                    setSubcategory_id(data.related_subcategories[0]?.id);
                } else {
                    setSubcategories(null);
                    setSubcategory_id('');
                }
            }).catch((error) => console.error(error));
        }
    }, [category_id]);

    const handleImageChange = (e) => {
        const files = e.target.files;
        setSelectedFiles(Array.from(files))
    };

    const submitOffer = () => {
        const subcategoryId = subcategory_id ? subcategory_id : null;
        if(selectedFiles.length === 0){
            Swal.fire({
                title: "Bitte ein Bild auswählen!",
                icon: "error",
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText: "Weiter",
                confirmButtonColor: "#0989ff",
            })
            return;
        }
        addOffer(title,
            category_id,
            subcategoryId,
            price,
            currency,
            postcode,
            city,
            address,
            description,
            selectedFiles[0].name,
            short_description,
        ).then((offer) => {
            offer.json().then((offer) => {
                createOfferImages(offer.id, selectedFiles).then(() => {
                    Swal.fire({
                        title: "Angebot erfolgreich hinzugefügt",
                        icon: "success",
                        showCloseButton: true,
                        focusConfirm: false,
                        confirmButtonText: "Weiter",
                        confirmButtonColor: "#0989ff",
                    })
                        .then(function () {
                            window.location = "/";
                        });
                })
            })
        }, (response) => {
            Swal.fire({
                title: "Angebot hinzufügen fehlgeschlagen",
                icon: "error",
                html: "Fehler im Backend\n" + response,
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText: "Weiter",
                confirmButtonColor: "#0989ff",
            })
        })
    };

    const handleSubmit = (e) => {
        e?.preventDefault();
        let errors = []
        if (!title.length > 0) {
            errors.push("Geben Sie einen Titel ein!");
        }
        if ((price.length === 0 && category_id !== 3) || (price.length === 0 && category_id !== 5)) {
            errors.push("<br/> Geben Sie einen Preis ein!");
        }
        if (!currency.length > 0) {
            errors.push("<br/> Geben Sie eine Währung an!");
        }
        if (!postcode.length > 0) {
            errors.push("<br/> Geben Sie Ihre Postleitzahl an!");
        }
        if (!city.length > 0) {
            errors.push("<br/> Geben Sie Ihre Stadt an!");
        }
        if (!address.length > 0) {
            errors.push("<br/> Geben Sie Ihre Addresse an!");
        }
        if (!description.length > 0) {
            errors.push("<br/> Geben Sie eine Beschreibung an!");
        }
        if (errors?.length > 0) {
            Swal.fire({
                title: "Fehler!",
                icon: "info",
                html: errors.join(""),
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText: "OK",
                confirmButtonColor: "#0989ff",
            });
        } else {
            submitOffer();
        }
    };

    return (
        <div className="AddOffer">
            <h1>Angebot erstellen</h1>
            <Box className="AddOfferBox">
                <ThemeProvider theme={defaultTheme}>
                    <Container component="main" maxWidth="lg">
                        <Box
                            component="form"
                            noValidate
                            onSubmit={handleSubmit}
                            sx={{mt: 3}}
                        >
                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <FormLabel>Titel:</FormLabel>
                                    <TextField type="text" name="title" value={title}
                                               onChange={(e) => setTitle(e.target.value)}
                                               style={{width: "300px"}}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <FormLabel>Kategorie:</FormLabel>
                                    <Select style={{width: "300px"}} name="category_id" value={category_id}
                                            onChange={(e) => {
                                                setCategory_id(e.target.value);
                                                if (e.target.value === "3" || e.target.value === "5") {
                                                    setPrice(0);
                                                }
                                            }}>
                                        {categories?.map(item => {
                                            return (<MenuItem key={item.id} value={item.id}>{item.name}</MenuItem>);
                                        })}
                                    </Select>
                                </Grid>
                                <Grid item xs={12}>
                                    <FormLabel>Unterkategorie:</FormLabel>
                                    <Select style={{width: "300px"}} name="subcategory_id"
                                            disabled={subcategories === null} value={subcategory_id}
                                            onChange={(e) => setSubcategory_id(e.target.value)}>
                                        {subcategories === null ? <MenuItem>Keine Unterkategorie vorhanden</MenuItem> :
                                            subcategories?.map(item => {
                                                return (<MenuItem key={item.id} value={item.id}>{item.name}</MenuItem>);
                                            })
                                        }
                                    </Select>
                                </Grid>
                                <Grid item xs={12}>
                                    <FormLabel>Preis:</FormLabel><br/>
                                    <TextField style={{width: "300px"}} type="number"
                                               InputProps={{inputProps: {min: 0}}} name="price"
                                               disabled={category_id === "3" || category_id === "5"}
                                               value={price} onChange={(e) => setPrice(e.target.value)}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <FormLabel>Währung:</FormLabel><br/>
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
                                </Grid>
                                <Grid item xs={12}>
                                    <FormLabel>Postleitzahl:</FormLabel><br/>
                                    <TextField style={{width: "300px"}} type="text" name="postcode" value={postcode}
                                               onChange={(e) => setPostcode(e.target.value)}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <FormLabel>Stadt:</FormLabel><br/>
                                    <TextField style={{width: "300px"}} type="text" name="city" value={city}
                                               onChange={(e) => setCity(e.target.value)}/>
                                </Grid>
                                <Grid item xs={12}>
                                    <FormLabel>Adresse: </FormLabel><br/>
                                    <TextField style={{width: "300px"}} type="text" name="address" value={address}
                                               onChange={(e) => setAddress(e.target.value)}/>
                                </Grid>
                                <Grid item xs={12}>
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
                                </Grid>
                                <Grid item xs={12}>
                                    <FormLabel> Bilder auswählen </FormLabel><br/>
                                    <Button
                                        style={{width: "300px"}}
                                        variant="contained"
                                        startIcon={<CloudUploadIcon/>}
                                        component="label">Datei auswählen
                                        <VisuallyHiddenInput type="file" name="primary_image"
                                                             onChange={handleImageChange} hidden multiple/>
                                        {/*<input type="file"*/}

                                        {/*/>*/}
                                    </Button>
                                </Grid>
                                <Button type="submit" variant="contained" style={{
                                    marginTop: "40px",
                                    width: "290px",
                                    marginLeft: "20px",
                                    marginBottom: "20px",
                                    color: ""
                                }}>Angebot erstellen</Button>
                            </Grid>
                        </Box>
                    </Container>
                </ThemeProvider>
            </Box>
        </div>
    );
}
