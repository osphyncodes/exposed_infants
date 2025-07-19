document.addEventListener('DOMContentLoaded', ()=> {
    document.querySelector('#id_search_value').focus()

    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').content;
    }

    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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


    // loadChildren();
})


