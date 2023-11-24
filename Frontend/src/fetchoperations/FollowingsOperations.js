/* Fetch Operations for Followings */

import {getAccessToken, getUser_id} from "../components/utils/StorageInterface";

const location = "http://127.0.0.1:8000";

// GET-Operations
export async function getFollowingsByUser() {
    return fetch(location + `/followings/user/${getUser_id()}`)
        .then((response) => response.json())
        .catch((error) => {
            console.log(error);
        });
}

// POST-Operations
export async function addFollowing(offer_id) {
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify({
            "offer_id": offer_id,
            "user_id": getUser_id(),
            "time_followed": new Date(Date.now()).toISOString(),
        }),
    };

    return fetch(location + "/followings/", requestOptions)
        .then((response) => {
            if (!response.ok) {
                return response.detail;
            } else {
                return response.json();
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

// DELETE-Operations
export async function deleteFollowing(following_id) {
    const requestOptions = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`,
        },
    };

    return fetch(location + "/followings/?following_id=" + following_id, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Fehler beim Löschen des Favoriten");
            }
            return true;
        });
}
