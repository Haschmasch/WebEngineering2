const location = 'http://127.0.0.1:8000/search/'

export async function getOffersBySubstring(substring) {
    return fetch(`${location}?query=${substring}`).then((response) => response.json());
}