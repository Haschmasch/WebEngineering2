import {useEffect, useState} from "react";
import {getFollowingsByUser} from "../../../fetchoperations/FollowingsOperations";
import Cards from "../../cards/Cards";

export default function FollowingListing() {
    const [followings, setFollowings] = useState([]);
    useEffect(() => {
        const response = getFollowingsByUser();
        if (response) {
            response.then((data) => {
                let array =[]
                data.forEach(element => {
                    array.push(element.related_offer)
                });
                setFollowings(array);
            }).catch((error) => console.error(error));
        }
    }, []);

    return (
        <>
            <h1>Deine Favoriten</h1>
            <Cards offers={followings}/>
        </>
    )
}