/* Subcategory page where all Offers to associated Subcategory shows up */

import React, {useEffect, useState} from 'react';
import {getSubcategoryWithOffers} from "../../../fetchoperations/SubCategoriesOperations";
import {useParams} from 'react-router-dom';
import Button from "@mui/material/Button";
import Cards from '../../cards/Cards';
import {isLoggedIn} from "../../utils/StorageInterface";
import AddIcon from "@mui/icons-material/Add";

export default function Subcategories() {
    const {subcategory_id} = useParams();
    const [subCategoryOffers, setSubCategoryOffers] = useState([]);
    const [subcategory, setSubcategory] = useState();

    useEffect(() => {
        const response = getSubcategoryWithOffers(subcategory_id);
        if (response) {
            response.then((data) => {
                setSubCategoryOffers(data.related_offers);
                setSubcategory(data.name);
            }).catch((error) => console.error(error));
        }
    }, [subcategory_id]);

    return (
        <>
            <h1>{subcategory}</h1>
            {isLoggedIn() && (<Button className={"offersNavbar"}
                                      variant="outlined"
                                      bgcolor="#456385"
                                      startIcon={<AddIcon color="#456385"/>}
                                      href="../../../AddOffer"
                                      style={{marginLeft: "20px", marginTop: "50px", backgroundColor: "fefefe"}}>
                Angebot hinzufügen
            </Button>)}
            <Cards offers={subCategoryOffers}/>
        </>
    );
};

