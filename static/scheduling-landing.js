$(document).ready(function() {
    var all_data = jQuery.parseJSON(data)
    $("#results_btn").attr("href", "/results/" + all_data.meeting_id);
    $("#meeting_id").attr("value", all_data.meeting_id);
});