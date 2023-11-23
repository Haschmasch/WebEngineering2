import {getAccessToken, getUser_id} from "../components/utils/StorageInterface";
import {getOffers} from "./OffersOperations";
const location = "http://127.0.0.1:8000/chats/";

// GET-Operations
export async function getChats() {
    return fetch(location).then((response) => response.json());
}

export async function getChat(chat_id) {
    return fetch(location + `${chat_id}`).then((response) => response.json());
}

export async function getChatByOffer(offer_id) {
    return fetch(location + `offer/${offer_id}`).then((response) => response.json());
}

export async function getOwnChatByOffer(offer_id) {
    return fetch(location + `offer/${offer_id}`).then((response) => response.json()).then(chats => chats.filter(chat => chat.creator_id === getUser_id())[0]);
}

export async function getChatsByUser() {
    return fetch(location + `user/${getUser_id()}`).then((response) => response.ok ? response.json() : []);
}

// POST-Operations
export async function addChat(offer_id) {

    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify({
            "offer_id": offer_id,
            "creator_id": getUser_id(),
            "time_followed": new Date(Date.now()).toISOString(),
        }),
    };

    return fetch(location, requestOptions)
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

export async function deleteChat(chat) {
    const requestOptions = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`,
        },
    };

    return fetch(location + `?chat_id=${chat.id}`, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Fehler beim Löschen des Chats");
            }
            return true;
        })
}

export async function getAllChatsInvolvingUser() {
    const chatByOffer = (await getOffers().then(offers => offers.filter(offer => offer.user_id === getUser_id())));
    const promise = await Promise.all(chatByOffer.map(offer => getChatByOffer(offer.id)));
    console.log(chatByOffer);
    console.log(promise);
    return promise.concat(await getChatsByUser());
}