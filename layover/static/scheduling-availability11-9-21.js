$(document).ready(function() {
	var all_data = jQuery.parseJSON(data);
	$("#user_name").html(all_data.name + "'s availability");

	console.log(meetingType);
	// Variable initialization
	var inPersonMeetingTable = Array(numTimes * 4).fill().map(() => Array(numCol - 1).fill(0));
	var virtualMeetingTable = Array(numTimes * 4).fill().map(() => Array(numCol - 1).fill(0));
	var currTable = true; // true for in-person. false for virtual
	// if(meetingType === "remote"){
	// 	$("#curr_table_type").html("Current table: virtual availability")
	// 	currTable = false;
	// }

	// If meetingType is strictly in-person, then hide all virtual tables and extend in-person table. 
	// Also hide buttons
	if(meetingType === "in_person"){
		$("#buttonWrapper").hide();
		$("#virtualSchedule").hide();
		$("#inPersonSchedule").attr("class", "row");
	}

	// If meetingType is strictly virtual, then hide all in-person tables. Also hide buttons
	if(meetingType === "remote"){
		$("#buttonWrapper").hide();
		$("#inPersonSchedule").hide();
		$("#virtualSchedule").attr("class", "row");
	}

	// If user already has data, then load that
	if(all_data.inPersonAvailability !== null){
		inPersonMeetingTable = all_data.inPersonAvailability;
	}
	if(all_data.virtualAvailability !== null){
		virtualMeetingTable = all_data.virtualAvailability;
	}

	$('#inPersonSchedule').append(buildTableHTML(inPersonMeetingTable));
	colorTable(inPersonMeetingTable, "inPersonSchedule");
	// registerClickable(inPersonMeetingTable);

	$('#virtualSchedule').append(buildTableHTML(virtualMeetingTable));
	colorTable(virtualMeetingTable, "virtualSchedule");
	// registerClickable(virtualMeetingTable);

	$(".clickable").click(updateTable);

	// $('#virtualSchedule').html("<div>abc</div>");
	// $('#virtualSchedule').css('background-color', "red");
	// $('#virtualSchedule').append("<div>abc</div>");
	// $("#virtualSchedule #abb").css('background-color', "blue");


	// // Must be after variable initialization
	// // Determines which table should be rendered
	// if(currTable){
	// 	$('#inPersonSchedule').append(buildTableHTML(inPersonMeetingTable));
	// 	$('#virtualSchedule').append(buildTableHTML(virtualMeetingTable));
	// 	colorTable(inPersonMeetingTable);
	// 	// Binds jquery clickable function to clickable class
	// 	registerClickable(inPersonMeetingTable);
	// }else{
	// 	$('#schedule').append(buildTableHTML(virtualMeetingTable));
	// 	colorTable(virtualMeetingTable);
	// 	// Binds jquery clickable function to clickable class
	// 	registerClickable(virtualMeetingTable);
	// }	


	function colorTable(availability, availIdStr){
		for(var i = 0 ; i < availability.length ; i++){
			for(var j = 0 ; j < availability[0].length ; j++){
				var currId = i * availability[0].length + j;
				var cellVal = availability[i][j];
				var color = 'white';
				if(cellVal === 0){
					color = "white";
				}else if( cellVal === 0.75){
					color = "#F4F569";
				}else{
					color = "#65EC59";
				}
				$("#" + availIdStr + " #"+currId).css('background-color', color)
			}
		}
	}

	function updateTable(event){
		var toUpdate;
		// Determine which table was clicked
		tableName = $(this).parent().parent().parent().parent().attr("id");
		if(tableName === "inPersonSchedule"){
			toUpdate = inPersonMeetingTable
		}else{
			toUpdate = virtualMeetingTable
		}
		var currId = parseInt($(this).attr("id"))
		var row = Math.floor(currId / (numCol - 1))
		var col = currId %(numCol - 1)
		var color = 'white';
		if(toUpdate[row][col] === 0){
			color = "#65EC59";
			toUpdate[row][col] = 1;
		}
		else if(toUpdate[row][col] === 1){
			color = "#F4F569";
			toUpdate[row][col] = 0.75;
		}else{
			color = "white";
			toUpdate[row][col] = 0;
		}
		$(this).css('background-color', color)
	}

	

	$("#submit_availability").click(function(){
		console.log("submitting availability");
		$.ajax({
			type: "POST",
			url: '/submitAvailability',
			data : JSON.stringify(
				{inPersonMeetingTable: inPersonMeetingTable,
				 virtualMeetingTable: virtualMeetingTable,
				"meeting_id": all_data.meeting_id,
				"email": all_data.email}
			),
			contentType : 'application/json',
			dataType: 'text',
			success: function(result){
				console.log("Successfully submitted availability")
				window.location = '/results/' + all_data.meeting_id
			},
			error: function(request, status, error){
				console.log("Error");
				console.log(request);
				console.log(status);
				console.log(error);
			}
		})
	});

});

	// function registerClickable(tableName){
	// 	console.log(tableName);
	// 	$(".clickable").click({tableName: tableName}, updateTable);
	// }

	// $("#change_table").click(function(){
	// 	// Remove current HTML table
	// 	$('#tableSchedule').remove();
	// 	currTable = !currTable;
	// 	if(currTable){
	// 		$('#schedule').append(buildTableHTML(inPersonMeetingTable));
	// 		colorTable(inPersonMeetingTable);
	// 		registerClickable(inPersonMeetingTable);
	// 		$('#change_table').html("Click to go to virtual availability");
	// 		$("#curr_table_type").html("Current table: in-person availability");
	// 	}else{
	// 		$('#schedule').append(buildTableHTML(virtualMeetingTable));
	// 		colorTable(virtualMeetingTable);
	// 		registerClickable(virtualMeetingTable);
	// 		$('#change_table').html("Click to go to in-person availability");
	// 		$("#curr_table_type").html("Current table: virtual availability");
	// 	}
	// });
