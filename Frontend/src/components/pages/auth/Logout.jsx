import Swal from "sweetalert2";

export async function Logout() {
  return Swal.fire({
    title: "Bist du dir sicher?",
    text: "Wollen Sie sich ausloggen?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#0989ff",
    cancelButtonColor: "#d33",
    confirmButtonText: "Ja",
    cancelButtonText: "Nein",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        text: "Sie haben sich erfolgreich abgemeldet.",
        icon: "success",
        confirmButtonColor: "#0989ff",
      }).then(() => {
        localStorage.clear();
        window.location.reload();
      });
    }
  });
}
