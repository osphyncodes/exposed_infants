document.addEventListener('DOMContentLoaded', function() {
    alert(1)
    const csrftoken = getCookie('csrftoken');
    function showLoading() { document.getElementById('loadingSpinner').style.display = 'block'; }
    function hideLoading() { document.getElementById('loadingSpinner').style.display = 'none'; }
    function updateTimestamp() { document.getElementById('lastUpdated').textContent = 'Last updated: ' + new Date().toLocaleString(); }

    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
    // Toggle button AJAX
    document.querySelectorAll('.toggle-btn input').forEach(toggle => {
        toggle.addEventListener('change', function() {
            const field = this.dataset.field;
            const tracingId = this.dataset.tracingId;
            const value = this.checked;
            showLoading();
            fetch('{% url "tracing:update_tracing_field" %}', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                body: JSON.stringify({ tracing_id: tracingId, field: field, value: value })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) { showAlert(type='error', message=data.error); this.checked = !value; }
                showAlert(type='success', message='Field updated successfully');
                updateTimestamp();
            })
            .catch(() => { showAlert(type='error', message='Error updating field'); this.checked = !value; })
            .finally(hideLoading);
        });
    });

    document.querySelectorAll('.editable-select').forEach(cell => {
        cell.addEventListener('click', function () {
            if (cell.classList.contains('editing')) return;
            const field = cell.dataset.field;
            const tracingId = cell.closest('tr').dataset.tracingId;
            const oldValue = cell.textContent.trim();

            // Create select element
            const select = document.createElement('select');
            select.className = 'form-select form-select-sm';

            // Options: empty, Yes, No
            const options = ["", "Came Back", "Attended Appointment", "Transferred Out", "Moved", "Declined/Refused", "Died", "Not Found", "Outside Tracing Area", "Did Not Return"];
            options.forEach(opt => {
                const option = document.createElement('option');
                option.value = opt;
                option.textContent = opt === "" ? "—" : opt; // show dash for empty
                if (opt.toLowerCase() === oldValue.toLowerCase()) {
                    option.selected = true;
                }
                select.appendChild(option);
            });

            cell.textContent = '';
            cell.appendChild(select);
            cell.classList.add('editing');
            select.focus();

            function save() {
                const newValue = select.value;
                fetch('{% url "tracing:update_tracing_field" %}', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        tracing_id: tracingId,
                        field: field,
                        value: newValue
                    })
                })
                    .then(res => res.json())
                    .then(data => {
                        if (!data.success) {
                            showAlert('error', data.error);
                        } else {
                            showAlert('success', 'Field updated successfully');
                            updateTimestamp();
                        }
                    })
                    .catch(() => showAlert('error', 'Error updating field'))
                    .finally(() => {
                        cell.textContent = newValue || ""; // fallback empty if no value
                        cell.classList.remove('editing');
                        hideLoading();
                    });
            }

            select.addEventListener('change', save);
            select.addEventListener('blur', save);
        });
    });

    document.querySelectorAll('.editable-cell').forEach(cell => {
        cell.addEventListener('click', function() {
            if (cell.classList.contains('editing')) return;
            const field = cell.dataset.field;
            const tracingId = cell.closest('tr').dataset.tracingId;
            const oldValue = cell.textContent;
            const input = document.createElement('input');
            input.type = 'text';
            input.value = oldValue;
            input.className = 'form-control form-control-sm';
            cell.textContent = '';
            cell.appendChild(input);
            cell.classList.add('editing');
            input.focus();
            function save() {
                const newValue = input.value;
                fetch('{% url "tracing:update_tracing_field" %}', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                    body: JSON.stringify({ tracing_id: tracingId, field: field, value: newValue })
                })
                .then(res => res.json())
                .then(data => { 
                    if (!data.success) showAlert(type='error', message=data.error); 
                    showAlert(type='success', message='Field updated successfully'); 
                    updateTimestamp(); 
                })
                .catch(() => showAlert(type='error', message='Error updating field'))
                .finally(() => { cell.textContent = newValue; cell.classList.remove('editing'); updateTimestamp(); hideLoading(); });
            }
            input.addEventListener('keypress', e => { if (e.key === 'Enter') save(); });
            input.addEventListener('blur', save);
        });
    });

    document.querySelectorAll('.editable-date').forEach(cell => {
        cell.addEventListener('click', function() {
            if (cell.classList.contains('editing')) return;
            const field = cell.dataset.field;
            const tracingId = cell.closest('tr').dataset.tracingId;
            const oldValue = cell.textContent;
            const input = document.createElement('input');
            input.type = 'date';
            input.value = oldValue;
            input.className = 'form-control form-control-sm';
            cell.textContent = '';
            cell.appendChild(input);
            cell.classList.add('editing');
            input.focus();
            function save() {
                const newValue = input.value;
                fetch('{% url "tracing:update_tracing_field" %}', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                    body: JSON.stringify({ tracing_id: tracingId, field: field, value: newValue })
                })
                .then(res => res.json())
                .then(data => { 
                    if (!data.success) {
                        showAlert(type='error', message=data.error)   
                    } else {
                    showAlert(type='success', message='Field updated successfully'); 
                    updateTimestamp(); 
                    }
                })
                .catch(() => showAlert(type='error', message='Error updating field'))
                .finally(() => { cell.textContent = newValue; cell.classList.remove('editing'); updateTimestamp(); hideLoading(); });
            }
            input.addEventListener('keypress', e => { if (e.key === 'Enter') save(); });
            input.addEventListener('blur', save);
        });
    });

    showHideBtn = document.getElementById('toggleFilters');

    document.getElementById('toggleFilters').addEventListener('click', ()=> {

        if (showHideBtn.innerText === 'Hide Filters') {
            document.getElementById('filter_id').style.display = 'none'
            showHideBtn.innerText = 'Show Filters'
        }else {
            document.getElementById('filter_id').style.display = 'block'
            showHideBtn.innerText = 'Hide Filters'
        }
    })

    // Phone modal
    const phoneModalEl = document.getElementById('phoneTracingModal');
    phoneModalEl.addEventListener('show.bs.modal', e => {
        const button = e.relatedTarget;
        document.getElementById('pt_tracing_id').value = button.dataset.tracingId;
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        document.getElementById('pt_date_called').value = now.toISOString().slice(0,16);
    });

    document.getElementById('savePhoneTracing').addEventListener('click', () => {
        const form = document.getElementById('phoneTracingForm');
        const formData = new FormData(form);
        const uniqueId = formData.get('tracing_id');
        showLoading();
        fetch('{% url "tracing:add_phone_tracing" %}', { method: 'POST', headers: { 'X-CSRFToken': csrftoken }, body: formData })
        .then(res => res.json())
        .then(data => {
            if (data.success) { 
                updateTimestamp(); 
                bootstrap.Modal.getInstance(phoneModalEl).hide(); 
                document.getElementById('phone_called_' + uniqueId).checked = true; 
                document.getElementById('tracing_attempted_' + uniqueId).checked = true;
                showAlert(type='success', message='Phone tracing recorded successfully');

                if (data.talking_to_client) {
                    document.getElementById('tracing_successful_' + uniqueId).checked = true;
                }
            }
            else showAlert(type='error', message=data.error);
        })
        .catch(() => showAlert(type='error', message='Error recording phone tracing'))
        .finally(() => {
            hideLoading();
        });
    });

    // Home modal
    const homeModalEl = document.getElementById('homeTracingModal');
    homeModalEl.addEventListener('show.bs.modal', e => {
        const button = e.relatedTarget;
        document.getElementById('ht_tracing_id').value = button.dataset.tracingId;
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        document.getElementById('ht_date_visited').value = now.toISOString().slice(0,16);
    });

    document.getElementById('saveHomeTracing').addEventListener('click', () => {
        const form = document.getElementById('homeTracingForm');
        const formData = new FormData(form);
        const uniqueId = formData.get('tracing_id');
        showLoading();
        fetch('{% url "tracing:add_home_tracing" %}', { method: 'POST', headers: { 'X-CSRFToken': csrftoken }, body: formData })
        .then(res => res.json())
        .then(data => {
            if (data.success) { 
                updateTimestamp(); 
                bootstrap.Modal.getInstance(homeModalEl).hide(); 
                document.getElementById('home_traced_' + uniqueId).checked = true; 
                document.getElementById('tracing_attempted_' + uniqueId).checked = true;
                showAlert(type='success', message='Home tracing recorded successfully');
                if (data.talking_to_client) {
                    document.getElementById('tracing_successful_' + uniqueId).checked = true;
                }
            }
            else showAlert(type='error', message=data.error);
        })
        .catch(() => showAlert(type='warning', message='Error recording home tracing'))
        .finally(
            hideLoading,
            document.getElementById('home_traced_{{ tracing.unique_id }}').checked = true
        );
    });

    // CSRF helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(cookie => {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            });
        }
        return cookieValue;
    }
});