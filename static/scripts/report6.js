$(document).ready(function(){
    $("#report-link-report6").addClass("active");
    $(".row").css("margin-left", "0");

    $("#report6-submit-button").off('click').on("click", function() {
        var year = $("#report6-year-input").val();
        var month = $("#report6-month-input").val();

        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/Report6/view",
            data: JSON.stringify({ year: year, month: month}),
            success: function(data){
                $('#table').bootstrapTable({
                    data: data,
                    pagination: true,
                    pageList: [10, 25, 50, 100],
                    pageSize: 10,
                    pageNumber: 1,
                    showRefresh: true,
                    columns: [{
                      field: 'category_name',
                      title: 'category name'
                    }, {
                      field: 'state',
                      title: 'state'
                    }, {
                      field: 'sold_quantity',
                      title: 'sold quantity'
                    }]
                });
            },
            error: function(data){
                alert(data.responseText);
            },
            dataType: "json"
        });
    });
});