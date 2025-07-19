document.addEventListener('DOMContentLoaded', function() {
    const tbody = document.getElementById('milestones-tbody');
    const birthYearFilter = document.getElementById('birth-year-filter');
    const reasonFilter = document.getElementById('reason-filter');
    const applyFiltersBtn = document.getElementById('apply-filters');
    const refreshBtn = document.getElementById('refresh-btn');
    const loadingSpinner = document.getElementById('loading-spinner');
    const downloadCsvBtn = document.getElementById('download-csv');
    const downloadPdfBtn = document.getElementById('download-pdf');
    const pagination = document.getElementById('pagination');
    const prevPage = document.getElementById('prev-page');
    const nextPage = document.getElementById('next-page');
    const paginationInfo = document.getElementById('pagination-info');
    
    let currentPage = 1;
    const itemsPerPage = 20;
    let allMilestones = [];
    let filteredMilestones = [];

    // Load initial data
    loadMissedMilestones();
    loadBirthYearFilters();

    // Event listeners
    applyFiltersBtn.addEventListener('click', () => {
        currentPage = 1;
        loadMissedMilestones();
    });
    
    refreshBtn.addEventListener('click', () => {
        currentPage = 1;
        birthYearFilter.value = '';
        reasonFilter.value = '';
        loadMissedMilestones();
    });
    
    downloadCsvBtn.addEventListener('click', downloadCSV);
    downloadPdfBtn.addEventListener('click', downloadPDF);
    
    prevPage.addEventListener('click', goToPrevPage);
    nextPage.addEventListener('click', goToNextPage);

    function goToPrevPage() {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    }

    function goToNextPage() {
        const totalPages = Math.ceil(filteredMilestones.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderTable();
        }
    }

    async function loadMissedMilestones() {
        showLoading();
        
        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    birth_year: birthYearFilter.value,
                    reason: reasonFilter.value
                })
            });

            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }

            const data = await response.json();
            allMilestones = data.missed_milestones;
            filteredMilestones = [...allMilestones];
            renderTable();
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to load missed milestones');
        } finally {
            hideLoading();
        }
    }

    function renderTable() {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const paginatedItems = filteredMilestones.slice(startIndex, endIndex);
        
        renderMissedMilestones(paginatedItems);
        updatePagination();
    }

    function updatePagination() {
        const totalItems = filteredMilestones.length;
        const totalPages = Math.ceil(totalItems / itemsPerPage);
        const startItem = ((currentPage - 1) * itemsPerPage) + 1;
        const endItem = Math.min(currentPage * itemsPerPage, totalItems);
        
        // Update pagination info
        document.getElementById('start-item').textContent = startItem;
        document.getElementById('end-item').textContent = endItem;
        document.getElementById('total-items').textContent = totalItems;
        
        // Update pagination controls
        prevPage.classList.toggle('disabled', currentPage === 1);
        nextPage.classList.toggle('disabled', currentPage === totalPages);
        
        // Update page numbers
        const pageNumbers = document.querySelectorAll('.page-item:not(#prev-page):not(#next-page)');
        pageNumbers.forEach(el => el.remove());
        
        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, currentPage + 2);
        
        for (let i = startPage; i <= endPage; i++) {
            const pageItem = document.createElement('li');
            pageItem.className = `page-item ${i === currentPage ? 'active' : ''}`;
            pageItem.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            pageItem.addEventListener('click', (e) => {
                e.preventDefault();
                currentPage = i;
                renderTable();
            });
            nextPage.parentNode.insertBefore(pageItem, nextPage);
        }
    }

    async function loadBirthYearFilters() {
        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({})
            });

            if (!response.ok) throw new Error('Failed to fetch birth years');

            const data = await response.json();
            populateBirthYearFilter(data.birth_years);
        } catch (error) {
            console.error('Error loading birth years:', error);
        }
    }

    function populateBirthYearFilter(years) {
        birthYearFilter.innerHTML = '<option value="">All Years</option>';
        years.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            birthYearFilter.appendChild(option);
        });
    }

    function renderMissedMilestones(milestones) {
        tbody.innerHTML = '';
        
        if (milestones.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="11" class="text-center py-4 text-muted">
                        <i class="fas fa-check-circle fa-2x text-success mb-2"></i>
                        <p class="mb-0">No missed milestones found</p>
                    </td>
                </tr>
            `;
            return;
        }

        milestones.forEach((child, index) => {
            const row = document.createElement('tr');
            const globalIndex = ((currentPage - 1) * itemsPerPage) + index + 1;
            
            // Format test reason for display
            let testReasonDisplay = '';
            if (child.test_reason === 'DBS_6wks_Ini') {
                testReasonDisplay = '<span class="badge bg-danger"><i class="fas fa-tint me-1"></i>DBS 6 Weeks</span>';
            } else if (child.test_reason === 'Rapid_1yr') {
                testReasonDisplay = '<span class="badge bg-warning text-dark"><i class="fas fa-vial me-1"></i>Rapid 1 Year</span>';
            } else {
                testReasonDisplay = '<span class="badge bg-secondary"><i class="fas fa-vial-virus me-1"></i>Rapid 2 Years</span>';
            }
            
            row.innerHTML = `
                <td>${globalIndex}</td>
                <td>${child.hcc_number}</td>
                <td>${child.child_name}</td>
                <td>${new Date(child.child_dob).toLocaleDateString()}</td>
                <td>${child.age_months}</td>
                <td>${child.guardian_name}</td>
                <td>${child.guardian_phone || 'N/A'}</td>
                <td>${testReasonDisplay}</td>
                <td>${new Date(child.due_date).toLocaleDateString()}</td>
                <td>
                    <span class="badge rounded-pill ${child.days_overdue > 30 ? 'bg-danger' : 'bg-warning text-dark'}">
                        ${child.days_overdue} days
                    </span>
                </td>
                <td>
                    <a href="${child.view_url}" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-eye me-1"></i>View
                    </a>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    function downloadCSV() {
        if (filteredMilestones.length === 0) {
            alert('No data to download');
            return;
        }

        // CSV header
        let csvContent = "No,HCC Number,Child Name,Date of Birth,Age (Months),Guardian,Phone,Missed Test,Due Date,Days Overdue\n";

        // Add data rows
        filteredMilestones.forEach((child, index) => {
            const testReason = child.test_reason === 'DBS_6wks_Ini' ? 'DBS 6 Weeks' : 
                             child.test_reason === 'Rapid_1yr' ? 'Rapid 1 Year' : 'Rapid 2 Years';
            
            csvContent += [
                index + 1,
                `"${child.hcc_number}"`,
                `"${child.child_name}"`,
                new Date(child.child_dob).toLocaleDateString(),
                child.age_months,
                `"${child.guardian_name}"`,
                `"${child.guardian_phone || 'N/A'}"`,
                `"${testReason}"`,
                new Date(child.due_date).toLocaleDateString(),
                child.days_overdue
            ].join(',') + '\n';
        });

        // Create download link
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', `missed_milestones_${new Date().toISOString().slice(0,10)}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function downloadPDF() {
        if (filteredMilestones.length === 0) {
            alert('No data to download');
            return;
        }

        const element = document.createElement('div');
        element.innerHTML = `
            <h3 style="text-align: center;">Missed Milestones Report</h3>
            <p style="text-align: center;">Generated on ${new Date().toLocaleDateString()}</p>
            <table border="1" style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th>No</th>
                        <th>HCC Number</th>
                        <th>Child Name</th>
                        <th>Date of Birth</th>
                        <th>Age (Months)</th>
                        <th>Missed Test</th>
                        <th>Due Date</th>
                        <th>Days Overdue</th>
                    </tr>
                </thead>
                <tbody>
                    ${filteredMilestones.map((child, index) => `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${child.hcc_number}</td>
                            <td>${child.child_name}</td>
                            <td>${new Date(child.child_dob).toLocaleDateString()}</td>
                            <td>${child.age_months}</td>
                            <td>${child.test_reason === 'DBS_6wks_Ini' ? 'DBS 6 Weeks' : 
                                 child.test_reason === 'Rapid_1yr' ? 'Rapid 1 Year' : 'Rapid 2 Years'}</td>
                            <td>${new Date(child.due_date).toLocaleDateString()}</td>
                            <td>${child.days_overdue}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;

        const opt = {
            margin: 10,
            filename: `missed_milestones_${new Date().toISOString().slice(0,10)}.pdf`,
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };

        html2pdf().from(element).set(opt).save();
    }

    function showLoading() {
        loadingSpinner.style.display = 'flex';
    }

    function hideLoading() {
        loadingSpinner.style.display = 'none';
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});