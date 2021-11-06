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

	const numCol = 8;
	const numTimes = 16;

	// Uncomment this
	var inPersonResultTable = all_data.compiled_avail;
	// var virtualResultTable = all_data.virtualResult;
	var currTable = true; // true for in-person. false for virtual
	var meetingType = all_data.meeting_info.meeting_type;
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
		// Binds jquery clickable function to clickable class
		// registerClickable(inPersonMeetingTable);
	}else{
		$('#sched-results').append(buildTableHTML(virtualMeetingTable));
		// Binds jquery clickable function to clickable class
		// registerClickable(virtualMeetingTable);
	}

	// Builds HTML table using the table Structure
	function buildTableHTML(availability){
	
		var currTime = new Date('December 17, 1995 7:00:00');
		var currCellId = 0;
		// Initialize backend data structure to store times. Fill with 0's
		// inPersonMeetingTable = Array(numTimes * 4).fill().map(() => Array(numCol - 1).fill(0));
		var table = '<table id=tableSchedule>';

		table += [
			"<tr>",
			"  <th></th> <th>Sunday</th> <th>Monday</th> <th>Tuesday</th>",
			"  <th>Wednesday</th> <th>Thursday</th> <th>Friday</th> <th>Saturday</th>",
			"</tr> "
		].join("\n")

		var i = 0; // Tracks the current row we're on

		// Loop through all the times we want
		for(var aTime = 0 ; aTime < numTimes ; aTime++){
			// append time or blank cell
			table += "<tr>"
			table += createTimeCell(currTime)
			// append remaining cells
			for(var j = 0 ; j < availability[0].length ; j++){
				table += createBlankCellWithId(currCellId, availability[i][j]);
				currCellId++;
			}
			i++;

			table += "</tr>"

			// Create three rows of empty cells below time cell
			for(var numSlots = 0 ; numSlots < 3 ; numSlots++){
				table += "<tr>"
				table += createBlankCellWithoutId()

				// append remaining rows
				for(var j = 0 ; j < availability[0].length ; j++){
					table += createBlankCellWithId(currCellId, availability[i][j]);
					currCellId++;
				}
				i++;
				table += "</tr>"
			}
		}
		table += '</table>'
		return table

	}

	// $("#sched-results").html(result) 

	var currTime = new Date('December 17, 1995 7:00:00');
	var currCellId = 0;
	var result = '<table id=tableSchedule>';

	result += [
		"<tr>",
		"  <th></th> <th>Sunday</th> <th>Monday</th> <th>Tuesday</th>",
		"  <th>Wednesday</th> <th>Thursday</th> <th>Friday</th> <th>Saturday</th>",
		"</tr> "
	].join("\n")

	var i = 0; // Tracks the current row we're on

	// Loop through all the times we want
	for(var aTime = 0 ; aTime < numTimes ; aTime++){
		// append time or blank cell
		result += "<tr>"
		result += createTimeCell(currTime)
		// append remaining cells
		for(var j = 0 ; j < all_data.compiled_avail[0].length ; j++){
			result += createBlankCellWithId(currCellId, all_data.compiled_avail[i][j]);
			currCellId++;
		}
		i++;

		result += "</tr>"

		// Create three rows of empty cells below time cell
		for(var numSlots = 0 ; numSlots < 3 ; numSlots++){
			result += "<tr>"
			result += createBlankCellWithoutId()

			// append remaining rows
			for(var j = 0 ; j < all_data.compiled_avail[0].length ; j++){
				result += createBlankCellWithId(currCellId, all_data.compiled_avail[i][j]);
				// console.log(result); 
				// console.log("tagg is: " + '#'+currCellId)
				// $('#'+currCellId).css('background-color', 'black');
				// $('#10').css('background-color', 'red');
				currCellId++;
			}
			i++;
			result += "</tr>"
		}
	}

	result += '</table>'

	function createBlankCellWithId(currCellId, cellVal){

		ret = "<td id=" + currCellId + " class=clickable bgcolor=" ;
		// ret = "<td id=" + currCellId;
		if(cellVal === 0){
			ret += "white";
		}else if( cellVal === 0.75){
			ret += "#F4F569";
			// ret += "rgba(101, 236, 89, 0.5)"
		}else{
			ret += "#65EC59";
			// console.log("run")
			// ret += "rgb(0,0,0)";
		}
		// #\30 
		ret += "><br></td>";
		console.log(ret)
		return ret
	}

	function createBlankCellWithoutId(){
		ret = "<td><br></td>";
		return ret
	}

	function createTimeCell(currTime){
		ret = "<td>" + currTime.getHours() + ":00</td>";
		currTime.setHours(currTime.getHours() + 1);
		return ret;
	}
	
	// $("#sched-results").html(result)                            // Display the overlaid availabilities as a table

	// $("#7").css('background-color', 'red')

	var fullList = "<ul>"
	$.each(all_data.meeting_info.users, function(i, value){     // Iterate through users
		fullList += "<li>" + i + "</li>"                        // End list for individual user
	});
	fullList += "</ul>"                                     	// End list for all users

	$("#users-list").html(fullList)                             // Display list of users

    // Display list of Top 5 best times
	var bestTimes = "<ul>"
	$.each(all_data.best_times, function(i, value){
	    bestTimes += "<li>" + value + "</li>"
	})
	bestTimes += "</ul>"
	$("#best-times").html(bestTimes);

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