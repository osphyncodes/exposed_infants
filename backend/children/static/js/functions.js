
function makeTableInteractive(tableId, titleId) {
    console.log('zikutheka');
    const table = document.getElementById(tableId);
    const tbody = table.querySelector("tbody");
    const headers = table.querySelectorAll("thead th");
    const count = getTableRowCount(tableId);
    const title = document.getElementById(titleId);
    
    // Dynamically adjust rowsPerPageOptions based on record count
    const possibleOptions = [1, 5, 10, 25, 50];
    const rowsPerPageOptions = possibleOptions.filter(opt => opt <= count);
    rowsPerPageOptions.push("Show All"); // Add "Show All" option
    
    let currentPage = 1;
    let rowsPerPage = 5;
    let sortColumn = null;
    let sortDirection = 'asc';

    const getRows = () => Array.from(tbody.querySelectorAll("tr"));

    if (title) {
        title.innerText = `${title.innerText} (${count})`;
    }

    function clearSortIcons() {
        headers.forEach(th => {
            const icon = th.querySelector("i.fa");
            if (icon) th.removeChild(icon);
        });
    }

    function addSortIcon(th, direction) {
        const icon = document.createElement("i");
        icon.className = direction === 'asc' ? 'fa fa-arrow-up ms-2' : 'fa fa-arrow-down ms-2';
        th.appendChild(icon);
    }

    function sortTableByColumn(index) {
        const rows = getRows();
        const direction = (sortColumn === index && sortDirection === 'asc') ? 'desc' : 'asc';
        sortDirection = direction;
        sortColumn = index;

        rows.sort((a, b) => {
            const aText = a.children[index].textContent.trim();
            const bText = b.children[index].textContent.trim();
            const aVal = isNaN(aText) ? aText.toLowerCase() : parseFloat(aText);
            const bVal = isNaN(bText) ? bText.toLowerCase() : parseFloat(bText);
            if (aVal < bVal) return direction === 'asc' ? -1 : 1;
            if (aVal > bVal) return direction === 'asc' ? 1 : -1;
            return 0;
        });

        tbody.innerHTML = "";
        rows.forEach(row => tbody.appendChild(row));
        renderPage(currentPage);
        clearSortIcons();
        addSortIcon(headers[index], direction);
    }

    function renderPaginationControls(totalPages) {
        let topControls = document.getElementById(`${tableId}-top-pagination`);
        if (!topControls) {
            topControls = document.createElement("div");
            topControls.id = `${tableId}-top-pagination`;
            topControls.className = "d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2";
            table.parentElement.insertBefore(topControls, table);
        }

        // Add export buttons (CSV, JSON, PDF)
        const exportButtons = `
            <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-secondary" id="${tableId}-export-csv">
                    <i class="fas fa-file-csv me-1"></i> CSV
                </button>
                <button class="btn btn-sm btn-outline-secondary" id="${tableId}-export-json">
                    <i class="fas fa-file-code me-1"></i> JSON
                </button>
                <button class="btn btn-sm btn-outline-secondary" id="${tableId}-export-pdf">
                    <i class="fas fa-file-pdf me-1"></i> PDF
                </button>
            </div>
        `;

        // Dropdown for rows per page
        const dropdown = `
            <div class="d-flex align-items-center gap-2">
                <label class="form-label m-0">Rows per page:</label>
                <select class="form-select form-select-sm w-auto" id="${tableId}-rows-select">
                    ${rowsPerPageOptions.map(opt => 
                        `<option value="${opt === "Show All" ? count : opt}" ${opt === (rowsPerPage === count ? "Show All" : rowsPerPage) ? 'selected' : ''}>
                            ${opt === "Show All" ? "Show All" : opt}
                        </option>`
                    ).join('')}
                </select>
            </div>
        `;

        // Page navigation controls
        const pageSelect = Array.from({ length: totalPages }, (_, i) =>
            `<option value="${i + 1}" ${i + 1 === currentPage ? 'selected' : ''}>Page ${i + 1}</option>`).join('');

        const pageControl = `
            <div class="d-flex align-items-center gap-2">
                <button class="btn btn-sm btn-outline-primary" id="${tableId}-prev" ${currentPage === 1 ? 'disabled' : ''}>
                    <i class="fas fa-chevron-left"></i> Prev
                </button>
                <select class="form-select form-select-sm w-auto" id="${tableId}-page-select">${pageSelect}</select>
                <button class="btn btn-sm btn-outline-primary" id="${tableId}-next" ${currentPage === totalPages ? 'disabled' : ''}>
                    Next <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        `;

        topControls.innerHTML = exportButtons + dropdown + pageControl;

        // Event handlers for pagination
        document.getElementById(`${tableId}-rows-select`).onchange = (e) => {
            const val = e.target.value;
            rowsPerPage = val === count.toString() ? count : parseInt(val);
            currentPage = 1;
            renderPage(currentPage);
        };

        document.getElementById(`${tableId}-page-select`).onchange = (e) => {
            currentPage = parseInt(e.target.value);
            renderPage(currentPage);
        };

        document.getElementById(`${tableId}-prev`).onclick = () => {
            if (currentPage > 1) {
                currentPage--;
                renderPage(currentPage);
            }
        };

        document.getElementById(`${tableId}-next`).onclick = () => {
            if (currentPage < totalPages) {
                currentPage++;
                renderPage(currentPage);
            }
        };

        // Event handlers for export buttons
        document.getElementById(`${tableId}-export-csv`).onclick = () => exportToCSV(tableId);
        document.getElementById(`${tableId}-export-json`).onclick = () => exportToJSON(tableId);
        document.getElementById(`${tableId}-export-pdf`).onclick = () => exportToPDF(tableId);
    }

    function renderPage(page) {
        const rows = getRows();
        const totalPages = Math.ceil(rows.length / (rowsPerPage === count ? count : rowsPerPage)) || 1;

        const start = (page - 1) * rowsPerPage;
        const end = rowsPerPage === count ? rows.length : start + rowsPerPage;

        rows.forEach((row, i) => {
            row.style.display = (i >= start && i < end) ? "" : "none";
        });

        renderPaginationControls(totalPages);
    }

    // Export functions
    function exportToCSV(tableId) {
        const table = document.getElementById(tableId);
        const rows = table.querySelectorAll("tr");
        let csv = [];

        // Extract headers
        const headers = Array.from(rows[0].querySelectorAll("th")).map(th => th.textContent.trim());
        csv.push(headers.join(","));

        // Extract data rows
        for (let i = 1; i < rows.length; i++) {
            const row = [];
            const cols = rows[i].querySelectorAll("td");
            for (let j = 0; j < cols.length; j++) {
                row.push(cols[j].textContent.trim());
            }
            csv.push(row.join(","));
        }

        const csvContent = csv.join("\n");
        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${tableId}_export.csv`;
        link.click();
    }

    function exportToJSON(tableId) {
        const table = document.getElementById(tableId);
        const rows = table.querySelectorAll("tr");
        const headers = Array.from(rows[0].querySelectorAll("th")).map(th => th.textContent.trim());
        const json = [];

        for (let i = 1; i < rows.length; i++) {
            const row = {};
            const cols = rows[i].querySelectorAll("td");
            for (let j = 0; j < cols.length; j++) {
                row[headers[j]] = cols[j].textContent.trim();
            }
            json.push(row);
        }

        const jsonContent = JSON.stringify(json, null, 2);
        const blob = new Blob([jsonContent], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${tableId}_export.json`;
        link.click();
    }

    function exportToPDF(tableId) {
        // Using jsPDF and html2canvas for PDF export (requires these libraries)
        if (typeof html2canvas === "undefined" || typeof jsPDF === "undefined") {
            alert("PDF export requires jsPDF and html2canvas libraries. Please include them in your project.");
            return;
        }

        const table = document.getElementById(tableId);
        html2canvas(table).then(canvas => {
            const imgData = canvas.toDataURL("image/png");
            const pdf = new jsPDF("p", "mm", "a4");
            const imgWidth = pdf.internal.pageSize.getWidth() - 20;
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            pdf.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);
            pdf.save(`${tableId}_export.pdf`);
        });
    }

    // Initialize sorting and pagination
    headers.forEach((th, index) => {
        th.style.cursor = "pointer";
        th.addEventListener("click", () => sortTableByColumn(index));
    });

    renderPage(currentPage);
}

function getTableRowCount(tableId) {
    const table = document.getElementById(tableId);
    if (!table) {
        console.error(`Table with id "${tableId}" not found.`);
        return 0;
    }

    const tbody = table.querySelector("tbody");
    if (!tbody) {
        console.error(`Table with id "${tableId}" has no <tbody>.`);
        return 0;
    }

    // Count only non-empty, visible rows (if needed, adjust this logic)
    const rows = tbody.querySelectorAll("tr");
    return rows.length;
}

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

    
