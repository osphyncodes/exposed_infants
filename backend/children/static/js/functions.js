function makeTableInteractive(tableId, titleId, filter_list = []) {
    const table = document.getElementById(tableId);
    if (!table) return;
    const tbody = table.querySelector("tbody");
    if (!tbody) return;
    const headers = table.querySelectorAll("thead th");
    const title = document.getElementById(titleId);

    // Count all rows initially
    const allRows = Array.from(tbody.querySelectorAll("tr"));
    const count = allRows.length;

    // Set up rows per page options
    const possibleOptions = [1, 5, 10, 25, 50];
    const rowsPerPageOptions = possibleOptions.filter(opt => opt <= count);
    rowsPerPageOptions.push("Show All");

    let currentPage = 1;
    let rowsPerPage = 5;
    let sortColumn = null;
    let sortDirection = 'asc';
    let activeFilters = {};

    // Update title with count
    if (title) {
        title.innerText = title.innerText.replace(/\(\d+\)$/, '').trim() + ` (${count})`;
    }

    // Utility: get all rows (not filtered)
    const getAllRows = () => Array.from(tbody.querySelectorAll("tr"));

    // Utility: get filtered rows (visible after filter)
    const getFilteredRows = () => getAllRows().filter(row => row.dataset.filtered !== "false");

    // Utility: get paginated rows (visible after filter and pagination)
    const getPaginatedRows = () => {
        const filtered = getFilteredRows();
        if (rowsPerPage === count) return filtered;
        const start = (currentPage - 1) * rowsPerPage;
        return filtered.slice(start, start + rowsPerPage);
    };

    // Clear sort icons
    function clearSortIcons() {
        headers.forEach(th => {
            const icon = th.querySelector("i.fa");
            if (icon) th.removeChild(icon);
        });
    }

    // Add sort icon
    function addSortIcon(th, direction) {
        const icon = document.createElement("i");
        icon.className = direction === 'asc' ? 'fa fa-arrow-up ms-2' : 'fa fa-arrow-down ms-2';
        th.appendChild(icon);
    }

    // Sort table by column
    function sortTableByColumn(index) {
        const rows = getFilteredRows();
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

        // Re-append sorted rows
        rows.forEach(row => tbody.appendChild(row));
        clearSortIcons();
        addSortIcon(headers[index], direction);
        currentPage = 1;
        render();
    }

    // Create filter controls
    function createFilterControls() {
        if (filter_list.length === 0) return;
        // Remove existing filter container if any
        const old = document.getElementById(`${tableId}-filters`);
        if (old) old.remove();

        const filterContainer = document.createElement("div");
        filterContainer.className = "table-filters mb-3";
        filterContainer.id = `${tableId}-filters`;
        filterContainer.style.background = "#f8fafc";
        filterContainer.style.border = "1px solid #e2e8f0";
        filterContainer.style.borderRadius = "12px";
        filterContainer.style.boxShadow = "0 2px 8px rgba(0,0,0,0.04)";
        filterContainer.style.padding = "24px 20px 16px 20px";
        filterContainer.style.marginBottom = "24px";

        const filterTitle = document.createElement("h5");
        filterTitle.className = "mb-4";
        filterTitle.textContent = "Filters";
        filterTitle.style.fontWeight = "bold";
        filterTitle.style.letterSpacing = "1px";
        filterTitle.style.color = "#334155";
        filterContainer.appendChild(filterTitle);

        const filterGrid = document.createElement("div");
        filterGrid.className = "row g-4";
        filterContainer.appendChild(filterGrid);

        headers.forEach((th, index) => {
            const headerText = th.textContent.trim();
            if (!filter_list.includes(headerText)) return;

            const colDiv = document.createElement("div");
            colDiv.className = "col-12 col-md-6 col-lg-4";
            colDiv.style.display = "flex";
            colDiv.style.flexDirection = "column";
            colDiv.style.marginBottom = "12px";

            const label = document.createElement("label");
            label.className = "form-label";
            label.textContent = headerText;
            label.htmlFor = `${tableId}-filter-${index}`;
            label.style.fontWeight = "600";
            label.style.color = "#1e293b";
            label.style.marginBottom = "6px";
            colDiv.appendChild(label);

            const select = document.createElement("select");
            select.className = "form-select";
            select.id = `${tableId}-filter-${index}`;
            select.style.marginBottom = "8px";
            select.style.maxWidth = "100%";
            select.style.fontSize = "1rem";
            select.style.borderRadius = "8px";
            select.style.border = "1px solid #cbd5e1";

            // Determine column type
            const sampleValue = tbody.querySelector(`tr td:nth-child(${index + 1})`)?.textContent.trim();
            let columnType = 'text';
            if (sampleValue) {
                if (!isNaN(sampleValue)) {
                    columnType = 'number';
                } else if (Date.parse(sampleValue) || sampleValue.match(/^\d{1,2}\/\d{1,2}\/\d{4}$/)) {
                    columnType = 'date';
                }
            }

            const options = {
                'text': [
                    {value: '', text: 'No filter'},
                    {value: 'contains', text: 'Contains'},
                    {value: 'equals', text: 'Equals'},
                    {value: 'startsWith', text: 'Starts with'},
                    {value: 'endsWith', text: 'Ends with'}
                ],
                'number': [
                    {value: '', text: 'No filter'},
                    {value: 'equals', text: 'Equals'},
                    {value: 'greater', text: 'Greater than'},
                    {value: 'less', text: 'Less than'},
                    {value: 'between', text: 'Between'}
                ],
                'date': [
                    {value: '', text: 'No filter'},
                    {value: 'equals', text: 'On'},
                    {value: 'after', text: 'After'},
                    {value: 'before', text: 'Before'},
                    {value: 'between', text: 'Between'}
                ]
            };

            options[columnType].forEach(opt => {
                const option = document.createElement("option");
                option.value = opt.value;
                option.textContent = opt.text;
                select.appendChild(option);
            });

            colDiv.appendChild(select);

            const inputContainer = document.createElement("div");
            inputContainer.className = "input-group";
            inputContainer.id = `${tableId}-filter-input-${index}`;
            inputContainer.style.display = 'none';
            inputContainer.style.alignItems = "center";
            inputContainer.style.gap = "8px";

            if (columnType === 'date') {
                const input = document.createElement("input");
                input.type = "date";
                input.className = "form-control";
                input.id = `${tableId}-filter-value-${index}`;
                input.style.minWidth = "180px";
                input.style.width = "100%";
                input.style.fontSize = "1rem";
                input.style.borderRadius = "8px";
                input.style.border = "1px solid #cbd5e1";
                input.style.background = "#fff";
                input.style.marginRight = "6px";
                inputContainer.appendChild(input);

                const input2 = document.createElement("input");
                input2.type = "date";
                input2.className = "form-control d-none";
                input2.id = `${tableId}-filter-value2-${index}`;
                input2.placeholder = "End date";
                input2.style.minWidth = "180px";
                input2.style.width = "100%";
                input2.style.fontSize = "1rem";
                input2.style.borderRadius = "8px";
                input2.style.border = "1px solid #cbd5e1";
                input2.style.background = "#fff";
                input2.style.marginRight = "6px";
                inputContainer.appendChild(input2);
            } else {
                const input = document.createElement("input");
                input.type = columnType === 'number' ? "number" : "text";
                input.className = "form-control";
                input.id = `${tableId}-filter-value-${index}`;
                input.placeholder = "Value";
                input.style.minWidth = "180px";
                input.style.width = "100%";
                input.style.fontSize = "1rem";
                input.style.borderRadius = "8px";
                input.style.border = "1px solid #cbd5e1";
                input.style.background = "#fff";
                input.style.marginRight = "6px";
                inputContainer.appendChild(input);

                const input2 = document.createElement("input");
                input2.type = columnType === 'number' ? "number" : "text";
                input2.className = "form-control d-none";
                input2.id = `${tableId}-filter-value2-${index}`;
                input2.placeholder = "End value";
                input2.style.minWidth = "180px";
                input2.style.width = "100%";
                input2.style.fontSize = "1rem";
                input2.style.borderRadius = "8px";
                input2.style.border = "1px solid #cbd5e1";
                input2.style.background = "#fff";
                input2.style.marginRight = "6px";
                inputContainer.appendChild(input2);
            }

            const button = document.createElement("button");
            button.className = "btn btn-outline-secondary";
            button.type = "button";
            button.innerHTML = '<i class="fas fa-filter"></i>';
            button.style.borderRadius = "8px";
            button.style.fontWeight = "bold";
            button.style.fontSize = "1.1rem";
            button.style.padding = "6px 16px";
            button.onclick = () => applyFilter(index, headerText, columnType);
            inputContainer.appendChild(button);

            colDiv.appendChild(inputContainer);
            filterGrid.appendChild(colDiv);

            select.addEventListener('change', function() {
                const filterType = this.value;
                const inputDiv = document.getElementById(`${tableId}-filter-input-${index}`);
                const input1 = document.getElementById(`${tableId}-filter-value-${index}`);
                const input2 = document.getElementById(`${tableId}-filter-value2-${index}`);
                if (!filterType) {
                    inputDiv.style.display = 'none';
                    delete activeFilters[headerText];
                    applyFilters();
                    return;
                }
                inputDiv.style.display = 'flex';
                // Always show the first input
                if (input1) input1.classList.remove('d-none');
                // Show second input only for 'between'
                if (input2) input2.classList.toggle('d-none', filterType !== 'between');
            });
        });

        const clearAllButton = document.createElement("button");
        clearAllButton.className = "btn btn-outline-danger mt-3";
        clearAllButton.textContent = "Clear All Filters";
        clearAllButton.style.fontWeight = "bold";
        clearAllButton.style.borderRadius = "8px";
        clearAllButton.style.padding = "8px 20px";
        clearAllButton.onclick = clearAllFilters;
        filterContainer.appendChild(clearAllButton);

        table.parentElement.insertBefore(filterContainer, table);
    }

    // Apply a single filter
    function applyFilter(index, headerText, columnType) {
        const filterType = document.getElementById(`${tableId}-filter-${index}`).value;
        const value = document.getElementById(`${tableId}-filter-value-${index}`).value;
        const value2 = document.getElementById(`${tableId}-filter-value2-${index}`).value;

        if (!filterType || !value) {
            delete activeFilters[headerText];
            applyFilters();
            return;
        }

        activeFilters[headerText] = {
            index,
            type: filterType,
            value,
            value2,
            columnType
        };

        applyFilters();
    }

    // Apply all filters to all rows
    function applyFilters() {
        const rows = getAllRows();
        if (Object.keys(activeFilters).length === 0) {
            rows.forEach(row => { row.dataset.filtered = "true"; row.style.display = ""; });
            currentPage = 1;
            render();
            return;
        }

        rows.forEach(row => {
            let shouldShow = true;
            for (const [header, filter] of Object.entries(activeFilters)) {
                const cell = row.children[filter.index];
                const cellValue = cell.textContent.trim();
                if (filter.columnType === 'date') {
                    const cellDate = new Date(cellValue);
                    const filterDate = new Date(filter.value);
                    const filterDate2 = filter.value2 ? new Date(filter.value2) : null;
                    if (isNaN(cellDate.getTime())) { shouldShow = false; break; }
                    switch (filter.type) {
                        case 'equals': shouldShow = cellDate.toDateString() === filterDate.toDateString(); break;
                        case 'after': shouldShow = cellDate > filterDate; break;
                        case 'before': shouldShow = cellDate < filterDate; break;
                        case 'between': shouldShow = cellDate >= filterDate && (!filterDate2 || cellDate <= filterDate2); break;
                    }
                } else if (filter.columnType === 'number') {
                    const cellNum = parseFloat(cellValue);
                    const filterNum = parseFloat(filter.value);
                    const filterNum2 = filter.value2 ? parseFloat(filter.value2) : null;
                    if (isNaN(cellNum)) { shouldShow = false; break; }
                    switch (filter.type) {
                        case 'equals': shouldShow = cellNum === filterNum; break;
                        case 'greater': shouldShow = cellNum > filterNum; break;
                        case 'less': shouldShow = cellNum < filterNum; break;
                        case 'between': shouldShow = cellNum >= filterNum && (!filterNum2 || cellNum <= filterNum2); break;
                    }
                } else {
                    const cellText = cellValue.toLowerCase();
                    const filterText = filter.value.toLowerCase();
                    switch (filter.type) {
                        case 'contains': shouldShow = cellText.includes(filterText); break;
                        case 'equals': shouldShow = cellText === filterText; break;
                        case 'startsWith': shouldShow = cellText.startsWith(filterText); break;
                        case 'endsWith': shouldShow = cellText.endsWith(filterText); break;
                    }
                }
                if (!shouldShow) break;
            }
            row.dataset.filtered = shouldShow ? "true" : "false";
        });
        currentPage = 1;
        render();
    }

    // Clear all filters
    function clearAllFilters() {
        activeFilters = {};
        headers.forEach((th, index) => {
            const headerText = th.textContent.trim();
            if (filter_list.includes(headerText)) {
                const select = document.getElementById(`${tableId}-filter-${index}`);
                if (select) select.value = '';
                const inputDiv = document.getElementById(`${tableId}-filter-input-${index}`);
                if (inputDiv) inputDiv.style.display = 'none';
            }
        });
        applyFilters();
    }

    // Render pagination controls and export buttons
    function renderPaginationControls(totalPages) {
        let topControls = document.getElementById(`${tableId}-top-pagination`);
        if (!topControls) {
            topControls = document.createElement("div");
            topControls.id = `${tableId}-top-pagination`;
            topControls.className = "d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2";
            table.parentElement.insertBefore(topControls, table);
        }

        // Export buttons
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

        // Rows per page dropdown
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

        // Event handlers
        document.getElementById(`${tableId}-rows-select`).onchange = (e) => {
            const val = e.target.value;
            rowsPerPage = val === count.toString() ? count : parseInt(val);
            currentPage = 1;
            render();
        };

        document.getElementById(`${tableId}-page-select`).onchange = (e) => {
            currentPage = parseInt(e.target.value);
            render();
        };

        document.getElementById(`${tableId}-prev`).onclick = () => {
            if (currentPage > 1) {
                currentPage--;
                render();
            }
        };

        document.getElementById(`${tableId}-next`).onclick = () => {
            const totalPages = Math.ceil(getFilteredRows().length / (rowsPerPage === count ? count : rowsPerPage)) || 1;
            if (currentPage < totalPages) {
                currentPage++;
                render();
            }
        };

        document.getElementById(`${tableId}-export-csv`).onclick = () => exportToCSV(tableId);
        document.getElementById(`${tableId}-export-json`).onclick = () => exportToJSON(tableId);
        document.getElementById(`${tableId}-export-pdf`).onclick = () => exportToPDF(tableId);
    }

    // Render table (pagination + filter)
    function render() {
        const rows = getAllRows();
        const filtered = getFilteredRows();
        const totalPages = Math.ceil(filtered.length / (rowsPerPage === count ? count : rowsPerPage)) || 1;
        currentPage = Math.min(currentPage, totalPages);

        // Hide all rows first
        rows.forEach(row => row.style.display = "none");
        // Show only paginated filtered rows
        getPaginatedRows().forEach(row => row.style.display = "");
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

        // Extract data rows (only visible ones)
        for (let i = 1; i < rows.length; i++) {
            if (rows[i].style.display !== "none") {
                const row = [];
                const cols = rows[i].querySelectorAll("td");
                for (let j = 0; j < cols.length; j++) {
                    row.push(cols[j].textContent.trim());
                }
                csv.push(row.join(","));
            }
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
            if (rows[i].style.display !== "none") {
                const row = {};
                const cols = rows[i].querySelectorAll("td");
                for (let j = 0; j < cols.length; j++) {
                    row[headers[j]] = cols[j].textContent.trim();
                }
                json.push(row);
            }
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
        // Clone the table to modify for export
        const tableClone = table.cloneNode(true);
        // Hide filtered out rows in the clone
        Array.from(tableClone.querySelectorAll("tr")).forEach((row, i) => {
            if (i > 0 && table.querySelectorAll("tr")[i].style.display === "none") {
                row.style.display = "none";
            }
        });
        // Temporarily add to document
        tableClone.style.position = "absolute";
        tableClone.style.left = "-9999px";
        document.body.appendChild(tableClone);
        
        html2canvas(tableClone).then(canvas => {
            const imgData = canvas.toDataURL("image/png");
            const pdf = new jsPDF("p", "mm", "a4");
            const imgWidth = pdf.internal.pageSize.getWidth() - 20;
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            pdf.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);
            pdf.save(`${tableId}_export.pdf`);
            document.body.removeChild(tableClone);
        });
    }

    // Initialize
    headers.forEach((th, index) => {
        th.style.cursor = "pointer";
        th.addEventListener("click", () => sortTableByColumn(index));
    });
    createFilterControls();
    applyFilters(); // triggers render
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

function createTouchKeypad(divID, inputID) {
    // Check if the keypad already exists to avoid duplicates
    if (document.getElementById('touchKeypadContainer')) {
        return;
    }

    // Create the main container
    const container = document.createElement('div');
    container.id = 'touchKeypadContainer';
    container.style.position = 'fixed';
    container.style.bottom = '0';
    container.style.left = '270px';
    container.style.right = '0';
    container.style.backgroundColor = '#f0f0f0';
    container.style.padding = '15px 5px';
    container.style.boxShadow = '0 -5px 15px rgba(0,0,0,0.3)';
    container.style.zIndex = '1000';
    container.style.display = 'none';
    container.style.boxSizing = 'border-box';

    // Create toggle button (bigger and more visible)
    const toggleBtn = document.createElement('button');
    toggleBtn.textContent = 'ABC';
    toggleBtn.style.position = 'absolute';
    toggleBtn.style.top = '-45px';
    toggleBtn.style.right = '10px';
    toggleBtn.style.padding = '12px 20px';
    toggleBtn.style.fontSize = '18px';
    toggleBtn.style.backgroundColor = '#4CAF50';
    toggleBtn.style.color = 'white';
    toggleBtn.style.border = 'none';
    toggleBtn.style.borderRadius = '10px 10px 0 0';
    toggleBtn.addEventListener('click', toggleKeypad);
    toggleBtn.style.minWidth = '30px';

    // Create close button (bigger)
    const closeBtn = document.createElement('button');
    closeBtn.textContent = '× Close';
    closeBtn.style.position = 'absolute';
    closeBtn.style.top = '-45px';
    closeBtn.style.left = '10px';
    closeBtn.style.padding = '12px 20px';
    closeBtn.style.fontSize = '18px';
    closeBtn.style.backgroundColor = '#f44336';
    closeBtn.style.color = 'white';
    closeBtn.style.border = 'none';
    closeBtn.style.borderRadius = '10px 10px 0 0';
    closeBtn.addEventListener('click', () => {
        container.style.display = 'none';
    });

    // Create the keypad container
    const keypad = document.createElement('div');
    keypad.id = 'mainKeypad';
    keypad.style.display = 'none'
    createMainKeypad(keypad);

    // Create the numeric keypad container (initially hidden)
    const numKeypad = document.createElement('div');
    numKeypad.id = 'numericKeypad';
    createNumericKeypad(numKeypad);

    // Append all elements
    container.appendChild(toggleBtn);
    container.appendChild(closeBtn);
    container.appendChild(keypad);
    container.appendChild(numKeypad);

    // Add to the specified div
    document.getElementById(divID).appendChild(container);

    // Show the keypad when the input is focused
    const inputField = document.getElementById(inputID);
    if (inputField) {
        inputField.addEventListener('focus', () => {
            container.style.display = 'block';
        });

        // Also show on touchstart for better mobile experience
        inputField.addEventListener('touchstart', () => {
            container.style.display = 'block';
        });
    }

    function toggleKeypad() {
        const mainKeypad = document.getElementById('mainKeypad');
        const numKeypad = document.getElementById('numericKeypad');
        
        if (mainKeypad.style.display === 'none') {
            mainKeypad.style.display = 'block';
            numKeypad.style.display = 'none';
            toggleBtn.textContent = '123';
        } else {
            mainKeypad.style.display = 'none';
            numKeypad.style.display = 'block';
            toggleBtn.textContent = 'ABC';
        }
    }

    function createMainKeypad(container) {
        const rows = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['↑', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '←'],
            [' ', '.', ',', '?', '!']
        ];

        rows.forEach(row => {
            const rowDiv = document.createElement('div');
            rowDiv.style.display = 'flex';
            rowDiv.style.justifyContent = 'center';
            rowDiv.style.marginBottom = '10px';
            rowDiv.style.flexWrap = 'wrap';

            row.forEach(char => {
                const btn = document.createElement('button');
                btn.textContent = char === ' ' ? 'Space' : 
                                char === '←' ? '⌫' : 
                                char === '↑' ? '⇧' : char;
                btn.style.padding = '5px 0';
                btn.style.margin = '5px';
                btn.style.minWidth = char === ' ' ? '200px' : 
                                   ['↑', '←'].includes(char) ? '60px' : '50px';
                btn.style.fontSize = '22px';
                btn.style.backgroundColor = '#fff';
                btn.style.border = '2px solid #ddd';
                btn.style.borderRadius = '10px';
                btn.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
                btn.style.transition = 'all 0.1s';

                // Add touch feedback
                btn.addEventListener('touchstart', () => {
                    btn.style.transform = 'scale(0.95)';
                    btn.style.backgroundColor = '#e0e0e0';
                });
                
                btn.addEventListener('touchend', () => {
                    btn.style.transform = 'scale(1)';
                    btn.style.backgroundColor = '#fff';
                });

                btn.addEventListener('click', () => {
                    const input = document.getElementById(inputID);
                    if (!input) return;

                    if (char === '←') {
                        input.value = input.value.slice(0, -1);
                    } else if (char === '↑') {
                        // Toggle uppercase for next character (would need more logic for full implementation)
                        // Simplified for this example
                        input.value += '';
                    } else if (char === ' ') {
                        input.value += ' ';
                    } else {
                        input.value += char;
                    }
                    
                    // Trigger input event for any listeners
                    const event = new Event('input', { bubbles: true });
                    input.dispatchEvent(event);
                });

                rowDiv.appendChild(btn);
            });

            container.appendChild(rowDiv);
        });
    }

    function createNumericKeypad(container) {
        const rows = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['.', '0', '←']
        ];

        rows.forEach(row => {
            const rowDiv = document.createElement('div');
            rowDiv.style.display = 'flex';
            rowDiv.style.justifyContent = 'center';
            rowDiv.style.marginBottom = '15px';

            row.forEach(char => {
                const btn = document.createElement('button');
                btn.textContent = char === '←' ? '⌫' : char;
                btn.style.padding = '5px 5px';
                btn.style.margin = '2px';
                btn.style.minWidth = '80px';
                btn.style.fontSize = '16px';
                btn.style.backgroundColor = '#fff';
                btn.style.border = '2px solid #ddd';
                btn.style.borderRadius = '15px';
                btn.style.boxShadow = '0 3px 6px rgba(0,0,0,0.1)';
                btn.style.transition = 'all 0.1s';

                // Add touch feedback
                btn.addEventListener('touchstart', () => {
                    btn.style.transform = 'scale(0.95)';
                    btn.style.backgroundColor = '#e0e0e0';
                });
                
                btn.addEventListener('touchend', () => {
                    btn.style.transform = 'scale(1)';
                    btn.style.backgroundColor = '#fff';
                });

                btn.addEventListener('click', () => {
                    const input = document.getElementById(inputID);
                    if (!input) return;

                    if (char === '←') {
                        input.value = input.value.slice(0, -1);
                    } else {
                        input.value += char;
                    }
                    
                    // Trigger input event for any listeners
                    const event = new Event('input', { bubbles: true });
                    input.dispatchEvent(event);
                });

                rowDiv.appendChild(btn);
            });

            container.appendChild(rowDiv);
        });

    }
} 

