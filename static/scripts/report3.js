$(document).ready(function(){
    $("#report-link-report3").addClass("active");

    //Report 3 Table 1
    $("#report3-table1").bootstrapTable({
        url: '/api/Report3-Table1',
        pagination: true,
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        search: true,
        columns: [{
                field: 'ProductID',
                title: 'PID'
            },{
                field: 'ProductName',
                title: 'Product name'
            },{
                field: 'RetailPrice',
                title: 'Retail price'
            },{
                field: 'UnitsEverSold',
                title: 'Total units ever sold'
            },{
                field: 'UnitSoldOnDiscount',
                title: 'Total units sold on discount'
            },{
                field: 'ActualRevenue',
                title: 'Actual Revenue'
            },{
                field: 'PredictedRevenue',
                title: 'Predicted Revenue'
            },{
                field: 'RevenueDiff',
                title: 'Revenue Difference'
            }]
    });

});
