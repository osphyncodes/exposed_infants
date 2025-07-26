document.addEventListener('DOMContentLoaded', ()=> {
    const monthSelect = document.getElementById('month')
    const periodContainers = document.querySelectorAll('.period')
    const search_btn = document.getElementById('search-btn')
    const toggleBtn = document.getElementById('sidebarToggle');
    const tops = document.querySelector('.tops')
    

    // toggleBtn.addEventListener('click', ()=> {
    //     state = localStorage.getItem('sidebar-collapsed')

    //     if (state == 1){
    //         tops.style.left = '90px'
    //     }else{
    //         tops.style.left = '250px'
    //     }
    // })
    for (let index = 1; index <=42; index++) {

        var cnt = document.getElementById(`id-total-count${index}`)
        if(cnt){
            cnt.innerText = "Not Run"
        }
    }

    function changeMonthcolor() {
        var id = getMonthInt(monthSelect.value)

        periodContainers.forEach((item) => {
                item.style.background = ''
                item.style.color = ''
                item.fontweight = ''
        })

        periodContainers.forEach((item) => {
            if (item.dataset.id == id) {
                item.style.background = 'darkblue'
                item.style.color = 'white'
                item.fontweight = 'bold'
            }
        })
    }

    search_btn.addEventListener('click', async function(){
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const yearSelect = document.getElementById('year').value
        const id = parseInt(getMonthInt(monthSelect.value))
        const month = getMonthInt2(id)
        const monthYear = `${month} ${yearSelect}`
        const cohort = getBirthCohorts(monthYear)
        const c2date = getMonthRange(cohort.twoMonths)
        const c12date = getMonthRange(cohort.twelveMonths)
        const c24date = getMonthRange(cohort.twentyFourMonths)

        if (yearSelect == 'Select Reporting Year' || monthSelect.value == 'Select Reporting Month'){
            alert('Reporting year and month is required')
            return
        }

        showLoading('Generating. Please wait...');
        url = search_btn.dataset.url
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                cohort2Date: {
                    dates: c2date,
                    type: 1
                },
                cohort12Date: {
                    dates: c12date,
                    type: 2
                },
                cohort24Date: {
                    dates: c24date,
                    type: 3
                }   
            })
        })

        if (!response.ok) {
              const errorData = await response.json();
              console.error("Error:", errorData.error || "Unknown error");
              alert(errorData.error || "An error occurred");
              return;
        }

        const data = await response.json()

        for (let index = 1; index <=42; index++) {

            var cnt = document.getElementById(`id-total-count${index}`)

            

            if (cnt) {
                cnt_id = `count${index}`
                cnt.innerText = data[cnt_id]
                list = data[`count${index}_children`]
                
                localStorage.removeItem(cnt.id)
                if (cnt.innerText != 0){
                    setEncryptedItem(cnt.id, list)

                    cnt.addEventListener('click', (event)=>{
                        var gotten_data = []
                        var table_data = []
                        var num = 0
                        gotten_data = getDecryptedItem(event.target.id)
                        title_what = event.target.dataset.what

                        count_data = gotten_data.length
                        headers = [
                            '#',
                            'HCC Number',
                            'Name',
                            'Gender',
                            'Date of Birth',
                            'Locator',
                            'Guardian',
                            'Phone Number',
                            'Mother ART#',
                            'Action'
                        ]

                        gotten_data.forEach((e)=>{
                            num += 1

                            table_data += `
                                <tr>
                                    <td>${num}</td>
                                    <td>${e.hcc_number}</td>
                                    <td>${e.child_name}</td>
                                    <td>${e.gender}</td>
                                    <td>${e.birthdate}</td>
                                    <td>${e.locator}</td>
                                    <td>${e.guardian}</td>
                                    <td>${e.guardian_phone}</td>
                                    <td>${e.mother_art_number}</td>
                                    <td>
                                        <a href="${e.url}" class="btn btn-sm btn-outline-primary">
                                            <i class="fas fa-eye me-1"></i>View
                                        </a>
                                    </td>
                                </tr>
                            `
                        })
                        showDynamicTable(headers, table_data, 2,`${title_what} (${count_data})`)
                        console.log(table_data)
                    })
                }
                
                changeMonthcolor()
                if (parseInt(cnt.innerText) != 0){
                    cnt.style.color = 'blue'
                    cnt.style.fontweight = 'bold'
                    cnt.style.cursor = 'pointer'
                }else {
                    cnt.style.color = 'black'
                    cnt.style.fontweight = ''
                    cnt.style.cursor = ''   
                }
                
            };
            
        };

        hideLoading()
    })

    function getMonthRange(monthYearStr) {
    if (!monthYearStr) return null;

    // Try to parse input like "Jan 2025" or "January 2025"
    const [monthStr, yearStr] = monthYearStr.trim().split(/\s+/);

    const monthMap = {
        jan: 0, january: 0,
        feb: 1, february: 1,
        mar: 2, march: 2,
        apr: 3, april: 3,
        may: 4,
        jun: 5, june: 5,
        jul: 6, july: 6,
        aug: 7, august: 7,
        sep: 8, september: 8,
        oct: 9, october: 9,
        nov: 10, november: 10,
        dec: 11, december: 11
    };

    const month = monthMap[monthStr.toLowerCase()];
    const year = parseInt(yearStr);

    if (month === undefined || isNaN(year)) {
        return null;
    }

    var firstDate = new Date(year, month, 1);
    var lastDate = new Date(year, month + 1, 0); // day 0 of next month = last day of this month


    firstDate = getLocalDateString(firstDate)
    lastDate = getLocalDateString(lastDate)
    return {
        firstDate,
        lastDate
    };
    }

    function getLocalDateString(date = new Date()) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
    function getDate(date, day){

    }
    
    function getMonthInt(month) {
        if (!month) return -1;

        const monthMap = {
            january: 1, jan: 1,
            february: 2, feb: 2,
            march: 3, mar: 3,
            april: 4, apr: 4,
            may: 5,
            june: 6, jun: 6,
            july: 7, jul: 7,
            august: 8, aug: 8,
            september: 9, sep: 9,
            october: 10, oct: 10,
            november: 11, nov: 11,
            december: 12, dec: 12
        };

        const key = month.toLowerCase().trim();
        return monthMap[key] || -1;
    }

    function getMonthInt2(monthOrNum) {
        switch (monthOrNum) {
            case 1: return 'Jan'
            case 2: return 'Feb'
            case 3: return 'Mar'
            case 4: return 'Apr'
            case 5: return 'May'
            case 6: return 'Jun'
            case 7: return 'Jul'
            case 8: return 'Aug'
            case 9: return 'Sep'
            case 10: return 'Oct'
            case 11: return 'Nov'
            case 12: return 'Dec'
            default: return 'Not Available'
        }
    }

    function getBirthCohorts(reportingDate) {
        const months = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ];
        
        const [reportingMonth, reportingYear] = reportingDate.split(' ');
        const reportingMonthIndex = months.indexOf(reportingMonth);
        const reportingYearNum = parseInt(reportingYear);
        
        // 2-month cohort (born 3 months before reporting month)
        let twoMonthOffset = 3;
        let twoMonthCohortMonthIndex = reportingMonthIndex - twoMonthOffset;
        let twoMonthCohortYear = reportingYearNum;
        if (twoMonthCohortMonthIndex < 0) {
            twoMonthCohortMonthIndex += 12;
            twoMonthCohortYear--;
        }
        
        // 12-month cohort (born 14 months before reporting month)
        let twelveMonthOffset = 14;
        let twelveMonthCohortMonthIndex = (reportingMonthIndex - (twelveMonthOffset % 12));
        let twelveMonthCohortYear = reportingYearNum - Math.floor(twelveMonthOffset / 12);
        if (twelveMonthCohortMonthIndex < 0) {
            twelveMonthCohortMonthIndex += 12;
            twelveMonthCohortYear--;
        }
        
        // 24-month cohort (born 26 months before reporting month)
        let twentyFourMonthOffset = 26;
        let twentyFourMonthCohortMonthIndex = (reportingMonthIndex - (twentyFourMonthOffset % 12));
        let twentyFourMonthCohortYear = reportingYearNum - Math.floor(twentyFourMonthOffset / 12);
        if (twentyFourMonthCohortMonthIndex < 0) {
            twentyFourMonthCohortMonthIndex += 12;
            twentyFourMonthCohortYear--;
        }
        
        return {
            twoMonths: `${months[twoMonthCohortMonthIndex]} ${twoMonthCohortYear}`,
            twelveMonths: `${months[twelveMonthCohortMonthIndex]} ${twelveMonthCohortYear}`,
            twentyFourMonths: `${months[twentyFourMonthCohortMonthIndex]} ${twentyFourMonthCohortYear}`
        };
    }

})
