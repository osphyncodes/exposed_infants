document.addEventListener('DOMContentLoaded', function() {
    const importBtn = document.getElementById('importBtn');
    const csvFileInput = document.getElementById('csvFile');
    const resultsDiv = document.getElementById('results');
    const errorListDiv = document.getElementById('errorList');
    const url = importBtn.dataset.url
    console.log(url)    

    importBtn.addEventListener('click', function() {
        const file = csvFileInput.files[0];
        if (!file) {
            alert('Please select a CSV file first');
            return;
        }
        
        const formData = new FormData();
        formData.append('csv_file', file);
        
        importBtn.disabled = true;
        importBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Importing...';
        
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
            },
        })
        .then(response => response.json())
        .then(data => {
            resultsDiv.style.display = 'block';
            document.getElementById('createdCount').textContent = data.results.created || 0;
            document.getElementById('updatedCount').textContent = data.results.updated || 0;
            document.getElementById('unchangedCount').textContent = data.results.unchanged || 0;
            
            if (data.results.errors && data.results.errors.length > 0) {
                errorListDiv.style.display = 'block';
                const errorsList = document.getElementById('errors');
                errorsList.innerHTML = '';
                
                data.results.errors.forEach(error => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item list-group-item-danger';
                    li.textContent = `Row ${JSON.stringify(error.row)}: ${error.error}`;
                    errorsList.appendChild(li);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during import');
        })
        .finally(() => {
            importBtn.disabled = false;
            importBtn.innerHTML = '<i class="fas fa-file-import"></i> Import Cumulative';
        });
    });
});