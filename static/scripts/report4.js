$(document).ready(function(){
    $("#report-link-report4").addClass("active");
    //Manufacturer Name Dropdown
    createStateList('State');

    function createStateList(id) {
        var state_list = '';
        $.getJSON("/api/Report4-StateList", function(data) {
            state_list += '<option value="">Select '+ id + '</option>';
            $.each(data, function(key, val) {
                state_list += '<option value="' + key + '">' + val.state + '</option>';
            });
            $('#report4-statelist').html(state_list);
        });
    }

    //hide table 2, view detail button, table 3 by default
    $('#report4-table2').hide();
    $("#report4-statelist").change(function(){
        var selected_state = $(this).children("option:selected").text();
        selectedStateData = {"selected_state": selected_state};

        //show table2 result
        function renderReport4Table2(){
            $.ajax({
                url: "/api/Report4-Table2",
                type: "GET",
                data: selectedStateData,
                success: function(result){
                    if (result.length == 0){
                        $('#report4-table2').hide();
                    }else{
                        $('#report4-table2').show();
                        $('#report4-table2').bootstrapTable('load', result);
                    }
                },
                error: function(){
                    alert("ajax post failed");
                }
            });
        }

        renderReport4Table2();
    });

});
