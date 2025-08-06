document.addEventListener("DOMContentLoaded", async () => {
    const table_id = 'id-vl-register-table'

    tbody = document.getElementById('vl_reg_tbody')
    url = tbody.dataset.url

    
    const dataDiv = document.getElementById("user-data");

    try {
        const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"), // only needed if CSRF is enabled
        },
        body: JSON.stringify({ info: "requesting user data" }), // adjust payload as needed
        });

        const data = await response.json();
        tr = ''
        data.results.forEach(r => {
           tr += `
                <tr>
                    <td>${r.arv_number ?? ""}</td>
                    <td>${r.accession_number ?? ""}</td>
                    <td>${r.status ?? ""}</td>
                    <td>${r.order_date ?? ""}</td>
                    <td>${r.result ?? ""}</td>
                    <td>${r.date_received ?? ""}</td>
                    <td>${r.mode_of_delivery ?? ""}</td>
                    <td>${r.test_reason ?? ""}</td>
                    <td>${r.tat_days ?? ""}</td>
                </tr>
            `


        });

        tbody.innerHTML = tr

        makeTableInteractive(table_id, 'table_title')
    } catch (error) {
        console.log("Failed to load data.");
        console.error("Error fetching user data:", error);
    }
})