////function getCssValuePrefix() {
////    'use strict'

////    var retuenValue = ''; //default to standard syntax
////    var prefixes = ['-o-', '-ms-', '-moz-', '-webkit-'];

////    // Create a temporary DOM object for testing
////    var dom = document.createElement('div');

////    for (var i = 0; i < prefixes.length; i++) {
////        // Attempt to set the style
////        dom.style.background = prefixes[i] + 'linear-gradient(#ffffff, #000000)';

////        // Detect if the style was successfully set
////        if (dom.style.background) {
////            retuenValue = prefixes[i];
////        }
////    }

////    dom = null;
////    dom.remove();

////    return retuenValue;
////}

function index() {
    'use strict'

    // TRANSACTIONS
    var myCanvas = document.getElementById("transactions");
    myCanvas.height = "330";

    var myCanvasContext = myCanvas.getContext("2d");
    var gradientStroke1 = myCanvasContext.createLinearGradient(0, 80, 0, 280);
    gradientStroke1.addColorStop(0, hexToRgba(myVarVal, 0.8) || 'rgba(32, 128, 176, 0.8)');
    gradientStroke1.addColorStop(1, hexToRgba(myVarVal, 0.2) || 'rgba(32, 128, 176, 0.2) ');

    var gradientStroke2 = myCanvasContext.createLinearGradient(0, 80, 0, 280);
    gradientStroke2.addColorStop(0, hexToRgba(myVarVal1, 0.8) || 'rgba(5, 195, 251, 0.8)');
    gradientStroke2.addColorStop(1, hexToRgba(myVarVal1, 0.8) || 'rgba(5, 195, 251, 0.2) ');

    var gradientStroke3 = myCanvasContext.createLinearGradient(0, 80, 0, 280);
    gradientStroke3.addColorStop(0, hexToRgba(myVarVal, 0.8) || 'rgba(32, 128, 176, 0.8)');
    gradientStroke3.addColorStop(1, hexToRgba(myVarVal, 0.2) || 'rgba(32, 128, 176, 0.2) ');

    document.getElementById('transactions').innerHTML = ''; 
    var myChart;
    myChart = new Chart(myCanvas, {

        type: 'line',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"],
            type: 'line',
            datasets: [{
                label: 'Total Sales',
                data: [100, 210, 180, 454, 454, 230, 230, 656, 656, 350, 350, 600],
                backgroundColor: gradientStroke1,
                borderColor: myVarVal,
                pointBackgroundColor: '#fff',
                pointHoverBackgroundColor: gradientStroke1,
                pointBorderColor: myVarVal,
                pointHoverBorderColor: gradientStroke1,
                pointBorderWidth: 0,
                pointRadius: 0,
                pointHoverRadius: 0,
                borderWidth: 2,
                fill: 'origin'
            }, {
                label: 'Total Orders',
                data: [300, 410, 380, 654, 654, 430, 430, 856, 856, 550, 550, 800],
                //data: [200, 530, 110, 110, 480, 520, 990, 435, 475, 738, 454, 800],
                backgroundColor: 'transparent',
                borderColor: '#2080b0',
                pointBackgroundColor: '#fff',
                pointHoverBackgroundColor: gradientStroke2,
                pointBorderColor: '#05c3fb',
                pointHoverBorderColor: gradientStroke2,
                pointBorderWidth: 0,
                pointRadius: 0,
                pointHoverRadius: 0,
                borderWidth: 1,
                fill: 'origin',

                }, {
                    label: 'Total Orders',
                    //data: [400, 450, 450, 756, 756, 500, 500, 554, 554, 280, 310, 200],
                    data: [200, 310, 280, 554, 554, 330, 330, 756, 756, 450, 450, 700],
                    backgroundColor: gradientStroke1,
                    borderColor: myVarVal,
                    pointBackgroundColor: '#fff',
                    pointHoverBackgroundColor: gradientStroke1,
                    pointBorderColor: myVarVal,
                    pointHoverBorderColor: gradientStroke1,
                    pointBorderWidth: 0,
                    pointRadius: 0,
                    pointHoverRadius: 0,
                    borderWidth: 2,
                    fill: 'origin',

                }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            tooltips: {
                enabled: false,
            },
            legend: {
                display: false,
                labels: {
                    usePointStyle: false,
                },
            },
            scales: {
                xAxes: [{
                    display: true,
                    gridLines: {
                        display: false,
                        drawBorder: false,
                        color: 'rgba(119, 119, 142, 0.08)'
                    },
                    ticks: {
                        fontColor: '#333333',
                        autoSkip: true,
                    },
                    scaleLabel: {
                        display: false,
                        labelString: 'Month',
                        fontColor: '#dddddd'
                    }
                }],
                yAxes: [{
                    ticks: {
                        min: 0,
                        max: 1050,
                        stepSize: 150,
                        fontColor: "#333333",
                    },
                    display: true,
                    gridLines: {
                        display: true,
                        drawBorder: false,
                        zeroLineColor: 'rgba(142, 156, 173,0.1)',
                        color: "rgba(142, 156, 173,0.1)",
                    },
                    scaleLabel: {
                        display: false,
                        labelString: 'sales',
                        fontColor: 'transparent'
                    }
                }]
            },
            title: {
                display: false,
                text: 'Normal Legend'
            }
        }
    });
}

