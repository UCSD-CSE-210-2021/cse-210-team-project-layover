var setupStartEndTimes = function(){
	var startTime = $("<select id='start_time' class='form-control' name='start_time'>")
	var endTime = $("<select id='end_time' class='form-control' name='end_time'>")
	var i = 0;
	for (i; i < 24; i++){
		var AMPM = i <= 11 ? "am" : "pm";

		// Setup display time
		var displayTime;
		if (i == 0){ displayTime = 12; }
		else if (i >= 13){ displayTime = i - 12; }
		else{ displayTime = i; }

		// Create options and add to appropriate selects
		var startTimeOption = $("<option value='" + i + "'>" + displayTime + ":00 " + AMPM + "</option>")
		var endTimeOption = $("<option value='" + i + "'>" + displayTime + ":00 " + AMPM + "</option>")
		startTime.append(startTimeOption);
		endTime.append(endTimeOption);
	}
	startTime.val(8)    // Set start value to 8am
	endTime.val(18)     // Set end value at 6pm
	$("#start_time_container").append(startTime);
	$("#end_time_container").append(endTime);
}

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

	setupStartEndTimes();

	// Disallow end time before start time
	$("#start_time").on("change", function(){
		var i = $(this).val();
		var myEndTime = $("#end_time");
		myEndTime.empty();
		for(i; i < 24; i++){
			var AMPM = i <= 11 ? "am" : "pm";
			var displayTime;

			if (i == 0){ displayTime = 12; }
			else if (i >= 13){ displayTime = i - 12; }
			else{ displayTime = i; }

			var endTimeOption = $("<option value='" + i + "'>" + displayTime + ":00 " + AMPM + "</option>")
			myEndTime.append(endTimeOption);
		}
		var setEndTime = $(this).val() == 23 ? 23 : parseInt($(this).val()) + 1;
		myEndTime.val(setEndTime);
	})

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