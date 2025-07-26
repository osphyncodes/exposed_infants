
// const pdfParser = require("./pdfParser");

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("defaulter-search-form");
  const defmiss = document.getElementById('defmiss')
  const what = defmiss.dataset.what
  


  form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const startDate = document.getElementById("start_date").value;
      const endDate = document.getElementById("end_date").value;
      const today = new Date().toISOString().split("T")[0];
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const url = form.dataset.url;
      const loadingSpinner = document.getElementById("loading-spinner");
      const id = `osphyncodes_${startDate}${endDate}`

    //   if (endDate > today) {
    //       alert("End date cannot be greater than today.");
    //       return;
    //   }

      const submitButton = form.querySelector('button[type="submit"]');
      submitButton.disabled = true;
      loadingSpinner.style.display = "flex";

      available = localStorage.getItem(id)     

      if(!available){
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({
                    start_date: startDate,
                    end_date: endDate
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error("Error:", errorData.error || "Unknown error");
                alert(errorData.error || "An error occurred");
                return;
            }

            const data = await response.json();

            setEncryptedItem(id, data)
            renderResults(data)

        } catch (error) {
            console.error("Network error:", error);
            alert("Network error occurred");
        } finally {
            // Re-enable the submit button and hide spinner
            submitButton.disabled = false;
            loadingSpinner.style.display = "none";
        }
      }else {
        renderResults(getDecryptedItem(id))
        submitButton.disabled = false;
        loadingSpinner.style.display = "none";
      }
      
  });

  

  // CSRF token helper
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Render results to HTML table
  function renderResults(clients) {
    const tableDiv = document.getElementById("defaulters-tbody");
    const defTile = document.getElementById('report_defaulter')

    var datas = clients.appointments
    

    if (datas.length === 0) {
      tableDiv.innerHTML = "<h3 class='text-danger'>No clients found.</h3>";

        defTile.innerText = "Appointments Report"
      
      return;
    }

    tableDiv.innerHTML = ''
    var html = ''


    clients.appointments.forEach((client, index) => {
      html += `
        <tr>
          <td>${index + 1}</td>
          <td>${client.hcc_number}</td>
          <td>${client.child_name}</td>
          <td>${client.child_dob} (${client.age_in_months})</td>
          <td>${client.mother_art_number}</td>
          <td>${client.guardian_phone}</td>
          <td>${client.appointment_date}</td>
          <td>${client.action_needed}</td>
          <td>
            <a href="${client.view_url}" class="btn btn-sm btn-outline-primary">
              <i class="fas fa-eye me-1"></i>View
            </a>
          </td>
        </tr>
      `;
    });

    tableDiv.innerHTML = html;
    defTile.innerText = `Appointments Report (${clients.count})`
    
  }


  function downloadCSV(tableID) {
      const table = document.getElementById(tableID);
      const rows = table.querySelectorAll('tr');
      let csvContent = '';

      // Process headers
      const headerCells = rows[0].querySelectorAll('th, td');
      const headerRow = Array.from(headerCells)
          .map(cell => `"${cell.textContent.trim()}"`)
          .join(',');
      csvContent += headerRow + '\r\n';

      // Process data rows
      for (let i = 1; i < rows.length; i++) {
          const cells = rows[i].querySelectorAll('td');
          const row = Array.from(cells)
              .map(cell => `"${cell.textContent.trim()}"`)
              .join(',');
          csvContent += row + '\r\n';
      }

      // Create download link
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);

      if (what == 'Def'){
        link.setAttribute('download', 'defaulters_report.csv');
      }else {
        link.setAttribute('download', 'Missed_Appointment_report.csv');
      }
      
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
  }

  // import { html2pdf } from "./pdfParser";

  // Function to download PDF
  function downloadPDF(tableID) {
      const table = document.getElementById(tableID);
      
      // Use html2pdf library (make sure it's included in your project)
      const opt = {
          margin: 10,
          filename: 'defaulters_report.pdf',
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { scale: 2 },
          jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
      };

      // Create a clone of the table to avoid modifying the original
      const tableClone = table.cloneNode(true);
      document.body.appendChild(tableClone);
      
      // Generate PDF
      html2pdf()
          .from(tableClone)
          .set(opt)
          .save()
          .then(() => {
              document.body.removeChild(tableClone);
          });
  }

  // Add event listeners to your buttons
  document.getElementById('download-csv-btn').addEventListener('click', function() {
      downloadCSV('tables'); // Pass your table ID
  });
});




