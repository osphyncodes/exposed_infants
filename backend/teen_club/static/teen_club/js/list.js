document.addEventListener("DOMContentLoaded", (e) => {
  const sign = document.querySelectorAll(".signup");
  const register = document.querySelectorAll(".register");

  register.forEach((el) => {
    el.addEventListener("click", (e) => {
      fetch(`/teen_club/api/update/register/${e.target.dataset.pk}`, {
        method: "GET",
      })
        .then((response) => response.json())
        .then((data) => {
          if (e.target.innerText == "No") {
            e.target.innerText = "Yes";
          } else {
            e.target.innerText = "No";
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });

  sign.forEach((el) => {
    el.addEventListener("click", (e) => {
      fetch(`/teen_club/api/update/sign/${e.target.dataset.pk}`, {
        method: "GET",
      })
        .then((response) => response.json())
        .then((data) => {
          if (e.target.innerText == "No") {
            e.target.innerText = "Yes";
          } else {
            e.target.innerText = "No";
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });
});
