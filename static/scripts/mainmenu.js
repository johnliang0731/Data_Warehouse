
$(document).ready(function(){
  $('#table').bootstrapTable();
  $('#sub-table').bootstrapTable();
  $('#table').hide();
  $('#sub-table').hide();
  $("#report-link-main-menu-button").addClass("active");
  $("#main-menu-dropdown-container").css("display", "block");


  $("#report-link-stores").off('click').on("click", function() {
    activateNavLink($(this));
    $('#table').show();
    $('#city-population-section').hide();
    $('#table').bootstrapTable('refreshOptions', {
        url: '/Stores',
        type: "GET",
        pagination: true,
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        columns: [{
            field: 'store_number',
            title: 'Store Number'
        }, {
            field: 'phone_number',
            title: 'Phone Number'
        }, {
            field: 'street_address',
            title: 'Street Address'
        }, {
            field: 'city_name',
            title: 'City Name'
        }, {
            field: 'state',
            title: 'State'
        }]
    });

    $('#sub-table').show();
    $('#sub-table').bootstrapTable('refreshOptions', {
        url: '/Stores_Count',
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        columns: [{
            field: 'count_store',
            title: 'Total Number of Stores'
        }]
    });
  });

  $("#report-link-manufacturers").off('click').on("click", function() {
    activateNavLink($(this));
    $('#table').show();
    $('#city-population-section').hide();
    $('#table').bootstrapTable('refreshOptions',{
        url: '/Manufacturer',
        type: "GET",
        pagination: true,
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        search: true,
        columns: [{
            field: 'manufacturer_name',
            title: 'Manufacturer Name'
        }, {
            field: 'max_discount',
            title: 'Max Discount'
        }]
      });

    $('#sub-table').show();
    $('#sub-table').bootstrapTable('refreshOptions', {
        url: '/Manufacturer_Count',
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        columns: [{
            field: 'count_manufacturer',
            title: 'Total Number of Manufacturers'
        }]
      });
  });
  $("#report-link-products").off('click').on("click", function() {
    activateNavLink($(this));
    $('#table').show();
    $('#city-population-section').hide();
    $('#table').bootstrapTable('refreshOptions', {
      url: '/Product',
      pagination: true,
      pageList: [10, 25, 50, 100],
      pageSize: 10,
      pageNumber: 1,
      search: true,
      columns: [{
          field: 'PID',
          title: 'PID'
      }, {
          field: 'product_name',
          title: 'product name'
      }, {
          field: 'retail_price',
          title: 'retail price'
      }]      
    });

    $('#sub-table').show();
    $('#sub-table').bootstrapTable('refreshOptions', {
        url: '/Product_Count',
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        columns: [{
            field: 'count_product',
            title: 'Total Number of Products'
        }]
      });
  }); 

  $("#report-link-memberships-sold").off('click').on("click", function() {
    activateNavLink($(this));
    $('#city-population-section').hide();
    $('#table').show();
    $('#table').bootstrapTable('refreshOptions', {
      url: '/MembershipsSold',
      pagination: true,
      pageList: [10, 25, 50, 100],
      pageSize: 10,
      pageNumber: 1,
      search: true,
      columns: [{
          field: 'MemberID',
          title: 'Membership ID'
      }, {
          field: 'SignupDate',
          title: 'Signup Date'
      }]      
    });

    $('#sub-table').show();
    $('#sub-table').bootstrapTable('refreshOptions', {
        url: '/Membership_Count',
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        columns: [{
            field: 'count_membership',
            title: 'Total Number of Membership'
        }]
      });
  }); 

  $("#report-link-view-holiday").off('click').on("click", function() {
    activateNavLink($(this));
    $(".row").css("margin-left", "0");
    $("#holiday-management-container").removeClass("hidden");
    $('#table').show();
    $('#sub-table').hide();
    $('#city-population-section').hide();
    $('#table').bootstrapTable('refreshOptions', {
        url: '/Holiday',
        type: "GET",
        pagination: true,
        pageList: [10, 25, 50, 100],
        pageSize: 10,
        pageNumber: 1,
        showRefresh: true,
        columns: [{
            field: 'date_time',
            title: 'date'
        }, {
            field: 'holiday_name',
            title: 'holiday name'
        }]
    });
    $("#holiday-management-container").show();
  });

  $("#add-holiday-button").off('click').on("click", function() {
    var year = $("#holiday-year-input").val();
    var month = $("#holiday-month-input").val();
    var day = $("#holiday-day-input").val();
    var holiday_name = $("#holiday-name-input").val();
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/Holiday",
      data: JSON.stringify({ year: year, month: month, day: day, holiday_name: holiday_name, mode: "add"}),
      success: function(data){
        $("#table").bootstrapTable("refresh");
      },
      error: function(data){
        alert(data.responseText);
      },
      dataType: "json"
    });
  });

  $("#update-holiday-button").off('click').on("click", function() {
    var year = $("#holiday-year-input").val();
    var month = $("#holiday-month-input").val();
    var day = $("#holiday-day-input").val();
    var holiday_name = $("#holiday-name-input").val();
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/Holiday",
      data: JSON.stringify({ year: year, month: month, day: day, holiday_name: holiday_name, mode: "update"}),
      success: function(data){
        $("#table").bootstrapTable("refresh");
      },
      error: function(data){
        alert(data.responseText);
      },
      dataType: "json"
    });
  });

  $("#delete-holiday-button").off('click').on("click", function() {
    var year = $("#holiday-year-input").val();
    var month = $("#holiday-month-input").val();
    var day = $("#holiday-day-input").val();
    var holiday_name = $("#holiday-name-input").val();
    $.ajax({
      type: "POST",
      contentType: "application/json; charset=utf-8",
      url: "/Holiday",
      data: JSON.stringify({ year: year, month: month, day: day, holiday_name: holiday_name, mode: "delete"}),
      success: function(data){
        $("#table").bootstrapTable("refresh");
      },
      error: function(data){
        alert(data.responseText);
      },
      dataType: "json"
    });
  });


  // City Population Page
  $("#report-link-population").off('click').on("click", function() {
    activateNavLink($(this));
    $("#city-population-section").removeClass("hidden");
    $('#table').show();
    $("#city-population-section").removeClass("hidden");
    $("#city-population-section").show();
    $('#sub-table').hide();
    $('#table').bootstrapTable('refreshOptions', {
      url: '/api/City-Info',
      pagination: true,
      pageList: [10, 25, 50, 100],
      pageSize: 10,
      pageNumber: 1,
      search: true,
      columns: [{
          field: 'city_name',
          title: 'City'
      }, {
          field: 'state',
          title: 'State'
      }, {
          field: 'population',
          title: 'Population'
      }]      
    }); 

    // Create city,state list for selection
    createCityList('City');
    function createCityList(id) {
      var city_list = '';
      $.getJSON("/api/City-CityList", function(data) {
        city_list += '<option value="000">Select City,State</option>';
        $.each(data, function(key, val) {
          city_list += '<option value="' + val.state + '">' + val.city_name + ',' + val.state + '</option>';
        });
        $('#city-citySelectLIst').html(city_list); 
      });
    }

    // Send city,state,population data to app.py to update database
    $("#change-population-button").off('click').on("click", function() {
      var selected_state = $('#city-citySelectLIst').find("option:selected").text();
      var str = selected_state.split(",");
      var selectedCity = str[0]
      var selectedState = str[1]
      var InputPopulation = $("#inputPopulation").val();
      $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/api/Update-City-Population",
        data: JSON.stringify({ selectedState: selectedState, selectedCity: selectedCity, InputPopulation: InputPopulation}),
        success: function(data){
          $('#table').bootstrapTable("refresh");
        },
        error: function(data){
          alert(data.responseText);
        },
        dataType: "json"
      });
    });
  });


  function activateNavLink(nav_link) {
    $("a[id *= report-link]").removeClass("active");
    nav_link.addClass("active");
    $("#dashboard-name").text(nav_link.text());
    $("#holiday-management-container").addClass("hidden");
    $("#city-population-section").addClass("hidden");
    $("input").val("");
  }
});
