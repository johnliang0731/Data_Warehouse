$(document).ready(function(){
    $("#report-link-report1").addClass("active");
    
    //Report 1 Table 1
    $("#report1-table1").bootstrapTable({
            url: '/api/Report1-Table1',
            pagination: true,
            pageList: [10, 25, 50, 100],
            pageSize: 10,
            pageNumber: 1,
            search: true,
            columns: [{
                field: 'ManufacturerName',
                title: 'Manufacturer Name'
            }, {
                field: 'ProductCount',
                title: 'Product Count'
            }, {
                field: 'AvgRetailPrice',
                title: 'Avg Retail Price'
            }, {
                field: 'MinRetailPrice',
                title: 'Min Retail Price'
            }, {
                field: 'MaxRetailPrice',
                title: 'Max Retail Price'
            }]
    });
    
    //Manufacturer Name Dropdown
    createManufacturerList('Manufacturer');

    function createManufacturerList(id) {
        var manufacturer_list = '';
        $.getJSON("/api/Report1-ManufacturerList", function(data) {
            manufacturer_list += '<option value="">Select '+ id + '</option>';
            $.each(data, function(key, val) {
                manufacturer_list += '<option value="' + key + '">' + val.manufacturer_name + '</option>';
            });
            $('#report1-manufacturerlist').html(manufacturer_list); 
        });
    }
    
    //hide table 2, view detail button, table 3 by default
    $('#report1-table2').hide();
    $('#report1-viewdetail').hide();
    $('#report1-table3').hide();


    $("#report1-manufacturerlist").change(function(){
        var selected_manufacturer = $(this).children("option:selected").text(); 
        
        selectedManufacturerData = {"selected_manufacturer": selected_manufacturer};

        //show table2 result
        function renderReport1Table2(){
            $.ajax({
                url: "/api/Report1-Table2",  
                type: "GET",
                data: selectedManufacturerData,
                success: function(result){
                    if (result.length == 0){
                        $('#report1-table2').hide();
                        $('#report1-viewdetail').hide();
                        $('#report1-table3').hide();
                    }else{
                        $('#report1-table2').show();
                        $('#report1-table2').bootstrapTable('load', result);
                        $('#report1-viewdetail').show();
                        $('#report1-table3').hide();
                    }
                    
                }, 
                error: function(){
                    alert("ajax post failed");
                }
            });
        }

        renderReport1Table2();
    });

    //show table3 result
    $('#report1-viewdetail').on("click", function(){

        function renderReport1Table3(){
            //return table3 result
            $.ajax({
                url: "/api/Report1-Table3",  
                type: "GET",
                data: selectedManufacturerData,
                success: function(result){
                    if (result.length == 0){
                        $('#report1-table3').hide();
                    }else{
                        $('#report1-table3').show();
                        $('#report1-table3').bootstrapTable('load', result); 
                    }
                }, 
                error: function(){
                    alert("ajax post failed");
                }
            });
        }
        renderReport1Table3();
    });
});


