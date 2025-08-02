document.addEventListener('DOMContentLoaded', ()=> {
    const search = document.getElementById('search')
    const buttons = document.querySelectorAll('.button')


    buttons.forEach((button)=> {
        button.addEventListener('click', (event)=> {
            text = event.target.innerText
            searchText = search.value
            url = search.dataset.url
            value = ''
            
            if(text != 'Del' && text != "Enter" ) {
                value = searchText + text
                search.value = parseInt(value)
            }else if ( text == 'Del') {
                search.value = parseInt(left(searchText, searchText.length - 1))
                console.log(left(searchText, searchText.length - 1));
                
            }else {
                if (!searchText) {
                    alert('Please enter art number')
                    return
                }

                fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()  // For Django
                },
                body: JSON.stringify({
                    arv_number: searchText
                })
                })
                .then(response => response.json())
                .then(data => {
                console.log('Success:', data);

                    const tbody = document.querySelector("#resultsTable tbody");
                    
                    const visitsbody = document.getElementById('visitsbody')
                    const p = document.getElementById('patient_details')
                    tbody.innerHTML = ''
                    visitsbody.innerHTML = ''
                     p.innerText = data.p

                     if(data.p == "Record Not Found"){
                        p.style.color = 'blue';
                        setTimeout(() => {
                            p.innerText = "Search Client";
                            p.style.color = 'black';
                        }, 3000);
                     }

                    if (data.patients){
                        const length = data.patients.order_date.length;
                        for (let i = 0; i < length; i++) {
                            const row = document.createElement("tr");

                            const orderDate = document.createElement("td");
                            orderDate.textContent = data.patients.order_date[i];
                            row.appendChild(orderDate);

                            const result = document.createElement("td");
                            result.textContent = data.patients.result[i];
                            row.appendChild(result);

                            const dateReceived = document.createElement("td");
                            dateReceived.textContent = data.patients.date_received[i];
                            row.appendChild(dateReceived);

                            tbody.appendChild(row);
                        }

                        if (data.visits){
                            array = data.visits
                            dd = ''

                            array.forEach((v)=>{
                                dd += `
                                    <tr>
                                        <td>${v.visit_date}</td>
                                        <td>${v.vl_draw}</td>
                                        <td>${v.regimen}</td>
                                        <td>${v.arv_given}</td>
                                        <td>${v.next_appointment}</td>
                                    </tr>
                                `
                            })
                            
                            visitsbody.innerHTML = dd
                        }
                    }

                    
                        

                    search.value = null
                    
                })
                .catch(error => {
                console.error('Error:', error);
                });
            }
        })
    })

    function left(str, n) {
        if (!str) return '';
        return str.substring(0, n);
    }

    function right(str, n) {
        if (!str) return '';
        return str.substring(str.length - n);
    }

    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            if (cookie.trim().startsWith(name + '=')) {
            return cookie.trim().substring(name.length + 1);
            }
        }
        return '';
    }

})