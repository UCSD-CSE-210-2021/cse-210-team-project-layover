// This file will contain any javascript computation that we need for the setup-landing html page
// It is here where we will grab the setup information to inform what our scheduling will be:
//     in-person, remote, both; fixed dates, general week; etc.

// Runs right when page is accessed
$(document).ready(function() {

    // Toggle hide/show div for start/end date
    $("#general_week").click(function() {
        $("#start_date_div").addClass("hideDiv");
        $("#end_date_div").addClass("hideDiv");
        $("#start_date").attr("required", false);
        $("#end_date").attr("required", false);
    });

    // Toggle hide/show div for start/end date
    $("#specific_date").click(function() {
        $("#start_date_div").removeClass("hideDiv");
        $("#end_date_div").removeClass("hideDiv");
        $("#start_date").attr("required", true);
        $("#end_date").attr("required", true);
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

});