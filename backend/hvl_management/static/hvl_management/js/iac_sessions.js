document.addEventListener("DOMContentLoaded", (e) => {
  const search_ctn = document.getElementById("id_search_by");
  const search_input = document.getElementById("id_search_value");

  const init_value = JSON.parse(localStorage.getItem("search_by_value"));

  if (init_value) {
    search_ctn.value = init_value;
  }

  search_ctn.addEventListener("change", (e) => {
    localStorage.setItem("search_by_value", JSON.stringify(e.target.value));
  });

  search_input.focus();
});
