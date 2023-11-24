/* Homepage with all Offers */

import React, {useEffect, useState} from 'react';
import {getOffers} from "../../../fetchoperations/OffersOperations";
import Cards from '../../cards/Cards';
import Button from "@mui/material/Button";
import './Home.css';
import {isLoggedIn} from "../../utils/StorageInterface";
import AddIcon from "@mui/icons-material/Add";

export default function Home() {
    const [offers, setOffers] = useState([]);

    useEffect(() => {
        getOffers().then((data) => {
            setOffers(data);
        }).catch((error) => console.error(error));
    }, []);

    return (
        <>
            <div className="home-title">
                <h1>Das beste Kleinanzeigeportal</h1>
                <p>Einfach gut</p>
            </div>
            {isLoggedIn() && (<Button className={"offersNavbar"}
                                      variant="outlined"
                                      bgcolor="#456385"
                                      startIcon={<AddIcon color="#456385"/>}
                                      href="AddOffer"
                                      style={{marginLeft: "20px", marginTop: "50px", backgroundColor: "fefefe"}}>
                Angebot hinzufügen
            </Button>)}
            <Cards offers={offers}/>
        </>
    );
};
