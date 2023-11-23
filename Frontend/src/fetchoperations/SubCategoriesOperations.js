import {getAccessToken} from "../components/utils/StorageInterface";

const location = "http://127.0.0.1:8000";

// GET-Operations
export async function getSubcategories() {
    return fetch(location + `/subcategories/`).then((response) => response.json());
}

export async function getSubcategory(subcategory_id) {
    return fetch(location + `/subcategories/${subcategory_id}`).then((response) => response.json());
}

export async function getSubcategoryByName(subcategory_name) {
    return fetch(location + `/subcategories/name/${subcategory_name}`).then((response) => response.json());
}

export async function getSubcategoryWithOffers(subcategory_id) {
    return fetch(location + `/subcategories/offers/${subcategory_id}`).then((response) => response.json());
}

export async function getSubcategoryWithCategory(subcategory_id) {
    return fetch(location + `/subcategories/category/${subcategory_id}`).then((response) => response.json());
}

// POST-Operations
export async function addSubcategory(category_id, name) {
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify({
            "category_id": category_id,
            "name": name,
        }),
    };
    return fetch(location + "/subcategories/", requestOptions)
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

//PUT-Operation
export async function updateSubcategory(category_id, name, id) {
    const requestOptions = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`
        },
        body: JSON.stringify({
            "category_id": category_id,
            "name": name,
            "id": id,
        }),
    };
    return fetch(location + "/subcategories/", requestOptions)
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
export async function deleteSubcategory(subcategory_id) {
    const requestOptions = {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${getAccessToken()}`,
        },
    };

    return fetch(location + `?subcategory_id=${subcategory_id}`, requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Fehler beim Löschen der Unterkategorie");
            }
            return true;
        })
        .then((error) => {
            console.log(error);
        });
}