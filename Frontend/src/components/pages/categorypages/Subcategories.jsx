import React, { useEffect, useState } from 'react';
import { getSubcategoryWithOffers } from "../../../fetchoperations/SubCategoriesOperations";
import { useParams } from 'react-router-dom';
import { createSvgIcon } from '@mui/material/utils';
import Button from "@mui/material/Button";
import Cards from '../../cards/Cards';

function Subcategories() {
    const {subcategory_id} = useParams();
    const [subcategoryoffers, setSubcategoryOffers] = useState([]);  
    const auth = localStorage.getItem("isLogin");
    const [subcategory, setSubcategory] = useState();

    const PlusIcon = createSvgIcon(
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>,
        'Plus',
      );
    
    useEffect(() => {
        const response = getSubcategoryWithOffers(subcategory_id);
        if (response) {
            response.then((data) => {
                setSubcategoryOffers(data.related_offers);
                setSubcategory(data.name);
            }).catch((error) => console.error(error));
        }
    }, [subcategory_id]);
    return (
        <>
            <h1>{subcategory}</h1>
            {auth ? (<Button className={"offersNavbar"}
                        variant="outlined"
                        color="inherit"
                        startIcon={<PlusIcon/>}
                        href="../../../AddOffer"
                        style={{ marginLeft: "20px", marginTop: "20px" }}>
                            Angebot hinzufügen
                        </Button>) : (<>
            </>)}

            <Cards offers={subcategoryoffers}/>
        </>
    );
}

export default Subcategories;