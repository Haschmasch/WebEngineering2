import React, {useEffect, useState} from 'react';
import {getOffers} from "../../../fetchoperations/OffersOperations";
import Cards from '../../cards/Cards';
import Button from "@mui/material/Button";
import {createSvgIcon} from '@mui/material/utils';

function Home() {
    const [offers, setOffers] = useState([]);
    const auth = localStorage.getItem("isLogin");

    const PlusIcon = createSvgIcon(
        // credit: plus icon from https://heroicons.com/
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
        const response = getOffers();
        if (response) {
            response.then((data) => {
                setOffers(data);
            }).catch((error) => console.error(error));
        }
    }, []);

    return (
        <>
            <h1>Willkommen bei GenuineGoods!</h1>
            {auth ? (<Button className={"offersNavbar"}
                        variant="outlined"
                        color="inherit"
                        startIcon={<PlusIcon/>}
                        href="AddOffer"
                        style={{ marginLeft: "20px", marginTop: "20px" }}>
                            Angebot hinzufügen
                        </Button>) : (<>
            </>)}

            <Cards offers={offers}/>
        </>
    );
}

export default Home;
