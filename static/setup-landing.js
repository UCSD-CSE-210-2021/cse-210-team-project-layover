// This file will contain any javascript computation that we need for the setup-landing html page
// It is here where we will grab the setup information to inform what our scheduling will be:
//     in-person, remote, both; fixed dates, general week; etc.

// Runs right when page is accessed
$(document).ready(function() {

    // Toggle hide/show div for start/end date
    $("#general_week").click(function() {
        $("#start_date_div").addClass("hideDiv");
        $("#end_date_div").addClass("hideDiv");
    });

    // Toggle hide/show div for start/end date
    $("#specific_date").click(function() {
        $("#start_date_div").removeClass("hideDiv");
        $("#end_date_div").removeClass("hideDiv");
    });

    // Get today's date, set min value of start/end date to today
    var now = new Date();
    var dd = ("0" + now.getDate()).slice(-2);
    var mm = ("0" + (now.getMonth() + 1)).slice(-2);
    var yyyy = now.getFullYear();
    var today = yyyy + "-" + (mm) + "-" + (dd);

    $("#start_date").attr("min", today);
    $("#end_date").attr("min", today);

    // Change min/max values for start/end dates depending date change
    $("#start_date").change(function(){
        $("#end_date").attr("min", $("#start_date").val());
    });
    $("#end_date").change(function(){
        $("#start_date").attr("max", $("#end_date").val());
    });

});