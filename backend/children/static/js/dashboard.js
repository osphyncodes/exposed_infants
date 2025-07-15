

    // Data passed from Django view
    const childrenPerMonthLabels = JSON.parse('{{ children_per_month_labels|escapejs }}');
    const childrenPerMonthData = JSON.parse('{{ children_per_month_data|escapejs }}');
    const genderLabels = JSON.parse('{{ gender_labels|escapejs }}');
    const genderData = JSON.parse('{{ gender_data|escapejs }}');
    const visitTrendsLabels = JSON.parse('{{ visit_trends_labels|escapejs }}');
    const visitTrendsData = JSON.parse('{{ visit_trends_data|escapejs }}');
    const uniqueChildrenTrendsData = JSON.parse('{{ unique_children_trends_data|escapejs }}');
    const appTrendsLabels = JSON.parse('{{ app_trends_labels|escapejs }}');
    const appTrendsData = JSON.parse('{{ app_trends_data|escapejs }}');

    // Children Registered Per Month Chart
    const childrenPerMonthOptions = {
        series: [{
            name: 'Children Registered',
            data: childrenPerMonthData
        }],
        chart: {
            type: 'bar',
            height: 350,
            toolbar: {
                show: true,
                tools: {
                    download: true,
                    selection: true,
                    zoom: true,
                    zoomin: true,
                    zoomout: true,
                    pan: true,
                    reset: true
                }
            }
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                horizontal: false,
                columnWidth: '55%',
            },
        },
        dataLabels: {
            enabled: true
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        xaxis: {
            categories: childrenPerMonthLabels,
            labels: {
                style: {
                    fontSize: '12px'
                }
            }
        },
        yaxis: {
            title: {
                text: 'Number of Children'
            }
        },
        fill: {
            opacity: 1,
            colors: ['#3a86ff']
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val + " children"
                }
            }
        },
        responsive: [{
            breakpoint: 768,
            options: {
                chart: {
                    height: 300
                },
                plotOptions: {
                    bar: {
                        columnWidth: '60%'
                    }
                }
            }
        }]
    };

    const childrenPerMonthChart = new ApexCharts(
        document.querySelector("#childrenPerMonthChart"), 
        childrenPerMonthOptions
    );
    childrenPerMonthChart.render();

    // Gender Distribution Chart
    const genderDistributionOptions = {
        series: genderData,
        chart: {
            type: 'pie',
            height: 350,
            toolbar: {
                show: true
            }
        },
        labels: genderLabels,
        colors: ['#ff6392', '#3a86ff'],
        responsive: [{
            breakpoint: 768,
            options: {
                chart: {
                    height: 300
                },
                legend: {
                    position: 'bottom'
                }
            }
        }],
        legend: {
            position: 'right',
            offsetY: 0,
            height: 230,
        },
        dataLabels: {
            enabled: true,
            formatter: function (val, { seriesIndex, w }) {
                return w.config.labels[seriesIndex] + ': ' + val + '%'
            },
            dropShadow: {
                enabled: false
            }
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val + '%'
                }
            }
        }
    };

    const genderDistributionChart = new ApexCharts(
        document.querySelector("#genderDistributionChart"), 
        genderDistributionOptions
    );
    genderDistributionChart.render();

    // Visit Trends Chart
    const visitTrendsOptions = {
        series: [{
            name: 'Total Visits',
            data: visitTrendsData
        }],
        chart: {
            type: 'area',
            height: '98%',
            width: '97%',
            animations: {
                enabled: true,
                easing: 'easeinout',
                speed: 800,
                animateGradually: {
                    enabled: true,
                    delay: 150
                },
                dynamicAnimation: {
                    enabled: true,
                    speed: 350
                }
            },
            stacked: false,
            zoom: {
                enabled: true
            },
            toolbar: {
                show: true
            }
        },
        colors: ['#5e60ce', '#4ea8de'],
        dataLabels: {
            enabled: true
        },
        stroke: {
            curve: 'smooth',
            width: 2
        },
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                inverseColors: false,
                opacityFrom: 0.5,
                opacityTo: 0,
                stops: [0, 90, 100]
            },
        },
        markers: {
            size: 4,
            strokeWidth: 0,
            hover: {
                size: 6
            }
        },
        xaxis: {
            categories: visitTrendsLabels,
            labels: {
                style: {
                    fontSize: '12px'
                }
            }
        },
        yaxis: {
            title: {
                text: 'Number of Visits'
            },
            min: 0
        },
        tooltip: {
            shared: true,
            intersect: false,
            y: {
                formatter: function (val) {
                    return val + (val !== 1 ? ' visits' : ' visit')
                }
            }
        },
        responsive: [{
            breakpoint: 768,
            options: {
                chart: {
                    height: 300
                }
            }
        }]
    };

    const appTrendsOptions = {
        series: [{
            name: 'Total Appointments',
            data: appTrendsData
        }],
        chart: {
            type: 'area',
            height: '98%',
            width: '97%',
            animations: {
                enabled: true,
                easing: 'easeinout',
                speed: 800,
                animateGradually: {
                    enabled: true,
                    delay: 150
                },
                dynamicAnimation: {
                    enabled: true,
                    speed: 350
                }
            },
            stacked: false,
            zoom: {
                enabled: true
            },
            toolbar: {
                show: true
            }
        },
        colors: ['#5e60ce', '#4ea8de'],
        dataLabels: {
            enabled: true
        },
        stroke: {
            curve: 'smooth',
            width: 2
        },
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                inverseColors: false,
                opacityFrom: 0.5,
                opacityTo: 0,
                stops: [0, 90, 100]
            },
        },
        markers: {
            size: 4,
            strokeWidth: 0,
            hover: {
                size: 6
            }
        },
        xaxis: {
            categories: appTrendsLabels,
            labels: {
                style: {
                    fontSize: '12px'
                }
            }
        },
        yaxis: {
            title: {
                text: 'Number of Appointments'
            },
            min: 0
        },
        tooltip: {
            shared: true,
            intersect: false,
            y: {
                formatter: function (val) {
                    return val + (val !== 1 ? ' visits' : ' visit')
                }
            }
        },
        responsive: [{
            breakpoint: 768,
            options: {
                chart: {
                    height: 300
                }
            }
        }]
    };

    const appsTrendsChart = new ApexCharts(
        document.querySelector("#appsTrendsChart"), 
        appTrendsOptions
    );
    appsTrendsChart.render();

    const visitTrendsChart = new ApexCharts(
        document.querySelector("#visitTrendsChart"), 
        visitTrendsOptions
    );
    visitTrendsChart.render();

    // Chart view toggle functionality
    document.querySelectorAll('.btn-view').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.btn-view').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const viewType = this.getAttribute('data-view');
            genderDistributionChart.updateOptions({
                chart: {
                    type: viewType
                }
            });
        });
    });

    // Chart period toggle functionality
    document.querySelectorAll('.btn-period').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.btn-period').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // In a real implementation, you would fetch new data based on the period
            // For this example, we'll just simulate it by adjusting the x-axis
            const period = this.getAttribute('data-period');
            let labels = childrenPerMonthLabels;
            
            if (period === 'half-year') {
                labels = childrenPerMonthLabels.slice(-6);
            } else if (period === 'quarter') {
                labels = childrenPerMonthLabels.slice(-3);
            }
            
            childrenPerMonthChart.updateOptions({
                xaxis: {
                    categories: labels
                }
            });
        });
    });

    // Metric toggle functionality for visit trends
    document.querySelectorAll('.btn-metric').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.btn-metric').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const metric = this.getAttribute('data-metric');
            if (metric === 'visits') {
                visitTrendsChart.updateSeries([{
                    name: 'Total Visits',
                    data: visitTrendsData
                }, {
                    name: 'Unique Children',
                    data: uniqueChildrenTrendsData
                }]);
            } else {
                visitTrendsChart.updateSeries([{
                    name: 'Unique Children',
                    data: uniqueChildrenTrendsData
                }]);
            }
        });
    });

