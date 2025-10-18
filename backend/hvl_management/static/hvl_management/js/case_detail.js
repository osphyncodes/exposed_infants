document.addEventListener("DOMContentLoaded", function() {
    const numericRadio = document.getElementById("numericRadio");
    const alnumRadio = document.getElementById("alnumRadio");
    const numericField = document.getElementById("numericField");
    const alphanumericField = document.getElementById("alphanumericField");

    function toggleFields() {
        if (numericRadio.checked) {
            numericField.classList.remove("d-none");
            alphanumericField.classList.add("d-none");
        } else {
            numericField.classList.add("d-none");
            alphanumericField.classList.remove("d-none");
        }
    }

    // Attach listeners
    numericRadio.addEventListener("change", toggleFields);
    alnumRadio.addEventListener("change", toggleFields);

    // Run on load
    toggleFields();
});