$(document).ready(function() {
	var all_data = jQuery.parseJSON(data)
	$("#results_btn").attr("href", "/results/" + all_data.meetingID);
	$("#meeting_id").attr("value", all_data.meetingID);
	$("#meeting_name").html(all_data.meetingName)
});