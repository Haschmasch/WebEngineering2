/* after entering something into the searchbar, one gets results with all matching offer titles,
* usage of MUI library  */
import {useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {getOffersBySubstring} from "../../../fetchoperations/SearchOperations";
import CardItem from "../../cards/CardItem";
import {getFollowingsByUser} from "../../../fetchoperations/FollowingsOperations";
import '../../cards/Cards.css'
import Typography from "@mui/material/Typography";

export default function SearchPageListing() {

    const {search_String} = useParams()
    const [offers, setoffers] = useState([]);
    const [followings, setFollowings] = useState([]);
    const [needsNewFetch, setNeedsNewFetch] = useState(0);

    useEffect(() => {
        getOffersBySubstring(search_String).then(r => setoffers(r));
    }, [search_String]);

    useEffect(() => {
        getFollowingsByUser().then(r => setFollowings(r))
    }, [needsNewFetch]);

    return (
        <>
            <Typography>Ergebnisse für: "{search_String}"</Typography>
            <div className='cards'>
                <div className='cards__container'>
                    <div className='cards__wrapper'>
                        <ul className='cards__items'>
                            {offers.map((offer) => (
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
                                )
                            )}
                        </ul>
                    </div>
                </div>
            </div>
        </>
    )
}