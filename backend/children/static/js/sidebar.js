document.addEventListener('DOMContentLoaded', ()=> {
    document.querySelector('#id_search_value').focus()

    async function loadChildren() {
        const tbody = document.querySelector("#id-children-table tbody");
        const url = tbody.dataset.url;
        const view_url = tbody.dataset.view;


        console.log(view_url);
        
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")  // Needed unless you're using @csrf_exempt
            },
            body: JSON.stringify({ query: "get_children" })
        });

        if (!response.ok) {
            console.error("HTTP error", response.status);
            return;
        }

        tbody.innerHTML = ''

        const data = await response.json();

        data.forEach(child => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${child.hcc_number}</td>
                <td>${child.child_name}</td>
                <td>${child.child_gender}</td>
                <td>${child.mother_art_number}</td>
                <td>${child.child_gender}</td>
                <td>${child.guardian_name}</td>
                <td>${child.relationship}</td>
                <td>
                    <a href="${view_url}" class="btn btn-sm btn-primary">View</a>
                </td>
            ` 
            tbody.appendChild(tr)
        });

        
    }


    makeTableInteractive('id-children-table','table_title')
    // loadChildren();
})
console.log(3232);

