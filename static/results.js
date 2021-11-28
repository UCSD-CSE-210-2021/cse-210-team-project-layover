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

	// Uncomment this
	var inPersonResultTable = all_data.compiled_inperson;
	var virtualResultTable = all_data.compiled_virtual;
	var currTable = true; // true for in-person. false for virtual
	var meetingType = all_data.meeting_info.meeting_type;
	var startTime = all_data.meeting_info.day_start_time;
	var endTime = all_data.meeting_info.day_end_time;
	var bestTimesInPerson = all_data.best_times_inperson;
	var bestTimesIdxInPerson = all_data.best_times_idx_inperson;
	var bestTimesVirtual = all_data.best_times_virtual;
	var bestTimesIdxVirtual = all_data.best_times_idx_virtual;
	var usersMeetingInfo = all_data.meeting_info.users;
	
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
		$('#sched-results').append(buildTableHTML(startTime, endTime));
		colorTable(inPersonResultTable);
		highlightBestTimes(inPersonResultTable, bestTimesIdxInPerson);
		$("#best-times").html(buildRecommendationList(bestTimesInPerson));
	}else{
		$('#sched-results').append(buildTableHTML(startTime, endTime));
		colorTable(virtualResultTable);
		highlightBestTimes(virtualResultTable, bestTimesIdxVirtual);
		$("#best-times").html(buildRecommendationList(bestTimesVirtual));
	}

	function mimic_rgba(r, g, b, a){
		var bg_rgb = [255, 255, 255];

		if (a > 0){
			return "rgb(" + (r * a + bg_rgb[0] * (1 - a)) + ", " + (g * a + bg_rgb[1] * (1 - a)) + ", " + (b * a + bg_rgb[2] * (1 - a)) + ")"; 
		}
		else{
			return "rgb(222, 222, 222)";
		}
	}

	function colorTable(availability){
		for(var i = 0 ; i < availability.length ; i++){
			for(var j = 0 ; j < availability[0].length ; j++){
				var currId = i * availability[0].length + j;
				var cellVal = availability[i][j];

				if(currTable){
					// var color = "rgba(255, 124, 10, " + cellVal + ")";
					var color = mimic_rgba(255, 124, 10, cellVal**0.8);
				} 
				else{
					// var color = "rgba(0, 142, 224, " + cellVal + ")";
					var color = mimic_rgba(0, 142, 224, cellVal);
				}

				$("#"+currId).css('background-color', color);
			}
		}
	}
	
	function highlightBestTimes(availability, bestTimesIdxList){
		for(var i = 0 ; i < bestTimesIdxList.length ; i++){
			var col = bestTimesIdxList[i][0];
			var row = bestTimesIdxList[i][1];
			var currId = row * availability[0].length + col;
			// var color = "rgb(69, 240, 100)";
			if(currTable){
				var color = "rgb(228, 92, 58)";
			} 
			else{
				var color = "rgb(19, 64, 116)";
			}
			// console.log(currId);
			$("#"+currId).css('background-color', color);
			$("#"+currId).css('box-shadow', '0 0 0 1px #24272B');
		}
	}

	$("#change_table").click(changeTableData);

	function changeTableData(){
		// Remove current HTML table
		$('#tableSchedule').remove();

		// Locate participant of interest
		let allEmails = $('#users-list > ul > li')
		let displayEmail = undefined
		// Ref: https://stackoverflow.com/questions/10877903/check-if-text-in-cell-is-bold
		for(let i = 0; i < allEmails.length; i++){
			let currentEmail = allEmails[i]
			if(currentEmail.firstChild.nodeName === 'b' || currentEmail.firstChild.nodeName === 'B'){
				displayEmail = currentEmail.innerText
			}
		}

		// Toggle in-person and virtual availability
		currTable = !currTable;

		// Check displayed email
		if (displayEmail === 'Show All') { // show combined results
			if(currTable){
				$('#sched-results').append(buildTableHTML(startTime, endTime));
				$("#best-times").html(buildRecommendationList(bestTimesInPerson));
				colorTable(inPersonResultTable);
				highlightBestTimes(inPersonResultTable, bestTimesIdxInPerson);
				$('#change_table').html("Click to go to virtual availability");
				$("#curr_table_type").html("Current table: in-person availability");
			}else{
				$('#sched-results').append(buildTableHTML(startTime, endTime));
				$("#best-times").html(buildRecommendationList(bestTimesVirtual));
				colorTable(virtualResultTable);
				highlightBestTimes(virtualResultTable, bestTimesIdxVirtual);
				$('#change_table').html("Click to go to in-person availability");
				$("#curr_table_type").html("Current table: virtual availability");
			}
		} else { // show specific user
			if(currTable){
				$('#sched-results').append(buildTableHTML(startTime, endTime));
				$("#best-times").html(buildRecommendationList(bestTimesInPerson));
				colorTable(usersMeetingInfo[displayEmail].inPersonAvailability);
				$('#change_table').html("Click to go to virtual availability");
				$("#curr_table_type").html("Current table: in-person availability of <b>" + displayEmail + "</b>");
			}else{
				$('#sched-results').append(buildTableHTML(startTime, endTime));
				$("#best-times").html(buildRecommendationList(bestTimesVirtual));
				colorTable(usersMeetingInfo[displayEmail].virtualAvailability);
				$('#change_table').html("Click to go to in-person availability");
				$("#curr_table_type").html("Current table: virtual availability of <b>" + displayEmail + "</b>");
			}
		}

		// Hacky way to reformat time when re-rendered
		let currentTimeFormat = $('#timeFormatSelector > label > input:checked')[0].parentElement.innerText.trim()
		if (currentTimeFormat === '12-hour') {
			reformatTimeDisplay('12h')
		} else {
			reformatTimeDisplay('24h')
		}
	}


	var fullList = "<ul>"
	fullList += "<li style='cursor: pointer;' onclick='changeBoldEmail(\"Show All\")'><b>Show All</b></li>"
	$.each(all_data.meeting_info.users, function(i, value){     // Iterate through users
		fullList += "<li style='cursor: pointer;' onclick='changeBoldEmail(\"" + i + "\")'>" + i + "</li>"                        // End list for individual user
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