
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