$(function () {
    "use strict";
    var ctx = document.getElementById("chartArea");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"],
            datasets: [{
                label: "Data1",
                borderColor: "#6c5ffc",
                borderWidth: "3",
                backgroundColor: "rgba(108, 95, 252, .1)",
                data: [22, 44, 67, 43, 76, 45, 12, 22, 44, 67, 43, 76]
            }, {
                label: "Data2",
                borderColor: "rgba(32, 128, 176 ,0.9)",
                borderWidth: "3",
                backgroundColor: "rgba(	32, 128, 176, 0.7)",
                pointHighlightStroke: "rgba(5, 195, 251 ,1)",
                data: [22, 44, 67, 43, 76, 45, 12, 22, 44, 67, 43, 76]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            tooltips: {
                mode: 'index',
                intersect: false
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    ticks: {
                        fontColor: "#9ba6b5",
                    },
                    gridLines: {
                        color: 'rgba(119, 119, 142, 0.2)'
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        fontColor: "#9ba6b5",
                    },
                    gridLines: {
                        color: 'rgba(32, 128, 176, 0.2)'
                    },
                }]
            },
            legend: {
                labels: {
                    fontColor: "#9ba6b5"
                },
            },
        }
    });

    var ctx = document.getElementById("chartBar1").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
            datasets: [{
                label: 'Sales',
                data: [200, 450, 290, 367, 256, 543, 345, 290, 367],
                borderWidth: 2,
                backgroundColor: '#2080b2',
                borderColor: '#2080b2',
                borderWidth: 2.0,
                pointBackgroundColor: '#ffffff',

            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: true
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        stepSize: 150,
                        fontColor: "#9ba6b5",
                    },
                    gridLines: {
                        color: 'rgba(119, 119, 142, 0.2)'
                    }
                }],
                xAxes: [{
                    barPercentage: 0.4,
                    barValueSpacing: 0,
                    barDatasetSpacing: 0,
                    barRadius: 0,
                    ticks: {
                        display: true,
                        fontColor: "#9ba6b5",
                    },
                    gridLines: {
                        display: false,
                        color: 'rgba(119, 119, 142, 0.2)'
                    }
                }]
            },
            legend: {
                labels: {
                    fontColor: "#9ba6b5"
                },
            },
        }
    });
});

//(function ($) {
//    "use strict";

//    const ps = new PerfectScrollbar('.app-sidebar', {
//        useBothWheelAxes: true,
//        suppressScrollX: true,
//        suppressScrollY: false,
//    });
//    //const ps1 = new PerfectScrollbar('.header-dropdown-list', {
//    //    useBothWheelAxes: true,
//    //    suppressScrollX: true,
//    //    suppressScrollY: false,
//    //});
//    //const ps2 = new PerfectScrollbar('.notifications-menu', {
//    //    useBothWheelAxes: true,
//    //    suppressScrollX: true,
//    //    suppressScrollY: false,
//    //});
//    //const ps3 = new PerfectScrollbar('.message-menu-scroll', {
//    //    useBothWheelAxes: true,
//    //    suppressScrollX: true,
//    //    suppressScrollY: false,
//    //});

//    //P-scrolling
//})(jQuery);