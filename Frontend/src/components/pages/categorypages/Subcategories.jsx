import React, {useEffect, useState} from 'react';
import {getSubcategoryWithOffers} from "../../../fetchoperations/SubCategoriesOperations";
import {useParams} from 'react-router-dom';
import Button from "@mui/material/Button";
import Cards from '../../cards/Cards';
import {isLoggedIn} from "../../utils/StorageInterface";
import AddIcon from "@mui/icons-material/Add";

function Subcategories() {
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
                                      color="inherit"
                                      startIcon={<AddIcon/>}
                                      href="../../../AddOffer"
                                      style={{marginLeft: "20px", marginTop: "20px"}}>
                Angebot hinzufügen
            </Button>)}
            <Cards offers={subCategoryOffers}/>
        </>
    );
}

export default Subcategories;