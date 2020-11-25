$(document).ready(function(){
    $("#report-link-report5").addClass("active");

    //Report 5 Table 1
    $("#report5-table1").bootstrapTable({
        url: '/api/Report5-Table1',
        pagination: true,
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        columns: [
            {
                field: 'Year',
                title: 'Year'
            },
            {
                field: 'totalPerYear',
                title: 'Total Number of Item'
            },{
                field: 'averagePerDay',
                title: 'Average Unit Sold Per Day'
            },{
                field: 'soldOnGroundhogDay',
                title: 'Unit Sold on GroundhogDay'

        }]
    });
});

