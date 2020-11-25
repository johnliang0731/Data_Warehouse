$(document).ready(function(){
    $("#report-link-report8").addClass("active");
    
    //Report 8 Table 1
    $("#report8-table1").bootstrapTable({
            url: '/api/Report8-Table1',
            pagination: true,
            pageList: [10, 25, 50, 100],
            pageSize: 10,
            pageNumber: 1,
            search: true,
            columns: [{
                field: 'Year',
                title: 'Year'
            }, {
                field: 'CountMemberID',
                title: 'Count Member ID'
            }]
    });
    
    //Year Dropdown
    createYearList('Year');

    function createYearList(id) {
        var year_list = '';
        $.getJSON("/api/Report8-YearList", function(data) {
            year_list += '<option value="">Please select a year and view drill-down details: '+ '</option>';
            $.each(data, function(key, val) {
                year_list += '<option value="' + key + '">' + val.Year + '</option>';
            });
            $('#report8-yearlist').html(year_list); 
        });
    }
    
    //hide table 2, view detail button, table 3 by default
    $('#report8-table2').hide();
    $('#report8-table3').hide();
    $('#report8-table4').hide();


    $("#report8-yearlist").change(function(){
        var selected_year = $(this).children("option:selected").text();
        
        selectedYearData = {"selected_year": selected_year};

        //show table2 result
        function renderReport8Table2(){
            $.ajax({
                url: "/api/Report8-Table2",  
                type: "GET",
                data: selectedYearData,
                success: function(result){
                    if (result.length == 0){
                        $('#report8-table2').hide();
                    }else{
                        $('#report8-table2').show();
                        $('#report8-table2').bootstrapTable('load', result);
                        
                        // Change city cell to red if membership sold is >= 250
                        $('#report8-table2 > tbody > tr').each(function(){
                            var col1_value = $(this).find("td:nth-child(3)").text();
                            if (col1_value > 249) { 
                                $(this).find("td:nth-child(1)").css('background-color','red');
                            }
                        });

                    }
                    
                }, 
                error: function(){
                    alert("ajax post failed");
                }
            });
        }



        function renderReport8Table3(){
            $.ajax({
                url: "/api/Report8-Table3",  
                type: "GET",
                data: selectedYearData,
                success: function(result){
                    if (result.length == 0){
                        $('#report8-table3').hide();
                    }else{
                        $('#report8-table3').show();
                        $('#report8-table3').bootstrapTable('load', result);

                        // Change city cell to yellow if membership sold is <= 30
                        $('#report8-table3 > tbody > tr').each(function(){
                            var col1_value = $(this).find("td:nth-child(3)").text();
                            if (col1_value < 31) { 
                                $(this).find("td:nth-child(1)").css('background-color','yellow');
                            }
                        });

                    }
                    
                }, 
                error: function(){
                    alert("ajax post failed");
                }
            });
        }

        renderReport8Table2();
        renderReport8Table3();
        
        //CityState Dropdown
        createCityStateList(['CityName', 'State']);

        function createCityStateList(id) {
            var citystate_list = '';
            $.getJSON("/api/Report8-CityStateList", function(data) {
                citystate_list += '<option value="">Please select a (city, state) pair and view drill-down details: ' + '</option>';
                $.each(data, function(key, val) {
                    citystate_list += '<option value="' + key + '">' + val.CityName + ', ' +val.State + '</option>';
                });
                $('#report8-citystatelist').html(citystate_list); 
            });
            /*var state_list = '';
            $.getJSON("/api/Report8-StateList", function(data) {
                state_list += '<option value="">Select '+ id[1] + '</option>';
                $.each(data, function(key, val) {
                    state_list += '<option value="' + key + '">' + val.State + '</option>';
                });
                $('#report8-citystatelist').html(state_list); 
            });*/
        }



        $("#report8-citystatelist").change(function(){
            var selected_citystate = $(this).children("option:selected").text();

            selectedYearCityStateData = {"selected_citystate": selected_citystate, "selected_year": selected_year};

            //show table4 result
            function renderReport8Table4(){
                $.ajax({
                    url: "/api/Report8-Table4",  
                    type: "GET",
                    data: selectedYearCityStateData, 
                    success: function(result){
                        if (result.length == 0){
                            $('#report8-table4').hide();
                        }else{
                            $('#report8-table4').show();
                            $('#report8-table4').bootstrapTable('load', result);
                        }

                    }, 
                    error: function(){
                        alert("ajax post failed");
                    }
                });
            }

            renderReport8Table4();

        });

    });
    
    

    //show table3 result
   /* $('#report1-viewdetail').on("click", function(){

        function renderReport1Table3(){
            //return table3 result
            $.ajax({
                url: "/api/Report8-Table3",  
                type: "GET",
                data: selectedManufacturerData,
                success: function(result){
                    if (result.length == 0){
                        $('#report8-table3').hide();
                    }else{
                        $('#report8-table3').show();
                        $('#report8-table3').bootstrapTable('load', result); 
                    }
                }, 
                error: function(){
                    alert("ajax post failed");
                }
            });
        }
        renderReport1Table3();
    });*/
});



