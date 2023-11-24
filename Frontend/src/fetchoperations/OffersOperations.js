import {getAccessToken, getUser_id} from "../components/utils/StorageInterface";

const location = "http://127.0.0.1:8000/offers/";

// GET-Operations
export async function getOffers() {
    return fetch(location).then((response) => response.json());
}

export async function getOffer(offer_id) {
    return fetch(location + `${offer_id}`).then((response) => response.json());
}

export async function getOfferImages(offer_id) {
    return fetch(location + `${offer_id}/images`).then((response) => response.json());
}

export async function getOfferImagesName(offer_id) {
    return fetch(location + `${offer_id}/images/names`).then((response) => response.json());
}

export async function getOfferImageName(offer_id, image_name) {
    return fetch(location + `${offer_id}/images/${image_name}`).then((response) => response.json());
}

export async function getOfferThumbnail(offer_id) {
    return fetch(location + `${offer_id}/thumbnail}`).then((response) => response.json());
}

// POST-Operations
export async function addOffer(title,
                               category_id,
                               subcategory_id,
                               price,
                               currency,
                               postcode,
                               city,
                               address,
                               description,
                               primary_image,
                               short_description,
) {
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify({
            "title": title,
            "category_id": category_id,
            "subcategory_id": subcategory_id,
            "price": price,
            "currency": currency,
            "postcode": postcode,
            "city": city,
            "address": address,
            "description": description,
            "primary_image": primary_image,
            "short_description": short_description,
            "user_id": getUser_id(),
            "time_posted": new Date(Date.now()).toISOString()
        }),
    };
    return fetch(location, requestOptions)
}

export async function createOfferImages(offer_id, images) {
    const formData = new FormData();
    images.forEach(image => formData.append('files', image))
    console.log(formData)
    const requestOptions = {
        method: "POST",
        headers: {
/*            "boundary": Math.random().toString().substr(2),
            "Content-Type": "multipart/form-data",*/
            Authorization: `Bearer ${getAccessToken()}`
        },
        body: formData,
    };
    return fetch(location + `${offer_id}/images`, requestOptions)
        .then((response) => {
            if (!response.ok) {
                return response.detail;
            } else {
                return  response.json();
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

//PUT-Operation
export async function updateOffer(title, category_id, subcategory_id, price, currency, postcode, city,
                                  address, description, primary_image, short_description, id, closed) {
    const requestOptions = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify({
            "title": title,
            "category_id": category_id,
            "subcategory_id": subcategory_id,
            "price": price,
            "currency": currency,
            "postcode": postcode,
            "city": city,
            "address": address,
            "description": description,
            "primary_image": primary_image,
            "short_description": short_description,
            "user_id": getUser_id(),
            "time_posted": new Date(Date.now()).toISOString(),
            "id": id,
            "closed": closed
        }),
    };
    return fetch(location, requestOptions)
        .then((response) => response.json())
        .then((response) => {
            if (!response.ok) {
                return response.detail;
            } else {
                return response;
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

// DELETE-Operations
export async function deleteOffer(offer_id) {
    const requestOptions = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`,
        },
    };

    return fetch(location + `?offer_id=${offer_id}`, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Fehler beim Löschen des Angebots");
            }
            return true;
        })
        .then((error) => {
            console.log(error);
        });
}

export async function deleteOfferImage(offer_id, image_name) {
    const requestOptions = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`,
        },
    };

    return fetch(location + `${offer_id}/images/${image_name}`, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Fehler beim Löschen des Angebotsbild");
            }
            return true;
        })
        .then((error) => {
            console.log(error);
        });
}