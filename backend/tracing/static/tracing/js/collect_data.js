const table =
  new ExcelLikeTable(
    "excelTable",
    {
      defaultRowCount:
        JSON.parse(localStorage.getItem("hvlTableArrayCount")) || 1,
      allowEmptyRows: true,
    },
    JSON.parse(localStorage.getItem("hvlTableData"))
  ) || [];

async function getCHWs() {
  const response = await fetch("/tracing/api/get-chws/");
  if (response.ok) {
    const data = await response.json();
    const chws = data.chws;
    const chwSelect = document.getElementById("chwSelect");
    const chwData = [];
    chws.forEach((chw) => {
      chwData.push({ value: chw.id, label: `${chw.name} (${chw.chw_code})` });
    });

    return chwData;
  }
}

async function populateCHWField() {
  const chwOptions = await getCHWs();
  console.log("CHW Options:", chwOptions);
  // Add fields
  table.addField("Unique ID", "number", {
    placeholder: "Enter SN",
    required: true,
  });
  table.addField("Date Entered", "date");
  table.addField("CHW", "select", {
    options: chwOptions,
  });
  table.addField("ART Number", "number", {
    placeholder: "Enter ART Number",
    required: true,
  });

  table.addField("Name", "text", { placeholder: "Enter Name" });

  table.addField("Age", "number", { placeholder: "Enter Age" });

  table.addField("Gender", "select", {
    options: [
      { value: "Male", label: "Male" },
      { value: "FNP", label: "FNP" },
      { value: "FBF", label: "FBF" },
      { value: "FP", label: "FP" },
    ],
  });

  table.addField("Phone Number", "text", { placeholder: "Enter Phone Number" });

  table.addField("Type", "select", {
    options: [
      { value: "ART", label: "ART" },
      { value: "HCC", label: "HCC" },
      { value: "ICT", label: "ICT" },
    ],
  });

  table.addField("Reason", "select", {
    options: [
      { value: "Missed Appointment", label: "Missed Appointment" },
      { value: "Treatment Interrupter", label: "Treatment Interrupter" },
      { value: "Linkage", label: "Linkage" },
      { value: "EID Positive Result", label: "EID Positive Result" },
      { value: "EID Missed Milestone", label: "EID Missed Milestone" },
      { value: "High Viral Load", label: "High Viral Load" },
      { value: "Missed VL Milestone", label: "Missed VL Milestone" },
      { value: "ICT", label: "ICT" },
      { value: "Other", label: "Other" },
    ],
  });

  table.addField("With Phone", "select", {
    options: [
      { value: "No", label: "No" },
      { value: "Yes", label: "Yes" },
    ],
  });
}

populateCHWField();

// Connect buttons
table.connectAddRowButton("addRowBtn");
table.connectJSONButton("saveBtn", (data) => {
  localStorage.setItem("hvlTableData", JSON.stringify(data));
  localStorage.setItem("hvlTableArrayCount", data.length);
  showAlert("success", "Data successfully saved to local storage.");
});

table.connectJSONButton("submitBtn", async (data) => {
  localStorage.setItem("hvlTableData", JSON.stringify(data));
  localStorage.setItem("hvlTableArrayCount", data.length);

  for (const datas of data) {
    // check if all fields have values
    for (const key in datas) {
      if (!datas[key]) {
        showAlert("error", `Please fill in all fields (missing: ${key}).`);
        return;
      }
    }

    // check if date is valid and not in the future
    const enteredDate = new Date(datas["Date Entered"]);
    const currentDate = new Date();
    if (isNaN(enteredDate.getTime()) || enteredDate > currentDate) {
      showAlert(
        "error",
        "Please enter a valid date that is not in the future."
      );
      return;
    }
  }

  url = document.getElementById("submitBtn").dataset.url;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(data),
  });

  if (response.ok) {
    data = await response.json();
    showAlert(data.status, data.message || "Data successfully submitted.");
  } else {
    showAlert("error", `Failed to submit data. ${response.statusText}`);
  }
});

document.getElementById("clearBtn").addEventListener("click", () => {
  table.clear();
});

// Test the navigation
console.log(
  "Excel-like table initialized. Use Tab to move right, Enter to move down."
);
