$(document).ready(function(){
    $("#report-link-report2").addClass("active");

    //Report 2 Table 1
    $("#report2-table1").bootstrapTable({
        url: '/api/Report2-Table1',
        pagination: true,
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        search: true,
        columns: [{
                field: 'CategoryName',
                title: 'Category Name'
            },{
                field: 'ProductCount',
                title: 'Product Count'
            },{
                field: 'ManufacturerCount',
                title: 'Manufacturer Count'
            },{
                field: 'AvgRetailPrice',
                title: 'Avg Retail Price'
            }]
    });

});