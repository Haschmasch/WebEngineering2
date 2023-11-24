import React, {useEffect, useState} from 'react';
import {getCategoryWithOffers} from "../../../fetchoperations/CategoriesOperations";
import {useParams} from "react-router-dom";
import Button from "@mui/material/Button";
import AddIcon from '@mui/icons-material/Add';
import Cards from '../../cards/Cards';
import {isLoggedIn} from "../../utils/StorageInterface";

export default function Categories() {
    const {category_id} = useParams();
    const [offers, setOffers] = useState([]);
    const [category, setCategory] = useState();

    useEffect(() => {
        const response = getCategoryWithOffers(category_id);
        if (response) {
            response.then((data) => {
                setOffers(data.related_offers);
                setCategory(data.name);
            }).catch((error) => console.error(error));
        }
    }, [category_id]);

    return (
        <>
            <h1>{category}</h1>
            {isLoggedIn() && (<Button className={"offersNavbar"}
                                      variant="outlined"
                                      bgcolor="#456385"
                                      startIcon={<AddIcon color="#456385"/>}
                                      href="../../AddOffer"
                                      style={{marginLeft: "20px", marginTop: "50px", backgroundColor: "fefefe"}}>
                Angebot hinzufügen
            </Button>)}
            <Cards offers={offers}/>
        </>
    );
}