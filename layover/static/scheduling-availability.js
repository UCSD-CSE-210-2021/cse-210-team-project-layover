$(document).ready(function() {
	var all_data = jQuery.parseJSON(data);
	var meetingDetails = jQuery.parseJSON(meeting);
	var meetingType = meetingDetails.meeting_type;

	var startTime = meetingDetails.day_start_time;
	var endTime = meetingDetails.day_end_time;
	var numTimes = meetingDetails.day_end_time - meetingDetails.day_start_time;

	$(".nav-heading").text(all_data.name + "'s availability");
	$('#main_title').text("Layover: " + meetingDetails.name);
	// Variable initialization
	var inPersonMeetingTable = Array(numTimes * 4).fill().map(() => Array(numCol - 1).fill(0));
	var virtualMeetingTable = Array(numTimes * 4).fill().map(() => Array(numCol - 1).fill(0));

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

	// Render both tables regardless. Rely on above logic to hide appropriate table
	$('#inPersonSchedule').append(buildTableHTML(startTime, endTime));
	colorTable(inPersonMeetingTable, "inPersonSchedule");
	$('#virtualSchedule').append(buildTableHTML(startTime, endTime));
	colorTable(virtualMeetingTable, "virtualSchedule");

	// Tie updateTable function to clickable cells
	// $(".clickable").click(updateTable);

	// Bind copyTable function to the correct button
	$("#copyToVirtual").click({from: inPersonMeetingTable, to: virtualMeetingTable, tableType: "virtualSchedule"}, copyTable);
	$("#copyToInPerson").click({from: virtualMeetingTable, to: inPersonMeetingTable, tableType: "inPersonSchedule"}, copyTable);

	// Handle copying 1 table to another
	function copyTable(event){
		var from = event.data.from;
		var to = event.data.to;
		var tableType = event.data.tableType;
		deepCopyArr(from, to);
		colorTable(to, tableType);
	}

	// Deep copy the values of 'from' to 'to'
	function deepCopyArr(from, to){
		for(var i = 0 ; i < from.length ; i++){
			for(var j = 0 ; j < from[0].length ; j++){
				to[i][j] = from[i][j];
			}
		}
	}

	// Color the table. availIdStr is either "inPersonSchedule"
	// or "virtualSchedule". Represents the id of the wrapper div around 
	// each table
	function colorTable(availability, availIdStr){
		for(var i = 0 ; i < availability.length ; i++){
			for(var j = 0 ; j < availability[0].length ; j++){
				var currId = i * availability[0].length + j;
				var cellVal = availability[i][j];
				var color = '#ECECEC';
				if(cellVal === 0){
					color = '#ECECEC';
				}else if( cellVal === 0.75){
					color = '#FADE52';
				}else{
					color = '#65EC59';
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
		var color = '#ECECEC';
		if(toUpdate[row][col] === 0){
			color = '#65EC59';
			toUpdate[row][col] = 1;
		}
		else if(toUpdate[row][col] === 1){
			color = '#FADE52';
			toUpdate[row][col] = 0.75;
		}else{
			color = '#ECECEC';
			toUpdate[row][col] = 0;
		}
		$(this).css('background-color', color)
	}

	var isMouseDown = false;
	// var started = false;
	// var mousedownFired = false;

	$(function () {
        isMouseDown = false;
		$('#inPersonSchedule, #virtualSchedule').on('mousedown', '#tableSchedule td', function(){
			console.log("Mousedown");
            isMouseDown = true;
			var currId = parseInt($(this).attr("id"));	
			var row = Math.floor(currId / (numCol - 1));
			var col = currId %(numCol - 1);
			tableName = $(this).parent().parent().parent().parent().attr("id");

                if ($('#availabilitySelector > label > input:checked').val() == 'none') {
					$(this).css('background-color', '#ECECEC');

					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 0;
                }
                else if ($('#availabilitySelector > label > input:checked').val() == 'green') { 
					$(this).css('background-color', '#65EC59');

					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 1;
                }
                else if ($('#availabilitySelector > label > input:checked').val() == 'yellow') {    
					$(this).css('background-color', '#FADE52');

					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 0.75;
                }				

            return false; // prevent text selection
          })

		  $('#inPersonSchedule, #virtualSchedule').on('mouseover', '#tableSchedule td', function(){
            if (isMouseDown) {  
				started = false;				
				console.log("Dragging");
				
				var currId = parseInt($(this).attr("id"));
				var row = Math.floor(currId / (numCol - 1));
				var col = currId %(numCol - 1);
				tableName = $(this).parent().parent().parent().parent().attr("id");

                if ($('#availabilitySelector > label > input:checked').val() == 'none') {
					$(this).css('background-color', '#ECECEC');

					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 0;
				  }
				  else if ($('#availabilitySelector > label > input:checked').val() == 'green') { 
					$(this).css('background-color', '#65EC59');

					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 1;
				  }
				  else if ($('#availabilitySelector > label > input:checked').val() == 'yellow') {    
					$(this).css('background-color', '#FADE52');
		
					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 0.75;
				  }
          }})

		  $('#inPersonSchedule, #virtualSchedule').bind('selectstart', '#tableSchedule td', function(){
            return false; // prevent text selection in IE
          });

        $(document)
          .mouseup(function () {
            isMouseDown = false;
          });
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
	
	$('.noClick').on('mouseover mouseenter mouseleave mouseup mousedown', function() {
		return false
	 });
});