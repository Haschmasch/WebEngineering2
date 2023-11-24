const location = "http://127.0.0.1:8000";

// GET-Operations
export async function getCategories() {
    return fetch(location + "/categories/").then((response) => response.json());
}

export async function getCategory(category_id) {
    return fetch(location + `/categories/${category_id}`).then((response) => response.json());
}

export async function getCategoryWithOffers(category_id) {
    return fetch(location + `/categories/offers/${category_id}`).then((response) => response.json());
}

