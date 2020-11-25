$(document).ready(function(){
    $("#report-link-report7").addClass("active");

    //Report 7 Table 1
    $("#report7-table1").bootstrapTable({
        url: '/api/Report7-Table1',
        pagination: true,
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        search: true,
        columns: [{
                field: 'CityCategory',
                title: 'City Category'
            },{
                field: 'Year',
                title: 'Year'
            },{
                field: 'Revenue',
                title: 'Avg Revenue'
            }]
    });

});