function createNumericKeypad(containerID, inputID) {
    // Get elements
    const container = document.getElementById(containerID);
    const inputField = document.getElementById(inputID);
    
    // Clear container and disable input
    container.innerHTML = '';
    inputField.readOnly = true;
    inputField.style.cursor = 'default';
    inputField.style.backgroundColor = '#f9f9f9';
    
    // Add CSS styles
    const style = document.createElement('style');
    style.textContent = `
        .keypad-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            max-width: 250px;
            margin: 5px auto;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .keypad-btn {
            width: 60px;
            height: 60px;
            font-size: 20px;
            border: none;
            border-radius: 10px;
            background-color: white;
            cursor: pointer;
            transition: all 0.1s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .keypad-btn:active {
            transform: scale(0.95);
            background-color: #e0e0e0;
        }
        .keypad-btn-del {
            grid-column: 1;
            background-color: #ffebee;
            color: #d32f2f;
        }
        .keypad-btn-0 {
            grid-column: 2;
        }
        .keypad-btn-enter {
            grid-column: 3;
            background-color: #e8f5e9;
            color: #2e7d32;
        }
        .keypad-btn i {
            font-size: 1.2em;
        }
    `;
    document.head.appendChild(style);
    
    // Create container
    const keypadContainer = document.createElement('div');
    keypadContainer.className = 'keypad-container';
    container.appendChild(keypadContainer);
    
    // Create number buttons 1-9
    for (let i = 1; i <= 9; i++) {
        const btn = document.createElement('button');
        btn.className = 'keypad-btn';
        btn.textContent = i;
        btn.addEventListener('click', () => {
            inputField.value += i;
            triggerInputEvent(inputField);
        });
        keypadContainer.appendChild(btn);
    }
    
    // Delete button (←)
    const delBtn = document.createElement('button');
    delBtn.className = 'keypad-btn keypad-btn-del';
    delBtn.innerHTML = '<i class="fas fa-arrow-left"></i>';
    delBtn.addEventListener('click', () => {
        inputField.value = inputField.value.slice(0, -1);
        triggerInputEvent(inputField);
    });
    keypadContainer.appendChild(delBtn);
    
    // 0 button (centered)
    const zeroBtn = document.createElement('button');
    zeroBtn.className = 'keypad-btn keypad-btn-0';
    zeroBtn.textContent = '0';
    zeroBtn.addEventListener('click', () => {
        inputField.value += '0';
        triggerInputEvent(inputField);
    });
    keypadContainer.appendChild(zeroBtn);
    
    // Enter button (✓)
    const enterBtn = document.createElement('button');
    enterBtn.className = 'keypad-btn keypad-btn-enter';
    enterBtn.innerHTML = '<i class="fas fa-check"></i>';
    enterBtn.addEventListener('click', () => {
        const form = inputField.closest('form');
        if (form) form.submit();
    });
    keypadContainer.appendChild(enterBtn);
    
    function triggerInputEvent(input) {
        input.dispatchEvent(new Event('input', { bubbles: true }));
    }
}