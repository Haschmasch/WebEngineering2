import React, { useEffect, useState } from 'react';
import { getCategoryWithOffers } from "../../../fetchoperations/CategoriesOperations";
import { useParams } from "react-router-dom";
import { createSvgIcon } from '@mui/material/utils';
import Button from "@mui/material/Button";
import Cards from '../../cards/Cards';

function Categories() {
    const {category_id} = useParams();
    const [offers, setOffers] = useState([]);
    const auth = localStorage.getItem("isLogin");
    const [category, setCategory] = useState();

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
            {auth ? (<Button className={"offersNavbar"}
                        variant="outlined"
                        color="inherit"
                        startIcon={<PlusIcon/>}
                        href="../../../AddOffer"
                        style={{ marginLeft: "20px", marginTop: "20px" }}>
                            Angebot hinzufügen
                        </Button>) : (<>
            </>)}

            <Cards offers={offers}/>
        </>
    );
}

export default Categories;