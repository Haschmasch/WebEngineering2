import React, {useEffect, useState} from 'react';

import './Cards.css';
import {getFollowingsByUser} from "../../fetchoperations/FollowingsOperations";
import CardItem from "./CardItem";
import Grid from "@mui/material/Grid";
import {isLoggedIn} from "../utils/StorageInterface";

function Cards({offers}) {
    const [followings, setFollowings] = useState([]);
    const [needsNewFetch, setNeedsNewFetch] = useState(0);

    useEffect(() => {
        if (isLoggedIn()) {
            getFollowingsByUser().then(r => setFollowings(r))
        }
    }, [needsNewFetch]);

    return (
        <div className='cards'>
            <Grid container spacing={4} >
                {offers.map((offer, index) => (
                    <Grid item xs={12} sm={4} md={3} lg={2} xl={2} key={index} margin={"10px"} className='cards__items'>
                            <CardItem
                                key={offer.id}
                                src={offer.primary_image}
                                text={offer.title}
                                alt={offer.title}
                                label={offer.price + offer.currency}
                                path={`/offer/${offer.id}`}
                                id='offer_section'
                                offer_id={offer.id}
                                followings={followings}
                                setFollowings={setFollowings}
                                setNewFetch={setNeedsNewFetch}/>
                    </Grid>
                    )
                )}
            </Grid>
        </div>
    );
}

export default Cards;

// xs, extra-small: 0px
// sm, small: 600px
// md, medium: 900px
// lg, large: 1200px
// xl, extra-large: 1536px