import React, {useEffect, useState} from 'react';
import {getUserWithOffers} from '../../../fetchoperations/UsersOperation';
import Cards from '../../cards/Cards';

export default function UserOffers() {
    const [userOffers, setUserOffers] = useState([]);

    useEffect(() => {
        getUserWithOffers().then((data) => {
            setUserOffers(data.related_offers);
        }).catch((error) => console.error(error));
    }, []);

    return <Cards offers={userOffers}/>
};