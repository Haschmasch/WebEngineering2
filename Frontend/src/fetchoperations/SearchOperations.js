const location = 'http://127.0.0.1:8000/search/'

export async function getOffersBySubstring(substring) {
    return fetch(`${location}?query=${substring}`).then((response) => response.json());
}

export async function getOffersByOptionalParameters(query = '', category_id = '', subcategory_id = '', location = '', postcode = '', min_price = '', max_price = '', min_date = '', max_date = '') {
    return fetch(`${location}?query=${query}&category_id=${category_id}&subcategory_id=${subcategory_id}&location=${location}&postcode=${postcode}&min_price=${min_price}&max_price=${max_price}&min_date=${min_date}&max_date=${max_date}`).then((response) => response.json());
}