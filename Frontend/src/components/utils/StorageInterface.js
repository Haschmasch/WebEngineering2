import {getCurrentUser} from "../../fetchoperations/UsersOperation";

export async function storeCredentials(response) {

    if (response && Object.keys(response).includes("access_token")) {
        localStorage.setItem("access_token", response["access_token"]);
        localStorage.setItem("token_type", "bearer");

        const currentUserResponse = await getCurrentUser(response["access_token"]);

        if (currentUserResponse) {
            localStorage.setItem("user", currentUserResponse["name"]);
            localStorage.setItem("user_id", currentUserResponse["id"])
            localStorage.setItem("isLogin", "true");
            return Promise.resolve();
        }
    }
    return Promise.reject();
}

export function getAccessToken() {
    return localStorage.getItem("access_token")
}

export function getUser_id() {
    return parseInt(localStorage.getItem("user_id"))
}

export function isLoggedIn() {
    return localStorage.getItem("isLogin") === 'true' ;

}