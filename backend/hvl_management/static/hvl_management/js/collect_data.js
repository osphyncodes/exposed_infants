const table = new ExcelLikeTable('excelTable', {
    defaultRowCount: JSON.parse(localStorage.getItem('hvlTableArrayCount')) || 1,
    allowEmptyRows: true
}, JSON.parse(localStorage.getItem('hvlTableData'))) || [];

// Add fields
table.addField('SN', 'number', { placeholder: 'Enter SN', required: true });
table.addField('Date Entered', 'date');
table.addField('ART Number', 'number', { placeholder: 'Enter ART Number', required: true });
table.addField('Sex', 'select', { 
    options: [
        { value: 'male', label: 'Male' },
        { value: 'female', label: 'Female' },
    ] 
});
table.addField('Age', 'number', { placeholder: 'Enter Age' });
table.addField('Sample Log Number', 'number', { placeholder: 'Enter Sample Log Number' });
table.addField('Reason for Test', 'select', { 
    options: [
        { value: 'routine', label: 'Routine' },
        { value: 'targeted', label: 'Targeted' },
        { value: 'llv', label: 'FUP after Low Level Viraemia' },
        { value: '1000plus', label: 'FUP after >1000 copies/ml' },
        { value: 'repeat', label: 'Repeat (Rejected/Lost/Missing)'}
    ]
});

table.addField('Result Value', 'number', { placeholder: 'Enter Result Value' });

// Connect buttons
table.connectAddRowButton('addRowBtn');
table.connectJSONButton('saveBtn', (data) => {
    localStorage.setItem('hvlTableData', JSON.stringify(data));
    localStorage.setItem('hvlTableArrayCount', data.length);
    showAlert('success', 'Data successfully saved to local storage.');
});

table.connectJSONButton('submitBtn', async (data) => {
    localStorage.setItem('hvlTableData', JSON.stringify(data));
    localStorage.setItem('hvlTableArrayCount', data.length);

    for (const datas of data) {
        // check if all fields have values
        for (const key in datas) {
            if (!datas[key]) {
                showAlert('error', `Please fill in all fields (missing: ${key}).`);
                return;
            }
        }

        // check if date is valid and not in the future
        const enteredDate = new Date(datas['Date Entered']);
        const currentDate = new Date();
        if (isNaN(enteredDate.getTime()) || enteredDate > currentDate) {
            showAlert('error', 'Please enter a valid date that is not in the future.');
            return;
        }
    }

    url = document.getElementById('submitBtn').dataset.url;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        data = await response.json();
        showAlert(data.status, data.message || 'Data successfully submitted.');
    } else {
        showAlert('error', `Failed to submit data. ${response.statusText}`);
    }
});

document.getElementById('clearBtn').addEventListener('click', () => {
    table.clear();
});

// Test the navigation
console.log('Excel-like table initialized. Use Tab to move right, Enter to move down.');