
const location = "http://127.0.0.1:8000";

// GET-Operations
export async function getSubcategoryWithOffers(subcategory_id) {
    return fetch(location + `/subcategories/offers/${subcategory_id}`).then((response) => response.json());
}