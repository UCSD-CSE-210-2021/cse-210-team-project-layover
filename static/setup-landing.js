// This file will contain any javascript computation that we need for the setup-landing html page
// It is here where we will grab the setup information to inform what our scheduling will be:
//     in-person, remote, both; fixed dates, general week; etc.
$(document).ready(function() {
    $("#general_week").click(function() {
        $("#start_date_div").addClass("hideDiv");
        $("#end_date_div").addClass("hideDiv");
    });

    $("#specific_date").click(function() {
        $("#start_date_div").removeClass("hideDiv");
        $("#end_date_div").removeClass("hideDiv");
    });
})