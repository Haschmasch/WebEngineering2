/* page for Followings */

import {useEffect, useState} from "react";
import {getFollowingsByUser} from "../../../fetchoperations/FollowingsOperations";
import Cards from "../../cards/Cards";

export default function Following() {
    const [followings, setFollowings] = useState([]);

    useEffect(() => {
        getFollowingsByUser().then((data) => {
            setFollowings(data.map(element => element.related_offer));
        }).catch((error) => console.error(error));
    }, []);

    return (
        <>
            <h1>Deine Favoriten</h1>
            <Cards offers={followings}/>
        </>
    )
}