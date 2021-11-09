$(document).ready(function() {
	var all_data = jQuery.parseJSON(data);                  // Read in data
	$("#meeting_name").html(all_data.meeting_info.name + " Results")     // Write the heading dynamically

	// TODO: Use data to calculate table to display
	// var fullList = "<ul>"
	// $.each(all_data.meeting_info.users, function(i, value){              // Iterate through users
	// 	fullList += "<li>" + i + "<ul>";                    // Create top level list and nested list
	// 	$.each(value, function(j, v){                       // Iterate through user details
	// 		fullList += "<li>" + j + " = " + v + "</li>"    // Populate nested list results
	// 	})
	// 	fullList += "</ul></li>"                            // End list for individual user
	// });
	// fullList += "</ul>"                                     // End list for all users
	// $("#topDiv").html(fullList)                             // Display list in topDiv id from HTML file

	console.log(all_data);

	// Uncomment this
	var inPersonResultTable = all_data.compiled_inperson;
	var virtualResultTable = all_data.compiled_virtual;
	var currTable = true; // true for in-person. false for virtual
	var meetingType = all_data.meeting_info.meeting_type;
	var bestTimesInPerson = all_data.best_times_inperson
	var bestTimesVirtual = all_data.best_times_virtual
	if(meetingType === "remote"){
		$("#curr_table_type").html("Current table: virtual availability")
		currTable = false;
	}

	if(meetingType !== "either"){
		$('#change_table_div').hide()
	}

	// Must be after variable initialization
	// Determines which table should be rendered
	if(currTable){
		$('#sched-results').append(buildTableHTML(inPersonResultTable));
		colorTable(inPersonResultTable);
		$("#best-times").html(buildRecommendationList(bestTimesInPerson));
		// Binds jquery clickable function to clickable class
		// registerClickable(inPersonMeetingTable);
	}else{
		$('#sched-results').append(buildTableHTML(virtualResultTable));
		colorTable(virtualResultTable);
		$("#best-times").html(buildRecommendationList(bestTimesVirtual));
		// Binds jquery clickable function to clickable class
		// registerClickable(virtualMeetingTable);
	}


	function colorTable(availability){
		for(var i = 0 ; i < availability.length ; i++){
			for(var j = 0 ; j < availability[0].length ; j++){
				var currId = i * availability[0].length + j;
				var cellVal = availability[i][j];
				var color = color = "rgba(101, 236, 89, " + cellVal + ")";
				$("#"+currId).css('background-color', color)
			}
		}
	}

	$("#change_table").click(function(){
		// Remove current HTML table
		$('#tableSchedule').remove();
		currTable = !currTable;
		if(currTable){
			$('#sched-results').append(buildTableHTML(inPersonResultTable));
			$("#best-times").html(buildRecommendationList(bestTimesInPerson));
			colorTable(inPersonResultTable);
			$('#change_table').html("Click to go to virtual availability");
			$("#curr_table_type").html("Current table: in-person availability");
		}else{
			$('#sched-results').append(buildTableHTML(virtualResultTable));
			$("#best-times").html(buildRecommendationList(bestTimesVirtual));
			colorTable(virtualResultTable);
			$('#change_table').html("Click to go to in-person availability");
			$("#curr_table_type").html("Current table: virtual availability");
		}
	});


	var fullList = "<ul>"
	$.each(all_data.meeting_info.users, function(i, value){     // Iterate through users
		fullList += "<li>" + i + "</li>"                        // End list for individual user
	});
	fullList += "</ul>"                                     	// End list for all users

	$("#users-list").html(fullList)                             // Display list of users

	function buildRecommendationList(recommendationList){
    // Display list of Top 5 best times
		var bestTimes = "<ul>"
		$.each(recommendationList, function(i, value){
			bestTimes += "<li>" + value + "</li>"
		})
		bestTimes += "</ul>"
		return bestTimes;
	}

	//Link to Meeting
	$("#meetingId").html($(location).attr('href').split('/').slice(0,-2).join('/') + "/meeting/" + all_data.meeting_info.meeting_id);
	
	//Functionality to copy meeting ID on click
	$('#copyBtn').click(function(){
		navigator.clipboard.writeText($("#meetingId").text()).then(function () {
			alert('It worked! Do a CTRL - V to paste')
		}, function () {
			alert('Failure to copy. Check permissions for clipboard')
		});
	});	

	//Link to first's users (for now) editing page
	$('#editingPage').click(function(){
		window.location.href = document.referrer;
	  });
});