$(document).ready(function() {
	var all_data = jQuery.parseJSON(data);
	$("#user_name").html(all_data.userName + "'s availability");

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
	if(all_data.inPersonUserAvailability !== null){
		inPersonMeetingTable = all_data.inPersonUserAvailability;
	}
	if(all_data.remoteUserAvailability !== null){
		virtualMeetingTable = all_data.remoteUserAvailability;
	}

	// Render both tables regardless. Rely on above logic to hide appropriate table
	$('#inPersonSchedule').append(buildTableHTML(inPersonMeetingTable));
	colorTable(inPersonMeetingTable, "inPersonSchedule");
	$('#virtualSchedule').append(buildTableHTML(virtualMeetingTable));
	colorTable(virtualMeetingTable, "virtualSchedule");

	// Tie updateTable function to clickable cells
	$(".clickable").click(updateTable);

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

	var isMouseDown = false;

	$(function () {
        isMouseDown = false;		
		$('#inPersonSchedule, #virtualSchedule').on('mousedown', '#tableSchedule td', function(){
            isMouseDown = true; 
			
			var currId = parseInt($(this).attr("id"));
			var row = Math.floor(currId / (numCol - 1));
			var col = currId %(numCol - 1);
			tableName = $(this).parent().parent().parent().parent().attr("id");

                if ($('input[name="radio"]:checked').val() == 'none') {
					$(this).css('background-color', 'white');

					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 0;
                }
                else if ($('input[name="radio"]:checked').val() == 'green') { 
                  $(this).css('background-color', '#65EC59');

					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 1;
                }
                else if ($('input[name="radio"]:checked').val() == 'yellow') {    
					$(this).css('background-color', '#F4F569');

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
				
			var currId = parseInt($(this).attr("id"));
			var row = Math.floor(currId / (numCol - 1));
			var col = currId %(numCol - 1);
			tableName = $(this).parent().parent().parent().parent().attr("id");

                if ($('input[name="radio"]:checked').val() == 'none') {
					$(this).css('background-color', 'white');

					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 0;
				  }
				  else if ($('input[name="radio"]:checked').val() == 'green') { 
					$(this).css('background-color', '#65EC59');
		
					if(tableName === "inPersonSchedule"){
						toUpdate = inPersonMeetingTable
					}
					else{
						toUpdate = virtualMeetingTable
					}
					
					toUpdate[row][col] = 1;
				  }
				  else if ($('input[name="radio"]:checked').val() == 'yellow') {    
					$(this).css('background-color', '#F4F569'); 
		
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
				"meeting_id": all_data.meetingID,
				"email": all_data.userEmail,
				"user_name": all_data.userName}
			),
			contentType : 'application/json',
			dataType: 'text',
			success: function(result){
				console.log("Successfully submitted availability")
				window.location = '/results/' + all_data.meetingID
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