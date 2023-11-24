/* fetch Operation for Users */

import Swal from "sweetalert2";
import {getAccessToken, getUser_id} from "../components/utils/StorageInterface";

const location = "http://127.0.0.1:8000/users/";

// GET-Operations
export async function getUser(user_id) {
  return fetch( location + `${user_id}`)
      .then((response) => response.json())
      .catch((error) => {
        console.log(error);
      });
}

export async function checkUsernameAvailability(name) {
  const response = await fetch(location + `name/${name}`);
  return !response.ok;
}

export async function getCurrentUser() {
  const requestOptions = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${getAccessToken()}`,
    },
  };

  return fetch(location + "current/user", requestOptions)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Fehler bei der Anfrage");
        }
        return response.json();
      })
      .then((data) => {
        return data;
      });
}

export async function getUserWithOffers() {
  return fetch(location + `offers/${getUser_id()}`)
      .then((response) => response.json())
      .catch((error) => {
        console.log(error);
      });
}

// POST-Operations
export async function registerUser(name, email, password, phone_number) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: name,
      email: email,
      password: password,
      phone_number: phone_number,
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

export async function userLogin(username, password) {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`,
  };

  return fetch(location + "login", requestOptions)
      .then((response) => {
        if (!response.ok) {
          return Swal.fire({
            title: `<b>Fehlgeschlagen</b> `,
            icon: "error",
            html: "Der Benutzername oder das Passwort sind inkorrekt.",
            showCloseButton: true,
            confirmButtonText: "Nochmal versuchen",
            confirmButtonColor: "#0989ff",
          });
        } else {
          return response.json();
        }
      })
      .catch((error) => {
        console.error(error);
      });
}

// PUT-Operations
export async function updateUser(name, email, phone_number, time_created ) {
  const requestOptions = {
    method: "PUT",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${getAccessToken()}`, },
    body: JSON.stringify({
      name: name,
      email: email,
      phone_number: phone_number,
      time_created : time_created,
      id: getUser_id()
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
export async function deleteUser() {
  const requestOptions = {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getAccessToken()}`,
    },
  };

  return fetch(location + `?user_id=${getUser_id()}`, requestOptions)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Fehler beim Löschen des Benutzers");
        }
        return true;
      })
      .then(() => {
        localStorage.clear();
      });
}
