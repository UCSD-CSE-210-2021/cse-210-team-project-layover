$(document).ready(function() {
	var all_data = jQuery.parseJSON(data);
	$("#user_name").html(all_data.name + "'s availability");


	// Variable initialization
	var inPersonMeetingTable = Array(numTimes * 4).fill().map(() => Array(numCol - 1).fill(0));
	var virtualMeetingTable = Array(numTimes * 4).fill().map(() => Array(numCol - 1).fill(0));
	var currTable = true; // true for in-person. false for virtual
	if(meetingType === "remote"){
		$("#curr_table_type").html("Current table: virtual availability")
		currTable = false;
	}

	if(meetingType !== "either"){
		$('#change_table_div').hide()
	}

	// If user already has data, then load that
	if(all_data.inPersonAvailability !== null){
		inPersonMeetingTable = all_data.inPersonAvailability;
	}
	if(all_data.virtualAvailability !== null){
		virtualMeetingTable = all_data.virtualAvailability;
	}

	// Must be after variable initialization
	// Determines which table should be rendered
	if(currTable){
		$('#schedule').append(buildTableHTML(inPersonMeetingTable));
		colorTable(inPersonMeetingTable);
		// Binds jquery clickable function to clickable class
		registerClickable(inPersonMeetingTable);
	}else{
		$('#schedule').append(buildTableHTML(virtualMeetingTable));
		colorTable(virtualMeetingTable);
		// Binds jquery clickable function to clickable class
		registerClickable(virtualMeetingTable);
	}	

	function colorTable(availability){
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
				$("#"+currId).css('background-color', color)
			}
		}
	}

	function updateTable(event){
		toUpdate = event.data.tableName
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

	function registerClickable(tableName){
		console.log(tableName);
		$(".clickable").click({tableName: tableName}, updateTable);
	}

	$("#change_table").click(function(){
		// Remove current HTML table
		$('#tableSchedule').remove();
		currTable = !currTable;
		if(currTable){
			$('#schedule').append(buildTableHTML(inPersonMeetingTable));
			colorTable(inPersonMeetingTable);
			registerClickable(inPersonMeetingTable);
			$('#change_table').html("Click to go to virtual availability");
			$("#curr_table_type").html("Current table: in-person availability");
		}else{
			$('#schedule').append(buildTableHTML(virtualMeetingTable));
			colorTable(virtualMeetingTable);
			registerClickable(virtualMeetingTable);
			$('#change_table').html("Click to go to in-person availability");
			$("#curr_table_type").html("Current table: virtual availability");
		}
	});


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