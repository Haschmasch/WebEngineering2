import React, { useEffect, useState } from 'react';
import { getUserWithOffers } from '../../../fetchoperations/UsersOperation';
import Cards from '../../cards/Cards';
import Box from "@mui/material/Box";

function UserOffers() {
 
    const [userOffers, setUserOffers] = useState([]);  
    useEffect(() => {
        const response = getUserWithOffers();
        if (response) {
            response.then((data) => {
                setUserOffers(data.related_offers);
            }).catch((error) => console.error(error));
        }
    }, []);
    return (
        <>
            <Cards offers={userOffers}/>
        </>
    );
}

export default UserOffers;