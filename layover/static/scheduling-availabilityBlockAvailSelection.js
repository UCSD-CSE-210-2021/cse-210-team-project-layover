$(document).ready(function() {
	var all_data = jQuery.parseJSON(data);
	$("#user_name").html(all_data.name + "'s availability");

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
	$('#inPersonSchedule').append(buildTableHTML(inPersonMeetingTable));
	colorTable(inPersonMeetingTable, "inPersonSchedule");
	$('#virtualSchedule').append(buildTableHTML(virtualMeetingTable));
	colorTable(virtualMeetingTable, "virtualSchedule");

	// Tie updateTable function to clickable cells
	var isDragging = false;
	var toUpdate;
	var startI;
	var startJ;
	var prevEndI;
	var prevEndJ;
	var endI;
	var endJ;
	var colorVal;
	var tableName;

	// $("#tableSchedule").mousedown(function(){

	// 	console.log("called")
	// 	// Determine which table was clicked
	// 	console.log($(this));
	// 	tableName = $(this).parent().parent().parent().parent().attr("id");
	// 	console.log(tableName);
	// 	if(tableName === "inPersonSchedule"){
	// 		toUpdate = inPersonMeetingTable
	// 	}else{
	// 		toUpdate = virtualMeetingTable
	// 	}
	// 	var currId = parseInt($(this).attr("id"))
	// 	var row = Math.floor(currId / (numCol - 1))
	// 	var col = currId %(numCol - 1)
	// 	startI = row;
	// 	startJ = col;
	// 	endI = row;
	// 	endJ = col;
	// 	prevEndI = row;
	// 	prevEndJ = col;

	// 	// var color = 'white';
	// 	if(toUpdate[row][col] === 0){
	// 		colorVal = 1;
	// 		// color = "#65EC59";
	// 		toUpdate[row][col] = 1;
	// 	}
	// 	else if(toUpdate[row][col] === 1){
	// 		colorVal = 0.75;
	// 		// color = "#F4F569";
	// 		toUpdate[row][col] = 0.75;
	// 	}else{
	// 		colorVal = 0;
	// 		// color = "white";
	// 		toUpdate[row][col] = 0;
	// 	}
	// 	// $(this).css('background-color', color)

	// 	colorTable(toUpdate, tableName);
	// 	// set 
	// 	// colorVal
	// 	// startI
	// 	// startJ
	// 	// endI
	// 	// endJ

	// 	$(".clickable").mousemove(function(){
	// 		console.log("mouse moved");
	// 		// repeatedly try to update endI and endJ
	
	// 		var currId = parseInt($(this).attr("id"))
	// 		var row = Math.floor(currId / (numCol - 1))
	// 		var col = currId %(numCol - 1)
	
			
	// 		endI = row;
	// 		endJ = col;
	
	// 		// update if we have a new selection
	// 		if(endI != prevEndI || endJ != prevEndJ){
	// 			prevEndI = endI;
	// 			prevEndJ = endJ;
	// 			console.log("new:");
	// 			console.log("row: " + row + " col: " + col);
	
	// 			for(var i = startI ; i <= endI ; i++){
	// 				for(var j = startJ ; j <= endJ ; j++){
	// 					toUpdate[row][col] = colorVal;
	// 				}
	// 			}
	
	// 			colorTable(toUpdate, tableName);
	// 		}
	// 		// if endI and endJ changed then:
	// 		// modify grid
	// 		// call color grid
	
	// 		isDragging = true;
	// 	})

	// 	// modify grid
	// 	// call color grid

	// 	isDragging = false;
	// })
	// .mouseup(function(){
	// 	$(".clickable").unbind('mousemove');
	// })
	// .mouseout(function () {
	// 	$(".clickable").unbind('mousemove');
	// });

	// $(".clickable").mousedown(function(){

	// 	console.log("called")
	// 	// Determine which table was clicked
	// 	tableName = $(this).parent().parent().parent().parent().attr("id");
	// 	if(tableName === "inPersonSchedule"){
	// 		toUpdate = inPersonMeetingTable
	// 	}else{
	// 		toUpdate = virtualMeetingTable
	// 	}
	// 	var currId = parseInt($(this).attr("id"))
	// 	var row = Math.floor(currId / (numCol - 1))
	// 	var col = currId %(numCol - 1)
	// 	startI = row;
	// 	startJ = col;
	// 	endI = row;
	// 	endJ = col;
	// 	console.log("setting prev");
	// 	prevEndI = row;
	// 	prevEndJ = col;

	// 	// var color = 'white';
	// 	if(toUpdate[row][col] === 0){
	// 		colorVal = 1;
	// 		// color = "#65EC59";
	// 		toUpdate[row][col] = 1;
	// 	}
	// 	else if(toUpdate[row][col] === 1){
	// 		colorVal = 0.75;
	// 		// color = "#F4F569";
	// 		toUpdate[row][col] = 0.75;
	// 	}else{
	// 		colorVal = 0;
	// 		// color = "white";
	// 		toUpdate[row][col] = 0;
	// 	}
	// 	// $(this).css('background-color', color)

	// 	colorTable(toUpdate, tableName);
	// 	// set 
	// 	// colorVal
	// 	// startI
	// 	// startJ
	// 	// endI
	// 	// endJ

	// 	$(".clickable").mousemove(function(event){
	// 		// event.preventDefault();
	// 		console.log("mouse moved");
	// 		// repeatedly try to update endI and endJ
	
	// 		var currId = parseInt($(this).attr("id"))
	// 		var row = Math.floor(currId / (numCol - 1))
	// 		var col = currId %(numCol - 1)
	
			
	// 		endI = row;
	// 		endJ = col;
	
	// 		// update if we have a new selection
	// 		if(endI != prevEndI || endJ != prevEndJ){
	// 			console.log("startI: " + startI + " startJ: " + startJ);
	// 			console.log("endI: " + endI + " endJ: " + endJ);
	// 			console.log("prevEndI: " + prevEndI + " prevEndJ: " + prevEndJ);

	// 			var tmp

	// 			// if(startI > prevEndI){
	// 			// 	tmp = startI;
	// 			// 	startI = prevEndI;
	// 			// 	prevEndI = tmp;
	// 			// }

	// 			// if(startJ > prevEndJ){
	// 			// 	tmp = startJ;
	// 			// 	startJ = prevEndJ;
	// 			// 	prevEndJ = tmp;
	// 			// }

	// 			var topLeftI = startI;
	// 			var bottomRightI = prevEndI;
	// 			var topLeftJ = startJ;
	// 			var bottomRightJ = prevEndJ;

	// 			if(topLeftI > bottomRightI){
	// 				tmp = topLeftI;
	// 				topLeftI = bottomRightI;
	// 				bottomRightI = tmp;
	// 			}

	// 			if(topLeftJ > bottomRightJ){
	// 				tmp = topLeftJ;
	// 				topLeftJ = bottomRightJ;
	// 				bottomRightJ = tmp;
	// 			}

	// 			console.log("topLeftI: " + topLeftI + " bottomRightI: " + bottomRightI);
	// 			console.log("topLeftJ: " + topLeftJ + " bottomRightJ: " + bottomRightJ);
	// 			// console.log("prevEndI: " + prevEndI + " prevEndJ: " + prevEndJ);

	// 			for(var i = topLeftI ; i <= bottomRightI ; i++){
	// 				for(var j = topLeftJ ; j <= bottomRightJ ; j++){
	// 					toUpdate[i][j] = 0;
	// 				}
	// 			}

				

	// 			prevEndI = endI;
	// 			prevEndJ = endJ;
				
	// 			topLeftI = startI;
	// 			bottomRightI = endI;
	// 			topLeftJ = startJ;
	// 			bottomRightJ = endJ;


	// 			if(topLeftI > bottomRightI){
	// 				tmp = topLeftI;
	// 				topLeftI = bottomRightI;
	// 				bottomRightI = tmp;
	// 			}

	// 			if(topLeftJ > bottomRightJ){
	// 				tmp = topLeftJ;
	// 				topLeftJ = bottomRightJ;
	// 				bottomRightJ = tmp;
	// 			}

	// 			console.log("topLeftI: " + topLeftI + " bottomRightI: " + bottomRightI);
	// 			console.log("topLeftJ: " + topLeftJ + " bottomRightJ: " + bottomRightJ);

	// 			for(var i = topLeftI ; i <= bottomRightI ; i++){
	// 				for(var j = topLeftJ ; j <= bottomRightJ ; j++){
	// 					toUpdate[i][j] = colorVal;
	// 				}
	// 			}

	// 			// for(var i = startI ; i <= endI ; i++){
	// 			// 	for(var j = startJ ; j <= endJ ; j++){
	// 			// 		toUpdate[i][j] = colorVal;
	// 			// 	}
	// 			// }
	
	// 			console.log(toUpdate);

	// 			colorTable(toUpdate, tableName);
	// 		}
	// 		// if endI and endJ changed then:
	// 		// modify grid
	// 		// call color grid
	
	// 		isDragging = true;
	// 	})

	// 	// modify grid
	// 	// call color grid

	// 	isDragging = false;
	// })
	// .mouseup(function(){
	// 	$(".clickable").unbind('mousemove');
	// })


	// .mouseout(function () {
	// 	$(".clickable").unbind('mousemove');
	// });

	// .mousemove(function(){
	// 	console.log("mouse moved");
	// 	// repeatedly try to update endI and endJ

	// 	var currId = parseInt($(this).attr("id"))
	// 	var row = Math.floor(currId / (numCol - 1))
	// 	var col = currId %(numCol - 1)

	// 	console.log("row: " + row + " col: " + col);
	// 	endI = row;
	// 	endJ = col;

	// 	// update if we have a new selection
	// 	if(endI != prevEndI || endJ != prevEndJ){
	// 		prevEndI = endI;
	// 		prevEndJ = endJ;


	// 		for(var i = startI ; i <= endI ; i++){
	// 			for(var j = startJ ; j <= endJ ; j++){
	// 				toUpdate[row][col] = colorVal;
	// 			}
	// 		}

	// 		colorTable(toUpdate, tableName);
	// 	}
	// 	// if endI and endJ changed then:
	// 	// modify grid
	// 	// call color grid

	// 	isDragging = true;
	// })



	// .mouseup(function(){
	// 	var wasDragging = isDragging;
	// 	isDragging = false;
	// 	if (!wasDragging) {
	// 		console.log("no drag");
	// 		// $("#throbble").toggle();
	// 	}else{
	// 		console.log("dragging");
	// 	}
	// });
	
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

	// function registerClickable(tableName){
	// 	$(".clickable").on('click', {tableName: tableName}, updateTable);
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