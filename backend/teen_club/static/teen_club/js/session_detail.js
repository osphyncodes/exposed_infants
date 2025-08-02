document.addEventListener('DOMContentLoaded', function() {
    // Initialize Select2 for patient search

    // $('.select2').select2({
    //     width: '100%',
    //     placeholder: "Search patient...",
    //     allowClear: true,
    //     minimumInputLength: 2,
    //     ajax: {
    //         url: '/api/patients/search/',
    //         dataType: 'json',
    //         delay: 250,
    //         data: function(params) {
    //             return {
    //                 q: params.term,
    //                 page: params.page
    //             };
    //         },
    //         processResults: function(data, params) {
    //             params.page = params.page || 1;
    //             return {
    //                 results: data.results,
    //                 pagination: {
    //                     more: (params.page * 30) < data.total_count
    //                 }
    //             };
    //         },
    //         cache: true
    //     },
    //     templateResult: formatPatient,
    //     templateSelection: formatPatientSelection
    // });

    // Format patient results
    function formatPatient(patient) {
        if (patient.loading) return patient.text;
        return $(
            `<div class="patient-result">
                <strong>${patient.arv_number}</strong> - ${patient.name}<br>
                <small>Age: ${patient.age}, Gender: ${patient.gender}</small>
            </div>`
        );
    }

    // Format selected patient
    function formatPatientSelection(patient) {
        if (!patient.id) return patient.text;
        return `${patient.arv_number} - ${patient.name}`;
    }

    // Initialize charts
    if (document.getElementById('purposeChart')) {
        const purposeOptions = {
            series: JSON.parse(document.getElementById('purposeChart').dataset.series),
            chart: {
                type: 'donut',
                height: 300
            },
            labels: ['Clinic', 'Support'],
            colors: ['#3b82f6', '#10b981'],
            responsive: [{
                breakpoint: 480,
                options: {
                    chart: {
                        width: 200
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }]
        };
        new ApexCharts(document.querySelector("#purposeChart"), purposeOptions).render();
    }

    if (document.getElementById('schoolChart')) {
        const schoolOptions = {
            series: [{
                name: 'Students',
                data: JSON.parse(document.getElementById('schoolChart').dataset.series)
            }],
            chart: {
                type: 'bar',
                height: 300
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true,
                }
            },
            dataLabels: {
                enabled: true
            },
            colors: ['#6366f1'],
            xaxis: {
                categories: ['Not in School', 'Day School', 'Boarding School'],
            }
        };
        new ApexCharts(document.querySelector("#schoolChart"), schoolOptions).render();
    }

    if (document.getElementById('ageSexChart')) {
        const ageSexOptions = {
            series: [
                {
                    name: 'Male',
                    data: JSON.parse(document.getElementById('ageSexChart').dataset.male)
                },
                {
                    name: 'Female',
                    data: JSON.parse(document.getElementById('ageSexChart').dataset.female)
                }
            ],
            chart: {
                type: 'bar',
                height: 300
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: false,
                }
            },
            dataLabels: {
                enabled: true,
                position: 'end'
            },
            colors: ['#6366f1', '#0b8200ff'],
            xaxis: {
                categories: ['10-14yrs', '15-18yrs', '19-24yrs'],
            }
        };
        new ApexCharts(document.querySelector("#ageSexChart"), ageSexOptions).render();
    }

    const alertBox = document.querySelector('.alert')

    if(alertBox){
        setTimeout(()=>{
            alertBox.style.display = 'none'
        }, 4000)
    }

    const art_number = document.getElementById('art_number')
    const name_name = document.getElementById('name_name')
    url = art_number.dataset.url
    console.log(url)
    art_number.addEventListener('input', ()=>{
        fetch(url, {
            method: 'POST',
            body: JSON.stringify({
                'art_number': art_number.value
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if(data.name){
                console.log(data.name)
                console.log(name_name)
                name_name.value = data.name
            }  
        })
    })

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                // Check if this cookie string begins with the name we want
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    // Handle attendance form submission
    // const attendanceForm = document.getElementById('attendanceForm');
    // if (attendanceForm) {
    //     attendanceForm.addEventListener('submit', function(e) {
    //         e.preventDefault();
            
    //         fetch(this.action, {
    //             method: 'POST',
    //             body: new FormData(this),
    //             headers: {
    //                 'X-Requested-With': 'XMLHttpRequest'
    //             }
    //         })
    //         .then(response => response.json())
    //         .then(data => {
    //             if (data.success) {
    //                 window.location.reload();
    //             } else {
    //                 alert('Error: ' + (data.errors || 'Failed to save attendance'));
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error:', error);
    //             alert('An error occurred while saving attendance.');
    //         });
    //     });
    // }

    // Show patient details when selected
    const patientSelect = document.getElementById('patient');
    if (patientSelect) {
        patientSelect.addEventListener('change', function() {
            const patientId = this.value;
            if (patientId) {
                fetch(`/api/patients/${patientId}/`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('patient-name').textContent = data.name;
                        document.getElementById('patient-arv').textContent = data.arv_number;
                        document.getElementById('patient-age').textContent = data.age;
                        document.getElementById('patient-gender').textContent = data.gender;
                        
                        // Show modal with patient details
                        new bootstrap.Modal(document.getElementById('patientDetailsModal')).show();
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
        });
    }
});